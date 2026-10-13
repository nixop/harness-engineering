#!/usr/bin/env python3
"""Validate and merge what memory-extractor proposed, and build the agentic
memory in the same shape as the scripted one (ADR-0003 amendment 8: the
writer's output is checked against the registers before it reaches a store).

  agentic_build.py <corpus-dir> <extract.jsonl> <out-dir>

Writes <out-dir>/memory/{decisions,open_items,people}.jsonl, _index.json,
graph.cypher (reference schema), validation-report.md (what was merged,
dropped or flagged) and diff.md (agentic memory against the ground truth).
"""
import json, os, re, sys
from collections import Counter, defaultdict

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def q(s): return json.dumps(s, ensure_ascii=False)
def toks(s): return set(re.findall(r"[a-zа-я0-9]+", (s or "").lower())) - {"the", "a", "an", "of", "to", "on", "in", "and", "for", "is", "are", "at", "with", "by", "from", "as", "be"}
def sim(a, b):
    x, y = toks(a), toks(b)
    return len(x & y) / max(1, len(x | y))
def days(a, b):
    from datetime import date
    return abs((date.fromisoformat(a) - date.fromisoformat(b)).days)

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TOPICS = ["iac", "gateway", "timeouts", "retries", "idempotency", "database", "compute", "slo", "cost", "security", "cutover", "ownership"]
TOPIC_NAMES = {"iac": "infrastructure as code", "gateway": "API gateway", "timeouts": "gateway timeout", "retries": "retries", "idempotency": "idempotency",
               "database": "database", "compute": "compute platform", "slo": "SLO", "cost": "cost", "security": "security", "cutover": "cutover", "ownership": "ownership"}

TOPIC_FALLBACK = {"iac": ["drift", "terraform", "cloudformation", "cfn", "stack", "console"], "security": ["iam", "sigv4", "api key", "secret", "ssm", "credential"],
                  "compute": ["lambda", "eks", "kubernetes", "serverless", "poc", "concurrency"], "database": ["dynamo", "documentdb", "dry run", "decom"],
                  "retries": ["retry", "retries", "dlq", "sqs"], "slo": ["p95", "latency", "error budget"], "cutover": ["rollback", "runbook"], "cost": ["budget", "tag"]}

class Registry:
    def __init__(self, root):
        self.people = [json.loads(l) for l in open(f"{root}/memory/people.jsonl", encoding="utf-8")]
        self.by_key = {}
        for p in self.people:
            pk = "person:" + slug(p["name"])
            p["pkey"] = pk
            self.by_key[pk] = p
            for a in [p["name"], p["key"], p["name"].split()[0]] + p.get("aliases", []):
                self.by_key.setdefault("alias:" + a.lower(), p)
        self.issues = []
    def person(self, v, where):
        if not v: return None
        v = str(v).strip()
        if v in self.by_key: return self.by_key[v]["pkey"]
        s = v.lower().replace("person:", "")
        if "alias:" + s in self.by_key: return self.by_key["alias:" + s]["pkey"]
        for p in self.people:
            if slug(p["name"]) == slug(s) or slug(p["name"]).split("-")[0] == slug(s): return p["pkey"]
        self.issues.append(f"unresolved person {v!r} in {where}")
        return None
    def topic(self, v, where):
        if not v: self.issues.append(f"missing topic in {where}"); return None
        s = str(v).lower().replace("topic:", "").strip()
        if s in TOPICS: return s
        for t in TOPICS:
            if s.startswith(t) or t in s: return t
        for t, words in TOPIC_FALLBACK.items():
            if any(w in s for w in words): return t
        self.issues.append(f"unresolved topic {v!r} in {where}")
        return None
    def date(self, v, fallback, where):
        if v and ISO.match(str(v)): return str(v)
        if v: self.issues.append(f"bad date {v!r} in {where}, used {fallback}")
        return fallback

