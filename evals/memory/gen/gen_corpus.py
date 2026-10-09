#!/usr/bin/env python3
"""Generate the Relay corpus from its source of truth.

  gen_corpus.py <corpus-dir>

Reads  <corpus>/source/timeline.yaml, meetings-*.yaml, adr_prose.yaml
Writes <corpus>/meetings/*.txt, adr/ADR-NNN.md, memory/{decisions,people,
       open_items,glossary,documents,adrs}.jsonl, memory/reference-graph.cypher,
       memory/questions-templated.jsonl
Checks that every reference resolves and that dates and attendance agree.
"""
import glob, json, os, re, sys, random
import yaml

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def q(s): return json.dumps(s, ensure_ascii=False)

def load(root):
    t = yaml.safe_load(open(f"{root}/source/timeline.yaml", encoding="utf-8"))
    t["meetings"] = []
    for f in sorted(glob.glob(f"{root}/source/meetings-*.yaml")):
        t["meetings"] += yaml.safe_load(open(f, encoding="utf-8"))["meetings"]
    t["adr_prose"] = yaml.safe_load(open(f"{root}/source/adr_prose.yaml", encoding="utf-8"))
    return t

def validate(t):
    errs = []
    meet = {m["id"]: m for m in t["meetings"]}
    people = t["people"]
    for m in t["meetings"]:
        for p in m["attendees"]:
            if p not in people: errs.append(f"{m['id']}: unknown attendee {p}")
            else:
                j, l = people[p].get("joined"), people[p].get("left")
                if j and m["date"] < j: errs.append(f"{m['id']}: {p} attends before joining {j}")
                if l and m["date"] > l: errs.append(f"{m['id']}: {p} attends after leaving {l}")
        for sp, _ in m["turns"]:
            if sp not in m["attendees"]: errs.append(f"{m['id']}: speaker {sp} not in attendees")
    for d in t["decisions"]:
        m = meet.get(d["meeting"])
        if not m: errs.append(f"{d['id']}: meeting {d['meeting']} missing"); continue
        if m["date"] != d["date"]: errs.append(f"{d['id']}: date {d['date']} != meeting {m['date']}")
        for role in ("owner", "proposer", "objector"):
            if d.get(role) and d[role] not in m["attendees"]: errs.append(f"{d['id']}: {role} {d[role]} not at {m['id']}")
        if d.get("supersedes") and d["supersedes"] not in {x["id"] for x in t["decisions"]}: errs.append(f"{d['id']}: supersedes unknown")
    for o in t["open_items"]:
        if o["meeting"] not in meet: errs.append(f"{o['id']}: meeting missing")
        for d in o.get("raised_again", []):
            if not any(m["date"] == d for m in t["meetings"]): errs.append(f"{o['id']}: raised_again {d} has no meeting")
        if o.get("taken") and not any(m["date"] == o["taken"] for m in t["meetings"]): errs.append(f"{o['id']}: taken {o['taken']} has no meeting")
    for a in t["adrs"]:
        if a["id"] not in t["adr_prose"]: errs.append(f"{a['id']}: no prose")
    return errs

