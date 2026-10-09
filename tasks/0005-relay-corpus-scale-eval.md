# TASK-0005: Does the graph layer earn its place at scale? The Relay corpus

**Status:** In progress
**Source:** lab 6; follow-up to TASK-0004, whose 22 questions over 16 sources were too small to separate the memory modes (vector 93%, graph 77%, both 91%)
**Target:** harness-engineering for corpus, generators and results; abox branch `feat/llmd-embeddings-lab6` (from `lab5`) for cluster manifests; Codespace `abox-lab`
**Deliverable:** `corpus/relay/` generated from a single source of truth, 67 questions dominated by multi-hop and aggregate classes, the same three agents and scale as lab 5 run on scripted memory, results in ADR-0003 (second Validation) and the Changelog

---

## What changed from lab 5

| | Ledger (lab 5) | Relay (lab 6) |
|---|---|---|
| Sources | 16 | 70 (34 meetings, 22 docs, 4 Confluence, 10 ADRs) |
| Chunks | 70 | 244 |
| People | 5, static | 11, one leaves, two join |
| Decisions | 11 (3 superseded) | 30 (7 superseded, 1 rejected) |
| Open items | 1 | 8 (3 still open) |
| Chains | timeout ×3 | timeout ×3, retries ×3, IaC ×2, compute ×2; ADR chains incl. a section-level supersession and a never-accepted ADR |
| Questions | 22, mostly single-hop | 67: 45 templated from the timeline (current, history, chain, owner now/at date, objector, aggregate, unowned at date, stale docs at date, PoC basis, ADR status, dependency) + 22 hand-written (fact, contradiction, crosslingual, multi-hop, point-in-time) |
| Ground truth | hand-written | generated: `source/timeline.yaml` → graph, decisions, questions; prose written on top |

Fixed on purpose: bge-m3, the memory-eval agents with the v2 prompt structure (keys and recipes adapted to the Relay schema), the 0/1/2 scale.

## Hypothesis

Vector-only falls on chain, aggregate, owner-at-date, unowned-at-date and stale-docs-at-date questions, because five to ten chunks cannot cover a chain and cannot count. Graph-only falls on fact and crosslingual. Both should be the best overall by a margin that was invisible in lab 5. If both is not clearly ahead of vector here, ADR-0003's second layer is not earning its cost.

## Steps

1. [x] `source/timeline.yaml`, `meetings-*.yaml`, `adr_prose.yaml`; generator with validation (dates, attendance, references).
2. [x] 22 docs and 4 Confluence pages written against the timeline's dates and stale facts.
3. [x] `gen_questions.py`: 45 templated + 22 manual; every source path checked.
4. [x] Chunker extended to ADRs; 244 chunks. 51 claims (30 decisions, 8 open items, 13 ownership spans).
5. [ ] Cluster: lab6 branch, `relay-bge-m3` collection, agents with Relay keys and recipes; scripted ingest; 67 × 3 runs.
6. [ ] Score by class with the same judge; graph_diff not needed (scripted only).
7. [ ] Optional: agentic ingest with a validation step (ADR-0003 amendment 8) and compare against lab 5's 50%.
8. [ ] ADR-0003 Validation 2, Changelog, this report.

## Report
(pending)
