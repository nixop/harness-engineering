# TASK-0002: Deploy bge-m3 in the cluster as a sidecar and via llm-d (abox, branch `feat/llmd-embeddings`)

**Status:** Open
**Source:** [ADR-0002](../docs/adr/0002-embedding-server-deployment-topology.md)
**Target repo:** `abox` (`git@github.com:nixop/abox.git`), checked out next to this repo at `../abox`, **branch `feat/llmd-embeddings`**
**Deliverable:** one PR to that branch that (a) adds the `embed-api` pod with a native llama.cpp sidecar, (b) switches the branch's llm-d modelservice and standalone Deployment from nomic to bge-m3, (c) records measurements; plus a results entry in this repo's [CHANGELOG.md](../CHANGELOG.md)

---

## Goal

Make ADR-0002 real on the branch the next lab runs on. When done, the cluster serves bge-m3 in two shapes with identical vectors: a sidecar inside `embed-api`, and the llm-d pool behind the `/llmd` gateway route. The standalone Deployment serves the same model for the duration of the task as the measurement baseline, and the numbers go to the Changelog.

## Read first

1. ADR-0002, all of it. ADR-0001 for why the model is bge-m3.
2. [TASK-0001](0001-run-bge-m3-locally.md), section **Parameter contract**. Every pod spec in this task uses those flags. Do not re-derive them.
3. `../abox/CODEBASE.md`, `CONTRIBUTING.md`, `REVIEW.md` on the branch (they differ from `main`).
4. On the branch, the files you will change or copy from:
   - `releases/llmd.yaml`: the llm-d modelservice HelmRelease, Service, InferencePool + EPP, InferenceObjective, HTTPRoute. The comments are the institutional memory; read them before touching anything.
   - `releases/llama-cpp-embeddings.yaml`: the standalone Deployment. Its probes, resources and comments are the template for the sidecar container.
   - `releases/mcp-servers.yaml`: `qdrant-mcp`, the current consumer, with `EMBEDDINGS_BASE_URL`.
   - `images/nomic-embed/Dockerfile` and `.github/workflows/nomic-embed-image.yaml`: how the model is baked into the llama.cpp server image and published.
   - `README.md`, section "Embeddings: two backends", which this task rewrites.

## Constraints

- Parameter contract from TASK-0001, verbatim, in every container that runs the model. The only per-shape difference is `--parallel`.
- Every image reference pinned by tag **and** digest. No `latest`.
- Namespace in the same file as the workload; ReferenceGrant wherever an HTTPRoute attaches to `agentgateway-external` (CODEBASE.md convention).
- No new application code. `embed-api`'s app container is a stock Caddy image with a config in a ConfigMap.
- The branch is shared. Do not rebase or force-push it; branch off it (`feat/bge-m3-topologies`), open the PR against `feat/llmd-embeddings`.
- Vector dimension changes from 768 to 1024. Every Qdrant collection on the branch becomes invalid; see step 12.

## Steps

### 1. Baked image

1. Create `images/bge-m3-embed/Dockerfile` from `images/nomic-embed/Dockerfile`: `HF_REPO=gpustack/bge-m3-GGUF`, `HF_FILE=bge-m3-FP16.gguf`, **add a `sha256sum -c` against the hash in TASK-0001** after the download. Pin `LLAMA_IMAGE` to the same build line as the laptop install from TASK-0001's report if one exists; otherwise the current `ghcr.io/ggml-org/llama.cpp:server-b<build>`. Set `CMD` to the full parameter contract with `--parallel 1`, so the image alone is correct and pod specs override only what they must.
2. Create `.github/workflows/bge-m3-embed-image.yaml` from the nomic one. Image `ghcr.io/<owner>/abox/bge-m3-embed`, tag `f16-b<build>`, platforms `linux/amd64,linux/arm64`.
3. Run it from your branch with `gh workflow run`, wait, **make the GHCR package public** (new packages are private; the kind nodes have no pull secret), record tag and digest.

### 2. Sidecar: `embed-api`

