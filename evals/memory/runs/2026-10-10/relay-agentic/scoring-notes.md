# Scoring notes, Relay agentic memory with validation (judge: session owner)

TASK-0005 step 7. Memory here is what `memory-extractor` proposed from the 70 sources, after `agentic_build.py` validated and merged it, plus the same 244 raw chunks as the scripted runs. Prompts v5.2 for graph and both (v5.1 minus the list of ground-truth open-item ids), vector unchanged. Files: `extract.jsonl` (70 JSON proposals), `validation-report.md`, `diff.md` (against the ground truth), `memory/` (decisions, open items, graph, claims as built), traces, `answer-scores.json`, `judge-sheet.md`.

Pipeline: the extractor has no tools and returns one JSON object per source (decisions with proposer, objector, owner, replaces, adr, poc, closes, stale; ownership events; open-item events raised / raised_again / taken / closed; ADR, document and PoC blocks). The builder maps people and topics to the registers, forces decision dates onto the meeting date, merges duplicates within 5 days, resolves "replaces" to the latest earlier decision on the topic, attaches ADR links by topic and date, drops open-item follow-ups that have no prior raise, derives ownership spans from hand-over events and emits the graph in the reference schema. Only meetings produce decisions; ADRs and documents produce ADR, document and PoC nodes.

What the writer produced (`diff.md`): decisions 58 for 30 real, 27 matched (recall 0.90, precision 0.47); owner, proposer and objector right on 23 of 27; SUPERSEDES edges 11, 2 correct; ADR links 8 of 8; open items 40 for 8 (7 matched); ownership spans 19 for 13, 7 exact. Register issues: 1. No `input-required`, no unparseable JSON, 70 sources in 5 minutes.

Totals: vector 66%, graph 55%, both 66% (scripted v5 on the same questions: 82 / 90 / 95; lab-5 agentic without validation on Ledger: 50 / 39 / 50). Wrong answers: 11 / 14 / 12.

Where the agentic memory fails, by cause:
- Over-extraction of decisions. Progress reports become decisions ("The state has been cleaned up" is the current IaC decision for graph and both, t01 = 0; "Retry ownership ... transferred" is the current retries decision, t06 = 0). Histories carry two to three noise entries per topic (t02, t04, t07, t10, t12 = 1). Aggregates over-count (t28–t31 = 1: 5, 6, 8, 7 owned decisions for 2, 3, 5, 3).
- Over-extraction of open items. Every commitment in a meeting became a raised item (40 for 8), so "unowned on D" returns ten to twenty items (t33–t35 = 0 for graph and both, m19 = 0 for all).
- Wrong proposer. The meeting chair who says "фиксируем" is recorded as the proposer (Marat on t20, t22, t24); objectors are right.
- Supersession. The extractor's "replaces" gists matched the wrong earlier decision (t05 = 0: a 60 s delivery timeout from January is the "earlier" decision; chain 25%).
- Staleness never arrives. The extractor's `stale` notes name documents loosely ("document db", "ADR-004"), so almost no MAKES_STALE edge was built: stale docs 0–25%, m06 graph says the log is current.
- Ownership spans. The PoC-2 lead (Timur) and the chair (Marat) were recorded as topic owners of compute, so "who owned compute on 06-28" is wrong in all modes (t16 = 0); Ivan's span starts on 08-03 instead of 07-13 (t15 = 1).
- Missing rejected alternative (D18) and the dry-run decision D19 (recorded as an open-item "taken" instead): m17 = 1, m13 = 0.

What the validation step did fix, compared with lab 5: one key per person (11 Person nodes, no duplicates, no invented labels), every decision on one of the 12 topics with an ISO date and a source, ADR links complete, no self-loop SUPERSEDES, PoC numbers attached (t38–t40 = 2 in every mode), the document layer intact (fact 100% for vector and both). The remaining errors are semantic (what counts as a decision, who proposed it, which item is being re-raised) and a register cannot catch them.

Vector on agentic claims + raw chunks: 66% against 82% on scripted claims; the raw chunks carry the facts (m01–m03, m09, m10, t38–t44 all 2) and the agentic claims mislead on current state (t11 = 0: "SLO unchanged", m21 = 0, m04 = 0).
