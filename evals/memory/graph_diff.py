#!/usr/bin/env python3
"""Compare the graph the memory-writer agent built with the ground truth.

  graph_diff.py <corpus-dir> <graph-nodes.json> <graph-edges.json>

Reports: Person nodes vs the register (entity resolution), Decision nodes
matched to ground-truth decisions by topic + date (recall / precision),
SUPERSEDES edges found vs expected, open items, unresolved flags, and
foreign labels.
"""
import json, re, sys
from collections import Counter, defaultdict

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def main(root, nodes_path, edges_path):
    nodes = json.load(open(nodes_path, encoding="utf-8")); edges = json.load(open(edges_path, encoding="utf-8"))
    people = [json.loads(l) for l in open(f"{root}/memory/people.jsonl", encoding="utf-8")]
    truth = [json.loads(l) for l in open(f"{root}/memory/decisions.jsonl", encoding="utf-8")]
    by_label = defaultdict(list)
    for n in nodes: by_label[n["label"]].append(n)
    print("## Labels:", dict(Counter(n["label"] for n in nodes)), "| foreign:", sorted(set(by_label) - {"Person","Decision","Meeting","Document","Topic","OpenItem"}))
    # people
    canon = {slug(p["name"]) for p in people}
    pk = Counter(slug(n.get("name") or n["key"].split(":",1)[1]) for n in by_label["Person"])
    print(f"## Person nodes: {len(by_label['Person'])} for {len(people)} people; distinct after slugging: {len(pk)}; duplicates per person: {dict(pk)}; unresolved flagged: {sum(1 for n in by_label['Person'] if n.get('unresolved'))}")
    # decisions by (topic, date)
    td = truth and [t for t in truth if not t["id"].startswith("O")]
    truth_keys = {(slug(t["topic"]), t["date"]): t for t in td}
    found = {}
    for n in by_label["Decision"]:
        m = re.match(r"decision:([a-z0-9-]+):(\d{4}-\d{2}-\d{2})", n["key"] or "")
        if m: found.setdefault((m.group(1), m.group(2)), []).append(n)
    topic_alias = {"charge": "retries", "gateway": "gateway-timeout", "tariffs-legacy-code-exports": "tariffs"}
    hits = {}
    for (t, d), ns in found.items():
        tt = topic_alias.get(t, t)
        if (tt, d) in truth_keys: hits[(tt, d)] = ns
    print(f"## Decisions: {len(by_label['Decision'])} nodes vs {len(td)} in truth; matched truth decisions (topic+date): {len(hits)}/{len(td)} recall={len(hits)/len(td):.2f}; precision (nodes that match a truth decision)={sum(len(v) for v in hits.values())/max(1,len(by_label['Decision'])):.2f}")
    for k, t in truth_keys.items():
        print(f"   {'OK ' if k in hits else 'MISS'} {t['id']} {k[0]}@{k[1]}: {t['decision'][:70]}")
    # supersedes
    sup = [e for e in edges if e["type"] == "SUPERSEDES"]
    self_loops = [e for e in sup if e["from_key"] == e["to_key"]]
    print(f"## SUPERSEDES: {len(sup)} edges (expected 3), self-loops: {len(self_loops)}; statuses: {dict(Counter(n.get('status') for n in by_label['Decision']))}")
    for e in sup: print("   ", e["from_key"], "->", e["to_key"])
    # owners
    owns = [e for e in edges if e["type"] == "OWNS"]
    print(f"## OWNS edges: {len(owns)}; with from date: {sum(1 for e in owns if e.get('from_date'))}; with to date: {sum(1 for e in owns if e.get('to_date'))}")
    # open items
    oi = by_label["OpenItem"]
    print(f"## OpenItem nodes: {len(oi)} (expected 1):")
    for n in oi: print("   ", n["key"], "|", (n.get("text") or "")[:80])
    # topics
    print("## Topics:", sorted(n["key"] for n in by_label["Topic"]))

if __name__ == "__main__":
    main(*sys.argv[1:4])
