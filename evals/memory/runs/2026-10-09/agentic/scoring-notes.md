# Scoring notes, agentic memory (judge: session owner)

Memory here is ONLY what memory-writer wrote from the 16 sources (89 vector points, 34 Decision nodes, 14 Person nodes); the raw source chunks were not in the vector layer for this run. That is a deviation from ADR-0003's "claims plus source chunks" and makes this run a measure of extraction alone.

Structural defects found by graph_diff.py: decision recall 9/11 (missed the ownership transfer D07 and the rollback owner D11), precision 0.29 (34 nodes for 11 decisions; duplicates per meeting and per document), 3 key spellings per person, 1 SUPERSEDES edge and it is a self-loop, 10 OpenItem nodes for 1 real open item, invented labels Fact and DPerson, topics both with and without the "topic:" prefix. docs/gateway.md was never ingested: the writer answered "input-required" instead of writing.

- q05 vector=0, q06 both=0 vector=0: answered 5 s as current. The 5 s claim from the decision log is active, the 10 s decision from 09-28 was marked superseded by its own self-loop, so the newest active decision on the topic was wrong or missing from the hits.
- q06 graph=2: reached 10 s through the 10-02 "policy in prod" decision, a lucky duplicate.
- q09 all=0: the 09-21 "retries enabled" decision exists in the graph but nobody found it; vector hits were the 08-31 claims.
- q10 all=0: D11 (Irina takes rollback) was not extracted at all; the memory honestly says TBD.
- q11 both=0, graph=0: D07 (ownership transfer) not extracted; vector=2 because the writer stored the transfer as a text claim without the graph edge.
- q12: no speaker-level "objected" claim; the writer kept decisions, not disagreements.
- q18 both=2: clean list despite the noisy graph; graph=1 listed 7 "decisions" including three 5 s duplicates.
- q19: the time (10:00) was lost in extraction; date kept.
- q20 all=0: same as scripted; staleness is not computed.
- q22 all=0: the fact lives only in docs/gateway.md, which was never ingested; "not in memory" is the honest answer, scored 0 by the rubric.
