# Corpus: "Relay" webhook delivery service (lab 6)

A synthetic corpus for agent memory, ten times the size of `corpus/ledger`
and built so that multi-hop questions are the norm. Everything is invented.

## Story

One service, January to October 2026, four partly overlapping waves:

1. Infrastructure code from Terraform to CloudFormation (ADR-001), revised in April to a hybrid (ADR-004 supersedes ADR-001).
2. Relay behind the API gateway (ADR-002); timeouts and retries become gateway policy and then change three times.
3. DocumentDB to DynamoDB single-table, chosen on PoC-1 (ADR-003); a dry run nobody owns for three months.
4. EKS vs Lambda: two PoCs (ADR-005), serverless chosen (ADR-006), EKS rejected (ADR-007); Lambda breaks the wave-2 retry and timeout decisions (ADR-009, D20); secrets (ADR-008); a timeout ADR that was never accepted (ADR-010).

11 people in four groups; one leaves (Nikita, 2026-06-01), two join (Sergey 2026-04-06, Ivan 2026-07-06); ownership of retries moves twice, of the serverless PoC once. 30 decisions (7 superseded, 1 rejected), 8 open items (3 still open), 3 PoCs with numbers, 26 documents of which 14 have sections made stale by later decisions, 10 ADRs.

## Source of truth and generation

```
source/timeline.yaml      people, teams, topics, glossary, decisions, open items, PoCs, ADR metadata, document metadata (dates, what goes stale when)
source/meetings-*.yaml    34 meetings with speaker turns (Russian, ASR style)
source/adr_prose.yaml     context / options / consequences per ADR
evals/memory/gen/gen_corpus.py     -> meetings/*.txt, adr/ADR-NNN.md, memory/*.jsonl, memory/reference-graph.cypher
evals/memory/gen/gen_questions.py  -> memory/questions.jsonl (templated + source/questions-manual.jsonl)
```

Hand-written: `docs/*.md` (22) and `confluence/*.xhtml` (4). Their dates and stale facts are declared in `timeline.yaml`; the generator checks the files exist.

Regenerate after any change to `source/`:

```
.venv/bin/python evals/memory/gen/gen_corpus.py corpus/relay
.venv/bin/python evals/memory/gen/gen_questions.py corpus/relay
.venv/bin/python evals/memory/gen/gen_claims.py corpus/relay      # claims for the vector layer
.venv/bin/python evals/memory/chunk_corpus.py corpus/relay          # chunks for the vector layer
```

## Traps built in

| Trap | Example |
|---|---|
| Decision chains | gateway timeout 10 s → 30 s → 25 s; retries off → on at gateway → moved to SQS |
| ADR chains | ADR-001 → ADR-004; ADR-005 → ADR-006; ADR-009 supersedes a section of ADR-002; ADR-010 proposed and never accepted |
| Ownership over time | retries: Nikita → Anna (06-01) → Ivan (09-07); serverless PoC: Sergey → Ivan (07-13) |
| Unowned items | DynamoDB dry run unowned 05-04 to 08-10; 10x load test and DocumentDB credential rotation still unowned |
| Stale documents | gateway.md (3 facts), onboarding, team roster, decision log stops in June, runbook says rollback TBD |
| Decisions grounded in numbers | D10 on PoC-1, D17 on PoC-3; ADR-007 rejected on PoC-2 numbers |
| Dependencies | gateway stack depends on the stack layout; DynamoDB cutover a week before compute cutover |
| Objections | 8 recorded objectors, including the same person on both sides of the IaC story |
| Bilingual terms | клаудформейшн / cfn, дрифт, провижнд конкаренси, дед леттер, сингл тейбл |
