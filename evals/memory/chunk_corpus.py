#!/usr/bin/env python3
"""Chunk corpus/ledger into memory-ready pieces with rich metadata.

  chunk_corpus.py <corpus-dir> > chunks.jsonl

Three source kinds, three strategies:
  docs/*.md             by heading (## / #), front-matter gives title/updated/owner
  confluence/*.xhtml    macros stripped, status macro kept as text, users -> names,
                        split by <h1>/<h2>
  meetings/*.txt        windows of 4 speaker turns with 1-turn overlap; speaker set
                        and time range in metadata
Every chunk starts with a header line so a hit is traceable without payload.
"""
import json, os, re, sys, hashlib, html

USERS = {"dasha.volkova": "Dasha Volkova", "oleg.prikhodko": "Oleg Prikhodko",
         "irina.belova": "Irina Belova", "tim.horvat": "Tim Horvat", "marat.yusupov": "Marat Yusupov"}

def rec(text, meta):
    cid = hashlib.sha1((meta["file"] + "|" + text).encode()).hexdigest()[:12]
    return json.dumps({"id": cid, "text": text, "metadata": meta}, ensure_ascii=False)

def front_matter(s):
    m = re.match(r"---\n(.*?)\n---\n(.*)", s, re.S)
    if not m: return {}, s
    fm = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)
    return {k.strip(): v.strip() for k, v in fm.items()}, m.group(2)

def md_sections(body):
    cur, out, title = [], [], ""
    for line in body.splitlines():
        if line.startswith("#"):
            if cur: out.append((title, "\n".join(cur).strip()))
            title, cur = line.lstrip("#").strip(), []
        else:
            cur.append(line)
    if cur: out.append((title, "\n".join(cur).strip()))
    return [(t, b) for t, b in out if b]

def adr_meta(body):
    """ADRs have no front matter; read title/status/date/author from the generated header."""
    t = re.search(r"^# (.*)$", body, re.M); st = re.search(r"\*\*Status:\*\* (.*)", body)
    d = re.search(r"\*\*Date:\*\* (\S+)", body); a = re.search(r"\*\*Author:\*\* (.*)", body)
    return {"title": t.group(1) if t else "", "status": st.group(1) if st else "", "updated": d.group(1) if d else "", "owner": a.group(1) if a else ""}

def do_docs(root):
    for sub in ("docs", "adr"):
        if not os.path.isdir(os.path.join(root, sub)): continue
        for fn in sorted(os.listdir(os.path.join(root, sub))):
            if not fn.endswith(".md") or fn.startswith("."): continue
            raw = open(os.path.join(root, sub, fn), encoding="utf-8").read()
            if sub == "docs":
                fm, body = front_matter(raw)
            else:
                fm, body = adr_meta(raw), raw
            for section, text in md_sections(body):
                header = f"# {sub}/{fn} | {fm.get('title','')} | {section} | updated {fm.get('updated','')}" + (f" | status {fm['status']}" if fm.get("status") else "")
                print(rec(header + "\n" + text, {"file": f"{sub}/{fn}", "source": "docs-md" if sub == "docs" else "adr", "lang": "en",
                      "date": fm.get("updated", ""), "doc_title": fm.get("title", ""), "section": section,
                      "author": fm.get("owner", ""), "status": fm.get("status", "")}))

def strip_confluence(x):
    x = re.sub(r"<!--.*?-->", "", x, flags=re.S)
    x = re.sub(r'<ac:structured-macro ac:name="status".*?<ac:parameter ac:name="title">(.*?)</ac:parameter>.*?</ac:structured-macro>', r"[\1]", x, flags=re.S)
    x = re.sub(r'<ac:structured-macro ac:name="(toc|jira|drawio)".*?(/>|</ac:structured-macro>)', "", x, flags=re.S)
    x = re.sub(r'<ac:structured-macro ac:name="(info|warning|note)".*?<ac:rich-text-body>(.*?)</ac:rich-text-body></ac:structured-macro>', r"\2", x, flags=re.S)
    x = re.sub(r'<ac:link><ri:user ri:account-id="([^"]+)" /></ac:link>', lambda m: USERS.get(m.group(1), m.group(1)), x)
    x = re.sub(r'<ac:link><ri:page ri:content-title="([^"]+)" /></ac:link>', r"\1", x)
    x = re.sub(r"</(tr|li|p|h[1-6])>", "\n", x)
    x = re.sub(r"</t[dh]>", " | ", x)
    x = re.sub(r"<[^>]+>", "", x)
    x = html.unescape(x)
    return "\n".join(l.strip(" |") for l in x.splitlines() if l.strip(" |"))

def do_confluence(root):
    for fn in sorted(os.listdir(os.path.join(root, "confluence"))):
        if not fn.endswith(".xhtml") or fn.startswith("."): continue
        raw = open(os.path.join(root, "confluence", fn), encoding="utf-8").read()
        m = re.search(r"title: (.*?), version: (\d+), last updated: (\S+) by (.*?) -->", raw)
        title, updated, author = (m.group(1), m.group(3), m.group(4)) if m else (fn, "", "")
        text = strip_confluence(raw)
        # split on heading lines (they were h1/h2; after stripping we detect by original positions)
        heads = [h for h in re.findall(r"<h[12]>(.*?)</h[12]>", raw)]
        parts, cur, sec = [], [], title
        for line in text.splitlines():
            if line in heads:
                if cur: parts.append((sec, "\n".join(cur)))
                sec, cur = line, []
            else:
                cur.append(line)
        if cur: parts.append((sec, "\n".join(cur)))
        for section, body in parts:
            header = f"# confluence/{fn} | {title} | {section} | updated {updated}"
            print(rec(header + "\n" + body, {"file": f"confluence/{fn}", "source": "docs-confluence", "lang": "en",
                  "date": updated, "doc_title": title, "section": section, "author": author}))

def do_meetings(root, window=4, overlap=1):
    for fn in sorted(os.listdir(os.path.join(root, "meetings"))):
        if not fn.endswith(".txt") or fn.startswith("."): continue
        lines = open(os.path.join(root, "meetings", fn), encoding="utf-8").read().splitlines()
        head = lines[0]
        date = re.search(r"(\d{4}-\d{2}-\d{2})", fn).group(1)
        mtitle = head.lstrip("# ").split(",")[0]
        turns = [re.match(r"\[(\d\d:\d\d:\d\d)\] (\S+): (.*)", l) for l in lines[1:]]
        turns = [(m.group(1), m.group(2), m.group(3)) for m in turns if m]
        i = 0
        while i < len(turns):
            w = turns[i:i + window]
            text = "\n".join(f"[{t}] {s}: {x}" for t, s, x in w)
            header = f"# meetings/{fn} | {mtitle} {date} | {w[0][0]}–{w[-1][0]}"
            print(rec(header + "\n" + text, {"file": f"meetings/{fn}", "source": "meeting", "lang": "ru",
                  "date": date, "doc_title": f"{mtitle} {date}", "section": f"{w[0][0]}-{w[-1][0]}",
                  "speakers": sorted({s for _, s, _ in w})}))
            if i + window >= len(turns): break
            i += window - overlap

if __name__ == "__main__":
    root = sys.argv[1]
    do_docs(root); do_confluence(root); do_meetings(root)