def main(root, extract_path, out):
    reg = Registry(root)
    recs = [json.loads(l) for l in open(extract_path, encoding="utf-8")]
    os.makedirs(f"{out}/memory", exist_ok=True)
    report = ["# Validation report (agentic memory, Relay)", ""]
    nojson = [r["file"] for r in recs if not r.get("json")]
    report.append(f"Sources: {len(recs)}; without parseable JSON: {len(nojson)} {nojson}")
    recs = [r for r in recs if r.get("json")]
    # order: meetings by date first, then ADRs, docs
    def sdate(r):
        j = r["json"]; m = re.search(r"\d{4}-\d{2}-\d{2}", r["file"])
        return j.get("date") if ISO.match(str(j.get("date") or "")) else (m.group(0) if m else "9999")
    meetings = sorted([r for r in recs if r["file"].startswith("meetings/")], key=sdate)
    adrs = [r for r in recs if r["file"].startswith("adr/")]
    docs = [r for r in recs if r["file"].startswith(("docs/", "confluence/"))]

    decisions, open_items, own_events, stale, attend = [], [], [], [], defaultdict(set)
    meeting_nodes = {}
    # ---- meetings
    for r in meetings:
        j, f = r["json"], r["file"]
        mdate = reg.date(j.get("date"), sdate(r), f)
        mtype = "weekly sync" if "weekly-sync" in f else re.sub(r"^\d{4}-\d{2}-\d{2}-", "", os.path.basename(f)).replace(".txt", "").replace("-", " ")
        mkey = "meeting:" + mdate + ("" if mtype == "weekly sync" else ":" + slug(mtype))
        meeting_nodes[f] = (mkey, mdate, mtype)
        for a in j.get("attendees") or []:
            pk = reg.person(a, f)
            if pk: attend[mkey].add(pk)
        for d in j.get("decisions") or []:
            tp = reg.topic(d.get("topic"), f)
            if not tp or not d.get("text"): continue
            dd = reg.date(d.get("date"), mdate, f)
            if days(dd, mdate) > 3:
                report.append(f"- decision dated {dd} in a meeting of {mdate} ({f}): date set to the meeting date"); dd = mdate
            cand = {"topic": tp, "date": dd, "text": d["text"].strip(), "owner": reg.person(d.get("owner"), f), "proposer": reg.person(d.get("proposer"), f),
                    "objector": reg.person(d.get("objector"), f), "status": "rejected" if str(d.get("status", "")).lower() == "rejected" else "active",
                    "replaces": d.get("replaces"), "adr": d.get("adr"), "poc": d.get("poc"), "depends_on": d.get("depends_on"), "closes": d.get("closes"),
                    "source": f, "meeting": mkey, "stale": d.get("stale") or []}
            dup = next((x for x in decisions if x["topic"] == tp and days(x["date"], dd) <= 5 and sim(x["text"], cand["text"]) >= 0.5), None)
            if dup:
                report.append(f"- merged duplicate decision ({tp}, {dd}) from {f} into {dup['date']}: {cand['text'][:70]!r}")
                for k in ("owner", "proposer", "objector"):
                    dup[k] = dup[k] or cand[k]
                continue
            decisions.append(cand)
        for o in j.get("ownership") or []:
            obj = str(o.get("object") or "").strip()
            to = reg.person(o.get("to"), f); frm = reg.person(o.get("from"), f)
            if obj.startswith("topic:"):
                tp = reg.topic(obj, f); obj = "topic:" + tp if tp else None
            elif not obj.startswith("poc:"):
                tp = reg.topic(obj, f); obj = "topic:" + tp if tp else None
            if obj and to: own_events.append({"object": obj, "from": frm, "to": to, "date": reg.date(o.get("date"), mdate, f), "source": f})
        for o in j.get("open_items") or []:
            tp = reg.topic(o.get("topic"), f)
            if not tp or not o.get("text"): continue
            od = reg.date(o.get("date"), mdate, f); ev = str(o.get("event") or "raised").lower()
            match = next((x for x in open_items if x["topic"] == tp and sim(x["text"], o["text"]) >= 0.35), None)
            if match is None and ev != "raised":
                same = [x for x in open_items if x["topic"] == tp and x["status"] == "open" and x["raised"] < od]
                loose = max(same, key=lambda x: sim(x["text"], o["text"]), default=None)
                if loose and sim(loose["text"], o["text"]) >= 0.15: match = loose
                else:
                    report.append(f"- dropped open item {ev} without a prior raise ({tp}, {od}) in {f}: {o['text'][:60]!r}")
                    continue
            if match is None:
                open_items.append({"topic": tp, "text": o["text"].strip(), "raised": od, "source": f, "meeting": mkey, "owner": None, "taken": None, "closed_by": None, "raised_again": [], "status": "open"})
                continue
            if ev == "raised_again" and od not in match["raised_again"] and od != match["raised"]: match["raised_again"].append(od)
            elif ev == "taken":
                pk = reg.person(o.get("owner"), f)
                if pk: match["owner"], match["taken"], match["status"] = pk, od, "closed"
                else: report.append(f"- open item taken but no owner resolved ({tp}, {od}) in {f}")
            elif ev == "closed": match["status"] = "closed"; match["_closed_on"] = od
            elif ev == "raised": report.append(f"- open item raised twice ({tp}, {od}) in {f}, treated as raised again"); match["raised_again"].append(od)
        for d in j.get("decisions") or []:
            for s in d.get("stale") or []:
                if s.get("document") and s.get("fact"): stale.append({"document": s["document"], "fact": s["fact"], "topic": reg.topic(d.get("topic"), f), "date": reg.date(d.get("date"), mdate, f)})
    decisions.sort(key=lambda d: (d["date"], d["topic"]))
    # ids and keys
    for i, d in enumerate(decisions, 1): d["id"] = f"A{i:02d}"
    counts = Counter((d["topic"], d["date"]) for d in decisions)
    for d in decisions: d["key"] = f"decision:{d['topic']}:{d['date']}" + ("" if counts[(d["topic"], d["date"])] == 1 else f":{d['id'].lower()}")
    # supersedes: latest earlier non-rejected decision on the same topic
    for d in decisions:
        d["supersedes"] = None
        if d.get("replaces"):
            prev = [x for x in decisions if x["topic"] == d["topic"] and x["date"] < d["date"] and x["status"] != "rejected"]
            if prev:
                best = max(prev, key=lambda x: (sim(x["text"], d["replaces"]) > 0.15, x["date"]))
                d["supersedes"] = best["id"]; best["status"] = "superseded"; best["superseded_by"] = d["id"]
            else: report.append(f"- {d['id']} says it replaces {d['replaces'][:50]!r} but no earlier decision on {d['topic']} exists")
        d.setdefault("superseded_by", None)
    # depends_on / closes resolved by gist
    for d in decisions:
        d["depends_on_id"] = None
        if d.get("depends_on"):
            c = [x for x in decisions if x["date"] <= d["date"] and x is not d]
            if c:
                best = max(c, key=lambda x: sim(x["text"], d["depends_on"]))
                if sim(best["text"], d["depends_on"]) >= 0.2: d["depends_on_id"] = best["id"]
                else: report.append(f"- {d['id']} depends_on {d['depends_on'][:50]!r} not matched")
        d["closes_id"] = None
        if d.get("closes"):
            c = [o for o in open_items if o["raised"] <= d["date"]]
            if c:
                best = max(c, key=lambda o: sim(o["text"], d["closes"]))
                if sim(best["text"], d["closes"]) >= 0.25:
                    best["closed_by"] = d["id"]; best["status"] = "closed"; d["closes_id"] = best
                else: report.append(f"- {d['id']} closes {d['closes'][:50]!r} not matched")
    # ---- ADRs
    adr_nodes = []
    for r in adrs:
        j = r["json"]; a = j.get("adr") or {}
        if not a.get("id"): report.append(f"- ADR source {r['file']} has no adr block"); continue
        aid = str(a["id"]).upper().replace("ADR", "ADR-").replace("--", "-")
        aid = re.sub(r"ADR-?0*(\d+)", lambda m: f"ADR-{int(m.group(1)):03d}", aid)
        node = {"id": aid, "title": a.get("title") or aid, "status": str(a.get("status") or "Accepted").split()[0].capitalize(), "date": reg.date(a.get("date"), sdate(r), r["file"]),
                "author": reg.person(a.get("author"), r["file"]), "supersedes": a.get("supersedes"), "file": r["file"]}
        adr_nodes.append(node)
        rd = a.get("records_decision") or {}
        if rd.get("topic"):
            tp = reg.topic(rd["topic"], r["file"]); rdate = rd.get("date")
            c = [d for d in decisions if d["topic"] == tp and (not rdate or not ISO.match(str(rdate)) or days(d["date"], rdate) <= 7)]
            if c:
                best = max(c, key=lambda d: sim(d["text"], rd.get("gist") or node["title"]))
                best["adr"] = best.get("adr") or aid
            else: report.append(f"- {aid} records a decision on {tp} around {rdate} but none was extracted from meetings")
    for d in decisions:
        if d.get("adr"): d["adr"] = re.sub(r"ADR-?0*(\d+)", lambda m: f"ADR-{int(m.group(1)):03d}", str(d["adr"]).upper())
    # ---- documents and PoCs
    doc_nodes, poc_nodes = [], {}
    for r in docs:
        j = r["json"]; dd = j.get("document") or {}
        doc_nodes.append({"file": r["file"], "title": dd.get("title") or os.path.basename(r["file"]), "updated": reg.date(dd.get("updated"), "2026-01-01", r["file"]), "author": reg.person(dd.get("author"), r["file"])})
        pc = j.get("poc") or {}
        if pc.get("id"):
            pid = str(pc["id"]).lower().replace("poc-", "poc-")
            if not pid.startswith("poc-"): pid = "poc-" + pid
            poc_nodes[pid] = {"id": pid, "name": pc.get("name") or pid, "owner": reg.person(pc.get("owner"), r["file"]), "from": pc.get("from"), "to": pc.get("to"), "results": pc.get("results") or {}, "report": r["file"]}
    # ---- ownership spans per object
    spans = defaultdict(list)
    for e in sorted(own_events, key=lambda e: e["date"]):
        ss = spans[e["object"]]
        if e["from"] and not any(s[0] == e["from"] and s[2] is None for s in ss):
            ss.append([e["from"], None, None])  # owner known only from the hand-over
        for s in ss:
            if s[2] is None and s[0] != e["to"]: s[2] = e["date"]
        if not any(s[0] == e["to"] and s[2] is None for s in ss): ss.append([e["to"], e["date"], None])
    for obj, ss in spans.items():
        for s in ss:
            if s[1] is None: s[1] = min([x["date"] for x in decisions if "topic:" + x["topic"] == obj] + [s[2] or "2026-01-01"])
    # ---- people file, decisions file, open items file, index
    names = {p["pkey"]: p["name"] for p in reg.people}
    with open(f"{out}/memory/people.jsonl", "w", encoding="utf-8") as f:
        for p in reg.people: f.write(json.dumps({k: v for k, v in p.items() if k != "pkey"}, ensure_ascii=False) + "\n")
    with open(f"{out}/memory/decisions.jsonl", "w", encoding="utf-8") as f:
        for d in decisions:
            f.write(json.dumps({"id": d["id"], "date": d["date"], "topic": d["topic"], "decision": d["text"], "owner": names.get(d["owner"]), "proposer": names.get(d["proposer"]), "objector": names.get(d["objector"]),
                                "source": d["source"], "status": d["status"], "supersedes": d["supersedes"], "superseded_by": d["superseded_by"], "adr": d.get("adr"), "poc": d.get("poc"), "depends_on": d["depends_on_id"],
                                "closes": d["closes_id"]["text"] if d["closes_id"] else None}, ensure_ascii=False) + "\n")
    with open(f"{out}/memory/open_items.jsonl", "w", encoding="utf-8") as f:
        for i, o in enumerate(open_items, 1):
            o["id"] = f"Q{i}"
            f.write(json.dumps({"id": o["id"], "raised": o["raised"], "topic": o["topic"], "text": o["text"], "source": o["source"], "owner": names.get(o["owner"]), "taken": o["taken"], "closed_by": o["closed_by"], "raised_again": o["raised_again"], "status": o["status"]}, ensure_ascii=False) + "\n")
    tspans = {obj[6:]: [[next(p["key"] for p in reg.people if p["pkey"] == w), s, e] for w, s, e in ss] for obj, ss in spans.items() if obj.startswith("topic:")}
    json.dump({"dkey": {d["id"]: d["key"] for d in decisions}, "spans": tspans, "files": {}}, open(f"{out}/memory/_index.json", "w"), indent=1)
    # ---- graph
    g = []
    for lab in ("Person", "Team", "Meeting", "Document", "ADR", "Decision", "Topic", "OpenItem", "PoC"):
        g.append(f"CREATE CONSTRAINT {lab.lower()}_key IF NOT EXISTS FOR (n:{lab}) REQUIRE n.key IS UNIQUE;")
    for p in reg.people:
        g.append(f"MERGE (n:Person {{key: {q(p['pkey'])}}}) SET n.name = {q(p['name'])}, n.role = {q(p.get('role',''))}, n.aliases = {q(p.get('aliases', []))};")
    for t in TOPICS: g.append(f"MERGE (n:Topic {{key: {q('topic:'+t)}}}) SET n.name = {q(TOPIC_NAMES[t])};")
    for f_, (mk, md, mt) in meeting_nodes.items():
        g.append(f"MERGE (n:Meeting {{key: {q(mk)}}}) SET n.date = {q(md)}, n.type = {q(mt)}, n.file = {q(f_)};")
        for pk in attend[mk]: g.append(f"MATCH (p:Person {{key: {q(pk)}}}), (m:Meeting {{key: {q(mk)}}}) MERGE (p)-[:ATTENDED]->(m);")
    for d_ in doc_nodes:
        dk = "document:" + slug(d_["file"])
        g.append(f"MERGE (n:Document {{key: {q(dk)}}}) SET n.title = {q(d_['title'])}, n.file = {q(d_['file'])}, n.updated = {q(d_['updated'])};")
        if d_["author"]: g.append(f"MATCH (p:Person {{key: {q(d_['author'])}}}), (d:Document {{key: {q(dk)}}}) MERGE (p)-[:AUTHORED]->(d);")
    for a in adr_nodes:
        ak = "adr:" + a["id"].lower()
        g.append(f"MERGE (n:ADR {{key: {q(ak)}}}) SET n.id = {q(a['id'])}, n.title = {q(a['title'])}, n.status = {q(a['status'])}, n.date = {q(a['date'])}, n.file = {q(a['file'])};")
        if a["author"]: g.append(f"MATCH (p:Person {{key: {q(a['author'])}}}), (a:ADR {{key: {q(ak)}}}) MERGE (p)-[:AUTHORED]->(a);")
    for a in adr_nodes:
        if a.get("supersedes"):
            sup = re.sub(r"ADR-?0*(\d+)", lambda m: f"adr:adr-{int(m.group(1)):03d}", str(a["supersedes"]).upper())
            g.append(f"MATCH (a:ADR {{key: {q('adr:'+a['id'].lower())}}}), (b:ADR {{key: {q(sup)}}}) MERGE (a)-[:SUPERSEDES]->(b);")
    for pid, pc in poc_nodes.items():
        g.append(f"MERGE (n:PoC {{key: {q('poc:'+pid)}}}) SET n.name = {q(pc['name'])}, n.from = {q(pc.get('from') or '')}, n.to = {q(pc.get('to') or '')}, n.report = {q(pc['report'])}, n.results = {q(json.dumps(pc['results']))};")
        ss = spans.get("poc:" + pid)
        if ss:
            for w, s, e in ss: g.append(f"MATCH (p:Person {{key: {q(w)}}}), (c:PoC {{key: {q('poc:'+pid)}}}) MERGE (p)-[:OWNS {{from: {q(s)}" + (f", to: {q(e)}" if e else "") + "}]->(c);")
        elif pc["owner"]: g.append(f"MATCH (p:Person {{key: {q(pc['owner'])}}}), (c:PoC {{key: {q('poc:'+pid)}}}) MERGE (p)-[:OWNS {{from: {q(pc.get('from') or '2026-01-01')}}}]->(c);")
    dk = {d["id"]: d["key"] for d in decisions}
    for d in decisions:
        k = d["key"]
        g.append(f"MERGE (n:Decision {{key: {q(k)}}}) SET n.id = {q(d['id'])}, n.text = {q(d['text'])}, n.date = {q(d['date'])}, n.status = {q(d['status'])}, n.source = {q(d['source'])};")
        g.append(f"MATCH (n:Decision {{key: {q(k)}}}), (t:Topic {{key: {q('topic:'+d['topic'])}}}) MERGE (n)-[:ABOUT]->(t);")
        g.append(f"MATCH (n:Decision {{key: {q(k)}}}), (m:Meeting {{key: {q(d['meeting'])}}}) MERGE (n)-[:DECIDED_IN]->(m);")
        if d["owner"]: g.append(f"MATCH (p:Person {{key: {q(d['owner'])}}}), (n:Decision {{key: {q(k)}}}) MERGE (p)-[:OWNS {{from: {q(d['date'])}}}]->(n);")
        if d["proposer"]: g.append(f"MATCH (p:Person {{key: {q(d['proposer'])}}}), (n:Decision {{key: {q(k)}}}) MERGE (p)-[:PROPOSED]->(n);")
        if d["objector"]: g.append(f"MATCH (p:Person {{key: {q(d['objector'])}}}), (n:Decision {{key: {q(k)}}}) MERGE (p)-[:OBJECTED_TO]->(n);")
        if d.get("adr"): g.append(f"MATCH (n:Decision {{key: {q(k)}}}), (a:ADR {{key: {q('adr:'+d['adr'].lower())}}}) MERGE (n)-[:RECORDED_IN]->(a);")
        if d.get("poc"): g.append(f"MATCH (n:Decision {{key: {q(k)}}}), (c:PoC {{key: {q('poc:'+str(d['poc']).lower())}}}) MERGE (n)-[:BASED_ON]->(c);")
        if d["depends_on_id"]: g.append(f"MATCH (n:Decision {{key: {q(k)}}}), (m:Decision {{key: {q(dk[d['depends_on_id']])}}}) MERGE (n)-[:DEPENDS_ON]->(m);")
        if d["supersedes"]: g.append(f"MATCH (a:Decision {{key: {q(k)}}}), (b:Decision {{key: {q(dk[d['supersedes']])}}}) MERGE (a)-[:SUPERSEDES]->(b);")
    for obj, ss in spans.items():
        if obj.startswith("topic:"):
            for w, s, e in ss: g.append(f"MATCH (p:Person {{key: {q(w)}}}), (t:Topic {{key: {q(obj)}}}) MERGE (p)-[:OWNS {{from: {q(s)}" + (f", to: {q(e)}" if e else "") + "}]->(t);")
    for o in open_items:
        k = f"openitem:{o['topic']}:{o['raised']}"
        g.append(f"MERGE (n:OpenItem {{key: {q(k)}}}) SET n.id = {q(o['id'])}, n.text = {q(o['text'])}, n.raised = {q(o['raised'])}, n.status = {q(o['status'])}, n.raised_again = {q(o['raised_again'])};")
        g.append(f"MATCH (n:OpenItem {{key: {q(k)}}}), (t:Topic {{key: {q('topic:'+o['topic'])}}}) MERGE (n)-[:ABOUT]->(t);")
        g.append(f"MATCH (n:OpenItem {{key: {q(k)}}}), (m:Meeting {{key: {q(o['meeting'])}}}) MERGE (n)-[:RAISED_IN]->(m);")
        if o["owner"] and o["taken"]: g.append(f"MATCH (p:Person {{key: {q(o['owner'])}}}), (n:OpenItem {{key: {q(k)}}}) MERGE (p)-[:OWNS {{from: {q(o['taken'])}}}]->(n);")
        if o["closed_by"]: g.append(f"MATCH (n:OpenItem {{key: {q(k)}}}), (d:Decision {{key: {q(dk[o['closed_by']])}}}) MERGE (d)-[:CLOSES]->(n);")
    docfiles = {d_["file"] for d_ in doc_nodes}
    for s in stale:
        target = next((f_ for f_ in docfiles if f_.endswith(str(s["document"])) or slug(s["document"]) in slug(f_)), None)
        dec = next((d for d in decisions if d["topic"] == s["topic"] and d["date"] == s["date"]), None)
        if target and dec: g.append(f"MATCH (d:Document {{key: {q('document:'+slug(target))}}}), (n:Decision {{key: {q(dec['key'])}}}) MERGE (n)-[:MAKES_STALE {{since: {q(s['date'])}, fact: {q(s['fact'])}}}]->(d);")
        else: report.append(f"- stale note not linked: document {s['document']!r} / decision {s['topic']} {s['date']}")
    open(f"{out}/memory/graph.cypher", "w", encoding="utf-8").write("\n".join(g) + "\n")
    # ---- report and diff
    report += ["", f"Decisions kept: {len(decisions)} (rejected {sum(1 for d in decisions if d['status']=='rejected')}, superseded {sum(1 for d in decisions if d['status']=='superseded')}); open items: {len(open_items)}; ownership events: {len(own_events)}; ADRs: {len(adr_nodes)}; documents: {len(doc_nodes)}; PoCs: {len(poc_nodes)}; stale notes: {len(stale)}; graph lines: {len(g)}",
               "", "## Register issues (not written)", ""] + [f"- {i}" for i in sorted(set(reg.issues))]
    open(f"{out}/validation-report.md", "w", encoding="utf-8").write("\n".join(report) + "\n")
    truth = [json.loads(l) for l in open(f"{root}/memory/decisions.jsonl", encoding="utf-8")]
    tidx = json.load(open(f"{root}/memory/_index.json")); tspans_truth = tidx["spans"]
    hit, used = [], set()
    for t in truth:
        c = [d for d in decisions if days(d["date"], t["date"]) <= 3 and d["id"] not in used]
        best = max(c, key=lambda d: (sim(d["text"], t["decision"]) + (0.1 if d["topic"] == t["topic"] else 0)), default=None)
        if best and (sim(best["text"], t["decision"]) >= 0.15 if (best["topic"] == t["topic"] or t["topic"] == "ownership") else sim(best["text"], t["decision"]) >= 0.3):
            hit.append((t, best)); used.add(best["id"])
    diff = ["# Agentic memory vs ground truth (Relay)", "",
            f"- Decisions: truth {len(truth)}, agentic {len(decisions)}, matched {len(hit)} -> recall {len(hit)/len(truth):.2f}, precision {len(hit)/max(1,len(decisions)):.2f}",
            f"- Status agreement on matched: {sum(1 for t,d in hit if t['status']==d['status'])}/{len(hit)}; owner agreement: {sum(1 for t,d in hit if (t.get('owner') or '')==(names.get(d['owner']) or ''))}/{len(hit)}; proposer: {sum(1 for t,d in hit if (t.get('proposer') or '')==(names.get(d['proposer']) or ''))}/{len(hit)}; objector: {sum(1 for t,d in hit if (t.get('objector') or '')==(names.get(d['objector']) or ''))}/{len(hit)}",
            f"- SUPERSEDES: truth {sum(1 for t in truth if t.get('supersedes'))}, agentic {sum(1 for d in decisions if d['supersedes'])}, correct {sum(1 for t,d in hit if t.get('supersedes') and d['supersedes'] and any(tt['id']==t['supersedes'] and dd['id']==d['supersedes'] for tt,dd in hit))}",
            f"- ADR links on matched: truth {sum(1 for t,d in hit if t.get('adr'))}, agreed {sum(1 for t,d in hit if t.get('adr') and t['adr']==d.get('adr'))}",
            f"- Ownership spans (topics): truth {sum(len(v) for v in tspans_truth.values())}, agentic {sum(len(v) for v in tspans.values())}, exact (who, from, to) {sum(1 for tp,ss in tspans.items() for s in ss if any(s[0]==x[0] and s[1]==x[1] and s[2]==x[2] for x in tspans_truth.get(tp, [])))}",
            "", "## Missed decisions", ""] + [f"- {t['id']} {t['date']} {t['topic']}: {t['decision'][:90]}" for t in truth if t not in [h[0] for h in hit]] + \
           ["", "## Extra decisions (no ground-truth match)", ""] + [f"- {d['id']} {d['date']} {d['topic']}: {d['text'][:90]} ({d['source']})" for d in decisions if d["id"] not in used] + \
           ["", "## Open items", ""] + [f"- {o['id']} {o['raised']} {o['topic']} {o['status']} owner={names.get(o['owner'])} again={o['raised_again']}: {o['text'][:70]}" for o in open_items]
    truth_oi = [json.loads(l) for l in open(f"{root}/memory/open_items.jsonl", encoding="utf-8")]
    moi = sum(1 for t in truth_oi if any(o["topic"] == t["topic"] and sim(o["text"], t["text"]) >= 0.3 for o in open_items))
    diff.insert(6, f"- Open items: truth {len(truth_oi)}, agentic {len(open_items)}, matched {moi}")
    open(f"{out}/diff.md", "w", encoding="utf-8").write("\n".join(diff) + "\n")
    print("\n".join(diff[:8])); print(f"report: {out}/validation-report.md, graph lines {len(g)}, register issues {len(set(reg.issues))}")

if __name__ == "__main__":
    main(*sys.argv[1:4])
