#!/usr/bin/env python3
"""Ask every question to one kagent agent over A2A and save the full trace.

  agent_eval.py <a2a-base-url> <agent-name> <questions.jsonl> <out.jsonl>

<a2a-base-url> is the gateway, e.g. http://<gw-ip>; the agent endpoint is
<base>/api/a2a/kagent/<agent>/. Each record keeps the final answer, every
history message (tool calls and tool results included, as kagent returns
them) and wall time. Scoring is done separately, by a human reading traces.
"""
import json, sys, time, uuid, urllib.request

def ask(base, agent, text, timeout=300):
    url = f"{base}/api/a2a/kagent/{agent}/"
    body = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "message/send",
            "params": {"message": {"role": "user", "kind": "message", "messageId": str(uuid.uuid4()),
                                   "parts": [{"kind": "text", "text": text}]}}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.load(r)
    return d, round(time.time() - t0, 1)

def summarize(d):
    r = d.get("result", {})
    answer = " ".join(p.get("text", "") for a in r.get("artifacts", []) for p in a.get("parts", []))
    hist = r.get("history", [])
    calls = []
    for m in hist:
        for p in m.get("parts", []):
            if p.get("kind") == "data":
                data = p.get("data", {})
                if "name" in data and "args" in data:          # function call
                    calls.append({"tool": data["name"], "args": data.get("args")})
                elif "response" in data or "result" in data:   # function response
                    calls.append({"result": str(data.get("response", data.get("result")))[:3000]})
    return {"state": r.get("status", {}).get("state"), "answer": answer, "calls": calls, "history_len": len(hist)}

if __name__ == "__main__":
    base, agent, qpath, out = sys.argv[1:5]
    qs = [json.loads(l) for l in open(qpath, encoding="utf-8")]
    with open(out, "w", encoding="utf-8") as f:
        for q in qs:
            try:
                d, secs = ask(base, agent, q["q"])
                s = summarize(d)
                s["raw"] = d
            except Exception as e:
                s, secs = {"state": "error", "answer": str(e)[:500], "calls": [], "history_len": 0}, 0
            rec = {"id": q["id"], "lang": q["lang"], "agent": agent, "q": q["q"], "expect": q["expect"],
                   "expected_answer": q["answer"], "secs": secs, **s}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
            print(f"{q['id']} {agent} {s['state']} {secs}s calls={len([c for c in s['calls'] if 'tool' in c])} | {s['answer'][:90]}", file=sys.stderr)
