# Architecture Decision Records

This directory holds the ADRs for the harness-engineering lab. One file per decision, never edited after acceptance except to change its status (Deprecated / Superseded by ADR-NNNN).

## Index

| ID | Title | Status | Date |
|---|---|---|---|
| [ADR-0001](0001-embedding-model-for-docs-and-meeting-transcripts.md) | Embedding model for English project docs and Russian meeting transcripts | Proposed | 2026-10-05 |
| [ADR-0002](0002-embedding-server-deployment-topology.md) | Deployment topology for the embedding server in the cluster (standalone / sidecar / llm-d) | Proposed | 2026-10-06 |
| [ADR-0003](0003-agent-memory-structure.md) | Structure of agent memory: claims in a vector layer plus a graph layer with supersession | Accepted | 2026-10-08 |

## Conventions

- **Numbering:** four digits, sequential, zero-padded. Next free number is the last one in the index plus one.
- **File name:** `NNNN-short-kebab-title.md`.
- **Status lifecycle:** `Proposed` → `Accepted` → (`Deprecated` | `Superseded by ADR-NNNN`). Rejected proposals stay in the log with status `Rejected`.
- **Template:** copy [0000-adr-template.md](0000-adr-template.md).
- **Scope:** record decisions that are hard to reverse or that a future reader will ask "why" about. Do not record implementation details that the code already explains.
- **Evidence:** when a decision rests on benchmark numbers or vendor claims, cite the source and the date it was checked. Numbers in this field go stale within months.
- **Results:** outcomes of the tasks an ADR spawns go to [CHANGELOG.md](../../CHANGELOG.md), not into the ADR.
