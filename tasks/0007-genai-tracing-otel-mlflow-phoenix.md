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
| Our voice agent | `apps/voice-agent` (Gemini Live) | not instrumented: the Gemini Live WebSocket session produces no OTel spans; its delegation is the `POST /api/a2a/kagent/<agent>/` root span in kagent's traces, so the kagent trace above is what a voice question looks like from the gateway down | | |

Exports of all of the above: `evals/o11y/runs/2026-10-13/export/` (see its README).

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

## Verdict

- **For debugging an agent against the system it acts on, Jaeger.** It is the only backend that keeps the agent's tool call connected to the microservices it hit, because they share the trace context and the backend. GenAI attributes are readable but not understood.
- **For evaluating and costing agent runs, MLflow.** Per-trace token and cost totals with no configuration, sessions from the A2A context id, assessments and datasets on the same objects as the experiments this lab already produces. It needs the bridge (OTLP/HTTP only, experiment header, experiment created first) and a filter in front of it.
- **For reading what an agent actually said and called, Phoenix.** Span kinds, messages and tool calls rendered as such from both OpenInference and OTel GenAI semconv, filters by kind, projects as the unit of isolation. Auth-on by default in this chart is a trap for OTLP producers.

**Recommendation for the lab's agents:** keep exporting plain OTel GenAI semconv from kagent (it is what the Go ADK runtime does and all three backends read it) through the one bridge collector, with MLflow as the system of record for evals and cost (it is where TASK-0004/0005 scores would attach as assessments) and Phoenix as the reading UI. Jaeger stays as the demo's own backend; nothing needs to change in the agents for any of this.

## Acceptance

- [x] One kagent trace id visible in Jaeger, MLflow and Phoenix (`5520e0b1ac0068d0252816a59ea7a5da`)
- [x] One Astronomy Shop agent trace from the prompt API visible in all three (`3ba85aa506c6d3cc44ef02a567d9a666`; Phoenix classification confirmed through GraphQL)
- [x] Comparison table filled from observations
- [x] Recommendation recorded in the Changelog

## Looking at it

From the laptop (`gh codespace ports forward 8080:8080 8090:8090 5050:5000 6006:6006 16686:16686`; MLflow lands on 5050 because macOS AirPlay already answers on 5000): the store and its UIs at http://localhost:8080 (`/jaeger/ui/`, `/grafana/`, `/chatbot/`, `/feature/` for flagd), MLflow at http://localhost:5050 (experiments `kagent` and `otel-demo`, Traces tab), Phoenix at http://localhost:6006 (login `admin@localhost`, the initial password is `PHOENIX_DEFAULT_ADMIN_INITIAL_PASSWORD` in the `phoenix-secret` Secret of the `phoenix` namespace), kagent UI at http://localhost:8090.

## Known traps (confirmed)

- Phoenix with auth drops unauthenticated OTLP silently; the collector logs nothing.
- MLflow answers 404 on `/v1/traces` for an unknown experiment id and the exporter drops the batch.
- The Go ADK runtime in kagent agent pods reads `OTEL_EXPORTER_OTLP_ENDPOINT`, not the `_TRACES_` variant the controller injects; the endpoint must carry a scheme.
- `OTEL_SERVICE_NAME` on an agent pod is ignored; route on the underscored Agent name.
