# TASK-0007: GenAI traces in three backends: OpenTelemetry (Jaeger), MLflow, Phoenix

**Status:** Open
**Source:** lab 7: (1) get to know the OTel, MLflow and Phoenix interfaces; (2) obtain traces of the Astronomy Shop agent, of our retrieval/voice agent, or of any kagent agent; (3) compare the three o11y solutions (standard OTel, MLflow, Phoenix) from the GenAI point of view
**Target:** abox branch `feat/otel-o11y` (cluster from TASK-0006); harness-engineering for the comparison
**Deliverable:** the same agent traces in all three backends, a written comparison with screenshots or exported trace JSON, and a recommendation for which backend the lab's agents should report to

---

## Plan

1. [ ] Fan the kagent traces out: the bridge collector already sends them to MLflow; add Jaeger (the demo's, OTLP/gRPC `jaeger.otel-demo:4317`) and Phoenix (`phoenix-svc.phoenix:4317`) as additional exporters on the `traces/kagent` pipeline. One trace, three UIs.
2. [ ] Traces of the Astronomy Shop agent: the demo's `agent` component (LangGraph, Traceloop/OpenLLMetry instrumentation, VCR cassettes so no LLM key is needed) and `chatbot` (Gradio UI at `/chatbot/`). Drive it through the chatbot, find the trace in Jaeger and MLflow (experiment `otel-demo`); add Phoenix to the demo collector's traces pipeline if the comparison needs it there too.
3. [ ] Traces of our agents: `memory-eval-both` over the Relay memory (kagent, already traced) and the voice agent (`apps/voice-agent`, not instrumented today: the Gemini Live session is not an OTel span source; the A2A delegation lands in kagent's traces).
4. [ ] Compare per backend: span model (does it understand `gen_ai.*` attributes, prompts, completions, tool calls, token counts, cost), trace navigation for agent runs (nested LLM and tool spans, session grouping), evaluation features (feedback, LLM-as-judge, datasets), search and filtering, data retention and storage, operational cost on the 16 GiB machine, and how the agent code or collector had to change to make each one useful.
5. [ ] Write the comparison with the evidence (trace ids, screenshots, exported JSON under `evals/o11y/runs/<date>/`), and the recommendation.

## Acceptance

- [ ] One kagent trace id visible in Jaeger, MLflow and Phoenix
- [ ] One Astronomy Shop agent trace from the chatbot visible in at least two backends
- [ ] Comparison table filled from observations, not from documentation
- [ ] Recommendation recorded in the Changelog

## Known traps (expected)

- Phoenix needs a project name: it reads `openinference.project.name` or the OTLP resource attribute; without it everything lands in `default`.
- MLflow's OTLP endpoint needs a valid `x-mlflow-experiment-id` header or answers 404 (TASK-0006 fix 6).
- The demo collector cannot have exporters nulled out through the umbrella chart (see `releases/opentelemetry-demo.yaml`); add exporters, never remove.
