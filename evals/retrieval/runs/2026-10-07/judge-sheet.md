
## en01 [en] Which namespace does Phoenix run in and why is its startup probe widened?
**expected:** namespace phoenix; Alembic migrations on first boot take longer than the chart's 31s startup budget on KinD, so failureThreshold is raised to 120 at periodSeconds 5  
**expected object:** {'file': 'phoenix.yaml', 'kind': 'HelmRelease', 'name': 'phoenix'}

### retrieval-eval-bge-m3 (completed, 7.3s, 1 tool calls)
queries: ['Which namespace does Phoenix run in and why is its startup probe widened?']

Phoenix runs in the **`phoenix` namespace**.

Why the startup probe is widened:
- The chart’s default startup probe is too short for first boot.
- Phoenix runs **Alembic migrations against Postgres on first boot**, which takes longer on KinD, so the container can be killed before it ever binds `:6006`.
- The manifest says the probe budget is widened to **10 minutes**.

Supporting chunks:

1. **HelmRelease `phoenix` in namespace `phoenix`** from `phoenix.yaml`
   - `# phoenix.yaml | HelmRelease phoenix/phoenix`
   - `values:`
   - `# The chart's startup probe allows 31s (periodSeconds 1 x failureThreshold`
   - `# 30). Phoenix runs Alembic migrations against Postgres on first boot, which`
   - `# takes longer than that on KinD, so the probe kills the container before it`
   - `# ever binds :6006 and it restarts forever:`

2. **Same HelmRelease, widened probe budget** from `phoenix.yaml`
   - `# Widen the budget to 10 minutes. Liveness and readiness are left alone --`
   - `# they only start counting once the startup probe succeeds.`
   - `healthChecks:`
   - `startupProbe:`
   - `enabled: true`
   - `initialDelaySeconds: 5`
   - `periodSeconds: 5`
   - `failureThreshold: 120`

3. **

### retrieval-eval-minilm-l6 (completed, 10.2s, 1 tool calls)
queries: ['Which namespace does Phoenix run in and why is its startup probe widened?']

Phoenix runs in the **phoenix** namespace.

From **phoenix.yaml**:
- **Namespace / cluster/phoenix**
  > `apiVersion: v1`  
  > `kind: Namespace`  
  > `metadata:`  
  > `  name: phoenix`

The startup probe was widened because **Phoenix runs Alembic migrations against Postgres on first boot**, which takes longer than the original probe budget on KinD, causing restart loops. From **phoenix.yaml**:
- **HelmRelease / phoenix/phoenix**
  > `# The chart's startup probe allows 31s (periodSeconds 1 x failureThreshold`  
  > `# 30). Phoenix runs Alembic migrations against Postgres on first boot, which`
- **HelmRelease / phoenix/phoenix**
  > `# 30). Phoenix runs Alembic migrations against Postgres on first boot, which`  
  > `# takes longer than that on KinD, so the probe kills the container before it`  
  > `# ever binds :6006 and it restarts forever:`
- **HelmRelease / phoenix/phoenix**
  > `# Widen the budget to 10 minutes. Liveness and readiness are left alone --`  
  > `# they only start counting once the startup probe succeeds.`



### retrieval-eval-minilm-ml.failed-run1 (completed, 11.7s, 1 tool calls)
queries: ['Which namespace does Phoenix run in and why is its startup probe widened?']

Phoenix runs in the `phoenix` namespace.

Why the startup probe was widened:
- Phoenix runs Alembic migrations against Postgres on first boot, which takes longer than the default startup probe budget on KinD.
- The probe was widened so the container isn’t killed before it binds `:6006`; otherwise it would restart forever.
- The manifest comment says the budget was widened to 10 minutes, and liveness/readiness are left alone because they start counting only after startup succeeds.

Supporting chunks:
- **HelmRelease `phoenix/phoenix`** from `phoenix.yaml`
  - `metadata:`
  - `  name: phoenix`
  - `  namespace: phoenix`
  - `# The chart's startup probe allows 31s (periodSeconds 1 x failureThreshold`
  - `# 30). Phoenix runs Alembic migrations against Postgres on first boot, which`
- **HelmRelease `phoenix/phoenix`** from `phoenix.yaml`
  - `# takes longer than that on KinD, so the probe kills the container before it`
  - `# ever binds :6006 and it restarts forever:`
  - `#`
  - `#   Startup probe failed: dial tcp 10.244.2.10:6006: connect: connection refused`
- **HelmRelease `phoenix/phoenix`** from `phoenix.yaml`
  - `#   Container phoenix failed startup probe, will be restarted`
  

### retrieval-eval-minilm-ml (completed, 7.5s, 1 tool calls)
queries: ['Which namespace does Phoenix run in and why is its startup probe widened?']

Phoenix runs in the `phoenix` namespace, from `phoenix.yaml`.

Supporting lines:
- `# phoenix.yaml | HelmRelease phoenix/phoenix`
- `metadata:`
- `  name: phoenix`
- `  namespace: phoenix`

Why the startup probe is widened:
- `# The chart's startup probe allows 31s (periodSeconds 1 x failureThreshold 30). Phoenix runs Alembic migrations against Postgres on first boot, which`
- `# takes longer than that on KinD, so the probe kills the container before it`
- `# ever binds :6006 and it restarts forever:`
- `# Widen the budget to 10 minutes. Liveness and readiness are left alone --`
- `# they only start counting once the startup probe succeeds.`
- `healthChecks:`
- `  startupProbe:`
- `    enabled: true`
- `    initialDelaySeconds: 5`
- `    periodSeconds: 5`
- `    failureThreshold: 120`

So, Phoenix is in namespace `phoenix`, and the startup probe is widened because first-boot Alembic migrations take longer than the original probe window on KinD, causing restarts before the app binds to `:6006`.

## en02 [en] What is the Neo4j password used by the neo4j MCP server?
**expected:** abox-neo4j, from NEO4J_MCP_PASSWORD  
**expected object:** {'file': 'mcp-servers.yaml', 'kind': 'MCPServer', 'name': 'neo4j-mcp'}

### retrieval-eval-bge-m3 (completed, 3.2s, 1 tool calls)
queries: ['What is the Neo4j password used by the neo4j MCP server?']

The Neo4j password used by the neo4j MCP server is **`abox-neo4j`**.

Supported by:

- **MCPServer** `neo4j-mcp` in namespace **`kagent`** from **`mcp-servers.yaml`**:
  - `NEO4J_MCP_PASSWORD: abox-neo4j`

- **HelmRelease** `neo4j` in namespace **`neo4j`** from **`neo4j.yaml`**:
  - `password: "abox-neo4j"`

### retrieval-eval-minilm-l6 (completed, 3.3s, 1 tool calls)
queries: ['What is the Neo4j password used by the neo4j MCP server?']

The Neo4j password used by the neo4j MCP server is **`abox-neo4j`**.

Supporting chunks:

- **MCPServer `neo4j-mcp` in namespace `kagent`** from **`mcp-servers.yaml`**
  - `NEO4J_MCP_PASSWORD: abox-neo4j`
  - `# Matches releases/neo4j.yaml.`

- **HelmRelease `neo4j` in namespace `neo4j`** from **`neo4j.yaml`**
  - `password: "abox-neo4j"`

### retrieval-eval-minilm-ml.failed-run1 (completed, 3.6s, 1 tool calls)
queries: ['What is the Neo4j password used by the neo4j MCP server?']

The Neo4j password used by the neo4j MCP server is **`abox-neo4j`**.

Supporting chunks:

- **MCPServer `neo4j-mcp`** in namespace **`kagent`**, file **`mcp-servers.yaml`**  
  > `NEO4J_MCP_PASSWORD: abox-neo4j`  
  > `# Matches releases/neo4j.yaml.`

- **HelmRelease `neo4j`** in namespace **`neo4j`**, file **`neo4j.yaml`**  
  > `password: "abox-neo4j"`

### retrieval-eval-minilm-ml (completed, 2.1s, 1 tool calls)
queries: ['What is the Neo4j password used by the neo4j MCP server?']

The Neo4j password used by the neo4j MCP server is **`abox-neo4j`**.

Supporting chunks:

- **MCPServer `neo4j-mcp`** in namespace **`kagent`** from **`mcp-servers.yaml`**:
  > `NEO4J_MCP_PASSWORD: abox-neo4j`

- **HelmRelease `neo4j`** in namespace **`neo4j`** from **`neo4j.yaml`**:
  > `password: "abox-neo4j"`

## en03 [en] Which image runs the official qdrant MCP server and how is it started?
**expected:** ghcr.io/astral-sh/uv:python3.12-bookworm-slim with cmd uvx and args mcp-server-qdrant  
**expected object:** {'file': 'mcp-servers.yaml', 'kind': 'MCPServer', 'name': 'qdrant-official-minilm-l6'}

### retrieval-eval-bge-m3 (completed, 3.8s, 2 tool calls)
queries: ['Which image runs the official qdrant MCP server and how is it started?', 'qdrant official MCP server image cmd args uvx mcp-server-qdrant']

The official Qdrant MCP server is run as **MCPServer `qdrant-official-minilm-l6`** in namespace **`kagent`**, from file **`mcp-servers.yaml`**.

Supporting lines:
- `# mcp-servers.yaml | MCPServer kagent/qdrant-official-minilm-l6`
- `# Upstream publishes no image, only a PyPI package -- run it with uvx.`
- `deployment:`
- `image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- `cmd: uvx`
- `args:`
- `- mcp-server-qdrant`

So, it is started with **`uvx mcp-server-qdrant`** using image **`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`**.

### retrieval-eval-minilm-l6 (completed, 4.4s, 1 tool calls)
queries: ['Which image runs the official qdrant MCP server and how is it started?']

Found in `mcp-servers.yaml`:

- **MCPServer `qdrant-official-minilm-ml` in namespace `kagent`**
  - Image: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
  - Started with: `cmd: uvx` and `args: - mcp-server-qdrant`

Supporting lines:
> `deployment:`  
> `  image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim`  
> `  cmd: uvx`  
> `  args:`  
> `    - mcp-server-qdrant`

Also retrieved for the official qdrant MCP baseline:

- **MCPServer `qdrant-official-minilm-l6` in namespace `kagent`**
  - The store says: “Upstream publishes no image, only a PyPI package -- run it with uvx.”
  - Supporting lines:
> `# Upstream publishes no image, only a PyPI package -- run it with uvx.`

So, the official qdrant MCP server is run with **`uvx mcp-server-qdrant`**, and the manifest shows it under the `qdrant-official-minilm-ml` object using the **`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`** image.

### retrieval-eval-minilm-ml.failed-run1 (completed, 3.8s, 1 tool calls)
queries: ['Which image runs the official qdrant MCP server and how is it started?']

Found in `mcp-servers.yaml`:

- **MCPServer `qdrant-official-minilm-ml`** in namespace **`kagent`**
- **Image:** `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- **Started with:** `cmd: uvx` and `args: - mcp-server-qdrant`

Supporting lines:
> `image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim`  
> `cmd: uvx`  
> `args:`  
> `  - mcp-server-qdrant`

Also, the store notes for the related official server say:
> `# Upstream publishes no image, only a PyPI package -- run it with uvx.`

If you meant the other official server variant, `qdrant-official-minilm-l6`, the store says it is also run with `uvx`, and that upstream publishes no image.

