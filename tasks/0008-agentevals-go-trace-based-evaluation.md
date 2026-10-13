# TASK-0008: Evaluate our agents from their traces with agentevals-go

**Status:** Open (planned 2026-10-13, not started; the lab owner decided to run it when a project needs it)
**Source:** lab 8: (1) the Go rewrite of agentevals, https://github.com/triageagent-dev/evals ; (2) try scoring our agents' calls with its built-in evals
**Target:** abox branch `feat/otel-o11y` (the cluster and the bridge collector from TASK-0006/0007); harness-engineering for eval sets, runs and the report
**Deliverable:** our agents' traces scored with the built-in metrics against the Relay ground truth, compared with the manual 0/1/2 scores of TASK-0005; the tool either collecting sessions live beside the other three backends or used on demand from Claude Code over MCP

---

## What the tool is (read on 2026-10-13, repo at commit of 2026-10-12)

`agentevals-go` (module `github.com/triageagent-dev/agentevals-go`, Go 1.25) is a from-scratch port of the Python `agentevals`: it scores an agent's behaviour from its OpenTelemetry traces, without re-running the agent. Two ways in:

- **Offline:** `agentevals run <trace.json> --eval-set <golden.json> -m <metric>` on a Jaeger JSON or OTLP JSON/JSONL file. No server needed.
- **Live:** `agentevals serve` opens an OTLP receiver (`:4317` gRPC, `:4318` HTTP), groups incoming spans into sessions by `gen_ai.conversation.id`, shows them in the React UI on `:8001` (WebSocket live feed) and runs "Prepare Evaluation" over chosen sessions; with `--session-db` sessions and run history survive restarts. So it does collect traces continuously, but the analysis is a run you start, not a background process.

It understands three span dialects: Google ADK (`gcp.vertex.agent.*`), OTel GenAI semantic conventions and OpenInference (incl. the turn-pairing path for voice producers without message arrays). The shipped samples (`samples/helm.json`, `samples/k8s.json`) are kagent traces, and our kagent agents export exactly the `invoke_agent` → `generate_content` → `execute_tool` spans it expects (see `evals/o11y/runs/2026-10-13/export2/`).

**Metrics ported (10 of 12):**

| Metric | Needs | What it measures |
|---|---|---|
| `tool_trajectory_avg_score` | nothing | expected tool sequence vs the one in the trace, EXACT / IN_ORDER / ANY_ORDER |
| `response_match_score` | nothing | ROUGE-1 F of the final response vs the golden one |
| `final_response_match_v2` | Gemini key (`GEMINI_API_KEY`/`GOOGLE_API_KEY`) | LLM judge: is the final response equivalent to the golden one (5 samples, majority vote) |
| `hallucinations_v1` | Gemini key | every sentence of the answer labelled supported / unsupported / contradictory against instructions, prompt and tool outputs |
| `rubric_based_final_response_quality_v1`, `rubric_based_tool_use_quality_v1` | Gemini key, `--rubric "..."` | free-text rubrics judged per invocation |
| `safety_v1`, `multi_turn_*_v1` (3) | Vertex AI Managed Eval + GCP project | out of reach for this lab |

Not ported: performance metrics (token/latency aggregates), custom evaluators, logs ingestion. Eval set format: ADK `EvalSet` JSON (`eval_cases[].conversation[]` with `user_content`, `final_response`, `intermediate_data.tool_uses[]` / `tool_responses[]`); with several cases the match is by the first user turn's text.

**MCP server:** `agentevals mcp` (stdio) exposes `list_metrics`, `evaluate_traces` (local trace files, no server needed), `list_sessions`, `summarize_session`, `list_runs`, `get_run_results`. Registered in Claude Code it lets an agent evaluate a trace file on the fly in a conversation; `list_sessions`/`summarize_session` need a running `serve`.

## What we already have for it

