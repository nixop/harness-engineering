#!/usr/bin/env python3
"""Generate templated evaluation questions from the Relay timeline and merge
the hand-written ones from source/questions-manual.jsonl.

  gen_questions.py <corpus-dir>   -> memory/questions.jsonl

Templated classes (each in EN and RU where it makes sense):
  current        current decision on a topic with >= 2 decisions
  history        ordered history of a topic with a supersession chain
  chain          multi-hop: what did the decision that replaced X replace
  owner_now      current owner of a topic that changed hands
  owner_at       owner of a topic at a date between transfers
  objector       who objected to a decision, and who proposed it
  aggregate      counts: superseded decisions per topic, decisions owned by a person, ADR statuses
  unowned_at     open items with no owner at a date
  stale_docs     which documents are stale on a date and why
  poc_basis      which PoC and which numbers a decision rests on
  adr_status     status and supersession of an ADR
  dependency     what a decision depends on
"""
import json, os, sys, random
import yaml

def load(root):
    t = yaml.safe_load(open(f"{root}/source/timeline.yaml", encoding="utf-8"))
    idx = json.load(open(f"{root}/memory/_index.json", encoding="utf-8"))
    decs = [json.loads(l) for l in open(f"{root}/memory/decisions.jsonl", encoding="utf-8")]
    opens = [json.loads(l) for l in open(f"{root}/memory/open_items.jsonl", encoding="utf-8")]
    return t, idx, decs, opens

