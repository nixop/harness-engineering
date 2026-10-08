#!/usr/bin/env python3
"""Render agent traces side by side for manual scoring, and compute the
summary once scores are filled in.

  judge_sheet.py render <runs-dir>            -> prints a markdown sheet per question
  judge_sheet.py summarize <runs-dir> <scores.json>

scores.json: {"<qid>": {"<agent>": 0|1|2}} where 2 = correct and grounded in a
retrieved chunk, 1 = partially correct or correct but unsupported, 0 = wrong,
"not found", or hallucinated.
"""
import json, sys, glob, os
from collections import defaultdict

def load(runs):
    out = {}
    for f in sorted(glob.glob(os.path.join(runs, "agent-*.jsonl"))):
        agent = os.path.basename(f)[len("agent-"):-len(".jsonl")]
        out[agent] = {json.loads(l)["id"]: json.loads(l) for l in open(f, encoding="utf-8")}
    return out

def render(runs):
    data = load(runs)
    agents = list(data)
    qids = sorted(next(iter(data.values())).keys())
    for q in qids:
        r0 = data[agents[0]][q]
        print(f"\n## {q} [{r0['lang']}{(' / ' + r0['class']) if r0.get('class') else ''}] {r0['q']}\n**expected:** {r0['expected_answer']}  \n**expected sources:** {r0['expect']}")
        for a in agents:
            r = data[a][q]
            tools = [c for c in r["calls"] if "tool" in c]
            queries = [str(c["args"].get("query", c["args"]))[:80] for c in tools if isinstance(c.get("args"), dict)]
            print(f"\n### {a} ({r['state']}, {r['secs']}s, {len(tools)} tool calls)\nqueries: {queries}\n\n{r['answer'][:1200]}")

def summarize(runs, scores_path):
    data = load(runs); scores = json.load(open(scores_path))
    agg = defaultdict(lambda: defaultdict(lambda: {"n": 0, "sum": 0, "full": 0, "zero": 0, "calls": 0, "secs": 0.0}))
    for q, by in scores.items():
        for a, s in by.items():
            r = data[a][q]
            for lang in (r["lang"], "all") + ((r["class"],) if r.get("class") else ()):
                x = agg[a][lang]; x["n"] += 1; x["sum"] += s; x["full"] += int(s == 2); x["zero"] += int(s == 0)
                x["calls"] += len([c for c in r["calls"] if "tool" in c]); x["secs"] += r["secs"]
    print(f"{'agent':<26} {'slice':<13} {'n':>3} {'score%':>7} {'correct':>8} {'wrong':>6} {'calls':>6} {'secs':>5}")
    for a, by in agg.items():
        for lang in ("en", "ru", "fact", "temporal", "attribution", "contradiction", "unowned", "crosslingual", "all"):
            x = by.get(lang)
            if x: print(f"{a:<26} {lang:<13} {x['n']:>3} {100*x['sum']/(2*x['n']):>6.0f}% {x['full']:>8} {x['zero']:>6} {x['calls']/x['n']:>6.1f} {x['secs']/x['n']:>5.1f}")

if __name__ == "__main__":
    if sys.argv[1] == "render": render(sys.argv[2])
    else: summarize(sys.argv[2], sys.argv[3])
