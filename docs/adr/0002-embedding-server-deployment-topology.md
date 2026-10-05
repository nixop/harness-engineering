# ADR-0002: Deployment topology for the embedding server in the cluster

**Status:** Proposed
**Date:** 2026-10-06
**Deciders:** harness-engineering lab owner

## Context

[ADR-0001](0001-embedding-model-for-docs-and-meeting-transcripts.md) picked bge-m3. On laptops it runs under llama.cpp or Ollama ([TASK-0001](../../tasks/0001-run-bge-m3-locally.md)). This ADR decides how the same model is served **inside a Kubernetes cluster**, where there are three realistic shapes:

1. a **standalone** `llama-server` Deployment with its own Service, shared by every consumer;
2. a **sidecar**: `llama-server` as a second container inside the consumer's pod, reached over localhost;
3. **llm-d**: the model behind a Gateway API `InferencePool` with an endpoint picker (EPP), managed by the llm-d modelservice chart.

Target environment assumptions:

- A standard Kubernetes cluster (1.29 or newer, so native sidecars are available) with a Gateway API gateway that supports the Inference Extension. Clusters without that extension can run shapes 1 and 2 but not 3.
- CPU inference by default. bge-m3 at F16 is 1.16 GB mmap'd plus the attention working set for an 8192-token micro-batch. Every copy of the model costs that, and every shape that runs more than one copy pays it more than once.
- Consumers: a retrieval service that embeds queries on the hot path, and batch ingestion that embeds documents and transcripts. More consumers will appear.
- A vector store (Qdrant) whose collections are tied to the vector dimension; any model change is a re-index regardless of topology.

Constraints that shape the choice:

- **Same vectors everywhere.** Whatever the topology, the engine build, GGUF, pooling, normalisation and context must match the laptop setup defined in TASK-0001's parameter contract, or laptop-built and cluster-built indexes stop being interchangeable.
- **One serving path per model, not per consumer.** Two shared endpoints for the same model means two configs to keep in parity. Private copies (sidecars) are acceptable only where a single consumer owns the copy.
- **Minimal custom code.** The consumer used to demonstrate the sidecar must be nearly zero code, so that the pattern is copyable without dragging an application along.

What this ADR does not decide: autoscaling policy, GPU variants, and whether llm-d is the right home for a future generation model. Those get their own ADRs.

## Decision

Three things, in order of importance:

1. **Sidecar for the retrieval service.** The service that embeds user queries on the hot path gets `llama-server` as a Kubernetes native sidecar (`initContainers` entry with `restartPolicy: Always`): one pod, one embedder, localhost, no Service for the model, no cross-namespace routing. For the lab this consumer is a new minimal stand-in service, `embed-api`, that does nothing but expose the sidecar over HTTP; the real retrieval service later copies its pod spec. The sidecar is a **pattern demonstrated once**, not the default for every consumer.
2. **llm-d for the shared in-cluster endpoint.** Batch ingestion, any consumer that cannot afford a private copy, and external callers through the gateway use a single bge-m3 pool managed by llm-d. It is chosen because it is the one shape that extends to a second replica or a second model without a redesign, and because it is the platform's inference layer going forward: generation models will live behind the same `InferencePool` mechanism, and running embeddings through a different path would mean a second serving stack to operate.
3. **Standalone Deployment only as the measurement baseline.** During the test deployment ([TASK-0002](../../tasks/0002-deploy-bge-m3-sidecar-and-llmd-in-abox.md)) a plain Deployment runs the same image and args next to the llm-d pool so that llm-d's overhead is measured, not assumed. After the numbers are in the Changelog it is removed, unless a revisit trigger below fires.

All three shapes run the **same baked image** (`llama.cpp:server-<build>` with `bge-m3-FP16.gguf` in a layer) and the **same args** from the parameter contract in TASK-0001. Only `--parallel` (and with it `--ctx-size`, which is per-slot times slots) differs per shape.

## Options Considered

### Option A: Standalone Deployment + Service

| Dimension | Assessment |
|---|---|
| Complexity | Low. Namespace, Deployment, Service, HTTPRoute, ReferenceGrant. |
| Cost | One model copy regardless of consumer count. |
| Scalability | Replicas behind a plain Service; round-robin only, no request-aware routing. |
| Team familiarity | High. |

**Pros:** simplest shared endpoint; one copy; trivially reachable from laptops through the gateway for parity checks.
**Cons:** every call is a network hop; scaling is dumb; a second model is a second Deployment and route; it is a parallel serving stack next to whatever runs generation models.

### Option B: Sidecar in the consumer pod — chosen for the retrieval service

