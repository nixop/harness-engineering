#!/usr/bin/env python3
"""Feed every corpus source to the memory-writer agent over A2A, in
chronological order (meetings first, then docs, then Confluence), and keep
the agent's report for each. The agent has no file access, so the content
goes inside the message.

  agentic_ingest.py <a2a-base-url> <corpus-dir> <out.jsonl>
"""
import json, os, re, sys, time, uuid, urllib.request

def ask(base, agent, text, timeout=900):
    url = f"{base}/api/a2a/kagent/{agent}/"
    body = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "message/send",
            "params": {"message": {"role": "user", "kind": "message", "messageId": str(uuid.uuid4()),
                                   "parts": [{"kind": "text", "text": text}]}}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.load(r)
    return d, round(time.time() - t0, 1)

def sources(root):
    out = []
    for fn in sorted(f for f in os.listdir(os.path.join(root, "meetings")) if not f.startswith(".")):
        out.append(("meetings/" + fn, "meeting transcript (Russian, ASR)"))
    for fn in sorted(f for f in os.listdir(os.path.join(root, "docs")) if not f.startswith(".")):
        out.append(("docs/" + fn, "project document (Markdown)"))
    for fn in sorted(f for f in os.listdir(os.path.join(root, "confluence")) if not f.startswith(".")):
        out.append(("confluence/" + fn, "Confluence page (storage-format XHTML; ignore macros)"))
    return out

if __name__ == "__main__":
    base, root, out = sys.argv[1:4]
    with open(out, "w", encoding="utf-8") as f:
        for rel, kind in sources(root):
            content = open(os.path.join(root, rel), encoding="utf-8").read()
            msg = (f"Ingest this {kind} into memory. Source file: {rel}. "
                   f"Write every decision, ownership change, open item, commitment and durable fact as claims, "
                   f"following your rules. Then report what you wrote.\n\n--- BEGIN {rel} ---\n{content}\n--- END {rel} ---")
            try:
                d, secs = ask(base, "memory-writer", msg)
                r = d.get("result", {})
                answer = " ".join(p.get("text", "") for a in r.get("artifacts", []) for p in a.get("parts", []))
                calls = [p.get("data", {}).get("name") for m in r.get("history", []) for p in m.get("parts", []) if p.get("kind") == "data" and "name" in p.get("data", {})]
                rec = {"file": rel, "state": r.get("status", {}).get("state"), "secs": secs, "tool_calls": calls, "report": answer, "raw": d}
            except Exception as e:
                rec = {"file": rel, "state": "error", "secs": 0, "tool_calls": [], "report": str(e)[:500]}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
            print(f"{rel}: {rec['state']} {rec['secs']}s calls={len(rec['tool_calls'])} | {rec['report'][:100]}", file=sys.stderr)