### retrieval-eval-minilm-ml (completed, 3.2s, 1 tool calls)
queries: ['Which image runs the official qdrant MCP server and how is it started?']

The official Qdrant MCP server in the store is **MCPServer `qdrant-official-minilm-ml`** in namespace **`kagent`**, from **`mcp-servers.yaml`**.

Supporting lines:
- `image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- `cmd: uvx`
- `args:`
- `  - mcp-server-qdrant`

So it is started by running **`uvx mcp-server-qdrant`** from the **`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`** image.

Retrieved object:
- `MCPServer kagent/qdrant-official-minilm-ml` from `mcp-servers.yaml`

## en04 [en] Why does the kagent HelmRelease carry a kustomize postRenderer patching app.kubernetes.io/version?
**expected:** Flux appends the OCI digest as semver build metadata (0.10.1+dc7fc...), the chart has no appVersion so the label inherits the '+', which Kubernetes rejects as a label value  
**expected object:** {'file': 'kagent.yaml', 'kind': 'HelmRelease', 'name': 'kagent'}

### retrieval-eval-bge-m3 (completed, 4.4s, 1 tool calls)
queries: ['Why does the kagent HelmRelease carry a kustomize postRenderer patching app.kube']

The kagent `HelmRelease` carries that `kustomize` postRenderer patch because the chart’s `app.kubernetes.io/version` label would otherwise inherit Helm build metadata with a `+`, which Kubernetes rejects in label values.

Supporting lines from `kagent.yaml` (`HelmRelease`, `kagent` in namespace `kagent`):

- `# semver build metadata, so Helm sees 0.10.1+dc7fc6109072. kagent's Chart.yaml`
- `# has no appVersion, so app.kubernetes.io/version falls back to .Chart.Version`
- `# and inherits the '+', which Kubernetes rejects as a label value:`
- `#`
- `#   ServiceAccount "kagent-controller" is invalid: metadata.labels:`

And the patch itself:

- `postRenderers:`
- `- kustomize:`
- `    patches:`
- `    - patch: |`
- `        - op: add`
- `          path: /metadata/labels/app.kubernetes.io~1version`
- `          value: "0.10.1"`

Also related explanation from the same object:

- `# This is not visible in a local \`helm template\`: the build metadata is added`
- `# by Flux, not by the chart.`



### retrieval-eval-minilm-l6 (completed, 6.2s, 1 tool calls)
queries: ['Why does the kagent HelmRelease carry a kustomize postRenderer patching app.kube']

The `kagent` `HelmRelease` carries that `kustomize` postRenderer because Flux appends the OCIRepository artifact digest to the chart version, producing semver build metadata like `0.10.1+dc7fc6109072`. Since `kagent`’s `Chart.yaml` has no `appVersion`, `app.kubernetes.io/version` falls back to `.Chart.Version`, inherits the `+`, and Kubernetes rejects that as an invalid label value. The postRenderer patches the label to a clean `0.10.1`.

Object and source:
- `HelmRelease kagent/kagent` from `kagent.yaml`

Supporting lines from the store:
- `# Flux appends the OCIRepository artifact digest to the chart version as`
- `# semver build metadata, so Helm sees 0.10.1+dc7fc6109072. kagent's Chart.yaml`
- `# has no appVersion, so app.kubernetes.io/version falls back to .Chart.Version`
- `# and inherits the '+', which Kubernetes rejects as a label value:`
- `#`
- `#   ServiceAccount "kagent-controller" is invalid: metadata.labels:`
- `#   Invalid value: "0.10.1+dc7fc6109072"`
- `# The chart sanitises the '+' for helm.sh/chart but not for the image tags`
- `# or app.kubernetes.io/version, which the postRenderer above handles.`
- `- op: add`
- `path: /metadata/labels/app.kubernetes.io~1versio

### retrieval-eval-minilm-ml.failed-run1 (completed, 6.8s, 1 tool calls)
queries: ['Why does the kagent HelmRelease carry a kustomize postRenderer patching app.kube']

The `kagent` HelmRelease carries the `kustomize` postRenderer patch because Flux adds build metadata to the chart version, producing a value like `0.10.1+dc7fc6109072`, and the chart falls back to that for `app.kubernetes.io/version`. That `+` makes the label invalid in Kubernetes, so the manifest rewrites the label to `0.10.1`.

Supporting chunks from `kagent.yaml`:

- `HelmRelease kagent/kagent` in `kagent.yaml`:
  > `# Flux appends the OCIRepository artifact digest to the chart version as`
  > `# semver build metadata, so Helm sees 0.10.1+dc7fc6109072. kagent's Chart.yaml`
  > `# has no appVersion, so app.kubernetes.io/version falls back to .Chart.Version`
  > `# and inherits the '+', which Kubernetes rejects as a label value:`

- `HelmRelease kagent/kagent` in `kagent.yaml`:
  > `# This is not visible in a local \`helm template\`: the build metadata is added`
  > `# by Flux, not by the chart.`
  > `postRenderers:`
  > `- kustomize:`
  > `    patches:`
  > `    - patch: |`
  > `        - op: add`
  > `          path: /metadata/labels/app.kubernetes.io~1version`
  > `          value: "0.10.1"`

- `HelmRelease kagent/kagent` in `kagent.yaml`:
  > `# The chart sanitises the '+' for

### retrieval-eval-minilm-ml (completed, 3.5s, 1 tool calls)
queries: ['Why does the kagent HelmRelease carry a kustomize postRenderer patching app.kube']

The `kagent` HelmRelease carries the `kustomize` postRenderer patch because Flux appends the OCI artifact digest to the chart version, producing a version like `0.10.1+dc7fc6109072`, and the chart falls back to `.Chart.Version` for `app.kubernetes.io/version`. That `+` in the label value is rejected by Kubernetes, so the postRenderer rewrites the label to a safe value.

Supporting chunks from `kagent.yaml` (`HelmRelease` `kagent` in namespace `kagent`):

- “Flux appends the OCIRepository artifact digest to the chart version as semver build metadata, so Helm sees `0.10.1+dc7fc6109072`. kagent's Chart.yaml has no appVersion, so `app.kubernetes.io/version` falls back to `.Chart.Version` and inherits the `+`, which Kubernetes rejects as a label value”
- “This is not visible in a local `helm template`: the build metadata is added by Flux, not by the chart.”
- “The chart sanitises the `+` for `helm.sh/chart` but not for the image tags or `app.kubernetes.io/version`, which the postRenderer above handles.”

## en05 [en] What path prefix routes to the llama.cpp embeddings service through the gateway and what rewrite is applied?
**expected:** PathPrefix /llamacpp, URLRewrite ReplacePrefixMatch to /  
**expected object:** {'file': 'llama-cpp-embeddings.yaml', 'kind': 'HTTPRoute', 'name': 'llama-cpp-embeddings'}

### retrieval-eval-bge-m3 (completed, 3.0s, 1 tool calls)
queries: ['What path prefix routes to the llama.cpp embeddings service through the gateway ']

The HTTPRoute is **llama-cpp/llama-cpp-embeddings** in **llama-cpp-embeddings.yaml**.

Relevant lines:
- `path:` `type: PathPrefix`
- `value: /llamacpp`
- `filters:`
  - `type: URLRewrite`
  - `path:`
    - `type: ReplacePrefixMatch`
    - `replacePrefixMatch: /`

So the **path prefix** is **`/llamacpp`**, and it is **rewritten to `/`** with **ReplacePrefixMatch**.

### retrieval-eval-minilm-l6 (completed, 2.4s, 1 tool calls)
queries: ['What path prefix routes to the llama.cpp embeddings service through the gateway ']

The route is in **HTTPRoute `llama-cpp-embeddings`** in namespace **`llama-cpp`**, from **`llama-cpp-embeddings.yaml`**.

Relevant lines from the retrieved chunk:
- `path:`  
  `type: PathPrefix`  
  `value: /llamacpp`
- `urlRewrite:`  
  `path:`  
  `type: ReplacePrefixMatch`  
  `replacePrefixMatch: /`

So, the gateway routes requests with the **`/llamacpp`** path prefix, and it rewrites that prefix to **`/`**.



### retrieval-eval-minilm-ml.failed-run1 (completed, 4.1s, 1 tool calls)
queries: ['What path prefix routes to the llama.cpp embeddings service through the gateway ']

The gateway routes the path prefix `/llamacpp` to the `llama-cpp-embeddings` service, and it rewrites the prefix to `/`.

Supporting chunks:

- **HTTPRoute `llama-cpp/llama-cpp-embeddings`** from `llama-cpp-embeddings.yaml`
  - `path:`
  - `type: PathPrefix`
  - `value: /llamacpp`
  - `filters:`
  - `type: URLRewrite`
  - `urlRewrite:`
  - `path:`
  - `type: ReplacePrefixMatch`
  - `replacePrefixMatch: /`

- **ReferenceGrant `llama-cpp/llama-cpp-embeddings`** from `llama-cpp-embeddings.yaml`
  - `# External:   http://<gateway-ip>/llamacpp/v1/embeddings`
  - `# In-cluster: http://llama-cpp-embeddings.llama-cpp:8090/v1/embeddings`

These lines show the external gateway path and the rewrite applied.

### retrieval-eval-minilm-ml (completed, 2.5s, 1 tool calls)
queries: ['What path prefix routes to the llama.cpp embeddings service through the gateway ']

The gateway route is:

- **Object:** HTTPRoute `llama-cpp/llama-cpp-embeddings`
- **File:** `llama-cpp-embeddings.yaml`

Supported lines:
> `path:`  
> `  type: PathPrefix`  
> `  value: /llamacpp`

And the rewrite applied is:

> `filters:`  
> `  - type: URLRewrite`  
> `    urlRewrite:`  
> `      path:`  
> `        type: ReplacePrefixMatch`  
> `        replacePrefixMatch: /`

So the path prefix is **`/llamacpp`**, and it rewrites that prefix to **`/`**.



## en06 [en] Why does the /v1/embeddings route for llm-d bypass the endpoint picker?
**expected:** the EPP scorers (prefix-cache, kv-cache utilization, queue) are built for decode/prefill generation traffic, not a single-shot embed; with one replica there is nothing to schedule  
**expected object:** {'file': 'llmd.yaml', 'kind': 'HTTPRoute', 'name': 'llm-d-embedding'}

### retrieval-eval-bge-m3 (completed, 4.6s, 1 tool calls)
queries: ['Why does the /v1/embeddings route for llm-d bypass the endpoint picker?']

The store says the `/v1/embeddings` route bypasses the endpoint picker because it is intentionally sent straight to the decode Service, while only the other traffic goes through the pool/endpoint picker.

Relevant object and file:
- Kind: `HTTPRoute`
- Name: `llm-d-embedding`
- Namespace: `llm-d`
- File: `llmd.yaml`

Supporting lines:
- `# Two rules, mirroring the reference deployment's internal route: embeddings go straight to`
- `# the decode Service, everything else goes through the pool. The bypass is`
- `# deliberate on the reference cluster and worth keeping -- the EPP's scorers (prefix-cache,`
- `# kv-cache-utilization, queue) and its openai-parser are built around`
- `# decode/prefill generation traffic, not a pooling runner's single-shot`
- `/v1/embeddings. With one replica of one model there is also nothing to`
- `# schedule. The pool is what makes this extend to a second model later.`