- Traces of our agents in Jaeger JSON under `evals/o11y/runs/2026-10-13/export*/`: `memory-eval-both`, `retrieval-agent`, `k8s-agent`, the voice agent → kagent trace, the Astronomy Shop agent. One file per trace, the format `run` reads.
- Ground truth to build eval sets from: `corpus/relay/memory/questions.jsonl` (67 questions with answers and expected sources, TASK-0005) and `corpus/ledger` (22, TASK-0004); the manual 0/1/2 scores in `evals/memory/runs/2026-10-10/relay-scripted-v5/answer-scores.json`.
- The expected tool trajectory per question class is known from the v5 prompts (graph questions: `get-schema` → `read-cypher`; vector: `vector_find`; both: the two in some order) and from the tool call list `ask.py` prints.
- A bridge collector with fan-out (`releases/mlflow-otel-collector.yaml`): adding `serve` as one more OTLP exporter target is one block (its receivers bind on the host, so the LoadBalancer trick of TASK-0007 is not needed in that direction; the collector reaches the Codespace host at the kind bridge gateway).

## Plan when it is picked up

1. Codespace on abox `feat/otel-o11y`, `scripts/lab-restore.sh` (13 min). Build the tool there (`go build -o bin/agentevals ./cmd/agentevals`; Go is in the Codespace image, not on the laptop; no image is published).
2. **Offline first, no cluster needed for this step:** `agentevals run evals/o11y/runs/2026-10-13/export2/jaeger-kagent-retrieval-agent.json -m tool_trajectory_avg_score --eval-set <ours>` to confirm the GenAI-semconv converter reads our traces (check `conversionWarnings`, `numInvocations`), then `response_match_score` and, with the Codespace's Gemini key, `final_response_match_v2` and `hallucinations_v1` on the voice trace.
3. `gen_evalset.py` under `evals/memory/gen/`: Relay questions → ADK EvalSet (user text, golden answer, expected tool uses per class). Keep it next to `gen_questions.py`.
4. Live: `serve --session-db` on the Codespace host; the bridge collector's kagent route gets an `otlp/agentevals` exporter; run 20 Relay questions through `memory-eval-both` over A2A plus a few voice, retrieval and k8s calls; sessions appear in the UI; evaluate from the UI and from the CLI on the exported sessions.
5. Compare machine scores with the manual ones: `final_response_match_v2` vs the 0/1/2 scale, `hallucinations_v1` vs our "wrong answer" column, `tool_trajectory` vs the tool lists in the traces. Note where the judge disagrees with the human and why.
6. MCP: register `agentevals mcp` in Claude Code (`.mcp.json` in this repo, pointing at the built binary), ask it to evaluate a trace file in a conversation; record what that buys over the CLI.
7. Report, Changelog, PR.

## Acceptance

- [ ] Our Jaeger exports load without conversion warnings and `tool_trajectory_avg_score` runs offline
- [ ] An eval set generated from the Relay ground truth; at least 20 `memory-eval-both` traces scored with the two local and two judge metrics
- [ ] Machine vs manual score table with the disagreements explained
- [ ] Live sessions of our agents visible in `serve`, one evaluation run from the UI
- [ ] `agentevals mcp` used from Claude Code at least once, written up

## Known traps (expected)

- The judge metrics default to `gemini-2.5-flash` with 5 samples per invocation: 20 traces × 4 judge metrics is a few hundred Gemini calls; budget it.
- Our voice trace has two `invoke_agent` spans (voice agent and kagent) in one trace; check which one the converter takes as the invocation, or the user text and final response will come from the wrong level.
- `serve` without the OAuth variables is unauthenticated; keep it on the Codespace host, not behind the gateway.
- Phoenix split the voice trace when the parent span arrived late (TASK-0007); `serve` groups by `gen_ai.conversation.id`, which our voice agent and kagent set differently (session uuid vs A2A context id), so the two halves may land in two sessions. Setting one id on both is the fix.
