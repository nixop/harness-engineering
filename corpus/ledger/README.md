# Corpus: "Ledger" billing service

A synthetic corpus for agent memory (lab 5, TASK-0004). Everything here is
invented; no real company, person or transcript is used.

## The project

Ledger is an internal billing service. Over six weeks (2026-08-24 to
2026-10-02) the team moves it behind a new API gateway, replaces the tariff
schema, and argues about retries, timeouts and who owns what. The corpus is
written so that an agent with memory has something to remember *and* something
to get wrong:

| Trap | Where it lives | What a good memory does |
|---|---|---|
| A decision that changes | gateway timeout: 5 s (meeting 2) → 15 s (meeting 4) → 10 s with retry budget (meeting 6) | returns the latest value and can show the history |
| Docs contradict the meetings | `docs/gateway.md` still says 5 s after meeting 4 | names both, says which is newer |
| Ownership moved | retries: Oleg → Dasha (meeting 5) | answers with the current owner and when it changed |
| Open item nobody took | tariff migration dry-run on prod data | says it is unowned instead of inventing an owner |
| Same thing, two names | "retry budget" (EN docs) = "бюджет ретраев" / "повторы" (RU meetings) | matches across languages |
| Numbers in transcripts | latency SLO quoted as "двести миллисекунд" in speech, 200 ms in docs | normalises |
| Noisy ASR | names mangled ("Даша" → "даша", "Олег" → "олег", "gateway" → "гейтвей") | still attributes correctly |

## Layout

```
docs/         English Markdown, as if from the repo (6 pages)
confluence/   English pages exported from Confluence (storage-format XHTML, 3 pages)
meetings/     Russian ASR-style transcripts with speaker turns and timestamps (7 meetings)
memory/       what an agent should have remembered: decisions.jsonl, people.jsonl,
              questions.jsonl (gold answers for evaluation)
```

## People

| Name | Role | Speaks in meetings as |
|---|---|---|
| Dasha Volkova | backend lead | даша |
| Oleg Prikhodko | platform / gateway | олег |
| Marat Yusupov | product owner | марат |
| Irina Belova | SRE | ира |
| Tim Horvat | finance systems (joins from week 3) | тим |

## Conventions

- Dates are ISO in file names and inside documents.
- Meeting transcripts: `[hh:mm:ss] speaker: text`, lowercase speaker names, no
  punctuation discipline, occasional ASR errors on purpose, technical terms in
  English inside Russian sentences.
- Confluence pages are the storage-format XHTML the Confluence REST API returns,
  with macros, so the chunker has to strip them.
- `memory/decisions.jsonl` is the ground truth of what was decided, by whom,
  when, and what it superseded. `memory/questions.jsonl` is the eval set.
