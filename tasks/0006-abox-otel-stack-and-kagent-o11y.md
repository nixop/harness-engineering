# TASK-0006: abox from the `otel-demo` branch, kagent inside the observability stack, the lab-5 agents on top

**Status:** Done
**Source:** lab 6 ("deploy abox from the otel branch, add the agents and the kagent setup into the o11y system")
**Target:** abox branch `feat/otel-o11y` (from the author's `feat/otel-demo`), Codespace `abox-otel` (4 cores, 16 GiB, the maximum the account offers); harness-engineering for this report
**Deliverable:** a running cluster with the OpenTelemetry demo (Astronomy Shop), MLflow, Phoenix and kagent, where every kagent agent run is traced into the same stack the demo app reports to, the built-in observability agent queries the demo's Prometheus and Grafana, and the lab-5 memory agents answer over the Relay memory again

---

## What the `otel-demo` branch brings

99 commits over `main`: the OpenTelemetry demo chart (`opentelemetry-demo` 0.41.2, its own collector, flagd feature flags with fault injection, an LLM "agent" and "chatbot" component), MLflow 0.1.0 as a tracing backend with a bridge collector (OTLP/gRPC in, OTLP/HTTP out with `x-mlflow-experiment-id`), Phoenix, agentgateway-llm with tracing to Phoenix, plus the author's own triage stack (triage-core, triage-agent, service graph, onboarding pages), an ngrok operator for public access, and xray-memory.

## What could not be deployed and why

| Component | Reason | Effect |
|---|---|---|
| triage-core, triage-agent, graph-otel-demo, pages-triage | charts and images are personal GHCR packages of the course author; the fork's token gets 403 on every one | dropped from `releases/kustomization.yaml` |
| ngrok-operator | needs the author's ngrok account (Secret `ngrok-operator-credentials`, domain `triageagent.ngrok.dev`); it also sits in `releases/crds/`, so its HelmRelease never becoming Ready blocked the `releases` Kustomization behind it | dropped from both kustomizations |
| xray-memory | snapshots are age-encrypted with a key that is not in the repo | dropped |
| llm-d | duplicates the llama.cpp embedder for a comparison already done in TASK-0002; ~1.5 GiB the 16 GiB machine needs for the demo | dropped |

The files stay in the tree; only the kustomizations changed.

## Steps

1. [x] New Codespace on `feat/otel-demo`, `make run` (OpenTofu installer needed `--opentofu-version`; GitHub API rate limit).
2. [x] Flux takeover as in TASK-0005: ResourceSet and input provider annotated `reconcile=disabled`, `releases`, `releases-crds` and the OCIRepository suspended, bundle applied with `kubectl apply -k` from the branch.
3. [x] kagent in the o11y stack: `otel.tracing` on, OTLP/gRPC to the bridge collector; a `kagent` route (`service.name` matching `^kagent`) into its own MLflow experiment next to `otel-demo`.
4. [x] Prometheus, Grafana and Jaeger of the demo enabled again; kagent-tools and grafana-mcp pointed at them; the built-in `observability-agent` answers PromQL questions over the demo.
5. [x] Lab-5 agents (`memory-eval-vector/graph/both`, `memory-writer`, `memory-extractor`) with the bge-m3 embedder and the `relay-bge-m3` collection; Relay memory re-ingested through the MCP servers with `evals/retrieval/mcp_tools.py` (244 chunks in 311 s, 51 claims in 58 s, 656 Cypher statements; 295 points, 138 nodes).

## Report

**Run (2026-10-12/13, Codespace `abox-otel-5r5x4q5qppghp4jj`).** 77 pods, every HelmRelease Ready after the fixes below. MLflow experiments: `otel-demo` (id 1) and `kagent` (id 2) both receive traces; one A2A call to `k8s-agent` produces a trace with the LLM and tool spans. `observability-agent` through grafana-mcp: lists the demo's eight dashboards, computes the total request rate (1.7 req/s at the time) and the top services by rate with PromQL over the `webstore-metrics` datasource. `promql-agent` has no tools by design (it only writes PromQL).

**Fixes that were needed, in order.**

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | `releases` Kustomization never applies | `releases-crds` waits for ngrok-operator, which waits for a Secret nobody has | ngrok dropped from `releases/crds/kustomization.yaml` |
| 2 | after ~20 min every pod ImagePullBackOff or CrashLoopBackOff with "No space left on device" | Docker's data-root on the 32 GB root loop device of a fresh Codespace, not on `/tmp` as the author's scripts assume (same trap as 2026-10-07 in TASK-0003) | dockerd stopped, 19 GB rsynced to `/tmp/docker`, `/etc/docker/daemon.json` with `data-root`, nodes restarted, `fix-docker-acl.sh` re-run; cloud-provider-kind dies with dockerd and the gateway IP is unreachable until it is restarted |
| 3 | three HelmReleases "install failed: timeout" | 5-minute Helm timeout while images were still pulling | forced reconcile (`reconcile.fluxcd.io/forceAt`) once the pods were up |
| 4 | every agent answers nothing, task state `failed` | chart default `gpt-4.1-mini`, 403 for the lab's OpenAI project; the chart also writes the literal `OPENAI_API_KEY` into the Secret on every upgrade | `apiKey: ""`, `model: gpt-5.4-mini`, Secret created out of band (lab-5 convention) |
| 5 | controller log "traces export: invalid target address \"\"", no kagent spans anywhere | OTLP endpoint given as `host:port`; the Go exporter wants a URL | `http://otel-collector.mlflow.svc.cluster.local:4317` |
| 6 | bridge collector drops every demo span with HTTP 404 from MLflow | exporter header named experiment id `3` from the author's cluster; a fresh MLflow has only `0` | experiments created through the REST API, ids rewritten |
| 7 | grafana-mcp "forbidden: host not allowed", `observability-agent` fails to list tools | `mcp/grafana:latest` validates the Host header (loopback only by default); the controller calls it by Service name | `--allowed-hosts` with the in-cluster names; Grafana URL without `/api` |

| 8 | new agent pods `CreateContainerConfigError` after switching to `apiKey: ""` | the Helm upgrade deleted the chart-owned `kagent-openai` Secret | Secret re-created out of band; it must exist before the upgrade next time |

**Memory on the 16 GiB machine.** With the demo's backends on, 11.9 GB used and 4 GB available at idle; llm-d removed to make room for bge-m3. Jaeger 600 Mi, Prometheus 768 Mi, Grafana 256 Mi are the price of the agents having something to query.

## Acceptance

- [x] `kubectl get helmrelease -A` all Ready; the demo reachable through `frontend-proxy` on 8080
- [x] kagent traces visible in MLflow (experiment `kagent`) with LLM and tool spans
- [x] `observability-agent` answers a metrics question over the demo's Prometheus through Grafana
- [x] lab-5 memory agents answer a Relay question over the re-ingested memory (`memory-eval-both`: gateway timeout chain 10 s → 30 s → 25 s with dates and sources; retries owner Ivan Melnik since 2026-09-07)

## Known traps (new in this task)

- A fresh Codespace does not put Docker on `/tmp`; check `docker info | grep "Root Dir"` before `make run` and move it first.
- `pkill -f <pattern>` inside an `ssh` command kills the ssh session when the pattern appears in the command line itself; the script behind it survives only if it was started with `setsid nohup`.
- `cloud-provider-kind` must be restarted after any dockerd restart, or the LoadBalancer IP of agentgateway stops routing.
- mcp-grafana's `GRAFANA_URL` is the base URL; the chart default with `/api` is for an older image.
