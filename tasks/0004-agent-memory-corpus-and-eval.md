# TASK-0004: Build an agent-memory corpus, evaluate the agent on it, write the ADR

**Status:** Parts A–D done 2026-10-09; E and F (voice, avatar) pending
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

## Acceptance criteria
- [ ] Corpus committed with README, ground truth and 22 questions.
- [ ] Chunker handles Markdown, Confluence XHTML and transcripts; chunk counts recorded.
- [ ] `ledger-bge-m3` collection and Neo4j graph populated by the scripted path; counts recorded.
- [ ] Agentic ingest run once; its graph diffed against the scripted one (missing / extra / wrong nodes).
- [ ] 22 questions × 3 modes × 2 memories scored; table in ADR-0003.
- [ ] ADR-0003 written, status Proposed → Accepted after the eval.
- [ ] Changelog entry.
- [ ] Optional E and F: working demo recorded as a GIF or screenshots in `evals/memory/runs/<date>/`.

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
- **Not done:** parts E (voice agent) and F (avatar); the agentic run with validation + raw chunks; an "agentic claims + raw chunks" configuration.
