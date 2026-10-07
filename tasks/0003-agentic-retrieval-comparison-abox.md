# TASK-0003: Agentic retrieval comparison on abox: bge-m3 vs MiniLM via official qdrant MCP

**Status:** Done, pending PR to `feat/llmd-embeddings`
**Source:** lab assignment (deploy from `feat/llmd-embeddings`, add the official qdrant MCP, compare retrieval quality); validates [ADR-0001](../docs/adr/0001-embedding-model-for-docs-and-meeting-transcripts.md)
**Target:** GitHub Codespace `abox-lab` (4 CPU / 16 GB) on `nixop/abox`, branch `feat/llmd-embeddings`; changes land as a PR to that branch
**Deliverable:** three Qdrant collections built from the same chunks with three embedders, an agentic retrieval eval over them, results in ADR-0001 (Validation section) and in [CHANGELOG.md](../CHANGELOG.md)

---

## What is compared

| Label | Embedder | Served by | MCP tools | Dims | Max input |
|---|---|---|---|---|---|
| english-only | `sentence-transformers/all-MiniLM-L6-v2` | FastEmbed inside the official `mcp-server-qdrant` | `qdrant-store`, `qdrant-find` | 384 | 256 tokens |
| multilingual | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | FastEmbed inside a second official `mcp-server-qdrant` | `qdrant-store`, `qdrant-find` | 384 | 128 tokens |
| chosen | `BAAI/bge-m3` F16 | llama.cpp (`llama-cpp-embeddings` on the branch) behind the branch's own `qdrant-mcp` | `vector_store`, `vector_find` | 1024 | 8192 tokens |

bge-m3 is not in FastEmbed's model list, so it cannot run inside the official MCP; the branch's MCP is the only path for it. That asymmetry is part of what is being evaluated: the official MCP embeds in-process and was previously OOMKilled on a 2-core Codespace, which is why the branch replaced it.

## Lab steps mapped to work

| Lab step | Work |
|---|---|
| 1. Deploy from `feat/llmd-embeddings` | Codespace on the branch, `make fix-egress`, `make fix-docker-acl`, `make run`, `flux get all -A` Ready |
| 2. Add official qdrant MCP | Two `MCPServer` CRs (`qdrant-official-l6`, `qdrant-official-ml`) in `releases/mcp-servers.yaml`, `uvx mcp-server-qdrant`, memory limit 3Gi, `QDRANT_URL=http://qdrant.qdrant:6333`, own `COLLECTION_NAME` each |
| 3. Model for retrieval-agent and k8s-agent | Fix `kagent.yaml`: `apiKey: ""` so the chart expects an existing Secret; create `kagent-openai` Secret from `$OPENAI_API_KEY` (Codespaces secret) after bootstrap; model `gpt-4.1-mini` (chart default) |
| 4. Add official MCP tools | New Agent `retrieval-agent-official` with `qdrant-store` / `qdrant-find` from both official servers; original `retrieval-agent` keeps `vector_store` / `vector_find` |
| 5. System prompt for official MCP | Prompt of the new agent rewritten around the official tool names and the explicit `collection_name` argument; `TOOL_STORE_DESCRIPTION` / `TOOL_FIND_DESCRIPTION` env on the servers aligned with it |
| 6. Index data with all-MiniLM-L6-v2 | Deterministic ingest script pushes identical chunks of `releases/*.yaml` into `manifests-minilm-l6` and `manifests-minilm-ml` through each official server's store tool |
| 7. Index the same data with the default qdrant MCP | Same script, same chunks, into `manifests-bge-m3` through the branch's `qdrant-mcp` (re-pointed at bge-m3 per TASK-0002) |
| 8. Compare and record | Question set, agentic runs per toolset, scoring, results into ADR-0001 and CHANGELOG |

## Steps

### 1. Environment
1. `gh codespace create -R nixop/abox -b feat/llmd-embeddings -m standardLinux32gb`; `gh codespace ssh` into it.
2. `make fix-egress && make fix-docker-acl && make run`. Wait for `flux get all -A` to be fully Ready. Record what is not Ready and why before touching anything.
3. Confirm `OPENAI_API_KEY` is present in the Codespace env.

