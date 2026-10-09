#!/usr/bin/env python3
"""Send every Relay source to the tool-less memory-extractor agent over A2A
and keep its JSON. Sources go in chronological order: meetings by date,
then ADRs, docs and Confluence pages. The agent writes nothing; the output
is validated and turned into memory by agentic_build.py.

  agentic_extract.py <a2a-base-url> <corpus-dir> <out.jsonl> [--only meetings|adr|docs]
"""
import json, os, re, sys, time, uuid, urllib.request

def ask(base, agent, text, timeout=600):
    url = f"{base}/api/a2a/kagent/{agent}/"
    body = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "message/send",
            "params": {"message": {"role": "user", "kind": "message", "messageId": str(uuid.uuid4()),
                                   "parts": [{"kind": "text", "text": text}]}}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.load(r)
    return d, round(time.time() - t0, 1)

def sources(root, only=None):
    out = []
    def ls(sub): return sorted(f for f in os.listdir(os.path.join(root, sub)) if not f.startswith("."))
    if only in (None, "meetings"):
        out += [("meetings/" + f, "meeting transcript (Russian, ASR output without punctuation)") for f in ls("meetings")]
    if only in (None, "adr"):
        out += [("adr/" + f, "architecture decision record (Markdown)") for f in ls("adr")]
    if only in (None, "docs"):
        out += [("docs/" + f, "project document (Markdown with front matter)") for f in ls("docs")]
        out += [("confluence/" + f, "Confluence page (storage-format XHTML; ignore macros)") for f in ls("confluence")]
    return out

def parse_json(text):
    text = text.strip()
    m = re.search(r"\{.*\}", text, re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None

if __name__ == "__main__":
    base, root, out = sys.argv[1:4]
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    with open(out, "w", encoding="utf-8") as f:
        for rel, kind in sources(root, only):
            content = open(os.path.join(root, rel), encoding="utf-8").read()
            msg = (f"Extract the memory claims from this {kind}. Source file: {rel}.\n"
                   f"Return the JSON object only.\n\n--- BEGIN {rel} ---\n{content}\n--- END {rel} ---")
            try:
                d, secs = ask(base, "memory-extractor", msg)
                r = d.get("result", {})
                answer = " ".join(p.get("text", "") for a in r.get("artifacts", []) for p in a.get("parts", []))
                rec = {"file": rel, "state": r.get("status", {}).get("state"), "secs": secs, "json": parse_json(answer), "answer": answer}
            except Exception as e:
                rec = {"file": rel, "state": "error", "secs": 0, "json": None, "answer": str(e)[:500]}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
            j = rec["json"] or {}
            print(f"{rel}: {rec['state']} {rec['secs']}s json={'ok' if rec['json'] else 'NONE'} "
                  f"dec={len(j.get('decisions', []))} own={len(j.get('ownership', []))} oi={len(j.get('open_items', []))} unres={len(j.get('unresolved', []))}", file=sys.stderr)
