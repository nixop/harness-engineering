#!/usr/bin/env python3
"""Emit the Cypher (dates are ISO strings: the neo4j MCP serialises Neo4j date() values as empty) that builds the reference memory graph from
corpus/ledger/memory/{people,decisions}.jsonl and the meeting files.
Deterministic keys, MERGE only, so it is idempotent and matches the rules in
ADR-0003.

  graph_from_truth.py <corpus-dir> > reference-graph.cypher
"""
import json, os, re, sys

def q(s): return json.dumps(s, ensure_ascii=False)
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def main(root):
    mem = os.path.join(root, "memory")
    people = [json.loads(l) for l in open(os.path.join(mem, "people.jsonl"), encoding="utf-8")]
    decisions = [json.loads(l) for l in open(os.path.join(mem, "decisions.jsonl"), encoding="utf-8")]
    alias = {}
    for p in people:
        for a in p["aliases"] + [p["name"]]: alias[a.lower()] = p["name"]
    out = []
    out.append("CREATE CONSTRAINT person_key IF NOT EXISTS FOR (n:Person) REQUIRE n.key IS UNIQUE;")
    out.append("CREATE CONSTRAINT decision_key IF NOT EXISTS FOR (n:Decision) REQUIRE n.key IS UNIQUE;")
    out.append("CREATE CONSTRAINT meeting_key IF NOT EXISTS FOR (n:Meeting) REQUIRE n.key IS UNIQUE;")
    out.append("CREATE CONSTRAINT topic_key IF NOT EXISTS FOR (n:Topic) REQUIRE n.key IS UNIQUE;")
    out.append("CREATE CONSTRAINT openitem_key IF NOT EXISTS FOR (n:OpenItem) REQUIRE n.key IS UNIQUE;")
    out.append("CREATE CONSTRAINT document_key IF NOT EXISTS FOR (n:Document) REQUIRE n.key IS UNIQUE;")
    for p in people:
        k = "person:" + slug(p["name"])
        out.append(f"MERGE (n:Person {{key: {q(k)}}}) SET n.name = {q(p['name'])}, n.role = {q(p['role'])}, n.aliases = {q(p['aliases'])}" + (f", n.joined = {q(p['joined'])}" if p.get("joined") else "") + ";")
    # meetings + attendance from transcript headers
    for fn in sorted(os.listdir(os.path.join(root, "meetings"))):
        head = open(os.path.join(root, "meetings", fn), encoding="utf-8").readline()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", fn).group(1)
        mk = "meeting:" + date
        out.append(f"MERGE (m:Meeting {{key: {q(mk)}}}) SET m.date = {q(date)}, m.file = {q('meetings/'+fn)}, m.title = {q('Ledger sync '+date)};")
        spk = re.search(r"speakers: (.*)", head)
        for s in (spk.group(1).split(", ") if spk else []):
            name = alias.get(s.strip().lower())
            if name: out.append(f"MATCH (p:Person {{key: {q('person:'+slug(name))}}}), (m:Meeting {{key: {q(mk)}}}) MERGE (p)-[:ATTENDED]->(m);")
    # documents
    for sub in ("docs", "confluence"):
        for fn in sorted(os.listdir(os.path.join(root, sub))):
            raw = open(os.path.join(root, sub, fn), encoding="utf-8").read()
            if sub == "docs":
                t = re.search(r"^title: (.*)$", raw, re.M); u = re.search(r"^updated: (.*)$", raw, re.M); o = re.search(r"^owner: (.*)$", raw, re.M)
                title, updated, owner = t.group(1), u.group(1), o.group(1) if o else ""
            else:
                m = re.search(r"title: (.*?), version: \d+, last updated: (\S+) by (.*?) -->", raw)
                title, updated, owner = m.group(1), m.group(2), m.group(3)
            dk = "document:" + slug(f"{sub}-{fn}")
            out.append(f"MERGE (d:Document {{key: {q(dk)}}}) SET d.title = {q(title)}, d.file = {q(sub+'/'+fn)}, d.updated = {q(updated)}, d.source = {q(sub)};")
            if owner in alias.values():
                out.append(f"MATCH (p:Person {{key: {q('person:'+slug(owner))}}}), (d:Document {{key: {q(dk)}}}) MERGE (p)-[:AUTHORED]->(d);")
    # decisions and open items
    for d in decisions:
        tk = "topic:" + slug(d["topic"])
        out.append(f"MERGE (t:Topic {{key: {q(tk)}}}) SET t.name = {q(d['topic'])};")
        if d["id"].startswith("O"):
            k = "openitem:" + slug(d["topic"]) + ":" + d["date"]
            out.append(f"MERGE (o:OpenItem {{key: {q(k)}}}) SET o.text = {q(d['decision'])}, o.raised = {q(d['date'])}, o.status = {q(d['status'])}, o.source = {q(d['source'])};")
            out.append(f"MATCH (o:OpenItem {{key: {q(k)}}}), (t:Topic {{key: {q(tk)}}}) MERGE (o)-[:ABOUT]->(t);")
            mdate = re.search(r"(\d{4}-\d{2}-\d{2})", d["source"]).group(1)
            out.append(f"MATCH (o:OpenItem {{key: {q(k)}}}), (m:Meeting {{key: {q('meeting:'+mdate)}}}) MERGE (o)-[:RAISED_IN]->(m);")
            continue
        k = "decision:" + slug(d["topic"]) + ":" + d["date"]
        out.append(f"MERGE (n:Decision {{key: {q(k)}}}) SET n.id = {q(d['id'])}, n.text = {q(d['decision'])}, n.date = {q(d['date'])}, n.status = {q(d['status'])}, n.source = {q(d['source'])}" + (f", n.note = {q(d['note'])}" if d.get("note") else "") + ";")
        out.append(f"MATCH (n:Decision {{key: {q(k)}}}), (t:Topic {{key: {q(tk)}}}) MERGE (n)-[:ABOUT]->(t);")
        mdate = re.search(r"(\d{4}-\d{2}-\d{2})", d["source"]).group(1)
        out.append(f"MATCH (n:Decision {{key: {q(k)}}}), (m:Meeting {{key: {q('meeting:'+mdate)}}}) MERGE (n)-[:DECIDED_IN]->(m);")
        for owner in (d.get("owner") or "").split(";"):
            owner = owner.strip()
            if owner in alias.values():
                out.append(f"MATCH (p:Person {{key: {q('person:'+slug(owner))}}}), (n:Decision {{key: {q(k)}}}) MERGE (p)-[:OWNS {{from: {q(d['date'])}}}]->(n);")
    byid = {d["id"]: d for d in decisions}
    for d in decisions:
        if d.get("supersedes"):
            old = byid[d["supersedes"]]
            k_new = "decision:" + slug(d["topic"]) + ":" + d["date"]; k_old = "decision:" + slug(old["topic"]) + ":" + old["date"]
            out.append(f"MATCH (a:Decision {{key: {q(k_new)}}}), (b:Decision {{key: {q(k_old)}}}) MERGE (a)-[:SUPERSEDES]->(b);")
    # ownership transfer as explicit edges on the topic
    out.append("MATCH (p:Person {key: 'person:oleg-prikhodko'}), (t:Topic {key: 'topic:retries'}) MERGE (p)-[:OWNS {from: '2026-08-31', to: '2026-09-21'}]->(t);")
    out.append("MATCH (p:Person {key: 'person:dasha-volkova'}), (t:Topic {key: 'topic:retries'}) MERGE (p)-[:OWNS {from: '2026-09-21'}]->(t);")
    print("\n".join(out))

if __name__ == "__main__":
    main(sys.argv[1])