### 2. Agents get a model (lab step 3)
4. In `releases/kagent.yaml` set `providers.openAI.apiKey: ""` so the chart stops creating a Secret with a placeholder value. Keep `apiKeySecretRef: kagent-openai`, `apiKeySecretKey: OPENAI_API_KEY`, model `gpt-4.1-mini`.
5. `kubectl -n kagent create secret generic kagent-openai --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY"`. Add the command to the README's Codespaces section; the key never enters git.
6. Verify `k8s-agent` and `retrieval-agent` reach `Ready`, and a trivial question to `k8s-agent` through the kagent UI or API returns an answer.

### 3. Official MCP servers (lab steps 2, 5)
7. Add two `MCPServer` CRs: image `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`, `cmd: uvx`, `args: [mcp-server-qdrant]`, stdio transport (kmcp adapts it). Env per server: `QDRANT_URL`, `COLLECTION_NAME` (`manifests-minilm-l6` / `manifests-minilm-ml`), `EMBEDDING_MODEL`, `FASTMCP_LOG_LEVEL=INFO`, and `TOOL_STORE_DESCRIPTION` / `TOOL_FIND_DESCRIPTION` describing Kubernetes manifests, not generic memories. Resources: request 512Mi, limit 3Gi. First start downloads the ONNX model from Hugging Face; expect a slow first readiness and egress.
8. Confirm both pods are Running with no OOMKill after a store and a find call. Record idle RSS of each.

### 4. bge-m3 path (lab step 7 prerequisite)
9. Apply TASK-0002's bge-m3 change to `releases/llama-cpp-embeddings.yaml` (baked image or the gpustack GGUF, parameter contract from TASK-0001) and point `qdrant-mcp`'s `QDRANT_COLLECTION` at `manifests-bge-m3`. The llm-d switch from TASK-0002 is not needed for this comparison and can stay on nomic.

### 5. Agents and toolsets (lab steps 4, 5)
10. Add `releases/agent-retrieval-official.yaml`: copy of `retrieval-agent` with tools `qdrant-store` / `qdrant-find` from both official servers, Neo4j tools unchanged, and a prompt that: names the two collections and when to use which, passes `collection_name` explicitly on every call, and keeps the "retrieval reads, never re-ingests" rule verbatim.
11. Keep `retrieval-agent` on `vector_store` / `vector_find` against `manifests-bge-m3`.

