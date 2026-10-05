# Changelog

All notable changes to this lab are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Lab results (measurements, parity checks, verdicts) go under **Results** in the release they were produced in, with a link to the task that produced them.

## [Unreleased]

### Added
- ADR-0001: embedding model for English project docs and Russian meeting transcripts. Decision: bge-m3. ([docs/adr/0001](docs/adr/0001-embedding-model-for-docs-and-meeting-transcripts.md))
- ADR-0002: deployment topology for the embedding server in the cluster. Decision: native sidecar for the lab's `embed-api`, llm-d for the shared endpoint, standalone Deployment kept only as the measurement baseline. ([docs/adr/0002](docs/adr/0002-embedding-server-deployment-topology.md))
- TASK-0001: run bge-m3 locally on macOS / Linux with llama.cpp (recommended) or Ollama; defines the parameter contract every runtime follows. ([tasks/0001](tasks/0001-run-bge-m3-locally.md))
- TASK-0002: deploy bge-m3 in the cluster as a sidecar and via llm-d on abox branch `feat/llmd-embeddings`, with measurements. ([tasks/0002](tasks/0002-deploy-bge-m3-sidecar-and-llmd-in-abox.md))
- ADR template and index, task index.

### Results
- _none yet. TASK-0001 and TASK-0002 append here when done._