And the route itself shows the embeddings path and direct backend:
- `type: PathPrefix`
- `value: /llmd/v1/embeddings`
- `backendRefs:`
- `- name: llm-d-embedding`
- `port: 8000`



### retrieval-eval-minilm-l6 (completed, 4.9s, 1 tool calls)
queries: ['Why does the /v1/embeddings route for llm-d bypass the endpoint picker?']

The store says the bypass is deliberate because embeddings are meant to go straight to the decode service, while the endpoint picker is for generation traffic.

- **HTTPRoute `llm-d/llm-d-embedding`** from **`llmd.yaml`**
  - “**Two rules, mirroring the reference deployment's internal route: embeddings go straight to the decode Service, everything else goes through the pool. The bypass is deliberate on the reference cluster and worth keeping** …”
  - “**Both backends serve OpenAI-compatible /v1/embeddings, so they can only share one Gateway listener if the prefix is stripped before the hop.**”
  - “**backendRefs: … kind: InferencePool … name: llm-d-pool**” for the non-embedding path, and “**backendRefs: … name: llm-d-embedding**” for the embeddings path.

- **MCPServer `kagent/qdrant-mcp`** from **`mcp-servers.yaml`**
  - “**hit directly rather than through the EPP, whose scorers are built for generation traffic, not a pooling runner's single-shot embed. Direct means no model-based routing** …”

So, according to the retrieved manifest comments, `/v1/embeddings` bypasses the endpoint picker because embeddings are treated as direct decode-service traffic, not routed generation traffi

### retrieval-eval-minilm-ml.failed-run1 (completed, 6.9s, 2 tool calls)
queries: ['Why does the /v1/embeddings route for llm-d bypass the endpoint picker?', 'Why is the /v1/embeddings route for llm-d bypassing the endpoint picker?']

The store says the `/v1/embeddings` route bypasses the endpoint picker because that route is deliberately sent straight to the decode Service, and the endpoint picker’s scorers are for generation traffic, not single-shot embedding requests.

- **HTTPRoute `llm-d-embedding`** in **namespace `llm-d`** from **`llmd.yaml`**
  - `# Two rules, mirroring the reference deployment's internal route: embeddings go straight to`
  - `# the decode Service, everything else goes through the pool. The bypass is`
  - `# deliberate on the reference cluster and worth keeping -- the EPP's scorers (prefix-cache,`
  - `# kv-cache-utilization, queue) and its openai-parser are built around`
  - `# decode/prefill generation traffic, not a pooling runner's single-shot`

A related chunk also says:
- **HelmRelease `llm-d-embedding`** in **namespace `llm-d`** from **`llmd.yaml`**
  - `# llama.cpp, not vLLM. vLLM's CPU backend cannot serve this model`
  - `# here: the worker process is killed by a signal on the first forward`
  
So, from the retrieved manifests: the bypass is intentional because embedding requests are routed directly to decode, and the endpoint picker is designed for generation-style traffic.

### retrieval-eval-minilm-ml (completed, 6.2s, 3 tool calls)
queries: ['Why does the /v1/embeddings route for llm-d bypass the endpoint picker?', 'Why does the /v1/embeddings route for llm-d bypass the endpoint picker?', 'llm-d /v1/embeddings bypass endpoint picker why']

The store says the `/v1/embeddings` route bypasses the endpoint picker on purpose.

Relevant object:
- **HTTPRoute `llm-d-embedding`** in namespace **`llm-d`** from **`llmd.yaml`**

Supporting lines:
> `# Two rules, mirroring the reference deployment's internal route: embeddings go straight to`  
> `# the decode Service, everything else goes through the pool. The bypass is`  
> `# deliberate on the reference cluster and worth keeping -- the EPP's scorers (prefix-cache,`

Also related:
- **HelmRelease `llm-d-embedding`** in namespace **`llm-d`** from **`llmd.yaml`**
> `# llama.cpp, not vLLM. vLLM's CPU backend cannot serve this model`  
> `# here: the worker process is killed by a signal on the first forward`

And:
- **HelmRelease `llm-d-pool`** in namespace **`llm-d`** from **`llmd.yaml`**
> `# added, a blanket selector silently pulls its pods into this pool and`  
> `# the EPP starts handing embedding requests to the wrong server.`

So, from the retrieved chunks: it bypasses the endpoint picker because embeddings are meant to go directly to the decode service, and the bypass is described as deliberate to avoid the EPP routing them to the wrong server.

## en07 [en] Which pooling and normalisation flags does the bge-m3 llama-server use?
**expected:** --pooling cls and --embd-normalize 2  
**expected object:** {'file': 'llama-cpp-embeddings.yaml', 'kind': 'Deployment', 'name': 'llama-cpp-embeddings'}

### retrieval-eval-bge-m3 (completed, 4.2s, 2 tool calls)
queries: ['Which pooling and normalisation flags does the bge-m3 llama-server use?', 'bge-m3 llama-server pooling normalization flags --pooling --normalize']

The bge-m3 llama-server uses:

- `--pooling cls`
- `--embd-normalize 2`

Supported by this chunk from **Deployment `llama-cpp-embeddings` in namespace `llama-cpp`**, file **`llama-cpp-embeddings.yaml`**:

> `args:`  
> `  - --host`  
> `  - 0.0.0.0`  
> `  - --port`  
> `  - "8090"`  
> `  - --embeddings`  
> `  - --pooling`  
> `  - cls`  
> `  - --embd-normalize`  
> `  - "2"`



### retrieval-eval-minilm-l6 (completed, 2.8s, 1 tool calls)
queries: ['Which pooling and normalisation flags does the bge-m3 llama-server use?']

The bge-m3 llama-server uses:

- `--pooling cls`
- `--embd-normalize 2`

Supporting chunk:
- **Namespace** `cluster/llama-cpp`, **Name** `llama-cpp`, **File** `llama-cpp-embeddings.yaml`
- Quote:
  > `#   --embeddings --pooling cls --embd-normalize 2`

Also related deployment chunk:
- **Deployment** `llama-cpp/llama-cpp-embeddings`, **File** `llama-cpp-embeddings.yaml`
- Quote:
  > `# bge-m3 is an XLM-R encoder: a non-causal 8192-token micro-batch`



### retrieval-eval-minilm-ml.failed-run1 (completed, 3.1s, 1 tool calls)
queries: ['Which pooling and normalisation flags does the bge-m3 llama-server use?']

The bge-m3 `llama-server` uses:

- `--pooling cls`
- `--embd-normalize 2`

Supporting chunk:

- **Deployment** `llama-cpp/llama-cpp-embeddings` from **`llama-cpp-embeddings.yaml`**
  > `- --embeddings`  
  > `- --pooling`  
  > `- cls`  
  > `- --embd-normalize`  
  > `- "2"`

Retrieved object(s):
- `Deployment llama-cpp/llama-cpp-embeddings` in `llama-cpp-embeddings.yaml`

### retrieval-eval-minilm-ml (completed, 2.3s, 1 tool calls)
queries: ['Which pooling and normalisation flags does the bge-m3 llama-server use?']

Found in the store:

- **Deployment `llama-cpp/llama-cpp-embeddings`** from **`llama-cpp-embeddings.yaml`**
  - `"args:"`
  - `"- --embeddings"`
  - `"- --pooling"`
  - `"- cls"`
  - `"- --embd-normalize"`
  - `"- \"2\""`

Support from the retrieved chunk:

> `- --embeddings`  
> `- --pooling`  
> `- cls`  
> `- --embd-normalize`  
> `- "2"`

So the bge-m3 llama-server uses **`--pooling cls`** and **`--embd-normalize 2`**.

## en08 [en] Which collection and which prefixes does the qdrant-mcp server use for bge-m3?
**expected:** QDRANT_COLLECTION manifests-bge-m3; EMBEDDINGS_DOCUMENT_PREFIX and EMBEDDINGS_QUERY_PREFIX set to empty strings  
**expected object:** {'file': 'mcp-servers.yaml', 'kind': 'MCPServer', 'name': 'qdrant-mcp'}

### retrieval-eval-bge-m3 (completed, 4.0s, 2 tool calls)
queries: ['Which collection and which prefixes does the qdrant-mcp server use for bge-m3?', 'qdrant-mcp server bge-m3 collection prefixes manifests-bge-m3 EMBEDDINGS_DOCUMEN']

From `mcp-servers.yaml` for **MCPServer `qdrant-mcp`** in namespace **`kagent`**:

- **Collection:** `manifests-bge-m3`
- **Prefixes:** both empty
  - `EMBEDDINGS_DOCUMENT_PREFIX: ""`
  - `EMBEDDINGS_QUERY_PREFIX: ""`

Supporting lines:
> `QDRANT_COLLECTION: manifests-bge-m3`  
> `EMBEDDINGS_DOCUMENT_PREFIX: ""`  
> `EMBEDDINGS_QUERY_PREFIX: ""`

The chunk also notes:
> `# bge-m3 is symmetric: no instruction prefix on either side.`

### retrieval-eval-minilm-l6 (completed, 3.4s, 1 tool calls)
queries: ['Which collection and which prefixes does the qdrant-mcp server use for bge-m3?']

Found in **MCPServer `qdrant-mcp`** in namespace **`kagent`**, from **`mcp-servers.yaml`**:

- Collection:
  - `QDRANT_COLLECTION: manifests-bge-m3`
- Prefixes:
  - `EMBEDDINGS_DOCUMENT_PREFIX: ""`
  - `EMBEDDINGS_QUERY_PREFIX: ""`

Supporting lines:

> `QDRANT_COLLECTION: manifests-bge-m3`  
> `# bge-m3 is symmetric: no instruction prefix on either side. The server`  
> `# reads these with LookupEnv, so an empty value is honoured and turns the`  
> `# nomic defaults ("search_document: " / "search_query: ") off.`  
> `EMBEDDINGS_DOCUMENT_PREFIX: ""`  
> `EMBEDDINGS_QUERY_PREFIX: ""`

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 2.5s, 1 tool calls)
queries: ['Which collection and which prefixes does the qdrant-mcp server use for bge-m3?']

Found in **MCPServer `qdrant-mcp`** in **namespace `kagent`**, from **`mcp-servers.yaml`**.

Supporting lines:

- `QDRANT_COLLECTION: manifests-bge-m3`
- `EMBEDDINGS_DOCUMENT_PREFIX: ""`
- `EMBEDDINGS_QUERY_PREFIX: ""`

Relevant quoted context:

> `# mcp-servers.yaml | MCPServer kagent/qdrant-mcp`  
> `QDRANT_COLLECTION: manifests-bge-m3`  
> `# bge-m3 is symmetric: no instruction prefix on either side.`  
> `EMBEDDINGS_DOCUMENT_PREFIX: ""`  
> `EMBEDDINGS_QUERY_PREFIX: ""`

So the collection is **`manifests-bge-m3`**, and both prefixes are **empty strings**.

## en09 [en] Why is the OpenAI apiKey left empty in the kagent chart values?
**expected:** with a value the chart creates the kagent-openai Secret itself and the previous value was the literal string OPENAI_API_KEY; empty means the Secret is created out of band from the Codespaces secret  
**expected object:** {'file': 'kagent.yaml', 'kind': 'HelmRelease', 'name': 'kagent'}

### retrieval-eval-bge-m3 (completed, 4.5s, 1 tool calls)
queries: ['Why is the OpenAI apiKey left empty in the kagent chart values?']

