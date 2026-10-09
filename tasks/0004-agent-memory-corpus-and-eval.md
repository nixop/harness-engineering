# TASK-0004: Build an agent-memory corpus, evaluate the agent on it, write the ADR

**Status:** Done. Parts A–D 2026-10-09; E (voice over A2A) and F (avatar with the full memory loop) demonstrated live 2026-10-10
**Source:** lab 5 assignment: (1) build your own data corpus for agent memory, (2) evaluate your or the reference agent on it, (3) write an ADR; optional (4) avatar with a full memory loop, (5) voice agent delegating to kagent over A2A
**Target:** harness-engineering for corpus, tooling and docs; abox branch `feat/llmd-embeddings-lab5` (from `lab4`) for cluster manifests; Codespace `abox-lab` recreated for the run
**Deliverable:** `corpus/ledger/` with ground truth, a memory ingest into Qdrant + Neo4j, a three-mode evaluation (vector / graph / both), ADR-0003 with Validation, Changelog entry; then the optional voice and avatar apps under `apps/`

---

## Part A: corpus (done 2026-10-08)

`corpus/ledger/`: six English docs, three Confluence storage-format pages, seven Russian ASR-style meeting transcripts over six weeks, and `memory/` with the ground truth (`decisions.jsonl`, `people.jsonl`) and 22 evaluation questions in six classes (fact, temporal, attribution, contradiction, unowned, crosslingual). The README lists the traps the corpus is built around: a decision that changes three times, docs that go stale, moved ownership, an item nobody owns, bilingual terms, spoken numbers, ASR noise.

## Part B: memory model and ingest

1. Chunk sources as in lab 4 but with richer metadata: `source` (`docs-md` | `docs-confluence` | `meeting`), `lang`, `date`, `speaker` (meetings only, per turn group), `doc_title`, `section`. Meetings chunk by speaker-turn windows (3–5 turns, ~300 chars); docs by heading; Confluence by heading after stripping macros (keep `status` macro titles as text, drop `toc`, `jira`, `drawio`, convert `ac:link` users to names).
2. Vector layer: `manifests-bge-m3`'s sibling collection `ledger-bge-m3` through the branch `qdrant-mcp` (`vector_store`), same embedder and parameter contract.
3. Graph layer in Neo4j through `neo4j-mcp` (`write-cypher`): nodes `Person`, `Meeting`, `Document`, `Decision`, `Topic`, `OpenItem`; edges `ATTENDED`, `DECIDED_IN`, `OWNS` (with `from` date), `SUPERSEDES`, `ABOUT`, `MENTIONED_IN`, `DOCUMENTED_IN`, `RAISED_IN`. Keyed on `key` property, MERGE only, as the branch's retrieval-agent prompt already demands.
4. Two ingest paths, both recorded: scripted (deterministic, from `memory/decisions.jsonl` and `people.jsonl` for the graph; chunks for the vector) and agentic (`retrieval-agent` asked to read each transcript and write what it decides is worth remembering). The scripted graph is the reference; the agentic one is what is evaluated as "agent memory".

## Part C: evaluation

5. Three agents, same prompt family as lab 4: `memory-eval-vector` (vector_find only), `memory-eval-graph` (get-schema/read-cypher only), `memory-eval-both`. Prompt: answer from the stores, name source and date for every claim, say when a document is older than a decision, say "no owner" when the graph has none.
6. Run the 22 questions through each agent, against the scripted memory first, then against the agentic memory. Score 0/1/2 as in lab 4 plus two flags: `cites_source`, `dates_correct`.
7. Report per class × mode. Expected shape: vector wins on `fact`, graph on `attribution` and `unowned`, both on `temporal` and `contradiction`. Whatever the numbers say goes into ADR-0003 Validation and the Changelog.

## Part D: ADR-0003

8. "Structure of agent memory": unit of memory, two layers, schema, metadata, supersession policy, what the agent may write. Options: vector only, graph only, both, xray-memory as a product. Decision drafted before the eval, confirmed or amended by it.

## Part E (optional): voice agent over A2A

