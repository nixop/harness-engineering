# Tasks

Self-contained briefs for an AI agent (or a human) to execute. Each task names its inputs, the repo it touches, the acceptance criteria and the known traps. A task is done when every acceptance criterion is checked, the report section is filled in, and its results are recorded in [CHANGELOG.md](../CHANGELOG.md).

| ID | Title | Source | Status |
|---|---|---|---|
| [TASK-0001](0001-run-bge-m3-locally.md) | Run bge-m3 locally on macOS / Linux (llama.cpp recommended, Ollama fallback) | ADR-0001 | Open |
| [TASK-0002](0002-deploy-bge-m3-sidecar-and-llmd-in-abox.md) | Deploy bge-m3 in the cluster as a sidecar and via llm-d (abox, branch `feat/llmd-embeddings`) | ADR-0002 | Open |
| [TASK-0003](0003-agentic-retrieval-comparison-abox.md) | Agentic retrieval comparison on abox: bge-m3 vs MiniLM (English-only, multilingual) via official qdrant MCP | lab assignment, ADR-0001 | Done, pending PR |
| [TASK-0004](0004-agent-memory-corpus-and-eval.md) | Agent-memory corpus (Ledger), evaluation in three modes, ADR-0003; optional voice agent and avatar | lab 5 | A–D done, E–F pending |
| [TASK-0005](0005-relay-corpus-scale-eval.md) | Relay corpus: 70 sources generated from a timeline, 67 multi-hop questions, does the graph layer earn its place | lab 6, ADR-0003 | Done (agentic ingest optional, not run) |