The chart values leave `apiKey` empty on purpose so the chart does **not** create its own `kagent-openai` Secret. Instead, it references a Secret that is created separately from the Codespaces secret.

Supporting lines from `HelmRelease/kagent` in `kagent.yaml`:

> `# Empty on purpose. With a value here the chart creates the`  
> `# kagent-openai Secret itself -- and the previous value was the literal`  
> `# string "OPENAI_API_KEY", so every agent sat on an invalid key. Left`  
> `# empty, the chart only references the Secret and it is created out of`  
> `# band from the Codespaces secret of the same name:`  
> `#`  
> `#   kubectl -n kagent create secret generic kagent-openai \`  
> `#     --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY"`  
> `#`  
> `# Model stays at the chart default (gpt-4.1-mini).`  
> `apiKey: ""`

So the reason is: to avoid the chart generating an invalid secret and to rely on an externally created `kagent-openai` secret instead.

### retrieval-eval-minilm-l6 (completed, 4.8s, 1 tool calls)
queries: ['Why is the OpenAI apiKey left empty in the kagent chart values?']

The chart leaves `OpenAI.apiKey` empty on purpose so the chart does **not** create the `kagent-openai` Secret itself. Instead, the Secret is created separately from the `OPENAI_API_KEY` value.

Object: `HelmRelease kagent/kagent` in `kagent.yaml`

Supporting lines:
- `# Empty on purpose. With a value here the chart creates the`
- `# kagent-openai Secret itself -- and the previous value was the literal`
- `# string "OPENAI_API_KEY", so every agent sat on an invalid key. Left`
- `# empty, the chart only references the Secret and it is created out of`
- `# band from the Codespaces secret of the same name:`
- `apiKey: ""`

Also retrieved:
- `HelmRelease kagent/kagent` in `kagent.yaml`:
  - `#   kubectl -n kagent create secret generic kagent-openai \`
  - `#     --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY"`
  - `# Model stays at the chart default (gpt-4.1-mini).`


### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 3.8s, 1 tool calls)
queries: ['Why is the OpenAI apiKey left empty in the kagent chart values?']

The store says the OpenAI `apiKey` is left empty on purpose so the chart does **not** create the `kagent-openai` Secret itself; instead, the Secret is created out of band from a Codespaces secret with the same name.

Supporting chunk:

- **HelmRelease `kagent` in namespace `kagent`**, file **`kagent.yaml`**
  - `# Empty on purpose. With a value here the chart creates the`
  - `# kagent-openai Secret itself -- and the previous value was the literal`
  - `# string "OPENAI_API_KEY", so every agent sat on an invalid key. Left`
  - `# empty, the chart only references the Secret and it is created out of`
  - `# band from the Codespaces secret of the same name:`
  - `apiKey: ""`

A second retrieved chunk supports the same point:

- **HelmRelease `kagent` in namespace `kagent`**, file **`kagent.yaml`**
  - `# kagent-openai Secret itself -- and the previous value was the literal`
  - `# string "OPENAI_API_KEY", so every agent sat on an invalid key. Left`
  - `# empty, the chart only references the Secret and it is created out of`
  - `# band from the Codespaces secret of the same name:`



## en10 [en] Why is the agentgateway chart taken from cr.agentgateway.dev instead of the kgateway-dev chart?
**expected:** kgateway-dev's v2.2.x is capped at Kubernetes 1.35 and Gateway API 1.4; abox runs 1.37 and Gateway API 1.6.2  
**expected object:** {'file': 'agentgateway.yaml', 'kind': 'OCIRepository', 'name': 'agentgateway'}

### retrieval-eval-bge-m3 (completed, 6.7s, 2 tool calls)
queries: ['Why is the agentgateway chart taken from cr.agentgateway.dev instead of the kgat', 'agentgateway chart cr.agentgateway.dev kgateway-dev why taken from own chart str']

The store indicates it is taken from **the agentgateway project’s own chart stream, not kgateway-dev’s**.

- **Object:** `OCIRepository` `agentgateway-crds` in namespace `flux-system`
- **File:** `crds/agentgateway-crds.yaml`

Supporting lines:
> `# The agentgateway project's own chart stream, not kgateway-dev's. The`  
> `# kgateway-dev v2.2.x CRDs are rejected by Kubernetes 1.37: the`  
> `# AgentgatewayBackend schema's CEL rules exceed the cost budget by >100x.`

And also:

- **Object:** `OCIRepository` `agentgateway` in namespace `flux-system`
- **File:** `agentgateway.yaml`

Supporting lines:
> `# The agentgateway project's own chart stream. kgateway-dev's v2.2.x is`  
> `# capped at Kubernetes 1.35 and Gateway API 1.4; abox runs 1.37 and Gateway`

So, from the retrieved manifests, the reason is compatibility: **kgateway-dev v2.2.x is too limited for the cluster’s Kubernetes/Gateway API versions, and its CRDs are rejected on Kubernetes 1.37 due to CEL cost budget issues.**

### retrieval-eval-minilm-l6 (completed, 5.4s, 1 tool calls)
queries: ['Why is the agentgateway chart taken from cr.agentgateway.dev instead of the kgat']

The store says the `agentgateway` chart is taken from `cr.agentgateway.dev` because the `kgateway-dev` stream is too old for this cluster.

Relevant object:
- `OCIRepository` `flux-system/agentgateway` from `agentgateway.yaml`

Supporting lines:
> `# The agentgateway project's own chart stream. kgateway-dev's v2.2.x is`  
> `# capped at Kubernetes 1.35 and Gateway API 1.4; abox runs 1.37 and Gateway`  
> `# API 1.6.2. See releases/crds/agentgateway-crds.yaml.`  
> `url: oci://cr.agentgateway.dev/charts/agentgateway`

Also relevant:
- `OCIRepository` `flux-system/agentgateway-crds` from `crds/agentgateway-crds.yaml`

Supporting lines:
> `# The agentgateway project's own chart stream, not kgateway-dev's.`  
> `# The kgateway-dev v2.2.x CRDs are rejected by Kubernetes 1.37: the`  
> `# AgentgatewayBackend schema's CEL rules exceed the cost budget by >100x.`  
> `url: oci://cr.agentgateway.dev/charts/agentgateway-crds`

So, based on the manifest comments, it uses `cr.agentgateway.dev` because `kgateway-dev` v2.2.x is incompatible with the cluster’s Kubernetes/Gateway API versions, and the CRDs are rejected on Kubernetes 1.37.

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 3.8s, 1 tool calls)
queries: ['Why is the agentgateway chart taken from cr.agentgateway.dev instead of the kgat']

The store indicates the agentgateway chart is taken from the project’s own chart stream, not from `kgateway-dev`.

Relevant objects retrieved:

1. `OCIRepository flux-system/agentgateway` from `agentgateway.yaml`
   > `# The agentgateway project's own chart stream. kgateway-dev's v2.2.x is`
   > `# capped at Kubernetes 1.35 and Gateway API 1.4; abox runs 1.37 and Gateway`

2. `OCIRepository flux-system/agentgateway-crds` from `crds/agentgateway-crds.yaml`
   > `# The agentgateway project's own chart stream, not kgateway-dev's. The`
   > `# kgateway-dev v2.2.x CRDs are rejected by Kubernetes 1.37: the`
   > `# AgentgatewayBackend schema's CEL rules exceed the cost budget by >100x.`

So, according to the manifests, the reason is compatibility: `kgateway-dev` v2.2.x is too old / capped for the cluster’s Kubernetes 1.37 and Gateway API 1.4/1.37 environment, and its CRDs are rejected on Kubernetes 1.37.

## en11 [en] What memory limit does the multilingual MiniLM MCP server get and why?
**expected:** 3Gi; the server embeds in-process with FastEmbed and was OOMKilled before at 2Gi on a 2-core Codespace  
**expected object:** {'file': 'mcp-servers.yaml', 'kind': 'MCPServer', 'name': 'qdrant-official-minilm-ml'}

### retrieval-eval-bge-m3 (completed, 5.2s, 2 tool calls)
queries: ['What memory limit does the multilingual MiniLM MCP server get and why?', 'Why does the multilingual MiniLM MCP server have that memory limit?']

I found the memory limit, but not a stated reason for it.

- **Object:** `MCPServer` `qdrant-official-minilm-ml` in namespace `kagent`
- **File:** `mcp-servers.yaml`

Supporting lines:
> `requests:`  
> `  cpu: 100m`  
> `  memory: 512Mi`  
> `limits:`  
> `  cpu: "1"`  
> `  memory: 3Gi`

Reason support I found:
> `# Multilingual sibling, 50+ languages incl. Russian, 384 dims, but only`  
> `# a 128-token input window: anything longer is truncated by the model.`  
> `EMBEDDING_MODEL: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

So the store shows the limit is **3Gi**, but it does **not** explicitly say why that memory limit is set.

### retrieval-eval-minilm-l6 (completed, 3.3s, 1 tool calls)
queries: ['What memory limit does the multilingual MiniLM MCP server get and why?']

The multilingual MiniLM MCP server is **`kagent/qdrant-official-minilm-ml`** from **`mcp-servers.yaml`**.

- **Memory limit:** **3Gi**
- **Why:** the retrieved chunks show the resource limit, but I did **not** retrieve any chunk that explains the reason for that limit.

Supporting lines:
- `limits:`
- `memory: 3Gi`

And the multilingual model context:
- `# Multilingual sibling, 50+ languages incl. Russian, 384 dims, but only`
- `# a 128-token input window: anything longer is truncated by the model.`

So, from the store: **3Gi is confirmed; the “why” is not found in the retrieved chunks.**

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 4.3s, 1 tool calls)
queries: ['What memory limit does the multilingual MiniLM MCP server get and why?']

The multilingual MiniLM MCP server is `MCPServer/kagent/qdrant-official-minilm-ml` in `mcp-servers.yaml`, and it has a memory limit of **3Gi**.

Supporting lines:
- `limits:`
- `memory: 3Gi`

Why:
- The retrieved chunk says it is the “**Multilingual sibling, 50+ languages incl. Russian**” and shows the server using `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- The retrieved comparison note for the same manifest says the earlier branch was “**OOMKilled embedding in-process at a 2Gi limit on a 2-core Codespace**” and was later brought back “**with 3Gi**” on a 4-core Codespace.

Quoted evidence:
- `# Multilingual sibling, 50+ languages incl. Russian, 384 dims, but only`
- `# a 128-token input window: anything longer is truncated by the model.`
- `EMBEDDING_MODEL: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- `# This is the server the branch replaced with mcp/qdrant-mcp after it was`
- `# OOMKilled embedding in-process at a 2Gi limit on a 2-core Codespace. It is`
- `# back as the comparison baseline, on a 4-core Codespace, with 3Gi.`



## en12 [en] How does the retrieval-eval agent have to handle a question it cannot answer from the store?
**expected:** say 'not found in the store' and list the objects it did retrieve; never guess from general Kubernetes knowledge  
**expected object:** {'file': 'agent-retrieval-eval.yaml', 'kind': 'Agent', 'name': 'retrieval-eval-bge-m3'}

### retrieval-eval-bge-m3 (completed, 3.6s, 1 tool calls)
queries: ['How does the retrieval-eval agent have to handle a question it cannot answer fro']

The agent has to respond: **“not found in the store”** and **list the objects it did retrieve**, without guessing.

