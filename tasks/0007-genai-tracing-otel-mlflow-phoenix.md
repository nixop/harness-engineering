# TASK-0007: GenAI traces in three backends: OpenTelemetry (Jaeger), MLflow, Phoenix

**Status:** Done (comparison from live traces; UI walkthrough left to the lab owner, ports are forwarded)
**Source:** lab 7: (1) get to know the OTel, MLflow and Phoenix interfaces; (2) obtain traces of the Astronomy Shop agent, of our retrieval/voice agent, or of any kagent agent; (3) compare the three o11y solutions (standard OTel, MLflow, Phoenix) from the GenAI point of view
**Target:** abox branch `feat/otel-o11y` (cluster from TASK-0006); harness-engineering for the comparison and the exports under `evals/o11y/runs/2026-10-13/`
**Deliverable:** the same agent traces in all three backends, a comparison from what the backends actually recorded, and a recommendation for which backend the lab's agents should report to

---

## Setup for the comparison

One bridge collector (`releases/mlflow-otel-collector.yaml`) receives every span from kagent (controller and agent pods) and from the demo's own collector, routes them by source and fans each route out to all three backends:

```
kagent pods ──┐                     ┌─> Jaeger  (otel-demo namespace, OTLP/gRPC)
              ├─> bridge collector ─┼─> MLflow  (OTLP/HTTP, x-mlflow-experiment-id: kagent=2, otel-demo=1)
demo collector┘   (routing, filter) └─> Phoenix (OTLP/gRPC, bearer system key, openinference.project.name)
```

Three things had to change for that to work, each a trap worth knowing:

| # | Finding | Fix |
|---|---|---|
| 1 | kagent agent pods exported nothing: the controller passes `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` to them, the Go ADK runtime reads the generic `OTEL_EXPORTER_OTLP_ENDPOINT`. Only the controller's `invoke_agent` span existed. | `spec.declarative.deployment.env` on each Agent with the generic variable (`releases/agent-memory.yaml`); `OTEL_SERVICE_NAME` is ignored, the pod names its resource after the Agent with underscores (`memory_eval_both`) |
| 2 | The controller traces its own REST surface; every `POST /api/tasks` from an agent pod became a one-span trace: 183 of the first 200 traces in MLflow were 5 ms HTTP noise | `filter` processor on the kagent route dropping `kagent-controller` spans named `… /api/(tasks|sessions)` |
| 3 | Phoenix runs with auth (chart-generated `phoenix-secret`): OTLP without a key is accepted and silently dropped, the REST API answers 401 | system API key created once through GraphQL `createSystemApiKey` as the admin, stored in a Secret, injected into the exporter header with `${env:PHOENIX_API_KEY}` |

Also: the demo's LLM agent ships with VCR cassettes and a dead `LLM_BASE_URL`, so any unrecorded prompt fails ("Error code: 301", `gen_ai.task.status=failure`). It was pointed at the real OpenAI API with the lab key (`envOverrides` on the `agent` component, plain model id, `USE_VCR=False`).

## The traces