| Dimension | Assessment |
|---|---|
| Complexity | Low-Medium. One pod spec; native sidecar needs Kubernetes ≥ 1.29. No Service, no HTTPRoute for the model itself. |
| Cost | One model copy **per consumer replica**. For bge-m3 the sidecar is heavier than most apps it would serve. |
| Scalability | Scales with the consumer, which is right when the consumer is the only caller and wrong when it is not. |
| Team familiarity | Medium. A well-known production pattern for small encoders. |

**Pros:** no network hop, no DNS, no cross-namespace grant; model lifecycle tied to the consumer; startup ordering guaranteed by native-sidecar semantics; the smallest possible surface for a client that needs an embedder.
**Cons:** memory multiplies with replicas; no shared endpoint, so laptops and other consumers cannot reach it; every consumer has to carry the full parameter contract in its own pod spec; the app container needs its own route if the embedder is to be exercised from outside.

### Option C: llm-d (modelservice + InferencePool + EPP) — chosen for the shared endpoint

| Dimension | Assessment |
|---|---|
| Complexity | **High.** Modelservice Helm chart, InferencePool chart, Inference Extension CRDs, a gateway with the extension enabled, an EPP Deployment, an InferenceObjective per model. Several of these have version-coupling and chart-quality issues that have to be worked around. |
| Cost | The model copy plus the EPP pod plus the routing sidecar the modelservice chart renders. Steady-state overhead to be measured in TASK-0002. |
| Scalability | Request-aware routing across replicas; one pool can front several models. The only option with a story beyond "add replicas". |
| Team familiarity | Low-Medium. |

**Pros:** the shape that scales to replicas and to a second model; the same mechanism that will serve generation models, so one serving stack to operate; integrates with the Gateway API gateway rather than beside it.
**Cons:** for a single-replica embedding model the EPP adds nothing. Its scorers (prefix-cache, KV-cache utilisation, queue depth) are built for prefill/decode generation traffic, and the sane configuration routes `/v1/embeddings` straight to the model Service, bypassing the picker. The pool is an investment in the future, not a benefit today, and it costs memory and operational attention.

## Trade-off Analysis

**Why sidecar for the retrieval service and not for everything.** The sidecar wins exactly when there is one consumer with bounded concurrency and latency matters: no hop, no shared queue, no noisy neighbour. It loses the moment a second consumer appears, because the second copy costs another 1.2 GB plus working set. Query embedding on the hot path is the first case; ingestion plus laptops plus whatever comes next is the second.

**Why llm-d and not standalone for the shared endpoint.** On merit alone, today, standalone wins: fewer moving parts, same vectors, same latency at one replica. The deciding factor is direction. The platform will serve generation models, and those will run behind llm-d and the Inference Extension. Putting embeddings on the same mechanism means one gateway integration, one set of CRDs, one operational playbook. Keeping a separate standalone stack for embeddings would mean two serving paths, two configs and two things to keep in parity for the sake of saving one EPP pod.

**What the measurement baseline buys.** The decision for llm-d is made on direction, not on numbers, so TASK-0002 must produce the numbers: steady memory and p95 latency of llm-d versus a plain Deployment at one replica, same image, same args. If the overhead is ugly, the revisit trigger fires and the ADR is superseded in favour of standalone. Without the baseline the decision would be unfalsifiable.

**What we give up.** With the sidecar: a shared endpoint for the retrieval service, and memory per replica. With llm-d: simplicity, and some memory and attention. With dropping standalone afterwards: the easiest possible parity target for laptops, which the gateway route in front of llm-d has to replace.

## Consequences

- **Easier:** every consumer has one obvious choice: copy the `embed-api` pod spec for a private embedder, or call the shared route for a pooled one.
- **Easier:** one baked image and one args block are the source of truth for the parameter contract across laptops, sidecar and pool. The image's `CMD` carries the defaults; pod specs override as little as possible.
- **Harder:** two in-cluster shapes to keep in lockstep. Any change to the args block has to land in both pod specs, or vectors silently diverge. A parity check across shapes belongs in CI.
- **Harder:** llm-d's prerequisites (gateway with Inference Extension, CRDs, charts) become part of the platform baseline, and their version coupling is now our problem.
- **Harder:** on small nodes the sidecar pod and the pool compete for memory. If both do not fit, the sidecar consumer is the one scaled down in constrained environments, not the shared endpoint.
- **Revisit triggers:** (1) TASK-0002 measures llm-d at more than 1.5× the standalone p95 latency or more than 1 GiB extra steady memory at one replica; (2) a second consumer asks for a sidecar, which is the signal that the shared endpoint is not serving its purpose; (3) the generation-model plan changes so that llm-d is no longer the platform's inference layer, at which point embeddings go back to a plain Deployment.

## Follow-ups

- [TASK-0002](../../tasks/0002-deploy-bge-m3-sidecar-and-llmd-in-abox.md): test deployment of all three shapes on the abox sandbox, with measurements written to the [Changelog](../../CHANGELOG.md). The production rollout on the main cluster is a separate task, written after the numbers are in.
