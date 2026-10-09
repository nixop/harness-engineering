# ADR-0003: Structure of agent memory

**Status:** Accepted (with the two amendments in Validation)
**Date:** 2026-10-08, validated 2026-10-09
**Deciders:** harness-engineering lab owner

## Context

[ADR-0001](0001-embedding-model-for-docs-and-meeting-transcripts.md) chose the embedding model and [ADR-0002](0002-embedding-server-deployment-topology.md) how to serve it. Neither says what the agent actually *remembers*. Lab 4 showed that semantic search over raw chunks answers "what does X say" well. The questions a team actually asks an assistant after six weeks of meetings are different:

- "What did we decide about the timeout, and has it changed?" The answer is the latest decision plus its history, and the right source is a transcript, not the document that was never updated.
- "Who owns retries now?" Ownership moved; the current owner is a fact about a relationship with a start date.
- "Who is doing the dry run?" Nobody. A memory that cannot say "no one" will invent a name.
- "Is this document still true?" Requires comparing a document's date with the decisions made after it.

The lab corpus (`corpus/ledger/`) is built around exactly these cases, in two languages, with noisy transcripts. The question this ADR answers: how should memory be structured so that an agent gets these right, within the stack we have (Qdrant, Neo4j, kagent, MCP, bge-m3)?

Constraints:

- The lab uses the stores that already exist on the abox branch, a Qdrant collection and a Neo4j graph, each behind an MCP server. The decision below is about the *shape* of memory; which graph product holds it is an implementation detail of the lab, not part of the decision. A relational table of edges or a graph extension in Postgres would hold the same structure.
- The agent writes memory itself through those tools. Whatever structure we choose must be expressible as rules in a system prompt that a mid-size LLM follows reliably.
- Sources are bilingual and the embedder is symmetric and multilingual; memory must not depend on the language a fact was stated in.
- Nothing is deleted. A memory that is wrong or superseded is marked, not removed, so the history stays answerable.

## Decision

**Two layers, one unit of memory, written together.**

1. **The unit of memory is a *claim*:** one statement with `date`, `source` (file plus turn or section), `speaker_or_author`, `lang`, `topic`, and a `kind` from a closed set: `decision`, `fact`, `ownership`, `open_item`, `commitment`. A claim is small enough to be one vector and one graph node.
2. **Vector layer (bge-m3):** every claim's text plus every source chunk, with the metadata above as payload. This layer answers "what was said about X" in either language.
3. **Graph layer:** typed nodes `Person`, `Meeting`, `Document`, `Decision`, `OpenItem`, `Topic`; edges `DECIDED_IN`, `OWNS {from, to}`, `SUPERSEDES`, `ABOUT`, `RAISED_IN`, `DOCUMENTED_IN`, `ATTENDED`. Keys are deterministic strings (`decision:gateway-timeout:2026-09-28`), writes are MERGE-only. This layer answers "who", "since when", "what replaced what", and "no one".
4. **Supersession, not update:** a new decision on the same topic creates a new `Decision` node and a `SUPERSEDES` edge to the previous one; the old node gets `status: superseded`. The vector entry of the old claim is kept with `status` in its payload. "Current" is a query (`WHERE NOT (d)<-[:SUPERSEDES]-()`), not a field the agent has to keep in sync.
5. **Documents are claims with a date too.** A document section is stored with its `updated` date; when a decision is newer than the document that covers the same topic, the agent is instructed to say the document is stale and cite the decision.
6. **The agent may write only claims.** The prompt forbids writing summaries, opinions or anything without a source and a date. Memory written without a source is the failure mode this structure exists to prevent.
7. **Dates are ISO strings** (`YYYY-MM-DD`) in both layers, never a database temporal type: tools between the agent and the store serialise what they understand, and a date the agent cannot read is a date it cannot reason about.
8. **The writer's output is validated before it is stored.** Keys are checked against the people register, the term glossary and the key format; unknown keys are flagged `unresolved`, never invented; a SUPERSEDES edge must point at a different node on the same topic. Failed validation is a review item, not a write.
9. **Names and terms are normalised before they become keys.** Transcripts come from ASR and mangle names and technical terms ("гейтвей", "дрy ран", "sло"). Two dictionaries are part of the memory, not of the agent's judgement: a people register (canonical name, role, spoken aliases) and a term glossary (canonical term, aliases in both languages, topic). The writer maps speakers and topics through them; anything it cannot map is written with an `unresolved` flag and the original string, never with an invented key. The dictionaries reduce the error, they do not remove it: a term that is mangled in a way nobody anticipated still lands as a new topic, which is why unresolved entries are reviewed and merged, and why the raw chunks stay in the vector layer as the fallback.