### 6. Ingest (lab steps 6, 7)
12. Chunker: one chunk per YAML document in `releases/**/*.yaml`, leading comment block kept with the document, with metadata `{file, kind, name, namespace, lang}`. Documents longer than 100 tokens are additionally split at top-level keys so that the 128-token limit of the multilingual MiniLM is not silently truncating. Same chunk list for all three collections; commit it as `evals/retrieval/chunks.jsonl` in this repo.
13. Ingest script (Python, `mcp` client over kmcp's streamable-HTTP Service of each server) stores every chunk through the server's store tool. Three runs, three collections. Record chunk counts per collection with `curl qdrant.qdrant:6333/collections/<name>`.
14. Additionally run the agentic ingest once (`retrieval-agent` asked to ingest the kagent CRs via `k8s-agent`) so the lab's intended path is exercised, into a separate collection suffix `-agentic`. It is not part of the scored comparison.

### 7. Evaluate (lab step 8)
15. Question set `evals/retrieval/questions.jsonl`: 24 questions, 12 Russian and 12 English, each with the expected `{file, kind, name}` and a one-line expected answer. Mix: "what does X configure", "which object does Y", "why is Z pinned", and 4 questions whose answer lives in a comment block only.
16. For each question and each of the three toolsets: ask the agent (`retrieval-agent-official` with the collection named in the question's run config, or `retrieval-agent`), capture the full trace (tool calls, retrieved chunks, final answer).
17. Score: `hit@5` (expected object among retrieved chunks), answer correctness 0/1/2 against the rubric in abox `EVALS.md` style, number of tool calls, wall time. Judge is the session owner reading traces, not a second LLM.
18. Write results: a Validation section in ADR-0001 with the table (three embedders × RU/EN × metrics) and a two-paragraph reading of it; a Results entry in CHANGELOG.md; raw traces under `evals/retrieval/runs/<date>/`.

## Acceptance criteria
- [ ] Cluster from the branch is Ready in the Codespace; agents have a working model.
- [ ] Two official MCP servers run without OOMKill; branch MCP serves bge-m3.
- [ ] Three collections hold the same chunk count from the same chunk list.
- [ ] `retrieval-agent-official` answers through `qdrant-find`; `retrieval-agent` through `vector_find`.
- [ ] 24 questions × 3 toolsets traced and scored.
- [ ] ADR-0001 Validation section and CHANGELOG Results entry written; PR to `feat/llmd-embeddings` opened with manifests, README update, no secrets.

## Known traps
- **Codespace root disk is 32 GB and Docker's data-root is on it.** The branch's scripts assume Codespaces puts `/var/lib/docker` on `/tmp` (the 118 GB volume); on the `standardLinux32gb` machine it is a bind mount from the 32 GB loop device and the stack fills it: both Postgres pods crash with "No space left on device" and the Helm installs time out. Fix before `make run`: `kind delete cluster --name abox`, stop dockerd, write `{"data-root":"/tmp/docker"}` to `/etc/docker/daemon.json`, clear `/var/lib/docker/*`, restart dockerd with the same args `docker-init.sh` used. Worth folding into `scripts/setup.sh`. Found 2026-10-07.
- Official MCP OOMKilled before on 2-core/8GB with a 2Gi limit. Use the 4-core machine and 3Gi.
- First start of each official server downloads the model from Hugging Face; without `make fix-egress` the pod hangs.
- Multilingual MiniLM truncates at 128 tokens, L6 at 256. Chunking must respect the smallest, or the comparison measures truncation, not the model.
- Collection dimensions are fixed; three models need three collections.
- `apiKey: OPENAI_API_KEY` literal in `kagent.yaml` creates a Secret containing the string "OPENAI_API_KEY". Fix before anything else.
- Agentic ingest is non-deterministic; only the scripted ingest is comparable.

## Report (2026-10-07)
- **Codespace:** `abox-lab` (4 CPU / 16 GB), branch `feat/llmd-embeddings`, bootstrapped with `make run` after moving Docker's data-root to `/tmp/docker`.
- **PR:** not opened yet. Manifest changes sit uncommitted in the abox working tree (local and Codespace): `releases/kagent.yaml` (apiKey empty, model gpt-5.4-mini), `releases/mcp-servers.yaml` (+2 official servers, qdrant-mcp on bge-m3 collection with empty prefixes), `releases/llama-cpp-embeddings.yaml` (bge-m3 F16 via init-container download, parameter contract), `releases/agent-retrieval-eval.yaml` (3 agents), `releases/kustomization.yaml`. Applied with `kubectl apply -k` while the Flux `releases` Kustomization is suspended; resume it after the PR's tag is published.
- **Agent model:** gpt-5.4-mini. The chart default gpt-4.1-mini returned 403 model_not_found for the lab's project key.
- **Chunk count per collection:** 270 / 270 / 270 (`manifests-bge-m3` 1024-dim, `manifests-minilm-l6` 384-dim, `manifests-minilm-ml` 384-dim). Ingest time 185 s / 82 s / 122 s.
- **Memory (cgroup peak):** branch `qdrant-mcp` 54 MiB; llama.cpp bge-m3 pod 1384 MiB, 0 restarts; official MCP L6 2022 MiB; official MCP multilingual 2742 MiB after one OOMKill (exit 137) at the 3Gi limit during concurrent find and agent traffic.
- **llama.cpp image:** `ghcr.io/ggml-org/llama.cpp:server-b11429@sha256:2f8ebc2dde83c4bd7e5c6d61efa57965e0d5a79d29802c246c4593740d9c04c1`; GGUF sha256 verified by the init container.
- **Results table:** see ADR-0001, section Validation. Raw: `evals/retrieval/runs/2026-10-07/` (find results, ranked results, agent traces, judge sheet, scores, scoring notes).
- **Deviations:** (1) chunks capped at 350 chars for the multilingual MiniLM's 128-token window, so bge-m3's long context was not exercised; (2) three sibling agents instead of one agent with a swapped toolset, to avoid tool-name collisions between the two official servers; (3) the agentic ingest path (step 14) was not run; only the scripted ingest is in the comparison; (4) `--flash-attn on` added to the cluster llama-server, RU↔EN cosine matched the laptop run to four decimals.