Support from the retrieved object:

- **Agent / retrieval-eval-bge-m3 / kagent** — file `agent-retrieval-eval.yaml`
  > `- If nothing retrieved answers the question, say "not found in the store"`  
  > `  and list the objects you did retrieve. Do not guess from general`  
  > `  Kubernetes knowledge.`

Also retrieved from the same object:

- **Agent / retrieval-eval-bge-m3 / kagent** — file `agent-retrieval-eval.yaml`
  > `- Answer only from the chunks you retrieved. Name the object (kind, name,`  
  > `  namespace) and the file it came from, and quote the lines that support`  
  > `  the answer.`

### retrieval-eval-minilm-l6 (completed, 2.4s, 1 tool calls)
queries: ['How does the retrieval-eval agent have to handle a question it cannot answer fro']

The store says to handle unanswered questions by replying **“not found in the store”** and listing the objects retrieved.

**Object:** Agent `retrieval-eval-minilm-l6` in namespace `kagent`  
**File:** `agent-retrieval-eval.yaml`

Supporting lines:
> `- If nothing retrieved answers the question, say "not found in the store"`  
> `- Answer only from the chunks you retrieved. Name the object (kind, name, namespace) and the file it came from, and quote the lines that support the answer.`

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 2.5s, 1 tool calls)
queries: ['How does the retrieval-eval agent have to handle a question it cannot answer fro']

The store says to respond with **"not found in the store"** and to **list the objects you did retrieve** if nothing answers the question.

Supported by:

- **Agent kagent/retrieval-eval-minilm-ml** from `agent-retrieval-eval.yaml`
  > `- If nothing retrieved answers the question, say "not found in the store"`
  > `  and list the objects you did retrieve. Do not guess from general`
  > `  Kubernetes knowledge.`

- **Agent kagent/retrieval-eval-minilm-l6** from `agent-retrieval-eval.yaml`
  > `- If nothing retrieved answers the question, say "not found in the store"`
  > `  and list the objects you did retrieve. Do not guess from general`
  > `  Kubernetes knowledge.`

## ru01 [ru] В каком namespace работает Phoenix и почему у него расширен startup probe?
**expected:** namespace phoenix; миграции Alembic при первом старте дольше 31 с, поэтому failureThreshold 120 при periodSeconds 5  
**expected object:** {'file': 'phoenix.yaml', 'kind': 'HelmRelease', 'name': 'phoenix'}

### retrieval-eval-bge-m3 (completed, 3.8s, 1 tool calls)
queries: ['В каком namespace работает Phoenix и почему у него расширен startup probe?']

Phoenix работает в namespace `phoenix`.

Почему расширен `startupProbe`:
- В манифесте сказано, что стандартный startup probe слишком короткий, потому что Phoenix при первом запуске выполняет миграции Alembic в Postgres, и на KinD это занимает дольше, чем позволяет probe; иначе контейнер перезапускается, не успев начать слушать `:6006`.
- Также прямо указано: бюджет увеличили до 10 минут, а `liveness` и `readiness` не трогали, потому что они начинают считаться только после успешного startup probe.

Подтверждающие строки из объекта:
- `HelmRelease phoenix/phoenix`, namespace `phoenix`, файл `phoenix.yaml`:
  > `# Phoenix runs Alembic migrations against Postgres on first boot, which`  
  > `# takes longer than that on KinD, so the probe kills the container before it`  
  > `# ever binds :6006 and it restarts forever:`
- `HelmRelease phoenix/phoenix`, namespace `phoenix`, файл `phoenix.yaml`:
  > `# Widen the budget to 10 minutes. Liveness and readiness are left alone --`  
  > `# they only start counting once the startup probe succeeds.`

### retrieval-eval-minilm-l6 (completed, 4.1s, 1 tool calls)
queries: ['В каком namespace работает Phoenix и почему у него расширен startup probe?']

Phoenix работает в namespace **phoenix**.

Причина расширенного startup probe указана в `phoenix.yaml` в объекте **HelmRelease `phoenix`** (namespace `phoenix`):

> `# The chart's startup probe allows 31s (periodSeconds 1 x failureThreshold 30). Phoenix runs Alembic migrations against Postgres on first boot, which`  
> `# takes longer than that on KinD, so the probe kills the container before it`  
> `# ever binds :6006 and it restarts forever:`  
> `#`  
> `#   Startup probe failed: dial tcp 10.244.2.10:6006: connect: connection refused`

И отдельно видно, что probe расширили до 10 минут:

> `# Widen the budget to 10 minutes. Liveness and readiness are left alone --`  
> `# they only start counting once the startup probe succeeds.`

Источник: `phoenix.yaml`:
- **HelmRelease** `phoenix` / namespace `phoenix`
- **Namespace** `phoenix` / namespace `cluster`

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 4.0s, 1 tool calls)
queries: ['В каком namespace работает Phoenix и почему у него расширен startup probe?']

Phoenix работает в namespace `phoenix`.

Почему у него расширен `startupProbe`:
- чтобы дать приложению больше времени на первый запуск;
- потому что Phoenix выполняет миграции Alembic в Postgres при первом старте;
- на KinD это занимает дольше, чем стандартный бюджет, и иначе контейнер перезапускается до того, как откроет `:6006`.

Подтверждение из `phoenix.yaml`:

- `kind: HelmRelease`, `name: phoenix`, `namespace: phoenix`
  - `metadata:\n  name: phoenix\n  namespace: phoenix`
- причина увеличения `startupProbe`
  - `# Phoenix runs Alembic migrations against Postgres on first boot, which`
  - `# takes longer than that on KinD, so the probe kills the container before it`
  - `# ever binds :6006 and it restarts forever:`
- сам изменённый probe
  - `healthChecks:\n      startupProbe:\n        enabled: true\n        initialDelaySeconds: 5\n        periodSeconds: 5\n        failureThreshold: 120`

Also найден объект `Namespace cluster/phoenix` из `phoenix.yaml`:
- `kind: Namespace`, `name: phoenix`
- `metadata:\n  name: phoenix`

## ru02 [ru] Какой пароль Neo4j использует MCP-сервер neo4j?
**expected:** abox-neo4j  
**expected object:** {'file': 'mcp-servers.yaml', 'kind': 'MCPServer', 'name': 'neo4j-mcp'}

### retrieval-eval-bge-m3 (completed, 3.3s, 1 tool calls)
queries: ['Какой пароль Neo4j использует MCP-сервер neo4j?']

Пароль Neo4j для MCP-сервера `neo4j-mcp` — `abox-neo4j`.

Подтверждение из найденного объекта:

- **Kind:** `MCPServer`
- **Name:** `neo4j-mcp`
- **Namespace:** `kagent`
- **File:** `mcp-servers.yaml`

Цитата:
> `NEO4J_MCP_USERNAME: neo4j`  
> `# Matches releases/neo4j.yaml.`  
> `NEO4J_MCP_PASSWORD: abox-neo4j`  
> `NEO4J_MCP_DATABASE: neo4j`

Also consistent with:

- **Kind:** `HelmRelease`
- **Name:** `neo4j`
- **Namespace:** `neo4j`
- **File:** `neo4j.yaml`

Цитата:
> `password: "abox-neo4j"`

### retrieval-eval-minilm-l6 (completed, 2.5s, 1 tool calls)
queries: ['Какой пароль Neo4j использует MCP-сервер neo4j?']

Пароль Neo4j для MCP-сервера `neo4j-mcp` — `abox-neo4j`.

Источник:
- **MCPServer `neo4j-mcp`**, namespace `kagent`, файл `mcp-servers.yaml`
  - `NEO4J_MCP_PASSWORD: abox-neo4j`

Подтверждающая строка:
> `NEO4J_MCP_PASSWORD: abox-neo4j`

Также в другом фрагменте того же объекта есть комментарий:
> `# Matches releases/neo4j.yaml.`

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 2.6s, 1 tool calls)
queries: ['Какой пароль Neo4j использует MCP-сервер neo4j?']

Пароль Neo4j для MCP-сервера `neo4j-mcp` — `abox-neo4j`.

Подтверждение из найденных чанков:

- **MCPServer `neo4j-mcp` in namespace `kagent`**, file `mcp-servers.yaml`:
  > `NEO4J_MCP_PASSWORD: abox-neo4j`  
  > `NEO4J_MCP_DATABASE: neo4j`

- **HelmRelease `neo4j` in namespace `neo4j`**, file `neo4j.yaml`:
  > `password: "abox-neo4j"`



## ru03 [ru] Каким образом и из какого образа запускается официальный qdrant MCP?
**expected:** образ ghcr.io/astral-sh/uv:python3.12-bookworm-slim, команда uvx mcp-server-qdrant  
**expected object:** {'file': 'mcp-servers.yaml', 'kind': 'MCPServer', 'name': 'qdrant-official-minilm-l6'}

### retrieval-eval-bge-m3 (completed, 3.5s, 1 tool calls)
queries: ['Каким образом и из какого образа запускается официальный qdrant MCP?']

Официальный qdrant MCP запускается через `stdio` и `uvx`, из образа `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.

Поддерживающие строки из объекта **MCPServer `qdrant-official-minilm-ml`** в **namespace `kagent`** из файла **`mcp-servers.yaml`**:

> `spec:`  
> `  transportType: stdio`  
> `  stdioTransport: {}`  
> `  deployment:`  
> `    image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim`  
> `    cmd: uvx`  
> `    args:`  
> `      - mcp-server-qdrant`

Дополнительно, для объекта **MCPServer `qdrant-official-minilm-l6`** в том же файле есть пояснение:

> `# Upstream publishes no image, only a PyPI package -- run it with uvx.`

Если нужно, могу также показать, чем отличаются `qdrant-official-minilm-ml` и `qdrant-official-minilm-l6`.

### retrieval-eval-minilm-l6 (completed, 4.6s, 1 tool calls)
queries: ['Каким образом и из какого образа запускается официальный qdrant MCP?']

Официальный Qdrant MCP запускается как `stdio`-сервер через `uvx`, из образа `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.

Поддерживающий chunk:
- **MCPServer `kagent/qdrant-official-minilm-ml`** из файла `mcp-servers.yaml`
  - `transportType: stdio`
  - `deployment:`
    - `image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
    - `cmd: uvx`
    - `args:`
      - `mcp-server-qdrant`

Цитата:
```yaml
apiVersion: kagent.dev/v1alpha1
kind: MCPServer
metadata:
  name: qdrant-official-minilm-ml
  namespace: kagent
spec:
  transportType: stdio
  stdioTransport: {}
  deployment:
    image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim
    cmd: uvx
    args:
      - mcp-server-qdrant
```

If you want, I can also quote the chunk that mentions the package is upstream-only on PyPI and should be run with `uvx`.

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 3.4s, 1 tool calls)
queries: ['Каким образом и из какого образа запускается официальный qdrant MCP?']

Официальный qdrant MCP запускается как `MCPServer` `kagent/qdrant-official-minilm-l6` в namespace `kagent`, и в манифесте прямо указано, что его запускают через `uvx`, потому что upstream не публикует image.

Поддерживающие строки:
- `mcp-servers.yaml` — `MCPServer kagent/qdrant-official-minilm-l6`
- `# Upstream publishes no image, only a PyPI package -- run it with uvx.`
- `spec:`
- `transportType: stdio`
- `stdioTransport: {}`

