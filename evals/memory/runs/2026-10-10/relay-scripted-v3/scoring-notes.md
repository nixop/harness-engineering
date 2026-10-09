# Scoring notes, Relay scripted memory, prompt v3 (judge: session owner)

Same memory and questions as `../relay-scripted/` (prompt v2). Only the graph and both agents were re-run; the vector trace is copied from the v2 run for the summary. Prompt v3 (abox `releases/agent-memory.yaml`): full Cypher recipes for every templated class (current, history, chain, in force on D, owner on D, active decisions of P, unowned on D with the CLOSES rule, stale docs on D, "is document current", proposer/objector, PoC basis, dependency, ADR status, meeting on D); explicit "never call date()"; "always RETURN text, date, status, source"; topic:timeouts named for every timeout question; PoC and ADR keys listed; for the both agent a routing rule by question type and "an empty Cypher result is not 'not in memory'".

Totals: graph 87% (v2 84%), both 88% (v2 85%).

Fixed by v3: t03 (topic:timeouts), t16 and t34 (no more date()), t33 (OPTIONAL MATCH + "ow.to IS NULL" replaced by NOT EXISTS), t10/t11 (text returned instead of keys), m22 "not in memory" preamble gone, t30 graph (person key corrected after two tries).

Still wrong after v3:
- both m06 and graph m08 ended in `input-required`: the agent asked the user which document it meant instead of answering.
- both t30 = 0: `{key:'ivan-melnik'}` without the `person:` prefix, twice, then "0 decisions".
- both and graph m04 = 0: `Document {file:'gateway.md'}` instead of the full path `docs/gateway.md`.
- both m03 and m09: graph-first routing left one generic vector_find, so the rationale text from the ADR was not quoted.
- graph m20 = 0: queried a Meeting dated 2026-10-19 (the cutover date) instead of decisions on topic:cutover.

Ground-truth defects found while scoring (not the agents' fault):
- m15: `timeline.yaml` gives PoC-3 to Ivan from 2026-06-22, but Ivan joins on 2026-07-06 and D16 (2026-07-13) says the PoC moved from Sergey to Ivan. The expected answer (Sergey until 07-13) follows D16; the graph follows the PoC record. Scored against the graph for the PoC part.
- m19: the expected answer says O7 was raised again on 2026-10-05; the timeline lists only 2026-09-28. Scored against the timeline.
