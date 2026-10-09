# Scoring notes, Relay scripted memory (judge: session owner)

67 questions (22 manual m01–m22, 45 templated t01–t45) × 3 agents, scripted memory: 244 chunks + 51 claims in `relay-bge-m3`, reference graph from `timeline.yaml` in Neo4j. Scale as in lab 5: 2 = correct and grounded, 1 = partial or unsupported, 0 = wrong / "not in memory" / hallucinated. Scores in `answer-scores.json`, sheet in `judge-sheet.md`.

Run notes: the first vector/both run went to a port-forward on the old qdrant-mcp pod (collection `ledger-bge-m3`) and answered "not in memory" everywhere; re-ingested (295 points) and re-run. The graph agent answered t01–t08 before the async Cypher load finished; those eight were re-run and merged. The remaining tool errors are Cypher syntax errors by the agent: both 4 (t01, t15, t17, t35), graph 1 (t08), vector 0.

Totals: vector 84%, graph 84%, both 85% (49 / 49 / 50 fully correct; 4 / 3 / 3 wrong).

## Where each mode fails

Vector only
- aggregate 62%: t28 counted Anna's active decisions as 1 (ownership claims only, not decisions she owns), t30 gave 3 of Ivan's 5, t29 2 of Pavel's 3, t32 found 2 of 4 non-Accepted ADRs and said the list is incomplete. Five hits cannot enumerate.
- stale_docs 25%: t36 "not in memory", t37 three of eleven documents. Staleness is spread over 16 decision notes; no query surfaces them together.
- dependency 25%: t45 answered from ADR-002's Context instead of the DEPENDS_ON edge.
- contradiction: m04 stopped at the 30 s step and called it current (the 25 s chunk was not in the top hits); m06 said the decision log is current (same failure as lab 5 q20).
- m13 did not name who took the dry run; m18 found two of three retries decisions.

Graph only
- t03 = 0: "current decision on gateway timeout" was resolved to `topic:gateway` instead of `topic:timeouts`; the key list in the prompt has both and the agent picked the wrong one.
- chain 50%, t05/t08 = 1: the chain came out right but with no file field cited (the SUPERSEDES walk returned keys only).
- point_in_time 25%: m16 = 0 and m15 = 1, the agent did not filter OWNS by `from <= date < to`.
- m20 = 0, m01/m02/m03 = 1: runbook steps, retry delays and the networking rationale are document text, which the graph does not hold. By design.
- fact 62%, crosslingual 75%: same cause.

Both
- unowned_at 33%: t33 and t34 answered "no unowned items" because the Cypher used `NOT EXISTS { (o)<-[:OWNS]-(:Person) }` on items whose ownership is on the closing decision, and the agent trusted the empty result over the vector hits that named O1/O3/O4. t35 (as of today) was right.
- t16 = 1, m15 = 1, m22 = 2 with a "not in memory" preamble: when Cypher returns nothing the agent says "not in memory" even though its own vector call already had the answer. This is the single biggest cost of the combined mode: an empty graph result overrides a good vector hit.
- t10 and t02 = 1: listed decision keys and ADR dates instead of decision text and meeting dates.
- t11 = 1: current SLO printed with the old text (2 s / 99.5%) and the new date.
- m09 = 1: never quoted the 3.4 s cold number.

All three
- m06 = 0 everywhere: nothing in memory says the decision log is stale; it has to be computed from `doc.updated` versus later decisions, and no agent did it this time (the graph agent did in lab 5).
- m11 and m14 = 1 everywhere: the June→August retries reasoning and Timur's April position are in meeting prose, not in claims.