4. Create `releases/embed-api.yaml`: Namespace `embed-api`; ConfigMap with a Caddyfile that listens on `:8080` and `reverse_proxy 127.0.0.1:8090`; Deployment with:
   - `initContainers[0]`: name `embedder`, the baked image, `restartPolicy: Always` (this is what makes it a native sidecar), `args` from the parameter contract with `--parallel 2 --ctx-size 16384` (two slots of 8192; Caddy is the only caller, two concurrent requests is plenty), `startupProbe`/`readinessProbe` on `:8090/health`, resources from step 9.
   - `containers[0]`: `caddy:<version>@sha256:...`, port 8080, readiness on `:8080/health` proxied through.
   - Service `embed-api:8080`, ReferenceGrant, HTTPRoute `PathPrefix /embed-api` with `URLRewrite` to `/`. External URL `http://<gw-ip>/embed-api/v1/embeddings`.
   Comment every non-default value, in the style of the branch's manifests.
5. Add it to `releases/kustomization.yaml` alphabetically.

### 3. llm-d: switch the pool to bge-m3

6. In `releases/llmd.yaml`, change the modelservice values: the image volume to the new baked image (it mounts the GGUF from the image, see the comment block there), `args` to the parameter contract with the branch's current `--parallel`, `--ctx-size` scaled accordingly (`--parallel 8` needs `--ctx-size 65536`; if that does not fit the node, lower `--parallel`, never the per-slot size). Rename the `InferenceObjective` to `bge-m3`. Keep the `/v1/embeddings` → decode-Service bypass exactly as it is, and keep the comment explaining why.
7. Update `releases/mcp-servers.yaml`: `qdrant-mcp`'s `EMBEDDINGS_BASE_URL` to the llm-d Service (`http://llm-d-embedding.llm-d:8000`), and read `mcp/qdrant-mcp/README.md` "Switching the embeddings backend" for anything else the switch needs (model name, dimension).

### 4. Standalone baseline

8. In `releases/llama-cpp-embeddings.yaml`, swap the image for the baked bge-m3 one and the args for the parameter contract with the same `--parallel` as the llm-d decode pod, so the two are comparable. Leave everything else.

### 5. Size by measurement

9. Deploy with generous limits (4Gi per model container), then for **each of the three shapes** record:
   - idle RSS after readiness;
   - peak RSS and wall time for one ~8000-token input;
   - p50 / p95 latency for 50 requests of ~500 tokens at concurrency 1 and at concurrency equal to `--parallel`, measured from inside the cluster (a `curl` loop in a throwaway pod) and, for llm-d and `embed-api`, through the gateway.
   Use the same input file for all runs; commit it under `evals/embeddings/cluster-bench/inputs/` in **this** repo.
   If an 8000-token input pushes a container past 3Gi, add `--flash-attn on` to the baked image's `CMD` (so all shapes get it) and re-measure.
10. Set `requests` to idle + ~20 % and `limits` to peak + ~25 %, per shape. Write the numbers into each manifest's comment.
11. If the three shapes together do not fit a 2-core / 8 GB Codespace next to the rest of the stack, scale `embed-api` to zero replicas in a documented Codespaces note, as ADR-0002 says. Do not shrink slots.

### 6. Data

12. Delete and recreate the Qdrant collections `qdrant-mcp` uses with 1024-dim cosine vectors, and re-run the branch's ingest path (the `retrieval-agent` or whatever the README on the branch says). Confirm a Russian query returns something sensible from English content.

### 7. Verify

13. `flux get all -A` fully `Ready`; no pod restarts after five minutes.
14. For each of `http://<gw-ip>/embed-api/v1/embeddings`, `http://<gw-ip>/llmd/v1/embeddings` and the standalone in-cluster Service, run the verification block from TASK-0001: dim 1024, norm 1.0, RU↔EN cosine above 0.8, over-length rejected.
15. **Parity:** embed the same 20 strings on all three cluster shapes and on the laptop from TASK-0001's smoke record; pairwise cosine ≥ 0.999. Different llama.cpp builds between laptop and cluster are the usual cause when this fails; record both build numbers either way.
16. Save raw outputs under `evals/embeddings/cluster-bench/<date>/` in this repo.