Также найден связанный фрагмент с образом и командой для другого official-варианта:
- `mcp-servers.yaml` — `MCPServer kagent/qdrant-official-minilm-ml`
- `image: ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- `cmd: uvx`
- `args:`
- `- mcp-server-qdrant`

Если нужен именно образ для `qdrant-official-minilm-l6`, в найденных кусках он не указан; там сказано только, что image upstream не публикует и запуск идет через `uvx`.

## ru04 [ru] Зачем в HelmRelease kagent нужен postRenderer, который правит метку app.kubernetes.io/version?
**expected:** Flux добавляет digest как build metadata к версии чарта, метка получает '+', Kubernetes отвергает такое значение  
**expected object:** {'file': 'kagent.yaml', 'kind': 'HelmRelease', 'name': 'kagent'}

### retrieval-eval-bge-m3 (completed, 7.3s, 2 tool calls)
queries: ['Зачем в HelmRelease kagent нужен postRenderer, который правит метку app.kubernet', 'Зачем в HelmRelease kagent нужен postRenderer, который правит метку app.kubernet']

`postRenderer` нужен, чтобы исправить `app.kubernetes.io/version` на значение без `+`, потому что Flux добавляет build metadata в версию chart’а, а Kubernetes не принимает `+` в значениях label.

Подтверждение из `kagent.yaml` (`HelmRelease kagent`, namespace `kagent`):

- `# semver build metadata, so Helm sees 0.10.1+dc7fc6109072. kagent's Chart.yaml`
- `# has no appVersion, so app.kubernetes.io/version falls back to .Chart.Version`
- `# and inherits the '+', which Kubernetes rejects as a label value:`
- `#   ServiceAccount "kagent-controller" is invalid: metadata.labels:`

И ещё:

- `# This is not visible in a local \`helm template\`: the build metadata is added`
- `# by Flux, not by the chart.`
- `postRenderers:`
- `- kustomize:`
- `  patches:`
- `  - patch: |`
- `      - op: add`
- `        path: /metadata/labels/app.kubernetes.io~1version`
- `        value: "0.10.1"`

Также в том же объекте сказано, что chart сам санитизирует `+` для `helm.sh/chart`, но не для `app.kubernetes.io/version`:

- `# The chart sanitises the '+' for helm.sh/chart but not for the image tags`
- `# or app.kubernetes.io/version, which the postRenderer above handles.`

### retrieval-eval-minilm-l6 (completed, 6.8s, 1 tool calls)
queries: ['Зачем в HelmRelease kagent нужен postRenderer, который правит метку app.kubernet']

PostRenderer нужен, чтобы исправить `app.kubernetes.io/version` на допустимое значение, потому что без этого Helm/Flux подставляет версию с `+`, а Kubernetes отвергает такую метку.

**Объект:** `HelmRelease/kagent` в namespace `kagent`  
**Файл:** `kagent.yaml`

Поддерживающие фрагменты:

- `# This is not visible in a local \`helm template\`: the build metadata is added`
- `# by Flux, not by the chart.`
- `- op: add`
- `path: /metadata/labels/app.kubernetes.io~1version`
- `value: "0.10.1"`

И ещё:

- `# The chart sanitises the '+' for helm.sh/chart but not for the image tags`
- `# or app.kubernetes.io/version, which the postRenderer above handles.`
- `# semver build metadata, so Helm sees 0.10.1+dc7fc6109072. kagent's Chart.yaml`
- `# has no appVersion, so app.kubernetes.io/version falls back to .Chart.Version`
- `# and inherits the '+', which Kubernetes rejects as a label value:`
- `#`
- `#   ServiceAccount "kagent-controller" is invalid: metadata.labels:`
- `#   Invalid value: "0.10.1+dc7fc6109072"`

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 4.8s, 1 tool calls)
queries: ['Зачем в HelmRelease kagent нужен postRenderer, который правит метку app.kubernet']

В HelmRelease `kagent` `postRenderer` нужен, чтобы исправить `app.kubernetes.io/version` у объектов, которые Helm иначе рендерит с недопустимым значением версии `0.10.1+...` от Flux.

Поддержка из `kagent.yaml` (`HelmRelease`, `kagent`, `namespace: kagent`):

- `# Flux appends the OCIRepository artifact digest to the chart version as`
- `# semver build metadata, so Helm sees 0.10.1+dc7fc6109072. kagent's Chart.yaml`
- `# has no appVersion, so app.kubernetes.io/version falls back to .Chart.Version`
- `# and inherits the '+', which Kubernetes rejects as a label value:`
- `#   ServiceAccount "kagent-controller" is invalid: metadata.labels:`
- `#   Invalid value: "0.10.1+dc7fc6109072"`

И дальше прямо поясняется цель правки:

- `# All 21 broken objects carry app.kubernetes.io/name=kagent, so rewrite the label on those.`
- `postRenderers:`
- `- kustomize:`
- `  patches:`
- `  - patch: |`
- `      - op: add`
- `        path: /metadata/labels/app.kubernetes.io~1version`
- `        value: "0.10.1"`

То есть `postRenderer` нужен, чтобы убрать проблемный `+...` из `app.kubernetes.io/version` и сделать метку допустимой для Kubernetes, иначе часть объектов `kagent` не устанавливается.



## ru05 [ru] По какому префиксу пути через gateway доступен сервис эмбеддингов llama.cpp и какой rewrite применяется?
**expected:** PathPrefix /llamacpp, URLRewrite на /  
**expected object:** {'file': 'llama-cpp-embeddings.yaml', 'kind': 'HTTPRoute', 'name': 'llama-cpp-embeddings'}

### retrieval-eval-bge-m3 (completed, 2.6s, 1 tool calls)
queries: ['По какому префиксу пути через gateway доступен сервис эмбеддингов llama.cpp и ка']

Сервис эмбеддингов llama.cpp доступен через gateway по префиксу пути `/llamacpp`.

Применяется rewrite:
- `type: ReplacePrefixMatch`
- `replacePrefixMatch: /`

Подтверждающие строки из объекта **HTTPRoute `llama-cpp-embeddings`** в namespace **`llama-cpp`**, файл **`llama-cpp-embeddings.yaml`**:

> `path:`  
> `  type: PathPrefix`  
> `  value: /llamacpp`  
> `filters:`  
> `  - type: URLRewrite`  
> `    urlRewrite:`  
> `      path:`  
> `        type: ReplacePrefixMatch`  
> `        replacePrefixMatch: /`

### retrieval-eval-minilm-l6 (completed, 3.6s, 1 tool calls)
queries: ['По какому префиксу пути через gateway доступен сервис эмбеддингов llama.cpp и ка']

Сервис эмбеддингов `llama.cpp` доступен через gateway по префиксу пути `/llamacpp`, с rewrite `ReplacePrefixMatch` в `/`.

Подтверждение из объекта:
- `HTTPRoute llama-cpp/llama-cpp-embeddings` из файла `llama-cpp-embeddings.yaml`
  - `path:`
    - `type: PathPrefix`
    - `value: /llamacpp`
  - `urlRewrite:`
    - `path:`
      - `type: ReplacePrefixMatch`
      - `replacePrefixMatch: /`

Цитата:
```yaml
matches:
  - path:
      type: PathPrefix
      value: /llamacpp
filters:
  - type: URLRewrite
    urlRewrite:
      path:
        type: ReplacePrefixMatch
        replacePrefixMatch: /
```


### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 4.9s, 1 tool calls)
queries: ['По какому префиксу пути через gateway доступен сервис эмбеддингов llama.cpp и ка']

Сервис эмбеддингов llama.cpp доступен через gateway по префиксу пути **`/llamacpp/v1/embeddings`**, а rewrite в найденных чанках **не указан**.

Поддерживающие фрагменты:

- **ReferenceGrant / `llama-cpp-embeddings` / `llama-cpp`** из `llama-cpp-embeddings.yaml`:
  > `# External:   http://<gateway-ip>/llamacpp/v1/embeddings`  
  > `# In-cluster: http://llama-cpp-embeddings.llama-cpp:8090/v1/embeddings`

- **HTTPRoute / `llama-cpp-embeddings` / `llama-cpp`** из `llama-cpp-embeddings.yaml`:
  > `apiVersion: gateway.networking.k8s.io/v1`  
  > `kind: HTTPRoute`  
  > `metadata:`  
  > `  name: llama-cpp-embeddings`  
  > `  namespace: llama-cpp`  
  > `spec:`  
  > `  parentRefs:`  
  > `    - group: gateway.networking.k8s.io`  
  > `      kind: Gateway`  
  > `      name: agentgateway-external`  
  > `      namespace: agentgateway-system`

- **HTTPRoute / `llama-cpp-embeddings` / `llama-cpp`** из `llama-cpp-embeddings.yaml`:
  > `backendRefs:`  
  > `  - name: llama-cpp-embeddings`  
  > `    port: 8090`

По **rewrite** в retrieved chunks ничего прямого не видно, so **rewrite not found in the store**.

## ru06 [ru] Почему маршрут /v1/embeddings для llm-d идёт мимо endpoint picker?
**expected:** скореры EPP сделаны под генеративный трафик prefill/decode, а не под единичный embed; при одной реплике выбирать не из чего  
**expected object:** {'file': 'llmd.yaml', 'kind': 'HTTPRoute', 'name': 'llm-d-embedding'}

### retrieval-eval-bge-m3 (completed, 6.1s, 1 tool calls)
queries: ['Почему маршрут /v1/embeddings для llm-d идёт мимо endpoint picker?']

В найденных манифестах это сделано **намеренно**: маршрут `/v1/embeddings` **идёт напрямую в decode Service, а не через pool / endpoint picker**.

Поддерживающие фрагменты:

- **HTTPRoute `llm-d/llm-d-embedding`** из файла **`llmd.yaml`**:
  > `# Two rules, mirroring the reference deployment's internal route: embeddings go straight to`  
  > `# the decode Service, everything else goes through the pool. The bypass is`  
  > `# deliberate on the reference cluster and worth keeping -- the EPP's scorers (prefix-cache,`

- Там же:
  > `# decode/prefill generation traffic, not a pooling runner's single-shot`  
  > `# /v1/embeddings. With one replica of one model there is also nothing to`  
  > `# schedule. The pool is what makes this extend to a second model later.`

- И сам маршрут/перенаправление:
  > `matches:`  
  > `- path:`  
  > `type: PathPrefix`  
  > `value: /llmd/v1/embeddings`  
  > `filters:`  
  > `- type: URLRewrite`  
  > `urlRewrite:`  
  > `path:`  
  > `type: ReplacePrefixMatch`  
  > `replacePrefixMatch: /v1/embeddings`  
  > `backendRefs:`  
  > `- name: llm-d-embedding`  
  > `port: 8000`

Итого: **мимо endpoint picker он идёт потому, что это специально описанный by

### retrieval-eval-minilm-l6 (completed, 5.5s, 1 tool calls)
queries: ['Почему маршрут /v1/embeddings для llm-d идёт мимо endpoint picker?']

not found in the store

I retrieved these objects, but none directly says why `/v1/embeddings` for `llm-d` bypasses the endpoint picker:

- `HelmRelease llm-d/llm-d-pool` from `llmd.yaml`
  - “The EPP watches the pool's endpoints; without the model pods there is nothing to pick. Not a hard requirement, but it keeps first-apply ordering readable.”
  - “added, a blanket selector silently pulls its pods into this pool and the EPP starts handing embedding requests to the wrong server.”

