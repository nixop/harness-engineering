## Labels: {'DPerson': 1, 'Decision': 34, 'Document': 15, 'Fact': 27, 'Meeting': 14, 'OpenItem': 10, 'Person': 14, 'Topic': 17} | foreign: ['DPerson', 'Fact']
## Person nodes: 14 for 5 people; distinct after slugging: 5; duplicates per person: {'dasha-volkova': 3, 'irina-belova': 3, 'marat-yusupov': 3, 'oleg-prikhodko': 3, 'tim-horvat': 2}; unresolved flagged: 0
## Decisions: 34 nodes vs 11 in truth; matched truth decisions (topic+date): 9/11 recall=0.82; precision (nodes that match a truth decision)=0.29
   OK  D01 gateway-timeout@2026-08-24: Gateway upstream timeout 5 s on all Ledger routes
   OK  D02 slo@2026-08-24: POST /charge p95 latency SLO 200 ms over 5 minutes; availability 99.9%
   OK  D03 retries@2026-08-31: No retries on /ledger/charge until idempotency is in place; up to 2 re
   OK  D04 tariffs@2026-09-07: Tariff v2 keeps a mandatory legacy_code field; finance-export writes l
   OK  D05 idempotency@2026-09-07: Idempotency-Key header mandatory on /charge from 2026-09-15, 24 h key 
   OK  D06 gateway-timeout@2026-09-14: Gateway timeout raised to 15 s temporarily after the staging incident;
   MISS D07 ownership@2026-09-21: Retry policy ownership moves from Oleg to Dasha
   OK  D08 retries@2026-09-21: Retries enabled on /ledger/charge: max 2 retries, retry budget 20%
   OK  D09 gateway-timeout@2026-09-28: Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 
   OK  D10 cutover@2026-09-28: Gateway cutover on 2026-10-09 at 10:00, within the planned-work error 
   MISS D11 cutover@2026-10-02: Rollback owner for the cutover is Irina
## SUPERSEDES: 1 edges (expected 3), self-loops: 1; statuses: {'active': 33, 'superseded': 1}
    decision:gateway-timeout:2026-09-28 -> decision:gateway-timeout:2026-09-28
## OWNS edges: 47; with from date: 47; with to date: 0
## OpenItem nodes: 10 (expected 1):
    openitem:cutover:2026-10-09 | Rollback owner: TBD.
    openitem:gateway-timeout:2026-09-14 | временно но с датой пересмотра
    openitem:gateway-timeout:2026-09-21 | Таймаут: 15 секунд; пересмотр на следующей неделе.
    openitem:retries:2026-08-24 | ретраи на гейтвее пока не включать; charge не идемпотентный
    openitem:tariffs:2026-08-31 | dry run миграции тарифов на копии прода до бэкфила без владельца
    openitem:tariffs:2026-09-07 | дрy ран миграции тарифов кто нибудь взял?
    openitem:tariffs:2026-09-09 | tariff migration dry run on a copy of production data — no owner yet.
    openitem:tariffs:2026-09-21 | Драй ран миграции?
    openitem:tariffs:2026-09-28 | Бэкфил готов, dual write можно включать, но dry run не сделан.
    openitem:tariffs:2026-10-02 | Dry run миграции на копии прода
## Topics: ['charge', 'cutover', 'deployment', 'finance-export', 'gateway', 'gateway-timeout', 'idempotency', 'invoice', 'retries', 'slo', 'tariffs', 'topic:charge', 'topic:gateway-timeout', 'topic:idempotency', 'topic:retries', 'topic:slo', 'topic:tariffs']