### 8. Docs, PR, Changelog

17. Rewrite the README section "Embeddings: two backends" into the three shapes with their URLs, the parameter contract reference, and the measured numbers. Update `CODEBASE.md` component roles and tech stack (model row changes from nomic to bge-m3).
18. Open the PR against `feat/llmd-embeddings`. Title `feat: serve bge-m3 as embed-api sidecar and via llm-d`. Body: link ADR-0001 and ADR-0002, the measurement table, the dimension-change warning, and the Codespaces note if step 11 applied.
19. Run the branch's `REVIEW.md` prompt against your own diff first and fix what it flags.
20. In **this** repo, add an entry under `## [Unreleased] → ### Results` in `CHANGELOG.md`: date, PR link, the measurement table (idle RSS, peak RSS, p50/p95 at both concurrencies, per shape), the parity result, and whether any ADR-0002 revisit trigger fired.

## Acceptance criteria

- [ ] `embed-api` pod runs Caddy + native llama.cpp sidecar; `/embed-api/v1/embeddings` via the gateway returns correct vectors.
- [ ] llm-d pool serves bge-m3; `/llmd/v1/embeddings` returns correct vectors; `qdrant-mcp` is re-pointed and re-ingested at 1024 dims.
- [ ] Standalone Deployment serves bge-m3 with the same image and args, and the three-way measurement table exists.
- [ ] Parity across the three shapes and the laptop: cosine ≥ 0.999 on 20 fixed strings.
- [ ] Every image pinned by tag and digest; GGUF sha256 checked at build.
- [ ] Resources backed by written-down measurements.
- [ ] README and CODEBASE.md updated; PR against the branch, conventional commit title.
- [ ] CHANGELOG.md in harness-engineering has the results entry.
- [ ] Report below filled in.

## Out of scope

- Removing the standalone Deployment. ADR-0002 says it goes after the numbers are in; that is a follow-up PR once the ADR owner has read them.
- Anything on abox `main`. The RSIP filter there is pinned to `0.6.5` and will not reconcile new tags; that trap does not exist on the branch, which has an open filter and its own `releases-llmd-embeddings` artifact.
- Autoscaling, GPU images, a generation model in the pool.

## Known traps, from the branch's own history

- `flux-push.yaml` names the artifact after the branch. Cutting the tag on `feat/bge-m3-topologies` publishes to `releases-feat-bge-m3-topologies`; the bootstrap reads `var.releases_artifact`, which the branch sets to `releases-llmd-embeddings`. Either pass `-var releases_artifact=...` for your branch or cut the tag after merge. Decide and write it in the PR.
- `--ubatch-size` below the slot size fails long inputs with a batch error that looks like a truncation bug.
- The modelservice chart renders a Deployment but no Service; the branch spells the Service out by hand. Keep the selector in sync if you touch labels.
- InferencePool chart v1.5.0 is the newest published even though newer GIE releases exist; its `inferenceObjectives` template is broken, so the objective is a hand-written resource.
- The EPP needs CPU the 2-core Codespace cannot always give it; the pool pod sits `Pending`. The branch's `llmd.yaml` comments say what to lower.
- New GHCR packages are private by default.
- Nested-Docker egress on Codespaces: `make fix-egress` before `make run`. The branch also has `make fix-docker-acl` for non-root images.
- Native sidecar needs `restartPolicy: Always` on the init container; without it the embedder runs once and the pod never becomes ready.

## Report

- **PR:**
- **Image:** `ghcr.io/<owner>/abox/bge-m3-embed:f16-b<build>@sha256:...`
- **llama.cpp build (cluster / laptop):**
- **Measurements:** (paste the table also written to CHANGELOG.md)
- **Parity (3 shapes + laptop):**
- **Flash attention needed:** yes / no
- **Codespaces note applied (step 11):** yes / no
- **ADR-0002 revisit trigger fired:** none / which
- **Deviations from the parameter contract:** none / list
