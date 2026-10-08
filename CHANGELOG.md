# Changelog

All notable changes to this lab are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Lab results (measurements, parity checks, verdicts) go under **Results** in the release they were produced in, with a link to the task that produced them.

## [Unreleased]

### Added
- ADR-0001: embedding model for English project docs and Russian meeting transcripts. Decision: bge-m3. ([docs/adr/0001](docs/adr/0001-embedding-model-for-docs-and-meeting-transcripts.md))
- ADR-0002: deployment topology for the embedding server in the cluster. Decision: native sidecar for the lab's `embed-api`, llm-d for the shared endpoint, standalone Deployment kept only as the measurement baseline. ([docs/adr/0002](docs/adr/0002-embedding-server-deployment-topology.md))
- TASK-0001: run bge-m3 locally on macOS / Linux with llama.cpp (recommended) or Ollama; defines the parameter contract every runtime follows. ([tasks/0001](tasks/0001-run-bge-m3-locally.md))
- TASK-0002: deploy bge-m3 in the cluster as a sidecar and via llm-d on abox branch `feat/llmd-embeddings`, with measurements. ([tasks/0002](tasks/0002-deploy-bge-m3-sidecar-and-llmd-in-abox.md))
- TASK-0003: agentic retrieval comparison on abox, bge-m3 vs all-MiniLM-L6-v2 and paraphrase-multilingual-MiniLM-L12-v2 through the official qdrant MCP. ([tasks/0003](tasks/0003-agentic-retrieval-comparison-abox.md))
- TASK-0004: agent-memory corpus `corpus/ledger/` (synthetic billing project: EN docs, Confluence pages, RU meeting transcripts, ground-truth decisions and 22 eval questions), evaluation plan and ADR-0003. ([tasks/0004](tasks/0004-agent-memory-corpus-and-eval.md))
- ADR template and index, task index.

### Results
- 2026-10-09, TASK-0004 parts B–D: Ledger memory corpus ingested two ways (scripted ground truth; agentic via `memory-writer`) into bge-m3 vectors plus a Neo4j graph on abox `feat/llmd-embeddings-lab5`; 22 memory questions × 3 agents (vector / graph / both). Scripted memory: 93% / 77% / 91% after fixing string dates and graph prompts (graph was 57% before). Agentic memory: 50% / 39% / 50%, with decision precision 0.29, 3 key spellings per person, a self-loop SUPERSEDES and one document never ingested. ADR-0003 accepted with two amendments (ISO dates, validation before write). Details in ADR-0003 Validation and `evals/memory/runs/2026-10-09/`.
- 2026-10-07, TASK-0003: bge-m3 vs all-MiniLM-L6-v2 vs paraphrase-multilingual-MiniLM-L12-v2 on abox (`feat/llmd-embeddings`, 4-core Codespace), 270 manifest chunks, 24 RU/EN questions. Raw retrieval hit@1 RU/EN: bge-m3 0.67/0.92, MiniLM-L6 0.58/0.83, multilingual MiniLM 0.58/0.50. Agent answer correctness: 94% / 90% / 90%. Peak memory: llama.cpp+bge-m3 1.4 GiB stable; official MCP with FastEmbed 2.0 GiB (L6) and 2.7 GiB (multilingual, OOMKilled once at 3Gi). ADR-0001 confirmed; details in its Validation section and in `evals/retrieval/runs/2026-10-07/`.
- 2026-10-07, TASK-0001 (partial, reverted): bge-m3 F16 ran locally on an Apple M4 via llama.cpp 0.6.0 (b11429) with the parameter contract; dim 1024, norm 1.0, RU↔EN cosine 0.82–0.94 on 10 pairs, over-length input rejected, ~0.15 s per 500-token request. The install and model were removed afterwards at the owner's request; the same GGUF and flags in the cluster reproduced the RU↔EN cosine to four decimals (0.9393).
- 2026-10-07, environment: on the `standardLinux32gb` Codespace Docker's data-root sits on the 32 GB root volume, not on `/tmp`; the branch stack fills it and both Postgres pods die with "No space left on device". Moving the data-root to `/tmp/docker` fixed it. Recorded in TASK-0003 known traps.