def main(root):
    t, idx, decs, opens = load(root)
    names = {k: v["name"] for k, v in t["people"].items()}
    tname = {k: v["name"] for k, v in t["topics"].items()}
    by_id = {d["id"]: d for d in decs}
    qs = []
    n = [0]
    def add(cls, lang, q, answer, sources, layer="both", hops=1):
        n[0] += 1
        qs.append({"id": f"t{n[0]:02d}", "class": cls, "lang": lang, "q": q, "answer": answer, "sources": sorted(set(sources)), "layer": layer, "hops": hops})
    # current + history per topic with a chain
    for tk in t["topics"]:
        chain = [d for d in decs if d["topic"] == tk and (d.get("supersedes") or d.get("superseded_by"))]
        if not chain: continue
        cur = [d for d in decs if d["topic"] == tk and d["status"] == "active" and (d.get("supersedes"))]
        if cur:
            c = cur[-1]
            hist = sorted([d for d in decs if d["topic"] == tk and d["status"] in ("active", "superseded")], key=lambda d: d["date"])
            hist_txt = " → ".join(f"{d['date']}: {d['decision']}" for d in hist)
            add("current", "en", f"What is the current decision on {tname[tk]}, and when was it made?", f"{c['decision']} (decided {c['date']}, owner {c['owner']})", [c["source"]], "both")
            add("history", "ru", f"Как менялось решение по теме «{tname[tk]}»? Перечисли по датам.", hist_txt, [d["source"] for d in hist], "both", hops=len(hist))
            # chain: two hops
            if c.get("supersedes") and by_id[c["supersedes"]].get("supersedes"):
                mid = by_id[c["supersedes"]]; first = by_id[mid["supersedes"]]
                add("chain", "en", f"The current decision on {tname[tk]} replaced an earlier one. What did that earlier decision itself replace, and when?", f"{c['decision']} ({c['date']}) replaced '{mid['decision']}' ({mid['date']}), which replaced '{first['decision']}' ({first['date']})", [c["source"], mid["source"], first["source"]], "graph", hops=3)
    # ownership
    spans = idx["spans"]
    for tk, ss in spans.items():
        if len(ss) < 2: continue
        cur = [s for s in ss if s[2] is None][-1]
        add("owner_now", "ru", f"Кто сейчас владеет темой «{tname[tk]}» и с какой даты?", f"{names[cur[0]]}, с {cur[1]}", [d["source"] for d in decs if d.get("ownership", {}).get("topic") == tk], "graph")
        # at a date in the middle of the second-to-last span
        prev = ss[-2]
        mid_date = prev[1][:8] + "15" if prev[1][8:] < "15" else prev[1][:8] + "28"
        if prev[2] and mid_date < prev[2]:
            add("owner_at", "en", f"Who owned {tname[tk]} on {mid_date}?", f"{names[prev[0]]} (from {prev[1]} to {prev[2]})", [d["source"] for d in decs if d.get("ownership", {}).get("topic") == tk], "graph", hops=2)
    # objectors
    for d in decs:
        if d.get("objector"):
            add("objector", "ru" if int(d["id"][1:]) % 2 else "en",
                (f"Кто предложил и кто возражал против решения «{d['decision'][:60]}…»?" if int(d["id"][1:]) % 2 else f"Who proposed and who objected to the decision '{d['decision'][:60]}…'?"),
                f"proposer {d['proposer']}, objector {d['objector']}, {d['date']}", [d["source"]], "both")
    # aggregates
    sup = [d for d in decs if d["status"] == "superseded"]
    add("aggregate", "en", "How many decisions have been superseded, and on which topics?", f"{len(sup)}: " + "; ".join(f"{d['id']} ({tname[d['topic']]}, {d['date']})" for d in sup), [d["source"] for d in sup], "graph", hops=len(sup))
    for who in ("anna", "pavel", "ivan", "lena"):
        own = [d for d in decs if d.get("owner") == names[who] and d["status"] == "active"]
        add("aggregate", "ru", f"Какими действующими решениями владеет {names[who]}? Сколько их?", f"{len(own)}: " + "; ".join(f"{d['id']} {d['decision'][:50]}" for d in own), [d["source"] for d in own], "graph", hops=len(own))
    st = {}
    for a in t["adrs"]: st.setdefault(a["status"], []).append(a["id"])
    add("aggregate", "en", "Which ADRs are not Accepted, and what is their status?", "; ".join(f"{s}: {', '.join(v)}" for s, v in st.items() if s != "Accepted"), [f"adr/{a['id']}.md" for a in t["adrs"] if a["status"] != "Accepted"], "both")
    # unowned at dates
    for date in ("2026-06-15", "2026-08-17", "2026-10-05"):
        un = [o for o in opens if o["raised"] <= date and not (o.get("taken") and o["taken"] <= date) and not (o.get("closed_by") and by_id[o["closed_by"]]["date"] <= date)]
        add("unowned_at", "ru" if date < "2026-09" else "en",
            (f"Какие открытые вопросы были без владельца на {date}?" if date < "2026-09" else f"Which open items had no owner on {date}?"),
            "; ".join(f"{o['id']} {o['text']} (raised {o['raised']})" for o in un), [o["source"] for o in un], "graph", hops=len(un))
    # stale docs at a date
    for date in ("2026-07-01", "2026-10-05"):
        stale = []
        for doc in t["documents"]:
            for s in doc.get("stale", []):
                if s["since"] <= date: stale.append(f"{doc['file']} (updated {doc['updated']}): {s['fact']}, changed by {s['decision']} on {s['since']}")
        add("stale_docs", "en", f"Which documents were out of date on {date}, and why?", "; ".join(stale), [doc["file"] for doc in t["documents"] if any(s["since"] <= date for s in doc.get("stale", []))], "both", hops=len(stale))
    # poc basis
    for d in decs:
        if d.get("poc"):
            pc = next(p for p in t["pocs"] if p["id"] == d["poc"])
            add("poc_basis", "ru", f"На каком PoC и на каких цифрах основано решение «{d['decision'][:60]}…»?", f"{pc['name']}: {json.dumps(pc['results'], ensure_ascii=False)}; report {pc['report']}", [d["source"], pc["report"]], "both", hops=2)
    # adr status
    for a in t["adrs"]:
        if a.get("superseded_by") or a["status"] in ("Rejected", "Proposed"):
            add("adr_status", "en", f"What is the status of {a['id']} ('{a['title']}')?", f"{a['status']}" + (f", superseded by {a['superseded_by']}" if a.get("superseded_by") else "") + (f"; {a['note']}" if a.get("note") else ""), [f"adr/{a['id']}.md"], "both")
    # dependency
    for d in decs:
        for dep in d.get("depends_on") or []:
            add("dependency", "en", f"What did the decision '{d['decision'][:60]}…' depend on?", f"{by_id[dep]['decision']} ({by_id[dep]['date']})", [d["source"], by_id[dep]["source"]], "graph", hops=2)
    # merge manual
    manual_path = f"{root}/source/questions-manual.jsonl"
    manual = [json.loads(l) for l in open(manual_path, encoding="utf-8")] if os.path.exists(manual_path) else []
    for i, m in enumerate(manual, 1):
        m.setdefault("id", f"m{i:02d}"); m.setdefault("layer", "both"); m.setdefault("hops", 1)
    allq = qs + manual
    with open(f"{root}/memory/questions.jsonl", "w", encoding="utf-8") as f:
        for x in allq: f.write(json.dumps(x, ensure_ascii=False) + "\n")
    from collections import Counter
    print(f"{len(qs)} templated + {len(manual)} manual = {len(allq)} questions;", dict(Counter(x['class'] for x in allq)), dict(Counter(x['lang'] for x in allq)))

if __name__ == "__main__":
    main(sys.argv[1])