- `HTTPRoute llm-d/llm-d-embedding` from `llmd.yaml`
  - “the EPP's scorers (prefix-cache, kv-cache-utilization, queue) and its openai-parser are built around decode/prefill generation traffic, not a pooling runner's single-shot …”

- `Service llm-d/llm-d-embedding` from `llmd.yaml`
  - selector labels for `llm-d.ai/inferenceServing`, `llm-d.ai/model`, `llm-d.ai/role: decode`

- `HelmRelease llm-d/llm-d-embedding` from `llmd.yaml`
  - “These land on the pod template and are what the Service below selects.”
  - routing proxy comment mentioning `llm-d-routing-sidecar`

- `MCPServer kagent/qdrant-mcp` from `mcp-servers.yaml`
  - “hit directly rather than through the EPP, whose scorers are built for generat

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.1s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 5.1s, 1 tool calls)
queries: ['Почему маршрут /v1/embeddings для llm-d идёт мимо endpoint picker?']

В найденных фрагментах это объясняется так: маршрут `/v1/embeddings` **намеренно обходит EPP** и идёт напрямую к decode Service / embedding service, потому что EPP-скореры рассчитаны на generation traffic, а не на single-shot embeddings.

Поддерживающие фрагменты:

- **HTTPRoute `llm-d/llm-d-embedding`** из файла `llmd.yaml`  
  > `# Two rules, mirroring the reference deployment's internal route: embeddings go straight to`  
  > `# the decode Service, everything else goes through the pool. The bypass is`  
  > `# deliberate on the reference cluster and worth keeping -- the EPP's scorers (prefix-cache,`

- **HTTPRoute `llm-d/llm-d-embedding`** из файла `llmd.yaml`  
  > `# deliberate on the reference cluster and worth keeping -- the EPP's scorers (prefix-cache,`  
  > `# kv-cache-utilization, queue) and its openai-parser are built around`  
  > `# decode/prefill generation traffic, not a pooling runner's single-shot`

- **MCPServer `kagent/qdrant-mcp`** из файла `mcp-servers.yaml`  
  > `# hit directly rather than through the EPP, whose scorers are built for`  
  > `# generation traffic, not a pooling runner's single-shot embed. Direct`  
  > `# means no model-based routing, so EMBE

## ru07 [ru] Какие флаги pooling и нормализации использует llama-server для bge-m3?
**expected:** --pooling cls, --embd-normalize 2  
**expected object:** {'file': 'llama-cpp-embeddings.yaml', 'kind': 'Deployment', 'name': 'llama-cpp-embeddings'}

### retrieval-eval-bge-m3 (completed, 2.6s, 1 tool calls)
queries: ['Какие флаги pooling и нормализации использует llama-server для bge-m3?']

Для `llama-server`/`llama.cpp` route для `bge-m3` в найденном манифесте указаны такие флаги:

- `--pooling cls`
- `--embd-normalize "2"`

Источник:
- **Deployment** `llama-cpp/llama-cpp-embeddings`
- файл: `llama-cpp-embeddings.yaml`

Поддерживающие строки:
> `- --embeddings`  
> `- --pooling`  
> `- cls`  
> `- --embd-normalize`  
> `- "2"`

Также в том же объекте есть контекст:
> `# bge-m3 is an XLM-R encoder: a non-causal 8192-token micro-batch ...`

### retrieval-eval-minilm-l6 (completed, 4.7s, 2 tool calls)
queries: ['Какие флаги pooling и нормализации использует llama-server для bge-m3?', 'bge-m3 pooling normalization llama-server flags']

В манифесте для `llama-server` / `llama.cpp` для `bge-m3` указаны такие флаги:

- `--pooling cls`
- `--embd-normalize 2`

Это видно в объекте **Deployment `llama-cpp-embeddings`** в namespace **`llama-cpp`** из файла **`llama-cpp-embeddings.yaml`**:

> `args:`  
> `- --host`  
> `- 0.0.0.0`  
> `- --port`  
> `- "8090"`  
> `- --embeddings`  
> `- --pooling`  
> `- cls`  
> `- --embd-normalize`  
> `- "2"`

И также в комментарии того же файла:

> `--embeddings --pooling cls --embd-normalize 2`

Если хотите, могу ещё показать, где в манифесте объясняется, почему именно такие значения выбраны для `bge-m3`.

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 2.6s, 1 tool calls)
queries: ['Какие флаги pooling и нормализации использует llama-server для bge-m3?']

В `Deployment llama-cpp/llama-cpp-embeddings` из файла `llama-cpp-embeddings.yaml` `llama-server` для `bge-m3` использует:

- `--pooling cls`
- `--embd-normalize "2"`

Подтверждающие строки:

> `args:`  
> `- --host`  
> `- 0.0.0.0`  
> `- --port`  
> `- "8090"`  
> `- --embeddings`  
> `- --pooling`  
> `- cls`  
> `- --embd-normalize`  
> `- "2"`

Если нужно, могу также показать, где в манифесте указано, что это именно `bge-m3`.

## ru08 [ru] Какую коллекцию и какие префиксы использует сервер qdrant-mcp для bge-m3?
**expected:** manifests-bge-m3; префиксы документа и запроса пустые  
**expected object:** {'file': 'mcp-servers.yaml', 'kind': 'MCPServer', 'name': 'qdrant-mcp'}

### retrieval-eval-bge-m3 (completed, 3.2s, 1 tool calls)
queries: ['Какую коллекцию и какие префиксы использует сервер qdrant-mcp для bge-m3?']

Сервер **MCPServer `qdrant-mcp`** в namespace **`kagent`** использует:

- **коллекцию:** `manifests-bge-m3`
- **префиксы:** пустые значения, то есть `EMBEDDINGS_DOCUMENT_PREFIX: ""` и `EMBEDDINGS_QUERY_PREFIX: ""`

Подтверждающие строки из файла **`mcp-servers.yaml`**:

- `QDRANT_COLLECTION: manifests-bge-m3`
- `EMBEDDINGS_DOCUMENT_PREFIX: ""`
- `EMBEDDINGS_QUERY_PREFIX: ""`

Также в найденном чанке указано пояснение:

- `bge-m3 is symmetric: no instruction prefix on either side.`
- `the server reads these with LookupEnv, so an empty value is honoured and turns the nomic defaults ("search_document: " / "search_query: ") off.`

### retrieval-eval-minilm-l6 (completed, 4.1s, 2 tool calls)
queries: ['Какую коллекцию и какие префиксы использует сервер qdrant-mcp для bge-m3?', 'какую коллекцию и какие префиксы использует qdrant-mcp для bge-m3?']

Нашёл это в объекте **MCPServer `qdrant-mcp`** в namespace **`kagent`** из файла **`mcp-servers.yaml`**.

Поддерживающие строки:
- `QDRANT_COLLECTION: manifests-bge-m3`
- `# bge-m3 is symmetric: no instruction prefix on either side.`

То есть:
- **коллекция:** `manifests-bge-m3`
- **префиксы:** **не используются** для bge-m3, потому что он симметричный (“no instruction prefix on either side”).

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 2.4s, 1 tool calls)
queries: ['Какую коллекцию и какие префиксы использует сервер qdrant-mcp для bge-m3?']

Найдено в объекте **MCPServer `qdrant-mcp`** в namespace **`kagent`**, файл **`mcp-servers.yaml`**.

Поддерживающие строки:
- `QDRANT_COLLECTION: manifests-bge-m3`
- `# bge-m3 is symmetric: no instruction prefix on either side.`

То есть:
- **коллекция:** `manifests-bge-m3`
- **префиксы:** **никакие**, для bge-m3 указано, что он **symmetrically** работает и **instruction prefix отсутствует** на обеих сторонах.

## ru09 [ru] Почему в values чарта kagent ключ OpenAI оставлен пустым?
**expected:** иначе чарт сам создаёт Secret kagent-openai, а раньше там была строка-заглушка OPENAI_API_KEY; пустое значение означает, что Secret создаётся отдельно из секрета Codespaces  
**expected object:** {'file': 'kagent.yaml', 'kind': 'HelmRelease', 'name': 'kagent'}

### retrieval-eval-bge-m3 (completed, 5.0s, 1 tool calls)
queries: ['Почему в values чарта kagent ключ OpenAI оставлен пустым?']

В `values` чарта `kagent` ключ `openAI.apiKey` оставлен пустым, потому что иначе chart сам создаёт Secret `kagent-openai`, а раньше туда попадало буквальное значение `OPENAI_API_KEY`, из-за чего у агентов был невалидный ключ. Сейчас Secret создаётся отдельно, вне чарта, из одноимённого Codespaces secret.

Подтверждение из объекта:

- **HelmRelease `kagent/kagent`** — файл **`kagent.yaml`**
  - `providers:`
  - `  default: openAI`
  - `  openAI:`
  - `    # Empty on purpose. With a value here the chart creates the`
  - `    # kagent-openai Secret itself -- and the previous value was the literal`
  - `    # string "OPENAI_API_KEY", so every agent sat on an invalid key. Left`
  - `    # empty, the chart only references the Secret and it is created out`
  - `    # of band from the Codespaces secret of the same name:`
  - `    #`
  - `    #   kubectl -n kagent create secret generic kagent-openai \`
  - `    #     --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY"`
  - `    #`
  - `    # Model stays at the chart default (gpt-4.1-mini).`
  - `    apiKey: ""`



### retrieval-eval-minilm-l6 (completed, 4.8s, 1 tool calls)
queries: ['Почему в values чарта kagent ключ OpenAI оставлен пустым?']

В найденных фрагментах это объясняется так:

- **HelmRelease `kagent` в namespace `kagent`**, файл **`kagent.yaml`**:
  - `# Empty on purpose. With a value here the chart creates the`
  - `# kagent-openai Secret itself -- and the previous value was the literal`
  - `# string "OPENAI_API_KEY", so every agent sat on an invalid key. Left`
  - `# empty, the chart only references the Secret and it is created out of`
  - `# band from the Codespaces secret of the same name:`
  - `apiKey: ""`

- **HelmRelease `kagent` в namespace `kagent`**, файл **`kagent.yaml`**:
  - `# Model stays at the chart default (gpt-4.1-mini).`
  - `apiKey: ""`

Итого: ключ OpenAI оставлен пустым **намеренно**, чтобы chart **не создавал Secret сам**, а только **ссылался на уже существующий Secret `kagent-openai`**, созданный отдельно из Codespaces secret. Также в комментарии указано, что раньше там был буквальный текст `OPENAI_API_KEY`, из-за чего агенты получали невалидный ключ.

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.0s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 4.1s, 1 tool calls)
queries: ['Почему в values чарта kagent ключ OpenAI оставлен пустым?']

В найденном фрагменте это сделано намеренно: пустое значение не даёт чарду самому создавать Secret `kagent-openai`, а вместо этого ожидается Secret, созданный отдельно.

**Объект:** `HelmRelease kagent/kagent`  
**Namespace:** `kagent`  
**Файл:** `kagent.yaml`

Поддерживающие строки:

> `# Empty on purpose. With a value here the chart creates the`  
> `# kagent-openai Secret itself -- and the previous value was the literal`  
> `# string "OPENAI_API_KEY", so every agent sat on an invalid key. Left`  
> `# empty, the chart only references the Secret and it is created out of`  
> `# band from the Codespaces secret of the same name:`