| Trace | Source | Jaeger | MLflow | Phoenix |
|---|---|---|---|---|
| `memory-eval-both` answering "current gateway timeout, since when, what before" over the Relay memory (`5520e0b1…`) | kagent, Go ADK, OTel GenAI semantic conventions | 10 spans, 2 services: `invoke_agent` (controller) → `POST /` → `invocation` → `invoke_agent memory_eval_both` → 3 × `generate_content gpt-5.4-mini` interleaved with `execute_tool get-schema`, `execute_tool read-cypher`; every attribute raw (`gen_ai.usage.input_tokens` 4184 / 5511 / 5781, `gen_ai.tool.call.id`, Cypher text) | trace `tr-5520e0b1…`, state OK, 4.885 s; trace-level `mlflow.trace.tokenUsage` 15 476 in / 225 out, `mlflow.trace.cost` $0.0126 computed from the model name, `mlflow.trace.session` = the A2A context id; resource tags kept (pod, node, service) | project `kagent`: the same 10 spans with `span_kind` derived from `gen_ai.operation.name`: AGENT ×2, LLM ×3, TOOL ×2, UNKNOWN ×3 (HTTP); token count per span and per project (37 613 for the project at the time) |
| Astronomy Shop agent answering "Recommend a beginner telescope under 500 dollars" on OpenAI (`3ba85aa5…`) | demo `agent` (LangGraph + Traceloop/OpenLLMetry), through the demo collector | 22 spans, 3 services: `POST /prompt` → workflow → `invoke_agent LangGraph` → `execute_task model` → `ChatLLM.chat` (532 in / 13 out) → `execute_task tools` → `execute_tool list_products` → HTTP to `frontend` → gRPC `ProductCatalogService/ListProducts` → `sql.conn.query` → second `ChatLLM.chat` (2164 in / 187 out); the only backend that shows the agent's tool call continuing into the store's microservices | trace `tr-3ba85aa5…`, OK, 3.078 s, 2 696 in / 200 out, cost $0.0029 | project `otel-demo`: `ChatLLM.chat` as LLM with token counts (545, 2192), `execute_tool list_products` as TOOL, `LangGraph.workflow` and `invoke_agent LangGraph` as AGENT; the 1 000+ store traces around it are UNKNOWN |
| Our voice agent → `memory-eval-both` ("Какие решения были приняты в Relay 24 августа 2026 года?", `eb16b6a8…`) | `apps/voice-agent` (Node, Gemini Live), instrumented in this task: `voice_session` → `generate_content gemini-2.5-flash-native-audio` (user and agent transcripts) → `execute_tool ask_agent`, whose `traceparent` travels inside the A2A request through agentgateway | 13 spans, 3 services in one trace: `voice-agent` (3) → `kagent-controller` (2) → `memory_eval_both` (8: 3 × LLM, `get-schema`, `read-cypher`, `vector_find`); the spoken question and the Cypher the memory agent ran are 40 s apart in one waterfall | `tr-eb16b6a8…`, service `voice-agent`, 43.6 s, 15 486 in / 268 out tokens (the kagent agent's; the Gemini Live turn reports none), cost $0.0128, session id = the A2A context | project `kagent`: all 13 spans, `voice_session` and both `invoke_agent` as AGENT, the Gemini turn and the three gpt-5.4-mini calls as LLM, the four tool calls as TOOL |
| kagent `retrieval-agent` ("search the vector store for the gateway timeout decision", `d04f43f7…`) | kagent, Go ADK, given the generic OTLP endpoint like the memory agents | 10 spans: `invoke_agent` → 3 × `generate_content` with `get-schema` and `vector_find` between them | experiment `kagent` | project `kagent` |
| kagent `k8s-agent` (pod counts, several runs) | kagent built-in agent | `invoke_agent` → `generate_content` → `execute_tool k8s_get_resources` | experiment `kagent` | project `kagent` |

Exports of all of the above: `evals/o11y/runs/2026-10-13/export/` and `export2/` (see the run README).

Getting the voice agent into the trace took two more findings: the Node OTLP/gRPC exporter cannot reach the collector through `kubectl port-forward` (the chart binds the receivers to the pod IP, the forward dials localhost inside the pod and dies with "lost connection to pod" on the first span, and the exporter fails silently unless `diag` logging is on), so the bridge collector is now a LoadBalancer Service (cloud-provider-kind gives it 172.18.0.x) and the agent on the Codespace host exports to that; and the collector's kagent route had to name `voice-agent` explicitly. Context propagation needed nothing: the W3C `traceparent` header set on the A2A `message/send` request passed through agentgateway and the kagent controller's HTTP server instrumentation picked it up.

## Comparison from the GenAI point of view

| Dimension | OpenTelemetry + Jaeger | MLflow Tracing | Phoenix |
|---|---|---|---|
| What it understands | Nothing GenAI-specific. A span is a span; `gen_ai.*` and `traceloop.*` attributes are tags you read by hand. | OTel GenAI semconv and OpenInference both parsed: token usage and cost aggregated per trace, session id lifted from `gen_ai.conversation.id`, inputs/outputs shown per span. | OpenInference natively, OTel GenAI semconv mapped: `span_kind` LLM / TOOL / AGENT with token counts; prompts and completions rendered as messages. |
| Agent run navigation | Waterfall by time. Best for the question "where did the 3 s go": the tool call → HTTP → gRPC → SQL chain of the demo agent is visible only here, because the store services report to the same Jaeger. | Per trace: span tree, inputs/outputs, token and cost totals; per experiment: a table of runs with duration, tokens, cost, session. | Per project: traces table with kind filters, latency and token columns; per trace: tree with kind icons; sessions grouped by `session.id`. |
| Cost and tokens | Per span only if the SDK wrote `gen_ai.usage.*`; no totals. | Totals per trace and cost from a built-in price table (the `gpt-5.4-mini` run priced without configuration). | Totals per span, trace and project; no cost. |
| Evaluation | None. | Assessments (feedback and expectations) on traces, LLM-judge scorers, datasets built from traces, evaluation runs recorded as MLflow runs. | Evals (LLM-as-judge templates), annotations, datasets and experiments, prompt playground. |
| Search | By service, operation, tags, duration. | Filter by metadata, tags, state, duration, tokens. | Filter expressions over attributes and kinds (`span_kind == 'LLM'`), full text in inputs/outputs. |
| What the producer had to do | Export OTLP. | Export OTLP/HTTP with an experiment header (gRPC not accepted, hence the bridge), create the experiment first (404 otherwise). | Export OTLP with a project attribute and, with auth on, a system key. |
| Noise handling | Shows everything; the controller's REST spans are just more traces. | Everything becomes a trace row; the REST noise made the experiment unreadable until filtered at the collector. | Same, plus the demo's 1 000+ store traces drown the agent traces in `otel-demo` unless filtered by kind. |
| Cost on the 16 GiB machine | Jaeger in-memory, 600 Mi limit, traces gone on restart. | MLflow 2 Gi limit and a PVC (SQLite); needed probe and worker tuning on this node (author's notes in `releases/mlflow.yaml`). | Phoenix + its Postgres, ~1 Gi; startup probe widened for migrations. |
| Interface | Minimal, fast, engineer-oriented. | Experiment-centric: traces live next to runs and models. | Agent-centric: the only UI where "show me the LLM calls of this agent and their prompts" is one click. |

### Second pass with the lab owner (2026-10-13, after the UI walkthrough)

First impression from the UIs: "different interfaces; money only in MLflow and Phoenix; Jaeger is for ordinary services; MLflow and Phoenix look almost the same, MLflow also shows token usage, Phoenix does not seem to". Checked against the data:

- **Phoenix does count tokens and cost, per LLM span and per project**, from the same `gen_ai.usage.*` attributes MLflow reads: the voice trace costs $0.01282 for 15 754 tokens in Phoenix and $0.0128 in MLflow (same price table, same numbers); the `kagent` project stood at 122 617 tokens and $0.099 after eight traces. It is on the LLM spans (`generate_content gpt-5.4-mini`: 5 787 / 182 tokens, $0.0052) and in the project header, not on the AGENT or TOOL rows the traces table opens on, which is why it is easy to miss. The Gemini Live turn has no token attributes in either backend: the Live API does not report usage per turn.
- **Where Phoenix v20 actually shows it** (checked in the browser): the project's **Metrics** tab (cost per day, top models by cost, token usage, prompt/completion token details, LLM and tool span counts and errors); numbers appear on hover, not as headline cards. In the Traces table the `total tokens` and `total cost` columns are on by default but sit beyond the right edge behind the wide `input`/`output` columns, so they look absent until the Columns picker hides those. Cost in the table is rounded to cents ($0.01), the exact value is in the trace view and the API.
- **Phoenix splits a trace whose parent span arrives late.** The voice trace shows as two rows: `voice_session` with 0 tokens and a `POST /api/a2a/kagent/memory-eval-both/` root with 15 754 tokens and $0.01. The kagent spans were exported while the voice agent's `execute_tool` span was still open, so Phoenix filed them as an orphan root; the GraphQL trace object still reports the full $0.0128. Jaeger and MLflow show one trace. Worth knowing for any producer whose parent spans end after their children's export.
- **What is not visible on the first screen** is where the two differ from a trace viewer. Done on the same trace to show it: a human assessment `answer_correct=true` logged on `tr-eb16b6a8…` through MLflow's assessments API (Traces → the trace → Assessments), and a span annotation `answer_correct` with score 1 on the `voice_session` span through Phoenix's annotations API (the trace → Annotations). Both are the entry point for evaluation: MLflow scorers and LLM judges run over traces and write assessments, datasets are built from traces, prompts are versioned in a registry; Phoenix evals (built-in judge templates), datasets and experiments, prompt playground replaying a span with another model.
- **MLflow also ships an AI Gateway** (the lab owner's point): a proxy in front of LLM providers with a unified API, rate limits and tracing of every call. In this cluster that role is already played by `agentgateway-llm` (the author's `releases/agentgateway-llm.yaml`: model routes, per-tenant API keys, budgets, tracing to Phoenix), so MLflow's gateway would duplicate it; Phoenix has no gateway at all.
- **Jaeger stays the odd one out on purpose:** nothing GenAI-specific, but it is the only one that shows the kagent tool call continuing into the store's services, and the OTel stack has the matching metric side (span metrics in Prometheus/Grafana) that neither MLflow nor Phoenix offers.

## Verdict

- **For debugging an agent against the system it acts on, Jaeger.** It is the only backend that keeps the agent's tool call connected to the microservices it hit, because they share the trace context and the backend. GenAI attributes are readable but not understood.
- **For evaluating and costing agent runs, MLflow.** Per-trace token and cost totals with no configuration, sessions from the A2A context id, assessments and datasets on the same objects as the experiments this lab already produces. It needs the bridge (OTLP/HTTP only, experiment header, experiment created first) and a filter in front of it.
- **For reading what an agent actually said and called, Phoenix.** Span kinds, messages and tool calls rendered as such from both OpenInference and OTel GenAI semconv, filters by kind, projects as the unit of isolation. Auth-on by default in this chart is a trap for OTLP producers.

**Recommendation for the lab's agents:** keep exporting plain OTel GenAI semconv from kagent (it is what the Go ADK runtime does and all three backends read it) through the one bridge collector, with MLflow as the system of record for evals and cost (it is where TASK-0004/0005 scores would attach as assessments) and Phoenix as the reading UI. Jaeger stays as the demo's own backend; nothing needs to change in the agents for any of this.

## Acceptance

- [x] One kagent trace id visible in Jaeger, MLflow and Phoenix (`5520e0b1ac0068d0252816a59ea7a5da`); after the rebuild also our voice agent's own trace with the kagent spans inside it (`eb16b6a871b7b392f60f16d93ebd9972`)
- [x] One Astronomy Shop agent trace from the prompt API visible in all three (`3ba85aa506c6d3cc44ef02a567d9a666`; Phoenix classification confirmed through GraphQL)
- [x] Comparison table filled from observations
- [x] Recommendation recorded in the Changelog

## Looking at it

From the laptop (`gh codespace ports forward 8080:8080 8090:8090 5000:5050 6006:6006 16686:16686`, remote:local; MLflow lands on local 5050 because macOS AirPlay already answers on 5000): the store and its UIs at http://localhost:8080 (`/jaeger/ui/`, `/grafana/`, `/chatbot/`, `/feature/` for flagd), MLflow at http://localhost:5050 (experiments `kagent` and `otel-demo`, Traces tab), Phoenix at http://localhost:6006 (login `admin@localhost`; the initial password is `PHOENIX_DEFAULT_ADMIN_INITIAL_PASSWORD` in the `phoenix-secret` Secret of the `phoenix` namespace, and Phoenix asks to replace it at the first UI login, after which the Secret value no longer works; scripts use the system API key instead), kagent UI at http://localhost:8090.

## Trying the demo as a product: first observations (o11y point of view)

Started 2026-10-13 with the lab owner in the browser; continued in the next step.

- **The telemetry stack is the first thing that breaks.** On the 4-core / 16 GiB node Prometheus was OOMKilled every few minutes at the umbrella chart's 400 Mi limit (171 k head series, 40 k of them `k6_browser_http_req_duration_milliseconds_bucket` from the load generator's own browser metrics), and Grafana answered 500 then 503 because its datasource and its own health check timed out. Fixes: Prometheus 1 Gi, the k6/Chromium browser traffic off (`K6_BROWSER_ENABLED=false`, `LOCUST_BROWSER_TRAFFIC_ENABLED=false`; nine Chromium processes were ~40% of a node), demo traces no longer fanned to Phoenix. Observation: a demo built to show observability needs more observability budget than the application it observes.
- **Grafana Live does not work behind the demo's envoy.** `frontend-proxy` answers 403 to the websocket upgrade on `/grafana/api/live/ws` (Grafana itself answers 101 when called directly); its routing is baked into the image. Workaround: Grafana forwarded directly (`kubectl -n otel-demo port-forward svc/grafana 3000:80`, then http://localhost:3000/grafana/). Dashboards work either way, only the streaming refresh needs the socket.
- **No logs backend.** OpenSearch is off for memory; the collector's logs pipeline ends in the `debug` exporter, so logs exist only as collector stdout. The APM dashboard's log panels stay empty; every "why" question has to be answered from traces.
- **Metric cardinality is the demo's own noise.** The Prometheus `target_info` match the Grafana variable uses returns every service in the cluster (kagent, flux, helm-controller, agentgateway-llm...) because the demo's Prometheus scrapes the whole cluster through the OTLP receiver and annotations, not just the store.

### Fault scenario: payment fails for half the orders (2026-10-13, after the rebuild)

Baseline (span metrics over 5 min): ~23 calls/s across the store, 0 errors/s, frontend p95 44 ms. One order placed through the store API (`POST /api/cart`, `POST /api/checkout`) took 0.48 s and produced trace `019583769bbb332e022813987fd78cf0`: 47 spans over 11 services, 12 of them in `checkout`, 3 round trips to `flagd` for feature flags.

`paymentFailure` set to `50%` (written straight into flagd's file through the `flagd-ui` container; the UI's `POST /feature/api/write-to-file` answers 400 to the file as `read-file` returns it, the UI's own save format is different), twelve orders placed, metrics read after 90 s, then the flag reverted:

| Where | What it showed |
|---|---|
| Span metrics (Prometheus, `traces_span_metrics_calls_total{status_code="STATUS_CODE_ERROR"}`) | errors appear within one scrape interval on every hop of the chain: `payment charge` 0.054/s, `checkout PlaceOrder` 0.05/s, `frontend POST /api/checkout` 0.05/s, `frontend-proxy ingress` 0.079/s. The cause is readable from the service with the deepest erroring span, but only if you already know the call graph. |
| Business metric (`demo_payment_transactions_total`) | kept counting 0.23/s: it counts successful charges and has no failure counterpart, so the business view says nothing is wrong. |
| Jaeger, trace `7b650a1bd758a47bd4ea8a11507c8327` (50 spans) | the complete causal chain in one page: `payment charge` records an exception event "Payment request failed. Invalid token. demo.user_context.loyalty_level…", `checkout PlaceOrder` wraps it ("failed to charge card"), `frontend` re-raises it as gRPC `13 INTERNAL`, `frontend-proxy` marks the ingress span. The flag attribute on the payment span says why: the span carries the user's loyalty level the fault is keyed on. |
| Grafana (Spanmetrics dashboard) | error-rate panels per service turn red for the same four services; latency unchanged, so the failure mode is "fast error", not timeout. |
| Recovery | errors stop within one scrape interval of the revert; nothing lingers. |

Observations and questions for a real OTel rollout:

1. **Traces answer "why", metrics only "where".** The exception event on the payment span is the one piece of information that explains the failure; span metrics localise it to a service and operation but every hop reports the same error, so the error rate alone does not say which service is the cause.
2. **A silent error was already there before the injection.** `checkout → cart EmptyCart` fails at ~0.2/s ("Can't access cart storage … Wasn't able to connect to redis") while the order itself returns 200: the user never sees it, span metrics and Jaeger do. Question for a project: which background steps of a transaction are allowed to fail silently, and who watches that rate?
3. **Business metrics need a failure dimension.** A success-only counter (`demo_payment_transactions_total`) is blind to this incident; the failure signal lives only in the span status.
4. **Feature flags are part of the trace.** Every checkout spends 3 spans on flagd; the fault itself is a flag evaluation on the payment span. The same mechanism that injects faults also records them, which is the demo's point and a good pattern.
5. **No logs backend means no "what else happened".** With OpenSearch off, the only narrative is the exception events inside spans; the cart's Valkey problem has no log line to correlate with.
6. **The cost of the signal.** The store at ~23 calls/s produced 171 k head series in Prometheus and 1 000+ traces per minute into every backend that listened; the backends, not the store, were the first thing to fall over on a 16 GiB node.

## Known traps (confirmed)

- Phoenix with auth drops unauthenticated OTLP silently; the collector logs nothing.
- MLflow answers 404 on `/v1/traces` for an unknown experiment id and the exporter drops the batch.
- The Go ADK runtime in kagent agent pods reads `OTEL_EXPORTER_OTLP_ENDPOINT`, not the `_TRACES_` variant the controller injects; the endpoint must carry a scheme.
- `OTEL_SERVICE_NAME` on an agent pod is ignored; route on the underscored Agent name.
