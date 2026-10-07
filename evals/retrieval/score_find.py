#!/usr/bin/env python3
"""hit@k for raw find results. A hit is the expected object's chunk header
("# <file> | <kind> <ns>/<name>") appearing anywhere in the returned text,
which both MCP servers include verbatim because it is the first line of
every chunk. Rank is the position of the first chunk whose header matches.

  score_find.py <label> <find-results.jsonl> [more label/file pairs...]
"""
import json, re, sys
from collections import defaultdict

def rank_of(raw, exp):
    needle = f"# {exp['file']} | {exp['kind']} "
    # split into entries on chunk headers; each chunk starts with "# <file> | "
    heads = [m.start() for m in re.finditer(r"# [\w./-]+\.ya?ml \| ", raw)]
    for i, pos in enumerate(heads):
        seg = raw[pos: heads[i+1] if i+1 < len(heads) else pos+400]
        if seg.startswith(needle) and f"/{exp['name']}" in seg.split("\n")[0]:
            return i + 1
    return None

def main(pairs):
    table = {}
    for label, path in pairs:
        rows = [json.loads(l) for l in open(path, encoding="utf-8")]
        agg = defaultdict(lambda: {"n": 0, "hit1": 0, "hit5": 0, "mrr": 0.0, "ms": 0})
        for r in rows:
            k = rank_of(r["raw"], r["expect"])
            if k and k > 5: k = None   # cap at 5: the servers return 5 (branch) vs 10 (official) entries
            for key in (r["lang"], "all"):
                a = agg[key]; a["n"] += 1; a["ms"] += r["ms"]
                if k: a["mrr"] += 1.0 / k; a["hit5"] += int(k <= 5); a["hit1"] += int(k == 1)
            r["rank"] = k
        table[label] = {k: {"hit@1": round(v["hit1"]/v["n"],2), "hit@5": round(v["hit5"]/v["n"],2),
                            "mrr": round(v["mrr"]/v["n"],2), "avg_ms": v["ms"]//v["n"], "n": v["n"]} for k, v in agg.items()}
        with open(path.replace(".jsonl", ".ranked.jsonl"), "w", encoding="utf-8") as f:
            for r in rows: f.write(json.dumps({k: r[k] for k in ("id","lang","q","expect","rank","ms")}, ensure_ascii=False)+"\n")
    print(f"{'embedder':<12} {'lang':<4} {'hit@1':>6} {'hit@5':>6} {'mrr':>5} {'ms':>6}")
    for label, by in table.items():
        for lang in ("en", "ru", "all"):
            v = by.get(lang)
            if v: print(f"{label:<12} {lang:<4} {v['hit@1']:>6} {v['hit@5']:>6} {v['mrr']:>5} {v['avg_ms']:>6}")
    json.dump(table, open("find-scores.json", "w"), indent=1)

if __name__ == "__main__":
    a = sys.argv[1:]
    main(list(zip(a[0::2], a[1::2])))