# ---------- transcripts ----------
def render_meetings(t, root):
    os.makedirs(f"{root}/meetings", exist_ok=True)
    rnd = random.Random(42)
    files = {}
    for m in t["meetings"]:
        fn = f"{m['date']}-{slug(m['type'])}.txt"
        files[m["id"]] = f"meetings/{fn}"
        spk = ", ".join(t["people"][p]["aliases"][0] for p in m["attendees"])
        total = sum(len(x) for _, x in m["turns"]) // 11 + 5 * len(m["turns"])
        lines = [f"# Relay {m['type']}, {m['date']}, {max(10, total // 60 + 10)} min, ASR transcript (ru), speakers: {spk}"]
        tsec = rnd.randint(2, 9)
        for i, (sp, text) in enumerate(m["turns"]):
            al = t["people"][sp]["aliases"]
            label = al[1] if (len(al) > 1 and rnd.random() < 0.18) else al[0]
            lines.append(f"[{tsec//3600:02d}:{(tsec%3600)//60:02d}:{tsec%60:02d}] {label}: {text}")
            tsec += 3 + len(text) // 11 + rnd.randint(0, 4)
        open(f"{root}/meetings/{fn}", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return files

# ---------- ADRs ----------
def render_adrs(t, root, dec_by_id):
    os.makedirs(f"{root}/adr", exist_ok=True)
    names = {k: v["name"] for k, v in t["people"].items()}
    for a in t["adrs"]:
        p = t["adr_prose"][a["id"]]
        d = dec_by_id.get(a.get("decision"))
        out = [f"# {a['id']}: {a['title']}", "",
               f"**Status:** {a['status']}" + (f" (superseded by {a['superseded_by']})" if a.get("superseded_by") else "") + (f", supersedes {a['supersedes']}" if a.get("supersedes") else ""),
               f"**Date:** {a['date']}" + (f" (proposed {a['proposed']})" if a.get("proposed") else ""),
               f"**Author:** {names[a['author']]}", f"**Deciders:** Relay weekly sync" + (f", {d['date']}" if d else ""), "",
               "## Context", "", p["context"].strip(), "", "## Options considered", ""]
        out += [f"- {o}" for o in p["options"]]
        out += ["", "## Decision", ""]
        out.append(d["text"] + "." if d else "No decision recorded; see Status.")
        if d and d.get("objector"): out.append(f"\nObjection recorded from {names[d['objector']]}.")
        for sec, body in (p.get("sections") or {}).items():
            out += ["", f"### {sec}", "", body.strip()]
        out += ["", "## Consequences", "", p["consequences"].strip()]
        if a.get("note"): out += ["", f"> Note: {a['note']}"]
        open(f"{root}/adr/{a['id']}.md", "w", encoding="utf-8").write("\n".join(out) + "\n")

# ---------- ground truth ----------
def ground_truth(t, root, files):
    os.makedirs(f"{root}/memory", exist_ok=True)
    names = {k: v["name"] for k, v in t["people"].items()}
    sup_by = {}
    for d in t["decisions"]:
        if d.get("supersedes"): sup_by[d["supersedes"]] = d["id"]
    docs_stale = {}
    for doc in t["documents"]:
        for s in doc.get("stale", []):
            docs_stale.setdefault(s["decision"], []).append(f"{doc['file']} (updated {doc['updated']}) still {s['fact']}")
    for a in t["adrs"]:
        for s in a.get("stale", []):
            docs_stale.setdefault(s["decision"], []).append(f"{a['id']} section {s['section']} is stale since {s['since']}")
    decs = []
    for d in sorted(t["decisions"], key=lambda x: (x["date"], x["id"])):
        status = d.get("status") or ("superseded" if d["id"] in sup_by else "active")
        rec = {"id": d["id"], "date": d["date"], "topic": d["topic"], "decision": d["text"],
               "owner": names.get(d.get("owner")), "proposer": names.get(d.get("proposer")), "objector": names.get(d.get("objector")),
               "source": files[d["meeting"]], "status": status, "supersedes": d.get("supersedes"), "superseded_by": sup_by.get(d["id"]),
               "adr": d.get("adr"), "poc": d.get("poc"), "depends_on": d.get("depends_on"), "closes": d.get("closes")}
        if d.get("ownership"): rec["ownership"] = {"topic": d["ownership"]["topic"], "from": names[d["ownership"]["from"]], "to": names[d["ownership"]["to"]]}
        if docs_stale.get(d["id"]): rec["note"] = "; ".join(docs_stale[d["id"]])
        decs.append(rec)
    with open(f"{root}/memory/decisions.jsonl", "w", encoding="utf-8") as f:
        for r in decs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(f"{root}/memory/people.jsonl", "w", encoding="utf-8") as f:
        for k, p in t["people"].items():
            team = next((tk for tk, tv in t["teams"].items() if k in tv["members"]), None)
            f.write(json.dumps({"key": k, "name": p["name"], "role": p["role"], "aliases": p["aliases"], "team": t["teams"][team]["name"] if team else None,
                                "joined": p.get("joined"), "left": p.get("left")}, ensure_ascii=False) + "\n")
    with open(f"{root}/memory/open_items.jsonl", "w", encoding="utf-8") as f:
        for o in t["open_items"]:
            f.write(json.dumps({"id": o["id"], "raised": o["raised"], "topic": o["topic"], "text": o["text"], "source": files[o["meeting"]],
                                "owner": names.get(o.get("owner")), "taken": o.get("taken"), "closed_by": o.get("closed_by"), "raised_again": o.get("raised_again", []),
                                "status": "closed" if (o.get("closed_by") or o.get("taken")) else "open"}, ensure_ascii=False) + "\n")
    with open(f"{root}/memory/glossary.jsonl", "w", encoding="utf-8") as f:
        for k, tp in t["topics"].items(): f.write(json.dumps({"canonical": tp["name"], "aliases": tp["aliases"], "topic": k}, ensure_ascii=False) + "\n")
        for g in t["glossary"]: f.write(json.dumps(g, ensure_ascii=False) + "\n")
    with open(f"{root}/memory/documents.jsonl", "w", encoding="utf-8") as f:
        for doc in t["documents"]:
            f.write(json.dumps({**doc, "owner": names.get(doc.get("owner")), "exists": os.path.exists(f"{root}/{doc['file']}")}, ensure_ascii=False) + "\n")
        for a in t["adrs"]:
            f.write(json.dumps({"file": f"adr/{a['id']}.md", "title": f"{a['id']}: {a['title']}", "updated": a["date"], "owner": names[a["author"]], "status": a["status"], "exists": True}, ensure_ascii=False) + "\n")
    return decs

# ---------- graph ----------
def graph(t, root, files, decs):
    names = {k: v["name"] for k, v in t["people"].items()}
    out = []
    for lab in ("Person", "Team", "Meeting", "Document", "ADR", "Decision", "Topic", "OpenItem", "PoC"):
        out.append(f"CREATE CONSTRAINT {lab.lower()}_key IF NOT EXISTS FOR (n:{lab}) REQUIRE n.key IS UNIQUE;")
    for k, p in t["people"].items():
        out.append(f"MERGE (n:Person {{key: {q('person:'+slug(p['name']))}}}) SET n.name = {q(p['name'])}, n.role = {q(p['role'])}, n.aliases = {q(p['aliases'])}" + (f", n.joined = {q(p['joined'])}" if p.get('joined') else "") + (f", n.left = {q(p['left'])}" if p.get('left') else "") + ";")
    for tk, tv in t["teams"].items():
        out.append(f"MERGE (n:Team {{key: {q('team:'+tk)}}}) SET n.name = {q(tv['name'])};")
        for m in tv["members"]: out.append(f"MATCH (p:Person {{key: {q('person:'+slug(names[m]))}}}), (t:Team {{key: {q('team:'+tk)}}}) MERGE (p)-[:MEMBER_OF]->(t);")
    for tk, tv in t["topics"].items():
        out.append(f"MERGE (n:Topic {{key: {q('topic:'+tk)}}}) SET n.name = {q(tv['name'])}, n.aliases = {q(tv['aliases'])};")
    for m in t["meetings"]:
        mk = "meeting:" + m["date"] + ("" if m["type"] == "weekly sync" else ":" + slug(m["type"]))
        m["_key"] = mk
        out.append(f"MERGE (n:Meeting {{key: {q(mk)}}}) SET n.date = {q(m['date'])}, n.type = {q(m['type'])}, n.file = {q(files[m['id']])};")
        for p in m["attendees"]: out.append(f"MATCH (p:Person {{key: {q('person:'+slug(names[p]))}}}), (m:Meeting {{key: {q(mk)}}}) MERGE (p)-[:ATTENDED]->(m);")
    mkey = {m["id"]: m["_key"] for m in t["meetings"]}
    for doc in t["documents"]:
        dk = "document:" + slug(doc["file"])
        out.append(f"MERGE (n:Document {{key: {q(dk)}}}) SET n.title = {q(doc['title'])}, n.file = {q(doc['file'])}, n.updated = {q(doc['updated'])};")
        if doc.get("owner"): out.append(f"MATCH (p:Person {{key: {q('person:'+slug(names[doc['owner']]))}}}), (d:Document {{key: {q(dk)}}}) MERGE (p)-[:AUTHORED]->(d);")
    for a in t["adrs"]:
        out.append(f"MERGE (n:ADR {{key: {q('adr:'+a['id'].lower())}}}) SET n.id = {q(a['id'])}, n.title = {q(a['title'])}, n.status = {q(a['status'])}, n.date = {q(a['date'])}, n.file = {q('adr/'+a['id']+'.md')};")
        out.append(f"MATCH (p:Person {{key: {q('person:'+slug(names[a['author']]))}}}), (a:ADR {{key: {q('adr:'+a['id'].lower())}}}) MERGE (p)-[:AUTHORED]->(a);")
    for a in t["adrs"]:
        if a.get("supersedes"): out.append(f"MATCH (a:ADR {{key: {q('adr:'+a['id'].lower())}}}), (b:ADR {{key: {q('adr:'+a['supersedes'].lower())}}}) MERGE (a)-[:SUPERSEDES]->(b);")
        if a.get("supersedes_section"): out.append(f"MATCH (a:ADR {{key: {q('adr:'+a['id'].lower())}}}), (b:ADR {{key: {q('adr:'+a['supersedes_section']['adr'].lower())}}}) MERGE (a)-[:SUPERSEDES {{section: {q(a['supersedes_section']['section'])}}}]->(b);")
    for pc in t["pocs"]:
        out.append(f"MERGE (n:PoC {{key: {q('poc:'+pc['id'])}}}) SET n.name = {q(pc['name'])}, n.from = {q(pc['period'][0])}, n.to = {q(pc['period'][1])}, n.report = {q(pc['report'])}, n.results = {q(json.dumps(pc['results']))};")
        out.append(f"MATCH (p:Person {{key: {q('person:'+slug(names[pc['owner']]))}}}), (c:PoC {{key: {q('poc:'+pc['id'])}}}) MERGE (p)-[:OWNS {{from: {q(pc['period'][0])}}}]->(c);")
        out.append(f"MATCH (c:PoC {{key: {q('poc:'+pc['id'])}}}), (m:Meeting {{key: {q(mkey[pc['reviewed']])}}}) MERGE (c)-[:REVIEWED_IN]->(m);")
    dkey = {}
    for d in t["decisions"]:
        k = f"decision:{d['topic']}:{d['date']}" + ("" if sum(1 for x in t['decisions'] if x['topic']==d['topic'] and x['date']==d['date']) == 1 else f":{d['id'].lower()}")
        dkey[d["id"]] = k
    rec = {r["id"]: r for r in decs}
    for d in t["decisions"]:
        k, r = dkey[d["id"]], rec[d["id"]]
        out.append(f"MERGE (n:Decision {{key: {q(k)}}}) SET n.id = {q(d['id'])}, n.text = {q(d['text'])}, n.date = {q(d['date'])}, n.status = {q(r['status'])}, n.source = {q(r['source'])}" + (f", n.note = {q(r['note'])}" if r.get("note") else "") + ";")
        out.append(f"MATCH (n:Decision {{key: {q(k)}}}), (t:Topic {{key: {q('topic:'+d['topic'])}}}) MERGE (n)-[:ABOUT]->(t);")
        out.append(f"MATCH (n:Decision {{key: {q(k)}}}), (m:Meeting {{key: {q(mkey[d['meeting']])}}}) MERGE (n)-[:DECIDED_IN]->(m);")
        if d.get("owner"): out.append(f"MATCH (p:Person {{key: {q('person:'+slug(names[d['owner']]))}}}), (n:Decision {{key: {q(k)}}}) MERGE (p)-[:OWNS {{from: {q(d['date'])}}}]->(n);")
        if d.get("proposer"): out.append(f"MATCH (p:Person {{key: {q('person:'+slug(names[d['proposer']]))}}}), (n:Decision {{key: {q(k)}}}) MERGE (p)-[:PROPOSED]->(n);")
        if d.get("objector"): out.append(f"MATCH (p:Person {{key: {q('person:'+slug(names[d['objector']]))}}}), (n:Decision {{key: {q(k)}}}) MERGE (p)-[:OBJECTED_TO]->(n);")
        if d.get("adr"): out.append(f"MATCH (n:Decision {{key: {q(k)}}}), (a:ADR {{key: {q('adr:'+d['adr'].lower())}}}) MERGE (n)-[:RECORDED_IN]->(a);")
        if d.get("poc"): out.append(f"MATCH (n:Decision {{key: {q(k)}}}), (c:PoC {{key: {q('poc:'+d['poc'])}}}) MERGE (n)-[:BASED_ON]->(c);")
        for dep in d.get("depends_on", []): out.append(f"MATCH (n:Decision {{key: {q(k)}}}), (m:Decision {{key: {q(dkey[dep])}}}) MERGE (n)-[:DEPENDS_ON]->(m);")
    for d in t["decisions"]:
        if d.get("supersedes"): out.append(f"MATCH (a:Decision {{key: {q(dkey[d['id']])}}}), (b:Decision {{key: {q(dkey[d['supersedes']])}}}) MERGE (a)-[:SUPERSEDES]->(b);")
    # ownership of topics over time, from decisions with `ownership` plus initial owners
    initial = {"retries": ("nikita", "2026-03-30"), "compute": ("sergey", "2026-06-15"), "iac": ("pavel", "2026-01-12"), "gateway": ("pavel", "2026-03-02"),
               "database": ("denis", "2026-04-06"), "slo": ("lena", "2026-01-26"), "security": ("yulia", "2026-03-23"), "cost": ("olga", "2026-02-09"), "idempotency": ("nikita", "2026-05-18")}
    spans = {tp: [[who, since, None]] for tp, (who, since) in initial.items()}
    for d in sorted(t["decisions"], key=lambda x: x["date"]):
        o = d.get("ownership")
        if o:
            spans.setdefault(o["topic"], [])
            for s in spans[o["topic"]]:
                if s[2] is None and s[0] == o["from"]: s[2] = d["date"]
            spans[o["topic"]].append([o["to"], d["date"], None])
    if "idempotency" in spans:  # D13 moved both retries and idempotency
        spans["idempotency"][0][2] = "2026-06-01"; spans["idempotency"].append(["anna", "2026-06-01", None])
    for tp, ss in spans.items():
        for who, since, until in ss:
            out.append(f"MATCH (p:Person {{key: {q('person:'+slug(names[who]))}}}), (t:Topic {{key: {q('topic:'+tp)}}}) MERGE (p)-[:OWNS {{from: {q(since)}" + (f", to: {q(until)}" if until else "") + "}]->(t);")
    for o in t["open_items"]:
        k = f"openitem:{o['topic']}:{o['raised']}"
        status = "closed" if (o.get("closed_by") or o.get("taken")) else "open"
        out.append(f"MERGE (n:OpenItem {{key: {q(k)}}}) SET n.id = {q(o['id'])}, n.text = {q(o['text'])}, n.raised = {q(o['raised'])}, n.status = {q(status)}, n.raised_again = {q(o.get('raised_again', []))};")
        out.append(f"MATCH (n:OpenItem {{key: {q(k)}}}), (t:Topic {{key: {q('topic:'+o['topic'])}}}) MERGE (n)-[:ABOUT]->(t);")
        out.append(f"MATCH (n:OpenItem {{key: {q(k)}}}), (m:Meeting {{key: {q(mkey[o['meeting']])}}}) MERGE (n)-[:RAISED_IN]->(m);")
        if o.get("owner") and o.get("taken"): out.append(f"MATCH (p:Person {{key: {q('person:'+slug(names[o['owner']]))}}}), (n:OpenItem {{key: {q(k)}}}) MERGE (p)-[:OWNS {{from: {q(o['taken'])}}}]->(n);")
        if o.get("closed_by"): out.append(f"MATCH (n:OpenItem {{key: {q(k)}}}), (d:Decision {{key: {q(dkey[o['closed_by']])}}}) MERGE (d)-[:CLOSES]->(n);")
    for doc in t["documents"]:
        for s in doc.get("stale", []):
            out.append(f"MATCH (d:Document {{key: {q('document:'+slug(doc['file']))}}}), (n:Decision {{key: {q(dkey[s['decision']])}}}) MERGE (n)-[:MAKES_STALE {{since: {q(s['since'])}, fact: {q(s['fact'])}}}]->(d);")
    open(f"{root}/memory/reference-graph.cypher", "w", encoding="utf-8").write("\n".join(out) + "\n")
    return dkey, spans

if __name__ == "__main__":
    root = sys.argv[1]
    t = load(root)
    errs = validate(t)
    if errs:
        print("VALIDATION ERRORS:"); [print("  " + e) for e in errs]; sys.exit(1)
    files = render_meetings(t, root)
    decs = ground_truth(t, root, files)
    render_adrs(t, root, {d["id"]: d for d in t["decisions"]})
    dkey, spans = graph(t, root, files, decs)
    json.dump({"dkey": dkey, "spans": spans, "files": files}, open(f"{root}/memory/_index.json", "w"), indent=1, ensure_ascii=False)
    print(f"meetings {len(t['meetings'])}, turns {sum(len(m['turns']) for m in t['meetings'])}, decisions {len(decs)}, adrs {len(t['adrs'])}, graph lines {sum(1 for _ in open(root+'/memory/reference-graph.cypher'))}")
    missing = [d['file'] for d in t['documents'] if not os.path.exists(f"{root}/{d['file']}")]
    print(f"docs still to write: {len(missing)}")