The retrieval prompt routes by question shape, as lab 4's `retrieval-agent` already does: content questions start with the vector layer, relationship, ownership and history questions with the graph, and both are used when the question mixes them. Every answer cites source and date.

## Options Considered

### Option A: Vector layer only (raw chunks plus claims as text)

| Dimension | Assessment |
|---|---|
| Complexity | Low. One store, one tool pair. |
| Quality / fit | Good for facts and for bilingual recall. Cannot express "current vs. superseded", "owner since", or absence. Puts the burden of reasoning over dates and history on the LLM every time, from whatever five chunks came back. |
| Team familiarity | High (lab 4). |

**Pros:** simplest; everything lab 4 built works as is.
**Cons:** temporal and ownership questions depend on the right three chunks all landing in the top-k; "no owner" cannot be stated with confidence; nothing structural to audit.

### Option B: Graph layer only

| Dimension | Assessment |
|---|---|
| Complexity | Medium. Schema, Cypher in prompts, extraction quality is everything. |
| Quality / fit | Precise on relationships and history. Blind to anything the extractor did not turn into a node, and extraction from noisy Russian ASR into typed nodes is the weakest step in the pipeline. No semantic "find me something like this". |
| Team familiarity | Medium. |

**Pros:** answers "who / since when / what replaced what / nobody" exactly.
**Cons:** every miss in extraction is a permanent hole; questions phrased differently from the schema fail; bilingual matching has to be done at extraction time.

### Option C: Both layers, claim as the shared unit — chosen

| Dimension | Assessment |
|---|---|
| Complexity | Medium-High. Two writes per claim, prompt rules for both, a schema to maintain. |
| Quality / fit | Vector for recall across phrasing and language, graph for structure and absence. Each covers the other's blind spot; the shared claim id lets a vector hit be expanded in the graph. |
| Team familiarity | Medium; both halves exist on the branch. |

**Pros:** the only option that answers all six question classes in the corpus by construction.
**Cons:** two stores to keep consistent; the agent's write path is longer and must be exercised in the eval, not assumed.

### Option D: xray-memory as a product

| Dimension | Assessment |
|---|---|
| Complexity | Low to run, impossible to shape: snapshots are pre-built maps with a fixed embedder (nomic, 256 dims) and an encrypted format we cannot produce. |
| Quality / fit | Built for code graphs; `remember` writes free-text notes into a session map. No typed decisions, ownership or supersession. |
| Team familiarity | Low; images are public, the map key and the build tooling are not. |

**Pros:** a working memory server with a UI, in one HelmRelease.
**Cons:** we cannot build our own corpus into it, which is the point of the lab, and it would tie memory to nomic rather than the ADR-0001 model.

## Trade-off Analysis

**Why not stop at vector.** Lab 4's numbers were good because the questions were "what does this chunk say". The memory questions are about time, people and absence, and a vector store does not know what a date or an owner is. Making the LLM reconstruct history from five chunks every time is fragile and unauditable; the first time two chunks contradict each other the answer depends on their order.

**Why not graph alone.** The extraction step from a Russian ASR transcript into typed nodes is where errors enter. Keeping the raw chunks in the vector layer means a miss in extraction is recoverable by search, and the eval can measure how much the agentic extraction lost against the scripted ground truth.

**Why claims and not summaries.** A summary has no source and no date; it is where hallucinated memory comes from. A claim is the smallest thing that can be cited, and it embeds well because it is one sentence.

**What we give up.** Simplicity, and some ingest latency: each remembered claim is two tool calls. For a team assistant that reads a transcript once a week that is nothing.

## Consequences

- **Easier:** every answer can cite a source and a date, because every memory has them.
- **Easier:** "current" and "no owner" are queries, not judgment calls.
- **Harder:** the agent's write prompt is longer and stricter; it has to be tested with an eval, which is Part C of TASK-0004.
- **Harder:** two stores can drift if a write fails halfway; the claim id in both payloads is what makes drift detectable.
- **Harder:** the people register and the term glossary are data that must be maintained. Their source of truth should be external (staff directory, calendar attendees, a project glossary); the lab keeps them as files in the corpus.
- **Revisit triggers:** (1) the eval shows the graph layer adds nothing over vector on temporal and ownership questions; (2) agentic extraction quality is so low that the graph is mostly wrong, in which case the write path needs a different model or a human-in-the-loop, not a different structure; (3) a memory product appears that supports typed claims with supersession and our embedder.

## Validation (2026-10-09, TASK-0004)

