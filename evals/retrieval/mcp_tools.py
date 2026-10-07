#!/usr/bin/env python3
"""Talk to a kmcp-hosted MCP server over streamable HTTP: list tools, ingest
chunks through its store tool, or run find queries. Used by TASK-0003 so that
all three collections receive the identical chunk list and so that hit@k is
measured on the raw retrieval, without an LLM in the loop.

  mcp_tools.py tools  <url>
  mcp_tools.py ingest <url> <store-tool> <chunks.jsonl>            [--limit N]
  mcp_tools.py find   <url> <find-tool>  <questions.jsonl> <out.jsonl> [--k 5]

<url> is the server's streamable-HTTP endpoint, e.g.
  http://qdrant-official-minilm-l6.kagent:3000/mcp
Requires: pip install mcp
"""
import asyncio, json, sys, time
from mcp import ClientSession
try:  # mcp >= 2.x
    from mcp.client.streamable_http import streamable_http_client as _client
except ImportError:  # mcp 1.x
    from mcp.client.streamable_http import streamablehttp_client as _client

def _streams(obj):
    if hasattr(obj, "read_stream"):
        return obj.read_stream, obj.write_stream
    return obj[0], obj[1]

async def with_session(url, fn):
    try:
        cm = _client(url, terminate_on_close=False)
    except TypeError:
        cm = _client(url)
    async with cm as streams:
        r, w = _streams(streams)
        async with ClientSession(r, w) as s:
            await s.initialize()
            return await fn(s)

def text_of(result):
    return "\n".join(getattr(c, "text", "") for c in result.content if getattr(c, "type", "text") == "text")

def is_err(result):
    return bool(getattr(result, "is_error", None) or getattr(result, "isError", False))

async def cmd_tools(url):
    async def go(s):
        t = await s.list_tools()
        for tool in t.tools:
            print(f"{tool.name}: {tool.description}")
            print("   input:", json.dumps((getattr(tool, "input_schema", None) or getattr(tool, "inputSchema", {})).get("properties", {}), ensure_ascii=False)[:400])
    await with_session(url, go)

async def cmd_ingest(url, store_tool, path, limit):
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    if limit: rows = rows[:limit]
    async def go(s):
        ok = 0; t0 = time.time()
        for i, r in enumerate(rows):
            args = {"information": r["text"], "metadata": {k: str(v) for k, v in r["metadata"].items()} | {"chunk_id": r["id"]}}
            res = await s.call_tool(store_tool, args)
            if is_err(res):
                print(f"[{i}] ERROR {text_of(res)[:200]}", file=sys.stderr)
            else:
                ok += 1
            if (i + 1) % 25 == 0:
                print(f"  {i+1}/{len(rows)} stored, {time.time()-t0:.0f}s", file=sys.stderr)
        print(json.dumps({"stored": ok, "total": len(rows), "seconds": round(time.time()-t0, 1)}))
    await with_session(url, go)

async def cmd_find(url, find_tool, qpath, out, k):
    qs = [json.loads(l) for l in open(qpath, encoding="utf-8")]
    async def go(s):
        with open(out, "w", encoding="utf-8") as f:
            for q in qs:
                args = {"query": q["q"]}
                # the branch MCP takes limit; the official one uses QDRANT_SEARCH_LIMIT (default 10)
                if find_tool == "vector_find": args["limit"] = k
                t0 = time.time()
                res = await s.call_tool(find_tool, args)
                rec = {"id": q["id"], "lang": q["lang"], "q": q["q"], "expect": q["expect"],
                       "ms": round((time.time()-t0)*1000), "raw": text_of(res)[:20000], "error": is_err(res)}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                print(f"{q['id']} {rec['ms']}ms", file=sys.stderr)
    await with_session(url, go)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "tools": asyncio.run(cmd_tools(a[1]))
    elif a[0] == "ingest":
        limit = int(a[a.index("--limit")+1]) if "--limit" in a else 0
        asyncio.run(cmd_ingest(a[1], a[2], a[3], limit))
    elif a[0] == "find":
        k = int(a[a.index("--k")+1]) if "--k" in a else 5
        asyncio.run(cmd_find(a[1], a[2], a[3], a[4], k))
    else: print(__doc__)
