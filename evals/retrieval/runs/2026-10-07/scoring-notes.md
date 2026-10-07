# Scoring notes (judge: session owner, reading full traces in judge-sheet.md)

Scale: 2 = correct and grounded in a retrieved chunk; 1 = partially correct (object found, reason missing or muddled); 0 = wrong or "not found".
Only the completed re-run of retrieval-eval-minilm-ml is scored; its first run lost 17/24 questions when the MCP pod was OOMKilled (3Gi) mid-run.

en06  l6=1, ml=1: both retrieved the HTTPRoute comment but reconstructed the "why" vaguely; bge-m3 quoted the full scorer list and the one-replica argument.
en11  bge=1, l6=1: found 3Gi, did not surface the OOMKilled-at-2Gi comment; ml did.
ru03  ml=1: gave image and uvx but hedged that the image for the l6 object was "not in the chunks".
ru05  ml=0: answered the external URL prefix (/llamacpp/v1/embeddings) and said the rewrite was not found; the rewrite chunk was not retrieved.
ru06  l6=0: replied "not found in the store" although it had retrieved the scorer line; bge-m3 and ml answered correctly.
ru10  bge=1: found only the CRD-stream explanation, declared the chart question not found; the other two found both chunks.
ru11  all=1: 3Gi found by all; the reason (OOMKilled at 2Gi) lives in the L6 object's comment block, so all three either missed it or attributed it elsewhere.