22 questions in six classes (fact, temporal, attribution, contradiction, unowned, crosslingual; 11 RU, 11 EN) over the Ledger corpus, asked three ways: an agent with only the vector tool, only the graph tools, or both. Two memories: **scripted** (70 source chunks plus the 12 ground-truth claims in the vector layer; the reference graph) and **agentic** (only what `memory-writer` extracted from the 16 sources, nothing else). Answers scored 0/1/2 by the lab owner; traces, scores and notes under `evals/memory/runs/2026-10-09/`.

| Memory | vector only | graph only | both |
|---|---|---|---|
| scripted, v1 (graph dates as Neo4j `date()`, generic prompts) | 95% | 57% | 89% |
| scripted, v2 (ISO string dates, fixed topic and person keys, Cypher recipes in the prompt) | 93% | **77%** | **91%** |
| agentic (what the writer extracted) | 50% | 39% | 50% |

By class, scripted v2 (score %, vector/graph/both): fact 100/50/100, temporal 100/100/100, attribution 88/62/88, contradiction 75/100/75, unowned 100/100/75, crosslingual 100/75/100.

What the numbers say:

1. **The claim is the decision that mattered.** The scripted vector layer answers 93–95% because every decision is in it as one dated, sourced sentence with its status and owner. The structure the ADR asks for lives in the text of the claim; a vector store finds it in either language. The graph layer alone never beats it.
2. **The graph is only as good as the keys and the Cypher.** Going from 57% to 77% took no schema change: string dates instead of `date()` (the MCP returned temporal values empty), a fixed list of topic and person keys in the prompt, and three Cypher recipes. The remaining graph misses are by design (no speaker turns, no document text) or prompt gaps (attendance mistaken for authorship, "newest on topic" mistaken for "the decision about X").
3. **The graph earns its place on two questions the vector layer cannot do:** the stale decision log (q20) was answered correctly only by comparing `doc.updated` with a newer decision in the graph, and "no owner" (q14, q15) is a query there, not an inference. Both modes together are the right default; the measured cost of the graph on content questions is nil when the prompt routes correctly.
4. **Agentic extraction is the bottleneck, not the storage.** The same agents dropped to 50% on the memory the writer built: 34 Decision nodes for 11 real decisions (precision 0.29), two decisions never extracted (the ownership transfer and the rollback owner), three key spellings per person despite an explicit format in the prompt, one SUPERSEDES edge and it was a self-loop, ten OpenItem nodes for one open item, invented labels, and one document skipped because the agent asked a question instead of writing. The failures are all on the write path. Every one of them is detectable by a diff against the register and the key format, which argues for a validation step between the writer and the stores.
5. **Staleness has to be computed.** Five of six runs answered "the decision log is current" because nothing in memory said otherwise. A memory that stores documents with dates and decisions with dates has what it needs; the prompt has to ask for the comparison.

Verdict: the decision stands with two amendments, now folded into the Decision section: dates are ISO strings everywhere, and the writer's output is validated against the people register, the term glossary and the key format before it reaches the stores. Revisit trigger (2) fired in part: agentic extraction quality is low, and the fix is a validation and merge step, not a different structure.

## Validation 2 (2026-10-10, TASK-0005)

The Ledger run above had 22 questions over 16 sources, too few to separate the modes. The Relay corpus (`corpus/relay/`) is generated from one `timeline.yaml`: 70 sources (34 RU meetings, 22 EN docs, 4 Confluence pages, 10 ADRs), 244 chunks, 30 decisions of which 7 superseded and 1 rejected, 8 open items, 13 ownership spans, 3 PoCs with numbers. 67 questions, 45 templated from the timeline and 22 hand-written, weighted towards chains, aggregates, dates and stale documents. Same three agents, same scripted memory (chunks plus 51 claims in the vector layer, reference graph in Neo4j), same 0/1/2 scale. The vector agent kept its lab-5 prompt throughout; the graph and both agents were run with four prompt versions, the last one on a corrected ground truth with all three agents. Traces, scores and notes under `evals/memory/runs/2026-10-10/relay-scripted*/`.

| Memory | vector only | graph only | both |
|---|---|---|---|
| Ledger, scripted v2 (22 q) | 93% | 77% | 91% |
| Relay, prompt v2 (lab-5 prompts with Relay keys) | 84% | 84% | 85% |
| Relay, prompt v3 (full Cypher recipes per class, string dates, routing rule) | 84% | 87% | 88% |
| Relay, prompt v4 (prefixed keys, full file paths, no clarifying questions, two vector calls for rationale) | 84% | 89% | 93% |
| Relay, prompt v5 (open-item ids, raise counts, ADR and stale-fact two-step rules, rationale from ADR Context; two ground-truth defects fixed, all three agents re-run) | 82% | 90% | **95%** |

