# Scoring notes, Relay scripted memory, prompt v4 (judge: session owner)

Same memory and questions as `../relay-scripted/`; graph and both re-run, vector copied from the v2 run. Prompt v4 adds to v3: keys always carry their prefix (person:, topic:, poc:, adr:); document files are full corpus paths, short names matched with ENDS WITH; a date in a question is an as-of or decision date, not a meeting date; never ask the user a clarifying question (state the assumption instead); an ADR's status is reported with what is live on its topic; for "why" / "what does it mean" / number questions the both agent makes two vector_find calls (one in English) and quotes the document or ADR text.

Totals: graph 89% (v3 87%, v2 84%), both 93% (v3 88%, v2 85%); vector unchanged at 84%. Zero answers: graph 1, both 1 (v2: 3 and 3). No `input-required` states. Tool errors: graph 1, both 2.

Fixed by v4: m04 (full path, both and graph now say the doc is stale), m06 both (answered instead of asking), m08 graph (same), t30 both (person: prefix), m20 both (runbook steps from the vector layer), m09 both (quotes the ADR and PoC report), m13 graph, m22 both ($6,100 from the PoC report).

Remaining misses:
- both m13 = 0: the query selected open items *without* a CLOSES edge, so it picked O8 instead of O1. Wrong Cypher, not a missing recipe.
- both m03, m11, m14 = 1 and graph m03, m11, m12, m14 = 1: rationale and positions that live in meeting prose (custom resources for peering, async intake double-enqueues, Timur's April stance). The both agent quotes ADR-004 in m12 and m09 now; m03 still returns the boundary, not the reason.
- both t44 = 1, graph t44 = 1: ADR-010 reported as Proposed only, without the live 25 s decision, although the new rule asks for it. graph t42 = 1: the SUPERSEDES direction between ADRs was queried backwards.
- graph m20 = 0, m01/m02 = 1: document content, by design. graph m16 = 1: owner of `topic:timeouts` is not in the graph (the timeout decisions are owned, the topic is not), so it reported the gateway owner with a caveat.
- graph t02 and t10 = 1: history queries that filtered out superseded decisions.
- m15 and m19: see the ground-truth defects in `../relay-scripted-v3/scoring-notes.md`.
