# o11y run 2026-10-13: one trace, three backends

Evidence for TASK-0007. Cluster from TASK-0006 (abox `feat/otel-o11y`, Codespace `abox-otel`). Every file is an API export taken minutes after the run; no secrets (checked for key patterns).

| File | Backend | Trace |
|---|---|---|
| `export/jaeger-kagent-memory-eval-both.json` | Jaeger (the demo's, OTLP straight from the bridge collector) | kagent `memory-eval-both` answering "What is the current gateway timeout for Relay, since when, and what was it before?" over the Relay memory: trace `5520e0b1ac0068d0252816a59ea7a5da`, 10 spans, services `kagent-controller` + `memory_eval_both` |
| `export/mlflow-kagent-memory-eval-both.json` | MLflow (experiment `kagent`, id 2) | same trace, `tr-5520e0b1…` |
| `export/phoenix-kagent-memory-eval-both.json` | Phoenix (project `kagent`) | same trace, the 10 spans with Phoenix's `span_kind` |
| `export/jaeger-astronomy-shop-agent.json` | Jaeger | the OTel demo's LangGraph agent answering "Recommend a beginner telescope under 500 dollars." on the real OpenAI API (`gpt-5.4-mini`): trace `3ba85aa506c6d3cc44ef02a567d9a666`, 22 spans, services `agent` + `frontend` + `product-catalog` |
| `export/mlflow-astronomy-shop-agent.json` | MLflow (experiment `otel-demo`, id 1) | same trace |
| `export/mlflow-experiments.json`, `export/phoenix-projects.json` | | the experiment and project lists |

How the traces were produced: `memory-eval-both` through A2A on the gateway (`/tmp/lab/ask.py` in the Codespace, the same JSON-RPC `message/send` as every eval in this repo); the demo agent through `POST /prompt` on its Service (port 8010), which is what the chatbot UI calls.

Jaeger and Phoenix exports contain the full span attributes (prompts, tool arguments, Cypher). MLflow's REST trace object carries the trace-level aggregates (`mlflow.trace.tokenUsage`, `mlflow.trace.cost`, `mlflow.trace.session`); its spans are served to the UI from the tracking store and are not in this export.

## export2 (after the cluster rebuild the same day)

| File | Trace |
|---|---|
| `export2/jaeger-voice-agent-to-memory-eval-both.json`, `export2/mlflow-…`, `export2/phoenix-…` | our instrumented `apps/voice-agent` asking `memory-eval-both` about the 2026-08-24 decisions: `eb16b6a871b7b392f60f16d93ebd9972`, 13 spans, services `voice-agent` + `kagent-controller` + `memory_eval_both`, in all three backends |
| `export2/jaeger-kagent-retrieval-agent.json` | kagent `retrieval-agent` over the Relay vector store: `d04f43f7ea468c1ffb5bb8a2cc74fa27`, 10 spans |
| `export2/jaeger-astronomy-shop-agent-2.json` | the demo's LangGraph agent on OpenAI, "Which telescope is best for viewing planets?": `9f56ba009242fd4d821cdf3c58324142`, 22 spans |
| `export2/jaeger-store-checkout-payment-failure.json` | a store checkout during the `paymentFailure` 50% injection: `7b650a1bd758a47bd4ea8a11507c8327`, 50 spans, the exception chain payment → checkout → frontend |
