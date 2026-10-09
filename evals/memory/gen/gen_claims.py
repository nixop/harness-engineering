#!/usr/bin/env python3
"""Build the claim records for the vector layer from memory/*.jsonl (decisions, open items, ownership spans).

  gen_claims.py <corpus-root>   -> evals/memory/relay-claims.jsonl
"""
import sys
import json, re
root=sys.argv[1] if len(sys.argv)>1 else 'corpus/relay'
def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
rows=[]
for l in open(f'{root}/memory/decisions.jsonl', encoding='utf-8'):
    d=json.loads(l)
    kind = "ownership" if d.get("ownership") else "decision"
    text = (f"# claim {d['id']} | {d['topic']} | {d['date']} | {d['status']}\n{d['decision']}."
            + (f"\nSupersedes {d['supersedes']}." if d.get('supersedes') else "") + (f" Superseded by {d['superseded_by']}." if d.get('superseded_by') else "")
            + f"\nOwner: {d.get('owner') or 'none'}. Proposed by {d.get('proposer') or 'n/a'}" + (f"; objection from {d['objector']}." if d.get('objector') else ".")
            + (f" Recorded in {d['adr']}." if d.get('adr') else "") + (f" Based on {d['poc']}." if d.get('poc') else "")
            + (f"\nNote: {d['note']}" if d.get('note') else "") + f"\nSource: {d['source']}.")
    rows.append({"id": d["id"], "text": text, "metadata": {"file": d["source"], "source": "claim", "lang": "en", "date": d["date"], "claim_id": f"decision:{d['topic']}:{d['date']}", "kind": kind, "topic": d["topic"], "status": d["status"], "owner": d.get("owner") or "", "adr": d.get("adr") or ""}})
for l in open(f'{root}/memory/open_items.jsonl', encoding='utf-8'):
    o=json.loads(l)
    text = (f"# claim {o['id']} | {o['topic']} | raised {o['raised']} | {o['status']}\nOPEN ITEM: {o['text']}. Raised {o['raised']}" + (f", raised again on {', '.join(o['raised_again'])}" if o.get('raised_again') else "")
            + (f". Owner: {o['owner']} since {o['taken']}." if o.get('owner') and o.get('taken') else ". No owner.") + (f" Closed by {o['closed_by']}." if o.get('closed_by') else "") + f"\nSource: {o['source']}.")
    rows.append({"id": o["id"], "text": text, "metadata": {"file": o["source"], "source": "claim", "lang": "en", "date": o["raised"], "claim_id": f"openitem:{o['topic']}:{o['raised']}", "kind": "open_item", "topic": o["topic"], "status": o["status"], "owner": o.get("owner") or ""}})
idx=json.load(open(f'{root}/memory/_index.json'))
names={json.loads(l)['key']: json.loads(l)['name'] for l in open(f'{root}/memory/people.jsonl', encoding='utf-8')}
for tp, spans in idx['spans'].items():
    for who, since, until in spans:
        text=f"# claim ownership | {tp} | {since}\n{names[who]} owns {tp} from {since}" + (f" to {until}." if until else " (current).")
        rows.append({"id": f"own-{tp}-{since}", "text": text, "metadata": {"file": "memory/decisions.jsonl", "source": "claim", "lang": "en", "date": since, "claim_id": f"ownership:{tp}:{since}", "kind": "ownership", "topic": tp, "status": "superseded" if until else "active", "owner": names[who]}})
open('evals/memory/relay-claims.jsonl','w',encoding='utf-8').write("\n".join(json.dumps(r, ensure_ascii=False) for r in rows)+"\n")
print(len(rows), "claims (decisions + open items + ownership spans)")