9. `apps/voice-agent/`: TypeScript, runs in the abox Codespace. Browser page captures the microphone, a Node backend holds `GEMINI_API_KEY`, opens a Gemini Live session (`gemini-3.8-live`) with function declarations `ask_agent(agent, task)` and `list_agents()`, and executes the calls against kagent A2A (`/api/a2a/kagent/<agent>/`, `message/send`). The reply is spoken back. Port forwarded from the Codespace over HTTPS so the browser gets microphone access.
10. Demo script: "what did we decide about the gateway timeout" → `memory-eval-both`; "list the pods in kagent" → `k8s-agent`.

## Part F (optional): avatar with a full memory loop

11. `apps/avatar/`: React with `@runwayml/avatars-react`, backend endpoint that mints the Runway session with `RUNWAYML_API_SECRET`. The avatar fronts the same backend as the voice agent; after each exchange the backend asks the memory agent to `remember` what was said (vector_store + write-cypher), so the next session can recall it. Demo: tell the avatar a new decision, restart the session, ask about it.

## Parts E and F: what was built (2026-10-10)

- `apps/voice-agent/` (abox): Node backend (`server.ts`, runs the `.ts` directly on Node 22.6+) holding `GEMINI_API_KEY`, one Gemini Live session (`gemini-3.8-live`, audio in 16 kHz PCM16 from an AudioWorklet, audio out 24 kHz PCM16, both transcriptions on) per browser connection; tools `list_agents` (kagent REST `/api/agents`) and `ask_agent(agent, task)` (A2A `message/send`); a browser page with push-to-talk, a text box for keyboard tests and a log of transcripts and tool calls. The system prompt forbids answering from the model's own knowledge. `kagent.ts` is the shared client.
- `apps/avatar/` (abox): Express backend mints Runway `gwm1_avatars` sessions server-side (`realtimeSessions.create` with personality, start script and `backend_rpc` tools, polled until `READY`), serves the tools through `@runwayml/avatars-node-rpc`: `recall` → `memory-eval-both`, `ask_agent` → any agent, `remember` → `memory-writer`, `list_agents`. React page on `@runwayml/avatars-react` (`AvatarCall`, `useTranscript`). Full memory loop: every tool call is logged per session and on end the log goes to `memory-writer` as `avatar/<date>-session.txt`; the next session can `recall` it.
- Reference route (abox `apps/refs/`): the course author's `voice-agent` (Go, Gemini Live, MCP + A2A tools) and `avatar` (Go, Runway realtime avatars, MCP tools as `backend_rpc`) built from the private clones into `/workspaces/bin` (ghcr images and charts are closed to the lab token) and run next to the cluster with `run-voice-agent.sh` / `run-avatar.sh`: A2A to `memory-eval-both` and `k8s-agent`, `qdrant-mcp` and `neo4j-mcp` as the avatar's memory (ADR-0003 stores, so what the avatar stores the eval agents can read), the voice prompt replaced with `voice-agent.instruction.md`. The avatar server needs a Runway custom avatar UUID; our own `apps/avatar` works with Runway presets.
- Verified in the Codespace without the keys: the kagent path (`memory-eval-both` and `k8s-agent` answer over A2A from Node), syntax and `tsc` clean, Vite build, backend health, `/api/agents`, `connect` → 503 with a clear message. Not verified: the Gemini Live audio session and the Runway session, which need `GOOGLE_API_KEY` (Gemini) and `RUNWAYML_API_SECRET` as Codespaces secrets (then a Codespace stop/start) and a browser on the forwarded HTTPS port for the microphone.

## Parts E and F: live run (2026-10-10, Codespace `abox-lab`, cluster rebuilt after an idle shutdown)

