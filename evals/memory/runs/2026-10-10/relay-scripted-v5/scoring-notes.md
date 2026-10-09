# Scoring notes, Relay scripted memory, prompt v5 (judge: session owner)

Final run. All three agents re-run on a corrected memory; the earlier runs (`../relay-scripted/` v2, `-v3`, `-v4`) stay as they were for the prompt comparison.

What changed before this run:
- Ground truth: `timeline.yaml` now hands PoC-3 from Sergey to Ivan on 2026-07-13 (generator gained a `handover` field on PoCs) and O7 is raised again on 2026-09-28 and 2026-10-05 (the 10-05 meeting says so). Reference graph regenerated and reloaded (138 nodes); the 51 claims rebuilt with the new `evals/memory/gen/gen_claims.py` and re-upserted; the 244 chunks unchanged. Qdrant: 295 points.
- Prompt v5 (graph and both): open items listed by id with their short names ("the dry run" is O1); raise count = 1 + raised_again; a recipe for the longest-standing closed item; history never filters by status; ADR status is two queries (status, then what replaced it, and for Proposed/Rejected the live decision on its topic); "is this fact in document X still true" ends with the value in force; "what must happen before <date>" joins decisions on the event's topic and its dependencies with unowned items and runbook steps; the both agent quotes the ADR Context for rationale and the meeting of the date for a person's position.
- Infrastructure: a Flux reconcile from the upstream OCI artifact had reset kagent (model gpt-4.1-mini, secret overwritten with a literal), qdrant-mcp (collection abox-nomic) and the embedding server (nomic, 768 dims). Fixed by suspending the `releases` Kustomization and re-applying the branch manifests; the first v5 attempt (all answers `failed`, then "Vector dimension error") was discarded. A re-upsert of the claims before that was discovered had duplicated them (346 points); the duplicates were deleted by payload filter before the final run.

Totals: vector 82%, graph 90%, both 95%. Wrong answers (0): vector 4, graph 2, both 0. Tool errors: vector 0, graph 1, both 1. No `input-required`.

Remaining misses:
- both m03, m11, m14 = 1: rationale and positions that live in meeting prose. m11 now quotes the August meeting ("очередь ретраит лучше гейтвея") but not the double-enqueue reason; m03 returns the boundary and the SSM hand-off, not the custom-resources argument from ADR-004's Context (the agent did not run the "<ADR id> Context" query). m14 names Timur and Pavel but muddles Timur's April stance.
- both m04 and t44 = 1: the "value in force now" and "live decision for a Proposed ADR" steps were not executed although the prompt asks for them.
- both m18 = 1: the OWNS-on-decision query returned only D21's owner; m20 = 1: runbook steps plus Lena, without the DB-cutover date and the load test.
- graph m13 = 0: my recipe ranked closed items by raise date, which picks O8 (open 7 days) instead of O1 (open 98 days). Fixed in the prompt after the run (v5.1, ranks by days open; not re-run). The both agent got O1 right because its second query joined CLOSES.
- graph m20 = 0, m01/m02/m09 = 1: document and PoC-report content, by design.
- vector t28 = 0, t29/t30 = 1, t33–t35 = 1, t36 = 0, t37 = 1, t27 = 1: enumeration and date filtering over many claims; t45 = 0: no DEPENDS_ON in text; m06 = 0: staleness not computed.