И ещё:

> `#   kubectl -n kagent create secret generic kagent-openai \`  
> `#     --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY"`  
> `#`  
> `# Model stays at the chart default (gpt-4.1-mini).`  
> `apiKey: ""`

Итог: ключ OpenAI оставлен пустым, чтобы chart не создавал Secret с неверным значением, а использовал внешний Secret `kagent-openai`.

## ru10 [ru] Почему чарт agentgateway берётся с cr.agentgateway.dev, а не чарт kgateway-dev?
**expected:** kgateway-dev v2.2.x ограничен Kubernetes 1.35 и Gateway API 1.4, а abox на 1.37 и Gateway API 1.6.2  
**expected object:** {'file': 'agentgateway.yaml', 'kind': 'OCIRepository', 'name': 'agentgateway'}

### retrieval-eval-bge-m3 (completed, 5.2s, 2 tool calls)
queries: ['Почему чарт agentgateway берётся с cr.agentgateway.dev, а не чарт kgateway-dev?', 'Почему чарт agentgateway берётся с cr.agentgateway.dev, а не чарт kgateway-dev?']

Нашёл объяснение только для `agentgateway-crds`, не для `kgateway-dev`.

**Объект:** `OCIRepository` `flux-system/agentgateway-crds`  
**Файл:** `crds/agentgateway-crds.yaml`

Поддерживающие строки:
- `# The agentgateway project's own chart stream, not kgateway-dev's.`
- `# The kgateway-dev v2.2.x CRDs are rejected by Kubernetes 1.37: the`
- `# AgentgatewayBackend schema's CEL rules exceed the cost budget by >100x.`
- `url: oci://cr.agentgateway.dev/charts/agentgateway-crds`
- `ref:`
- `tag: "1.5.0"`

То есть в найденном манифесте прямо сказано, что используется **собственный chart stream agentgateway**, а **kgateway-dev** не подходит из-за проблем с CRD/schema на Kubernetes 1.37.

Если нужен точный ответ про конкретный чарт `agentgateway` vs `kgateway-dev`, в сторе это **not found in the store**.

### retrieval-eval-minilm-l6 (completed, 6.4s, 1 tool calls)
queries: ['Почему чарт agentgateway берётся с cr.agentgateway.dev, а не чарт kgateway-dev?']

В найденных манифестах это объясняется так:

- **OCIRepository `agentgateway` / `agentgateway-crds` в namespace `flux-system`**
  - `agentgateway.yaml`:
    > `# capped at Kubernetes 1.35 and Gateway API 1.4; abox runs 1.37 and Gateway`  
    > `# API 1.6.2. See releases/crds/agentgateway-crds.yaml.`  
    > `url: oci://cr.agentgateway.dev/charts/agentgateway`  
    > `ref:`  
    > `  tag: "1.5.0"`
  - `crds/agentgateway-crds.yaml`:
    > `# The agentgateway project's own chart stream, not kgateway-dev's. The`  
    > `# kgateway-dev v2.2.x CRDs are rejected by Kubernetes 1.37: the`  
    > `# AgentgatewayBackend schema's CEL rules exceed the cost budget by >100x.`  
    > `url: oci://cr.agentgateway.dev/charts/agentgateway-crds`  
    > `ref:`  
    > `  tag: "1.5.0"`

Из этих строк следует, что чарт берётся с **`cr.agentgateway.dev`**, потому что используется **собственный поток чартов agentgateway**, а **`kgateway-dev` не подходит**: его CRDs **отклоняются Kubernetes 1.37** из-за слишком дорогих CEL-правил схемы `AgentgatewayBackend`.

**Ответ:** `agentgateway` берётся с `cr.agentgateway.dev`, а не `kgateway-dev`, потому что в манифесте прямо указано, что это **“the agentgatewa

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.1s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 5.4s, 1 tool calls)
queries: ['Почему чарт agentgateway берётся с cr.agentgateway.dev, а не чарт kgateway-dev?']

Чарт `agentgateway` берётся из собственного OCI-репозитория `cr.agentgateway.dev`, а не из `kgateway-dev`, потому что в манифесте это явно описано как “the agentgateway project's own chart stream”, и рядом есть комментарий, что `kgateway-dev` не подходит для этой версии окружения.

Поддерживающие фрагменты:

- **OCIRepository `agentgateway` / `flux-system`** из файла `agentgateway.yaml`:
  > `# The agentgateway project's own chart stream. kgateway-dev's v2.2.x is`
  > `# capped at Kubernetes 1.35 and Gateway API 1.4; abox runs 1.37 and Gateway`

- **OCIRepository `agentgateway-crds` / `flux-system`** из файла `crds/agentgateway-crds.yaml`:
  > `# The agentgateway project's own chart stream, not kgateway-dev's. The`
  > `# kgateway-dev v2.2.x CRDs are rejected by Kubernetes 1.37: the`
  > `# AgentgatewayBackend schema's CEL rules exceed the cost budget by >100x.`

- **HelmRelease `agentgateway` / `agentgateway-system`** из файла `agentgateway.yaml`:
  > `chartRef:`
  > `  kind: OCIRepository`
  > `  name: agentgateway`
  > `  namespace: flux-system`

- **HelmRelease `agentgateway-crds` / `agentgateway-system`** из файла `crds/agentgateway-crds.yaml`:
  > `chartRef:`
  > `  kind: OCI

## ru11 [ru] Какой лимит памяти у MCP-сервера с мультиязычной MiniLM и почему?
**expected:** 3Gi; сервер эмбеддит внутри процесса через FastEmbed и раньше падал по OOM при 2Gi  
**expected object:** {'file': 'mcp-servers.yaml', 'kind': 'MCPServer', 'name': 'qdrant-official-minilm-ml'}

### retrieval-eval-bge-m3 (completed, 5.1s, 2 tool calls)
queries: ['Какой лимит памяти у MCP-сервера с мультиязычной MiniLM и почему?', 'Почему у MCP-сервера qdrant-official-minilm-ml memory limit 3Gi?']

Лимит памяти у **MCPServer `qdrant-official-minilm-ml`** в namespace **`kagent`** — **`3Gi`**.

Источник: **`mcp-servers.yaml`**

Поддерживающие строки:
- `limits:`
- `memory: 3Gi`

Почему: в найденных чанках **нет явного объяснения именно для `qdrant-official-minilm-ml`**. Есть только похожий комментарий для другого сервера (`qdrant-official-minilm-l6`), где сказано:
- `# This is the server the branch replaced with mcp/qdrant-mcp after it was`
- `# OOMKilled embedding in-process at a 2Gi limit on a 2-core Codespace. It is`
- `# back as the comparison baseline, on a 4-core Codespace, with 3Gi.`

Но это относится к **`qdrant-official-minilm-l6`**, а не к `qdrant-official-minilm-ml`, поэтому **почему именно у `qdrant-official-minilm-ml` стоит `3Gi`, в сторе не найдено**.

### retrieval-eval-minilm-l6 (completed, 2.3s, 1 tool calls)
queries: ['Какой лимит памяти у MCP-сервера с мультиязычной MiniLM и почему?']

found in the store.

Object: `MCPServer kagent/qdrant-official-minilm-ml` from `mcp-servers.yaml`

Relevant lines:
- `# Multilingual sibling, 50+ languages incl. Russian, 384 dims, but only`
- `# a 128-token input window: anything longer is truncated by the model.`

So the limit mentioned is a **128-token input window**, because the manifest comment says anything longer is truncated by the model.

Also retrieved for the same object:
- `requests:`
- `memory: 512Mi`
- `limits:`
- `memory: 3Gi`

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.1s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 4.0s, 2 tool calls)
queries: ['Какой лимит памяти у MCP-сервера с мультиязычной MiniLM и почему?', 'Какой memory limit у kagent/qdrant-official-minilm-ml и почему он такой?']

Лимит памяти у **MCPServer `kagent/qdrant-official-minilm-ml`** в файле **`mcp-servers.yaml`** — **`3Gi`**.

Почему:
- в найденном чанке указан лимит:
  > `limits:`  
  > `memory: 3Gi`
- рядом есть пояснение про модель:
  > `# Multilingual sibling, 50+ languages incl. Russian, 384 dims, but only`  
  > `# a 128-token input window: anything longer is truncated by the model.`

То есть по самим чанкам видно, что это multilingual MiniLM-сервер, а память ему выделена **3Gi**.  
**Object:** `MCPServer` `qdrant-official-minilm-ml` in namespace `kagent` from `mcp-servers.yaml`.

## ru12 [ru] Что должен сделать агент retrieval-eval, если ответа на вопрос в хранилище нет?
**expected:** сказать 'not found in the store' и перечислить найденные объекты, не угадывать  
**expected object:** {'file': 'agent-retrieval-eval.yaml', 'kind': 'Agent', 'name': 'retrieval-eval-bge-m3'}

### retrieval-eval-bge-m3 (completed, 2.9s, 1 tool calls)
queries: ['Что должен сделать агент retrieval-eval, если ответа на вопрос в хранилище нет?']

Если ответа на вопрос в хранилище нет, агент должен сказать **"not found in the store"** и **перечислить объекты, которые он всё же нашёл**. Подтверждение:

- **Agent / retrieval-eval-bge-m3 / kagent** from `agent-retrieval-eval.yaml`:
  > `- If nothing retrieved answers the question, say "not found in the store" and list the objects you did retrieve. Do not guess from general Kubernetes knowledge.`

- **Agent / retrieval-eval-minilm-ml / kagent** from `agent-retrieval-eval.yaml`:
  > `- If nothing retrieved answers the question, say "not found in the store"`



### retrieval-eval-minilm-l6 (completed, 2.8s, 1 tool calls)
queries: ['Что должен сделать агент retrieval-eval, если ответа на вопрос в хранилище нет?']

Agent retrieval-eval должен ответить: **"not found in the store"** и перечислить объекты, которые были найдены, если ни один из них не отвечает на вопрос.

Поддерживающие фрагменты из объекта **Agent `retrieval-eval-minilm-l6`** в namespace `kagent`, файл `agent-retrieval-eval.yaml`:

- `- If nothing retrieved answers the question, say "not found in the store"`
- `- and list the objects you did retrieve.`

Также из того же объекта:

- `- Answer only from the chunks you retrieved. Name the object (kind, name, namespace) and the file it came from, and quote the lines that support the answer.`

### retrieval-eval-minilm-ml.failed-run1 (failed, 0.1s, 0 tool calls)
queries: []



### retrieval-eval-minilm-ml (completed, 3.6s, 1 tool calls)
queries: ['Что должен сделать агент retrieval-eval, если ответа на вопрос в хранилище нет?']

Если ответа на вопрос в хранилище нет, агент должен сказать **"not found in the store"** и перечислить объекты, которые он всё же нашёл. Также он не должен гадать по общим знаниям Kubernetes.

Подтверждение из объекта **Agent `retrieval-eval-minilm-ml`** в namespace **`kagent`** из файла **`agent-retrieval-eval.yaml`**:

> `- Answer only from the chunks you retrieved. Name the object (kind, name,`
> `  namespace) and the file it came from, and quote the lines that support`
> `  the answer.`
>
> `- If nothing retrieved answers the question, say "not found in the store"`
> `  and list the objects you did retrieve. Do not guess from general`
> `  Kubernetes knowledge.`