By class, Relay prompt v5 (score %, vector / graph / both, n in brackets):

| class | vector | graph | both |
|---|---|---|---|
| current (5) / history (5) / chain (2) | 100 / 90 / 100 | 100 / 100 / 100 | 100 / 100 / 100 |
| owner now (3) / owner at date (3) / point in time (2) | 100 | 100 | 100 |
| objector (8) / PoC basis (3) | 100 | 100 | 100 |
| aggregate (8) | **56** | 100 | 94 |
| unowned at date (3) | **50** | 100 | 100 |
| stale docs at date (2) | **25** | 100 | 100 |
| dependency (2) | **25** | 50 | 75 |
| ADR status (4) | 100 | 88 | 88 |
| fact (4) / crosslingual (2) | 88 / 100 | **62 / 75** | 88 / 100 |
| contradiction (5) | 70 | 90 | 90 |
| multi-hop (4) | 62 | **38** | 75 |
| EN (35) / RU (32) | 84 / 80 | 91 / 89 | 96 / 94 |
| wrong answers (score 0) | 4 | 2 | **0** |
| tool calls / s per question | 3.0 / 4.5 | 1.6 / 5.1 | 1.9 / 4.8 |

What the numbers say:

1. **The hypothesis held where it was specific.** Vector-only scores 25–56% on aggregates, unowned items at a date, stale documents and dependencies: five to ten hits cannot enumerate, cannot filter by date, and staleness is spread over sixteen decision notes that no single query brings together. The graph answers those classes at 100% with one Cypher call. On the Ledger corpus these classes had one or two questions each and the gap was invisible.
2. **The claim still carries most of the load.** Vector-only holds 82% because ownership spans, decision status and supersession are in the claim text; "who owned X on date D", point-in-time and chain questions are 100% for vector without any graph. The graph layer is not needed for structure that fits in one sentence, only for structure that spans many claims.
3. **The combined mode was a prompt problem, not a storage problem.** With the lab-5 prompts (v2) both was one point above vector, because the agent treated an empty Cypher result as "not in memory" even when its own vector call had the answer, wrote `date()` against string dates, counted a missing OWNS edge as an owner, printed keys instead of decision text, dropped the `person:` prefix, looked documents up by short name and asked the user a question instead of answering. Each fix was a sentence in the prompt; v3 → v4 → v5 took both from 85% to 95% with zero wrong answers in 67. Nothing in the schema changed.
4. **What the graph still cannot do is by design.** The graph-only misses that remain are document content (retry delays, runbook steps, PoC-report numbers) and rationale or positions that live in meeting prose; those are vector-layer facts, and the both agent at 95% is the graph plus exactly that. The one graph zero that is not by design (m13) came from a recipe of mine that ranked closed items by raise date instead of days open; corrected after the run.
5. **Staleness is computed now.** The decision log question (m06), wrong in every run before v4, is answered by both and graph by the recipe "is document F current": compare `doc.updated` with decisions dated after it. The vector agent still says the log is current. The data was always there; the prompt had to ask for the comparison.
6. **The eval found two ground-truth defects** (PoC-3 ownership in the timeline contradicted D16; a hand-written answer listed a raise date the timeline lacked) and one generator gap (claims were built by an inline script). Both fixed before v5: the timeline has a PoC `handover` field, `gen_claims.py` exists, and the reference graph and claims were regenerated.

Verdict: the second layer earns its place on aggregate, unowned, stale-document and dependency questions (15 of 67), where vector-only scores 25–56% and the graph 100%, and the combined agent is thirteen points above vector overall with no wrong answer against four. The structure stands unchanged. Three amendments to the Decision's prompt contract, all applied in abox `releases/agent-memory.yaml` (memory-eval-graph, memory-eval-both): (a) an empty Cypher result is evidence of absence only in the graph-authoritative classes and never overrides a vector hit; (b) every templated question class has a named Cypher recipe in the prompt, including "owner at date", "unowned at date" with the CLOSES rule, "is document current", "longest-standing closed item" ranked by days open, and the two-step ADR-status and stale-fact rules; (c) keys are always prefixed, document files are full paths, open items and PoCs are addressed by id, and the agent states an assumption instead of asking the user. Revisit trigger (1) did not fire.

## Follow-ups

- [TASK-0004](../../tasks/0004-agent-memory-corpus-and-eval.md): ingest, evaluate, fill in Validation.
- [TASK-0005](../../tasks/0005-relay-corpus-scale-eval.md): Relay corpus at scale, Validation 2; prompt v5 for the memory-eval agents is in abox `feat/llmd-embeddings-lab6`.
