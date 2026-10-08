# Scoring notes, scripted memory (judge: session owner)

Scale 2/1/0 as in lab 4. Memory here is the scripted one: 70 chunks + 12 ground-truth claims in the vector layer, reference graph in Neo4j.

- q04 graph=1: value 20% found, definition paraphrased loosely, doc not cited.
- q07, q08, q09 graph=0: "not in memory". The agent searched Topic names for 'charge' / 'ledger charge'; the topics are 'retries' and 'gateway timeout'. Cypher text matching on the wrong field.
- q11 graph=1: owner right (Dasha), start date lost: the OWNS.from property is a Neo4j date() and the MCP returns it empty. Same defect behind "updated date not returned" in q03, q08, q15, q20.
- q12 graph=0 by design: the graph holds decisions, not who said what; vector found the turns.
- q13 graph=1: attendance and one decision, promises not modelled as nodes.
- q15 both=1: led with the finance dependency, got to "phase 0 has no owner" second; graph=1 found the open item but answered "not in memory" to the phase question.
- q16 graph=1: document node found but its text is not in the graph.
- q20 all=0: nobody compared the decision log's updated date (2026-09-09) with later decisions. The claim notes mention stale gateway.md and runbook, not the decision log. A real gap: staleness has to be computed, not remembered.
- q21 both=0, graph=0: Person lookup used name = 'Dasha' and alias match case-sensitively; node is 'Dasha Volkova' with alias 'dasha'. vector=2.
- q22 graph=0: not a decision, so not in the graph; the agent also answered in Spanish.
