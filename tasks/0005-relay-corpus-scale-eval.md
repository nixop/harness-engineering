# TASK-0005: Does the graph layer earn its place at scale? The Relay corpus

**Status:** Done (step 7 optional, not run); prompt iterated to v5
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
5. [x] Cluster: lab6 branch, `relay-bge-m3` collection, agents with Relay keys and recipes; scripted ingest; 67 × 3 runs, then graph and both re-run with prompt v3 and v4, and all three with v5 on the corrected ground truth.
6. [x] Score by class with the same judge; graph_diff not needed (scripted only).
7. [ ] Optional: agentic ingest with a validation step (ADR-0003 amendment 8) and compare against lab 5's 50%.
8. [x] ADR-0003 Validation 2, Changelog, this report.

## Report

**Run (2026-10-10, abox `feat/llmd-embeddings-lab6`, Codespace `abox-lab`).** 244 chunks + 51 claims ingested into `relay-bge-m3` through `qdrant-mcp` (295 points); reference graph loaded through `neo4j-mcp` (`memory/reference-graph.cypher`, 138 nodes). 67 questions × 3 agents, scored 0/1/2 by the lab owner. The vector agent kept its lab-5 prompt; the graph and both agents went through four prompt versions, and the last version was run with all three agents on a corrected ground truth. Files: `evals/memory/runs/2026-10-10/relay-scripted/` (prompt v2), `relay-scripted-v3/`, `relay-scripted-v4/`, `relay-scripted-v5/` (final; traces, `answer-scores.json`, `judge-sheet.md`, `scoring-notes.md`).

| prompt | vector only | graph only | both | wrong (0) v/g/b |
|---|---|---|---|---|
| v2, lab-5 prompts with Relay keys and recipes | 84% | 84% | 85% | 4 / 3 / 3 |
| v3, full Cypher recipe per question class, string dates, routing rule, empty graph result ≠ absence | 84% | 87% | 88% | 4 / 3 / 3 |
| v4, prefixed keys, full file paths, no clarifying questions, two vector calls for rationale | 84% | 89% | 93% | 4 / 1 / 1 |
| v5, open-item ids, raise counts, two-step ADR-status and stale-fact rules, rationale from ADR Context; ground truth fixed, all three re-run | 82% | 90% | **95%** | 4 / 2 / **0** |

Per class with v5 (vector / graph / both): aggregate 56 / 100 / 94, unowned at date 50 / 100 / 100, stale docs 25 / 100 / 100, dependency 25 / 50 / 75; fact 88 / 62 / 88, crosslingual 100 / 75 / 100, multi-hop 62 / 38 / 75; everything else 100 for both. Full table in ADR-0003 Validation 2.

**Answer to the title question.** Yes. On the classes the graph was built for (aggregate, unowned, stale documents, dependencies: 15 of 67 questions) vector-only scores 25–56% and the graph 100%; the combined agent ends thirteen points above vector with no wrong answer in 67 against four. The first run (v2) showed almost no margin, and every point gained since came from the prompt, not the schema: an empty Cypher result was read as "not in memory", `date()` was called on string dates, a missing OWNS edge counted as an owner, keys lost their prefix, documents were looked up by short name, the agent asked the user a question instead of answering, "the dry run" was not mapped to its open item. Each is one sentence in the prompt now (ADR-0003 amendments a–c).

**Lab 5 result confirmed at scale.** Vector-only holds 82% because the claims carry ownership spans, status and supersession as text; the graph adds only where many claims must be combined or compared by date. What the vector layer cannot do at all: count (t27–t30), filter by date (t33–t35), list what is stale (t36–t37), follow DEPENDS_ON (t45), or notice that a document is stale when nothing says so (m06).

**What the graph cannot do** stays the same across versions: retry delays, runbook steps, PoC-report numbers and the reasoning behind a decision are document and meeting text (graph-only fact 62%, multi-hop 38%). Both at 95% is the graph plus exactly those.

**Known traps added this run.** (1) A `kubectl port-forward` is bound to a pod; after a Deployment rollout it may still point at the old pod, which is how the first vector run ingested into `ledger-bge-m3` while the agents queried `relay-bge-m3` and answered "not in memory" 67 times. Check the collection count before running. (2) The neo4j-mcp Cypher load is asynchronous from the runner's point of view; the graph agent answered its first eight questions against a half-loaded graph. Wait for the node count. (3) `grep "exist"` on traces matches claim text ("until idempotency keys exist"), not errors; count tool errors by the `error` field. (4) An agent that ends in A2A state `input-required` has asked the user a question; the runner records an empty answer. The prompt must forbid it. (5) **Flux reverts the lab.** The `releases` Kustomization in abox points at the upstream OCI artifact (`ghcr.io/den-vasyliev/abox/releases-llmd-embeddings`), not at the branch. On its next reconcile it re-applied upstream manifests: the kagent HelmRelease was upgraded with `apiKey: "OPENAI_API_KEY"` (the Secret became that literal) and model `gpt-4.1-mini` (403 for the lab key), `qdrant-mcp` went back to collection `abox-nomic`, and the embedding server to nomic-embed (768 dims), so every agent answered `STREAM_ERROR` and then `vector_find` failed with "expected dim 1024". Fix: `kubectl -n flux-system patch kustomization releases -p '{"spec":{"suspend":true}}'`, then `kubectl apply -f releases/kagent.yaml releases/mcp-servers.yaml releases/llama-cpp-embeddings.yaml` from the branch checkout, recreate `kagent-openai` from the Codespace secret (`/workspaces/.codespaces/shared/user-secrets-envs.json`), restart the agent Deployments and the port-forwards. The suspend must be part of the bootstrap. (6) `qdrant-mcp vector_store` assigns a new point id on every call: re-ingesting a file duplicates its points. Delete by payload filter (`source = claim`) before re-upserting.

**Ground-truth defects fixed before v5.** `timeline.yaml` gave PoC-3 to Ivan from 2026-06-22 although Ivan joins on 07-06 and D16 (07-13) moves the PoC from Sergey to Ivan: the generator now takes `handover: {to, since}` on a PoC and emits two OWNS spans. O7 is raised again on 2026-09-28 and 2026-10-05 (the 10-05 meeting mentions it). The claims for the vector layer were built by an inline script; it is now `evals/memory/gen/gen_claims.py`. One recipe defect of mine remains documented: the v5 "longest-standing closed item" recipe ranked by raise date and picked O8; v5.1 ranks by days open and was not re-run.

**Not done.** Step 7 (agentic ingest with validation on Relay) was not run; it is the next experiment if the write path is revisited. Voice agent and avatar remain under TASK-0004 E–F.