- Secrets as Codespaces secrets (`GOOGLE_API_KEY`, `RUNWAYML_API_SECRET`), visible after a stop/start; ports 8081 and 8788 forwarded to the laptop with `gh codespace ports forward`, so the browser uses `http://localhost:…` (a secure context for microphone and camera).
- **F, avatar** (our `apps/avatar`, Runway character `e2d712e8-…` created by the user in the Runway dashboard; a second one, `c3563d62-…`, was created from the API with `create-avatar.ts` and a gen4_image portrait). Three sessions in the log (`evals/memory/runs/2026-10-10/avatar-voice-demo/avatar-app.log`): the avatar answered "how many PoCs" with three PoCs and the decisions on each through `recall` → `memory-eval-both`, checked pods and controller logs through `ask_agent` → `k8s-agent`, stored "DLQ alert threshold raised to 15 messages on 2026-10-10" through `remember` → `memory-writer`, and in the **next session** answered "what was decided about the DLQ alert threshold" from that claim with source `avatar/2026-10-09-session.txt`. The memory loop closes through the ADR-0003 stores, so `memory-eval-both` reads what the avatar wrote.
- **E, voice** (the author's `voice-agent` binary, `apps/refs/run-voice-agent.sh`, patched in `internal/tools/a2a.go` to read A2A answers from task artifacts, which is where kagent puts them; the original read only the status message and reported "finished in state completed" without text): Gemini Live over AI Studio (`gemini-2.5-flash-native-audio-preview-12-2025`), tools `ask_memory_eval_both`, `ask_k8s_agent`, `vector_find`, `end_conversation`; the first spoken "какие поды в kagent" produced the tool call but the A2A client failed on the agent card's in-cluster URL; after the fix below the same A2A call answers (curl through the card URL returns the pod list). After the artifacts patch the spoken "find how many pods do we have in our cluster" was answered through `ask_k8s_agent` (log in `avatar-voice-demo/voice-agent.log`), and "what was decided about the DLQ alert threshold" through `ask_memory_eval_both` listed the four retries decisions including the one the avatar had stored. In that answer the memory agent printed "source not found" for three nodes although every Decision node carries a source: its Cypher had left `d.source` out of RETURN. Prompt v5.3 adds: a retrieved node always has text and source, re-run the query with them rather than reporting them missing. The next spoken question, "were there previous decisions about the DLQ alert threshold", answered "none before 2026-10-10": the agent filtered the retries decisions by `text CONTAINS 'threshold'`, and earlier decisions use other words (D21 introduces the DLQ without naming a threshold); on a second try it also wrote the topic key without its `topic:` prefix and got an empty result. Prompt v5.4 makes the topic history query mandatory for "previous / earlier / history" questions (no text filter, then say which decisions mention the detail), and states in the recipes header that T is the prefixed key and an empty topic result means the key was wrong. Four A2A runs of the same question after v5.4 all return the chain 2026-03-30 → 2026-06-15 → 2026-08-24 → 2026-10-10. The voice instruction gained the matching rule: on history questions ask the memory agent for the topic history by date.

Traps found in the demo, all fixed in the code or the run scripts:
- kagent's A2A agent card (`/.well-known/agent-card.json`; `agent.json` is not it) advertises `http://kagent-controller.kagent.svc:8083/…`, which a client outside the cluster cannot resolve. Fix on the Codespace host: `127.0.0.1 kagent-controller.kagent.svc` in `/etc/hosts` plus `kubectl -n kagent port-forward svc/kagent-controller 8083:8083`.
- Runway caps a `backend_rpc` tool at `timeoutSeconds: 8` and the avatar retries the same call when it times out, while `memory-eval-both` takes 5–30 s: eight identical `recall` calls in a minute. Fix: calls are keyed and run once; a call not done in 7 s returns "still answering, call again", the retry gets the cached result. The memory agent is also asked for four short sentences.
- Runway ends a session at about five minutes (`COMPLETED`, `duration: 287`) although `maxDuration: 900` was requested; the page returns to Start call and the end-of-session write runs.
- Writing the whole exchange back through `memory-writer` at the end of a session re-created recalled answers as new decisions dated the session day (`decision:timeouts:2026-10-09`, a Meeting node, open items from `k8s-agent` output, three invented Person nodes). Cleaned from both stores; the end-of-session write is now one fact claim naming what was asked and what was stored. This is ADR-0003's "what the agent may write" rule in practice: a recalled answer is not a claim.
- The server, not the page, decides which avatar is used (`AVATAR_ID`); a Node process that renames itself `MainThread` survives `pkill -x node`, kill it by the pid that holds the port.

## Acceptance criteria
- [ ] Corpus committed with README, ground truth and 22 questions.
- [ ] Chunker handles Markdown, Confluence XHTML and transcripts; chunk counts recorded.
- [ ] `ledger-bge-m3` collection and Neo4j graph populated by the scripted path; counts recorded.
- [ ] Agentic ingest run once; its graph diffed against the scripted one (missing / extra / wrong nodes).
- [ ] 22 questions × 3 modes × 2 memories scored; table in ADR-0003.
- [ ] ADR-0003 written, status Proposed → Accepted after the eval.
- [ ] Changelog entry.
- [x] Optional E and F demonstrated; tool-call logs in `evals/memory/runs/2026-10-10/avatar-voice-demo/`.

## Needs from the owner
- Gemini API key (has it) → Codespaces secret `GEMINI_API_KEY` on `nixop/abox`, when Part E starts.
- Runway developer account and `RUNWAYML_API_SECRET`, when Part F starts.
- Access to `den-vasyliev/xray-memory`, `voice-agent`, `avatar` for reference reading; not blocking.

## Known traps
- Everything from TASK-0003 (Docker data-root, OOM of the official MCP, kmcp port-forwards) still applies.
- Neo4j on the branch has password `abox-neo4j` in the manifest; fine for a sandbox, say so in the ADR.
- The branch's `retrieval-agent` prompt is written for Kubernetes manifests; its graph rules (MERGE on `key`, no self-edges) carry over, the labels do not.
- Gemini Live is a stateful WebSocket; agentgateway cannot proxy it (noted on `feat/triage`). The voice backend talks to Gemini directly.
- Browser microphone needs a secure context: Codespace port forwarding gives HTTPS; plain `http://<ip>` will not.

## Report (2026-10-09, parts A–D)
- **Corpus:** 16 sources, 70 chunks (22 docs-md, 10 Confluence, 38 meeting windows), 12 ground-truth claims, 22 questions.
- **Cluster:** Codespace `abox-lab` rebuilt on `feat/llmd-embeddings-lab5` (Docker data-root on `/tmp/docker`), official MiniLM MCPs removed, `qdrant-mcp` on `ledger-bge-m3`, agents `memory-eval-{vector,graph,both}` and `memory-writer`. Flux `releases` suspended; manifests applied with `kubectl apply -k`. Commits on the branch: `b0e50cc`, `dce243d`, `c4cd274`, `50be6ff`, `fc292ee`.
- **Scripted memory:** 82 vectors (70 chunks + 12 claims), reference graph 11 decisions / 5 people / 7 meetings / 9 documents / 3 SUPERSEDES. Eval v1: vector 95%, graph 57%, both 89%. Eval v2 after fixes (ISO string dates; fixed topic/person keys and Cypher recipes in the prompts): 93% / 77% / 91%.
- **Agentic memory:** 16 writer runs (one `input-required` on docs/gateway.md), 89 vectors, graph 34 Decision / 14 Person / 10 OpenItem / 1 SUPERSEDES (self-loop). graph_diff: decision recall 9/11, precision 0.29. Eval: 50% / 39% / 50%.
- **Defects found and fixed in-lab:** neo4j MCP serialises Neo4j `date()` as empty; LLM Cypher searched topic names by substring and matched person names case-sensitively; both fixed by convention in the prompt. `pkill -f` with a pattern matching the ssh command kills the session (exit 255); use `pkill -x`.
- **Deviations:** agentic run had no raw chunks in the vector layer (extraction-only measure); agentic graph was not validated before the eval, which is exactly what ADR-0003 now requires; the scripted claims were authored from ground truth and are an upper bound.
- **Not done:** the live demos of E and F (keys pending); the agentic run with validation was done later under TASK-0005 step 7.
