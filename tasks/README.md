# Tasks

Self-contained briefs for an AI agent (or a human) to execute. Each task names its inputs, the repo it touches, the acceptance criteria and the known traps. A task is done when every acceptance criterion is checked, the report section is filled in, and its results are recorded in [CHANGELOG.md](../CHANGELOG.md).

| ID | Title | Source | Status |
|---|---|---|---|
| [TASK-0001](0001-run-bge-m3-locally.md) | Run bge-m3 locally on macOS / Linux (llama.cpp recommended, Ollama fallback) | ADR-0001 | Open |
| [TASK-0002](0002-deploy-bge-m3-sidecar-and-llmd-in-abox.md) | Deploy bge-m3 in the cluster as a sidecar and via llm-d (abox, branch `feat/llmd-embeddings`) | ADR-0002 | Open |
