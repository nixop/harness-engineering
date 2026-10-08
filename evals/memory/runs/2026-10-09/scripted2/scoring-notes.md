# Scoring notes, scripted memory v2 (judge: session owner)

Same memory as scripted v1 except: graph dates stored as ISO strings (the neo4j MCP returned Neo4j date() values empty), and the graph/both prompts carry the fixed topic keys, person keys and Cypher recipes for "current", "owner now" and "no owner".

- graph 57% -> 77%. All three "charge"/"retries" misses from v1 (q07-q09) are fixed: the agent now goes to topic:retries directly. Dasha lookup (q21) fixed by the person key. Ownership date (q11) now returned.
- q03, q04, q16 graph=1: documents' text is not in the graph, so rationale and definitions come out thin; expected by design.
- q12, q22 graph=0 by design (no speaker turns, no non-decision facts in the graph).
- q13 graph=1: found Tim via role, then listed every decision from meetings he attended as "his promises". Attendance is not authorship; the prompt needs that rule.
- q19 graph=0: picked the newest cutover-topic decision (rollback owner, 10-02) as the cutover date. "Newest on topic" is not "the decision about the date"; topic granularity is too coarse for this.
- q20 graph=2: the only run of the six that got the stale decision log right, by comparing doc.updated with a newer decision. both=0 and vector=0 again said "актуален".
- q15 both=1: still leads with the finance dependency before "no owner".
- q21 vector=1: two of three decisions.
