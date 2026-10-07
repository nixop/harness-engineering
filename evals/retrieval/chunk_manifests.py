#!/usr/bin/env python3
"""Deterministic chunker for TASK-0003.

Splits every YAML document under releases/ into small, self-describing chunks
so the same list can be stored through three different embedders. Chunks are
sized for the smallest input window in the comparison (multilingual MiniLM,
128 tokens): at most MAX_CHARS characters each, split on line boundaries with
a one-line overlap. Every chunk starts with a header naming the file and the
object so a hit is traceable without the metadata.

Usage: chunk_manifests.py <releases-dir> > chunks.jsonl
"""
import json, os, re, sys, hashlib

MAX_CHARS = 350
KIND_RE = re.compile(r"^kind:\s*(\S+)", re.M)
NAME_RE = re.compile(r"^metadata:\n(?:[ \t]+.*\n)*?[ \t]+name:\s*(\S+)", re.M)
NS_RE = re.compile(r"^metadata:\n(?:[ \t]+.*\n)*?[ \t]+namespace:\s*(\S+)", re.M)

def split_documents(text):
    docs, cur = [], []
    for line in text.splitlines():
        if line.strip() == "---":
            if any(l.strip() for l in cur):
                docs.append("\n".join(cur))
            cur = []
        else:
            cur.append(line)
    if any(l.strip() for l in cur):
        docs.append("\n".join(cur))
    return docs

def pieces(lines, header, max_chars):
    """Greedy line packing with one-line overlap; header counts toward the cap."""
    out, buf = [], []
    def size(b): return len(header) + 1 + sum(len(l) + 1 for l in b)
    for line in lines:
        if buf and size(buf + [line]) > max_chars:
            out.append(buf)
            buf = [buf[-1], line] if len(buf[-1]) + len(line) + len(header) + 3 <= max_chars else [line]
        else:
            buf.append(line)
    if buf:
        out.append(buf)
    return out

def main(root):
    n = 0
    for dirpath, _, files in sorted(os.walk(root)):
        for fn in sorted(files):
            if not fn.endswith((".yaml", ".yml")) or fn == "kustomization.yaml":
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root)
            for di, doc in enumerate(split_documents(open(path, encoding="utf-8").read())):
                kind = (KIND_RE.search(doc) or [None, "?"])[1]
                name = (NAME_RE.search(doc) or [None, "?"])[1]
                ns = (NS_RE.search(doc) or [None, "cluster"])[1]
                header = f"# {rel} | {kind} {ns}/{name}"
                lines = [l.rstrip() for l in doc.splitlines() if l.strip()]
                for pi, piece in enumerate(pieces(lines, header, MAX_CHARS)):
                    text = header + "\n" + "\n".join(piece)
                    cid = hashlib.sha1(f"{rel}|{di}|{pi}|{text}".encode()).hexdigest()[:12]
                    rec = {"id": cid, "text": text,
                           "metadata": {"file": rel, "kind": kind, "name": name, "namespace": ns,
                                        "doc": di, "piece": pi}}
                    print(json.dumps(rec, ensure_ascii=False))
                    n += 1
    print(f"{n} chunks", file=sys.stderr)

if __name__ == "__main__":
    main(sys.argv[1])
