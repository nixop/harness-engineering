
## m01 [en / fact] What is the delivery latency SLO and what exactly does it measure?
**expected:** p95 2 s over 5 minutes, from POST /deliver accepted to the first delivery attempt sent, not to the customer's answer; success rate 99.5% monthly  
**expected sources:** {'sources': ['docs/slo.md', 'meetings/2026-01-26-weekly-sync.txt']}

### memory-eval-both (completed, 5.1s, 3 tool calls)
queries: ['delivery latency SLO what it measures latency delivery SLO measure', 'SLO latency delivery what exactly measures end to end relay webhook', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

Assumption: by “delivery latency SLO” you mean the current Relay SLO on delivery latency.

The current decision says the delivery latency SLO is:

- **p95 = 3 s for 30 days after the serverless cutover, then back to 2 s**  
  Source: `meetings/2026-10-05-cutover-planning.txt`, date `2026-10-05`, status `active`

What it measures is:

- **from `POST /deliver` accepted to the first delivery attempt sent**
- It **measures Relay, not the customer**
- It **ends when the first attempt is sent, not when the customer answers**

Source: `docs/slo.md`, updated `2026-01-28`

So in short: the SLO measures **Relay’s time to start delivery**, not end-to-end customer response time.

### memory-eval-graph (completed, 5.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

The delivery latency SLO is:

- **Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s**  
  - **Date:** 2026-10-05  
  - **Status:** active  
  - **Source:** `meetings/2026-10-05-cutover-planning.txt`  
  - **Note:** `docs/slo.md` (updated 2026-01-28) still says p95 2 s with no stabilisation window

What it measures:
- It measures **delivery latency at p95** — i.e. the 95th percentile delivery time.
- The decision text does not define any different metric beyond that, so the live definition in memory is just **delivery p95 latency** with the post-cutover temporary threshold change above.

Source: `meetings/2026-10-05-cutover-planning.txt` (2026-10-05).

### memory-eval-vector (completed, 2.7s, 1 tool calls)
queries: ['What is the delivery latency SLO and what exactly does it measure?']

The delivery latency SLO is:

- **p95 = 2 seconds**
- measured over a **5-minute window**

What it measures:
- **from `POST /deliver` being accepted**
- to **the first delivery attempt being sent**

So it measures **Relay’s internal delivery dispatch latency**, **not** customer response time or end-to-end completion. The SLO page says it “ends when the first attempt is sent, not when the customer answers.”

**Sources**
- `docs/slo.md` — updated **2026-01-28**
- Decision `slo` from `meetings/2026-01-26-weekly-sync.txt` — **2026-01-26**, but it is **superseded** by the later `docs/slo.md` decision



## m02 [ru / fact] Сколько попыток доставки делает очередь до dead-letter и с какими задержками?
**expected:** 5 попыток, экспоненциально: 30 с, 2 мин, 10 мин, 30 мин, 2 ч; потом DLQ и алерт  
**expected sources:** {'sources': ['docs/retries-dlq.md', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.4s, 2 tool calls)
queries: ['очередь до dead-letter сколько попыток доставки задержки retry budget DLQ', 'dead-letter queue attempts delays retries DLQ Relay']

Очередь делает **5 попыток** доставки, после чего сообщение уходит в **dead-letter queue**.  
Задержки между попытками указаны как **30 s, 2 min, 10 min, 30 min, 2 h**.

Источник:
- `adr/ADR-009.md`, обновлено `2026-08-26`: «Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts…»
- `docs/retries-dlq.md`, обновлено `2026-08-27`: «SQS redrives with exponential backoff: 30 s, 2 min, 10 min, 30 min, 2 h.»

Если нужно, могу ещё сказать, включают ли эти 5 попыток первую отправку или только ретраи.

### memory-eval-graph (completed, 3.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.text CONTAIN"]

Очередь делает **5 попыток доставки до dead-letter**; про задержки между попытками в памяти **нет данных**.

Источник:
- `meetings/2026-08-24-weekly-sync.txt` — решение от `2026-08-24`: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”.

Если хотите, я могу ещё проверить, есть ли в памяти отдельное решение именно про **backoff/задержки** retries.

### memory-eval-vector (completed, 3.8s, 3 tool calls)
queries: ['Сколько попыток доставки делает очередь до dead-letter и с какими задержками?', 'сколько попыток доставки делает очередь до dead-letter и с какими задержками', 'доставки до dead-letter попытки задержки очередь']

Очередь делает **5 попыток доставки**, после чего сообщение попадает в **dead-letter queue**.

Задержки между ретраями:
- **30 s**
- **2 min**
- **10 min**
- **30 min**
- **2 h**

Источник:
- `docs/retries-dlq.md`, updated **2026-08-27** — “SQS redrives with exponential backoff: 30 s, 2 min, 10 min, 30 min, 2 h. After 5 attempts the message goes to relay-deliveries-dlq.”
- `adr/ADR-009.md`, updated **2026-08-26** — “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts.”

## m03 [en / fact] Why does the hybrid IaC layout keep networking in Terraform?
**expected:** cross-account peering and DNS delegation need custom resources in CloudFormation but are native in the Terraform the network team already maintains; moving network was 30% of the effort  
**expected sources:** {'sources': ['adr/ADR-004.md', 'meetings/2026-04-20-weekly-sync.txt', 'docs/iac-hybrid.md']}

### memory-eval-both (completed, 4.9s, 3 tool calls)
queries: ['Why does the hybrid IaC layout keep networking in Terraform? networking Terrafor', 'гибридный IaC почему сеть оставили в Terraform rationale networking Terraform', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERSE"]

The hybrid IaC layout keeps networking in Terraform because that boundary was decided in ADR-004 and recorded as the live decision on IaC: “networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation.” Source: `meetings/2026-04-20-weekly-sync.txt`, dated `2026-04-20`.

The memory also captures the rationale as an implementation boundary: Terraform exports network outputs such as VPC ID, private subnets, and VPC link ID to SSM Parameter Store, and CloudFormation consumes them with dynamic references. Changing a network output therefore requires a Terraform apply followed by a CloudFormation deploy, with no automatic trigger. Source: `docs/iac-hybrid.md`, updated `2026-04-24`.

Assumption: by “why” you meant the practical reason behind the boundary, not the historical decision status.

### memory-eval-graph (completed, 4.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.text CONTAINS 'n"]

The hybrid IaC layout keeps networking in Terraform because that is the active decision on the IaC topic:

- “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation” — date 2026-04-20, status active, source `meetings/2026-04-20-weekly-sync.txt`.
- That decision supersedes the earlier 2026-02-09 decision that had all components, including network, in CloudFormation.
- The decision’s note says `docs/iac-cloudformation.md` was still saying all infrastructure, including networking, moves to CloudFormation, which is why the hybrid layout was needed.

Source: `meetings/2026-04-20-weekly-sync.txt`, 2026-04-20.

### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['Why does the hybrid IaC layout keep networking in Terraform?', 'hybrid IaC layout networking Terraform', 'keep networking in Terraform hybrid IaC']

The memory says networking stays in Terraform because ADR-004 fixed the boundary that way: VPC, peering, and DNS remain in Terraform, while application stacks move to CloudFormation. The retrieved chunks do not give a deeper “why” beyond that decision. Sources: `adr/ADR-004.md` (2026-04-22) and `meetings/2026-04-20-weekly-sync.txt` (2026-04-20).

What I retrieved:
- `adr/ADR-004.md` (2026-04-22): “Hybrid: networking stays in Terraform, application stacks in CloudFormation” and “The boundary is fixed: VPC, peering and DNS in Terraform; data, compute and gateway stacks in CloudFormation.”
- `meetings/2026-04-20-weekly-sync.txt` (2026-04-20): “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation.”

If you want, I can also check whether memory contains the rationale that led to ADR-004.

## m04 [ru / contradiction] В gateway.md написано, что таймаут интеграции 10 секунд. Это актуально?
**expected:** нет; документ от 2026-03-18, таймаут менялся на 30 с (2026-05-18) и на 25 с (2026-08-24); текущее значение 25 с  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.8s, 1 tool calls)
queries: ["MATCH (doc:Document) WHERE doc.file ENDS WITH 'gateway.md' OPTIONAL MATCH (dec:D"]

Нет, не актуально.

`docs/gateway.md` был обновлён `2026-03-18`, а позже его изменили решения:
- `D12` от `2026-05-18`: `"Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14"` — `superseded`, источник `meetings/2026-05-18-weekly-sync.txt`
- `D21` от `2026-08-24`: `"Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off"` — `active`, источник `meetings/2026-08-24-weekly-sync.txt`

Значит, утверждение про `10 секунд` в `gateway.md` устарело.

### memory-eval-graph (completed, 5.8s, 1 tool calls)
queries: ["MATCH (doc:Document) WHERE doc.file ENDS WITH 'gateway.md' OR doc.title CONTAINS"]

Нет. `docs/gateway.md` сейчас устарел по этому факту: документ обновлён **2026-03-18** (`docs/gateway.md`), а позже есть решения, которые меняли интеграционный таймаут:

- **D12**: “Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14” — **2026-05-18**, `meetings/2026-05-18-weekly-sync.txt`
- **D21**: `2026-08-24` позже менял связанные правила для gateway, но именно про таймаут в документе показывает, что фраза про **10 s** уже не актуальна

Итог: по памяти графа таймаут интеграции **не 10 секунд**; документ `docs/gateway.md` это не отражает.

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['В gateway.md написано, что таймаут интеграции 10 секунд. Это актуально?', 'gateway.md integration timeout 10 seconds актуально', 'таймаут интеграции 10 секунд gateway.md']

Нет, **не актуально**.

- В `meetings/2026-05-18-weekly-sync.txt` от **2026-05-18** есть решение, что gateway integration timeout **повышен с 10 s до 30 s** после инцидента 2026-05-14. Это решение помечено как **superseded**, и там же указано, что `docs/gateway.md` от **2026-03-18** уже устарел по этому месту.
- В `docs/gateway.md` от **2026-03-18** действительно написано **10 seconds**, но этот документ старее решения от 2026-05-18, поэтому он stale.

Источники:
- `docs/gateway.md`, **2026-03-18**
- `meetings/2026-05-18-weekly-sync.txt`, **2026-05-18**

## m05 [en / contradiction] The team roster page says Anna owns retries. Is that right today?
**expected:** no; roster updated 2026-07-08, retries moved from Anna to Ivan on 2026-09-07  
**expected sources:** {'sources': ['confluence/team-roster.xhtml', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 5.3s, 2 tool calls)
queries: ["MATCH (p:Person {key:'person:anna-sokolova'})-[o:OWNS]->(t:Topic {key:'topic:ret", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.from <= '2026"]

No — Anna owned retries only from 2026-06-01 to 2026-09-07, so she does not own it today.

Today’s owner is Ivan Melnik, whose OWNS edge starts 2026-09-07 and has no end date.

Source: graph memory (OWNS edges on topic:retries).

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.to IS NULL RE"]

No — today the owner of retries is Ivan Melnik, not Anna. Source: ownership edge on topic:retries, with from 2026-09-07 and no to date, so the current owner is Ivan Melnik.

### memory-eval-vector (completed, 2.9s, 3 tool calls)
queries: ['The team roster page says Anna owns retries. Is that right today?', 'Anna owns retries', 'retries owner Anna']

No — the roster page is stale.

Current owner of retries is Ivan Melnik, from 2026-09-07. The roster page was updated 2026-07-08 and still lists Anna Sokolova as retries owner.

Sources:
- `meetings/2026-09-07-security-review.txt` (2026-09-07): retries ownership moves from Anna to Ivan; current owner Ivan Melnik.
- `confluence/team-roster.xhtml` (updated 2026-07-08): still lists Anna Sokolova as retries owner.

## m06 [ru / contradiction] Decision log в Confluence актуален?
**expected:** нет; последняя версия 2026-06-03, в нём нет решений после 1 июня: ретраи на gateway (06-15), два PoC (06-15), передача PoC Ване (07-13), выбор Lambda (08-03), таймаут 25 с и ретраи через SQS (08-24), SSM (09-07), бюджет (09-21), даты катовера (10-05)  
**expected sources:** {'sources': ['confluence/decision-log.xhtml', 'memory/decisions.jsonl']}

### memory-eval-both (completed, 3.4s, 2 tool calls)
queries: ["MATCH (doc:Document) WHERE doc.file CONTAINS 'decision-log' OR doc.title CONTAIN", "MATCH (doc:Document {file:'confluence/decision-log.xhtml'}) OPTIONAL MATCH (dec:"]

Нет — **decision log в Confluence уже не актуален**.

- **Файл:** `confluence/decision-log.xhtml`
- **Обновлён:** `2026-06-03`

После этой даты в памяти есть решения от `2026-06-15`, `2026-07-13`, `2026-08-03`, `2026-08-10`, `2026-08-24`, `2026-09-07`, `2026-09-21`, `2026-10-05`, значит документ устарел и пропускает эти изменения.

Если нужно, могу перечислить, **какие именно решения он уже не отражает**.

### memory-eval-graph (completed, 6.6s, 3 tool calls)
queries: ["MATCH (doc:Document) WHERE doc.file CONTAINS 'decision-log' OR doc.title CONTAIN", "MATCH (doc:Document {file:'confluence/decision-log.xhtml'}) OPTIONAL MATCH (dec:", "MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document {file:'confluence/decision-l"]

Нет, не актуален.

Сводка по `confluence/decision-log.xhtml`: файл обновлён `2026-06-03` (`confluence/decision-log.xhtml`, `2026-06-03`). После этой даты в памяти есть решения, которые меняют зафиксированные там факты; документ помечен как устаревший через изменение факта `stops at 2026-06-01` решением от `2026-06-15` (`meetings/2026-06-15-weekly-sync.txt`, `2026-06-15`), а также есть ещё ряд более поздних решений от `2026-06-15` до `2026-10-05`, например про retries, compute, timeout, security, budget и cutover (`meetings/2026-06-15-weekly-sync.txt`, `meetings/2026-07-13-weekly-sync.txt`, `meetings/2026-08-03-architecture-committee.txt`, `meetings/2026-08-10-weekly-sync.txt`, `meetings/2026-08-24-weekly-sync.txt`, `meetings/2026-09-07-security-review.txt`, `meetings/2026-09-21-weekly-sync.txt`, `meetings/2026-10-05-cutover-planning.txt`).

Если хотите, могу коротко перечислить, какие именно решения делают decision log устаревшим по темам.

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['Decision log в Confluence актуален?', 'Decision log Confluence current status updated decision log', 'Decision log Confluence stale updated date decision']

Да, в памяти есть актуальный Confluence decision log: страница **`confluence/decision-log.xhtml`** обновлена **2026-06-03** и помечена как источник решений из weekly sync; в ней прямо указано, что если страница расходится с записью встречи, то приоритет у записи встречи. Источник: **`confluence/decision-log.xhtml`**, дата **2026-06-03**.

Но есть нюанс: я не нашёл в памяти отдельного более нового решения, которое бы делало сам decision log неактуальным. Поэтому по памяти он выглядит **актуальным**. Источник: **`confluence/decision-log.xhtml`**, дата **2026-06-03**.

Что я retrieved:
- **`confluence/decision-log.xhtml`** — updated **2026-06-03**
- **`docs/onboarding.md`** — updated **2026-03-10**, там сказано, что решения записываются в Confluence decision log

Если хотите, я могу ещё проверить, не есть ли у этого decision log более свежая версия или конфликтующая запись.

## m07 [en / contradiction] ADR-010 says the gateway timeout for Lambda should be 20 s. Is that the policy?
**expected:** no; ADR-010 is Proposed and was never accepted; the live decision of 2026-08-24 is 25 s  
**expected sources:** {'sources': ['adr/ADR-010.md', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 4.1s, 4 tool calls)
queries: ['ADR-010 Context gateway timeout Lambda 20 s policy', 'ADR-010 gateway timeout Lambda 20 seconds', "MATCH (a:ADR {id:'adr-010'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:'adr-010'}) RETURN n.id, n.title"]

Assuming you mean whether ADR-010 is the live policy.

No — ADR-010 is **Proposed**, not accepted, so it is **not** the policy in force.

Evidence:
- `adr/ADR-010.md` updated `2026-09-23`: “**Proposed, not accepted. The live value was set by the team on 2026-08-24 at 25 s; this document still says 20 s.**”
- `adr/ADR-010.md` updated `2026-09-23`: “**No decision recorded; see Status.**”

So the 20 s value is what ADR-010 proposes, but the live decision is **25 s** as of `2026-08-24`.

### memory-eval-graph (completed, 5.0s, 3 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:'ADR-010'}) RETURN n.id, n.title", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20"]

ADR-010 is **Proposed**, not policy. The live policy on the timeout topic is: **“Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom”** — decision dated **2026-08-24**, source **meetings/2026-08-24-weekly-sync.txt**.  
ADR-010: **“Gateway timeout policy for Lambda integrations”**, dated **2026-09-23**, file **adr/ADR-010.md**.

So, **no**: the current policy in memory is **25 s**, not 20 s.

### memory-eval-vector (completed, 3.5s, 3 tool calls)
queries: ['ADR-010 says the gateway timeout for Lambda should be 20 s. Is that the policy?', 'What is the current policy for gateway timeout for Lambda?', 'gateway timeout Lambda 20 s policy ADR-010']

No — ADR-010 is **not** the current policy in memory.

What I found:
- **ADR-010** (`adr/ADR-010.md`, updated **2026-09-23**) is **Proposed** and says **“No decision recorded; see Status.”** It also lists **“20 s on every route, with per-route overrides”** as an option considered, not an accepted policy.
- The same ADR’s consequences section says it is **“Proposed, not accepted”** and that the **live value was set by the team on 2026-08-24 at 25 s**; it explicitly notes **“D20 (25 s) is the live decision and the ADR still proposes 20 s.”**

So the memory says:
- **20 s** = ADR proposal, not accepted
- **25 s** = live/current decision as of **2026-08-24**

If you want, I can also look for the decision record that established the 25 s policy.

## m08 [ru / contradiction] В runbook катовера написано, что владелец отката TBD. Кто на самом деле?
**expected:** Лена, решение 2026-10-05; runbook от 2026-09-29 устарел  
**expected sources:** {'sources': ['docs/runbook-cutover-serverless.md', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 3.3s, 1 tool calls)
queries: ['rollback runbook owner TBD who actually owns rollback cutover serverless cutover']

По факту владелец отката — **Лена Ким**.

Источник: `meetings/2026-10-05-cutover-planning.txt`, дата `2026-10-05`  
Там зафиксировано: **“Rollback owner for both cutovers is Lena. Owner: Lena Kim.”**

Примечание: в `docs/runbook-cutover-serverless.md` по состоянию на `2026-09-29` всё ещё написано `TBD`, но это устаревшее состояние.

### memory-eval-graph (completed, 6.0s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.text CONTAIN", "MATCH (o:OpenItem {id:'O2'}) RETURN o.id, o.text, o.raised, o.raised_again, o.st", "MATCH (p:Person)-[w:OWNS]->(o:OpenItem {id:'O2'}) RETURN p.name, w.from, w.to"]

Похоже, в runbook речь про O2 «Rollback runbook for the serverless cutover»; по памяти графа его сейчас ведёт **Lena Kim**.

- O2: **“Rollback runbook for the serverless cutover”**, raised **2026-08-24**, status **closed** — source в памяти: **O2**.
- Текущий владелец O2: **Lena Kim**, OWNS from **2026-09-21**, to **null** — source в памяти: **OWNS**.

Если хотите, могу ещё проверить, не было ли у этого item'а прежнего владельца до Lena Kim.

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['В runbook катовера написано, что владелец отката TBD. Кто на самом деле?', 'runbook катовера владелец отката TBD кто на самом деле', 'катовер откат владелец TBD']

На самом деле владелец отката — **Lena Kim**.

Источник:
- `meetings/2026-10-05-cutover-planning.txt` — **2026-10-05**: “Rollback owner for both cutovers is Lena. Owner: Lena Kim.”
- Там же указано, что `docs/runbook-cutover-serverless.md` от **2026-09-29** всё ещё писал `TBD`, то есть runbook устарел.

Дополнительно:
- `meetings/2026-10-05-cutover-planning.txt` — **2026-10-05**: “лена: откат беру я на оба катовера”.



## m09 [ru / crosslingual] Что на митингах называли «провижнд конкаренси» и почему без этого не проходит SLO?
**expected:** provisioned concurrency: прогретые инстансы Lambda на /deliver; без них p95 3.4 с при SLO 2 с, с ними 1.9 с (PoC-3)  
**expected sources:** {'sources': ['docs/poc-lambda-report.md', 'meetings/2026-07-27-poc-review.txt', 'adr/ADR-006.md']}

### memory-eval-both (completed, 6.2s, 3 tool calls)
queries: ['«провижнд конкаренси» SLO why needed meeting', 'provisioned concurrency SLO meeting explanation why needed', "MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'Run Relay on L"]

На митингах «провижнд конкаренси» называли обязательным условием для `/deliver` на Lambda: «без него не проходим» и «без него SLO missed».  

Почему:
- В обсуждении PoC говорили, что SLO 2 секунды относится к первой попытке доставки, и без provisioned concurrency его не укладывают.
- В ADR это сформулировано как условие, а не оптимизация: «Provisioned concurrency on /deliver is a condition, not an optimisation: without it the SLO is missed».

Источники:
- `meetings/2026-07-27-poc-review.txt` — 2026-07-27: «ваня: поэтому провижнд конкаренси на deliver обязательно без него не проходим»
- `meetings/2026-07-27-poc-review.txt` — 2026-07-27: «анна: sло две секунды это про первую попытку доставки а не про ответ клиента одна и девять проходит»
- `adr/ADR-006.md` — 2026-08-05: «Provisioned concurrency on /deliver is a condition, not an optimisation: without it the SLO is missed.»

Если нужно, могу ещё кратко объяснить, чем это было связано с p95 и асинхронным runtime, тоже по записям из памяти.

### memory-eval-graph (completed, 9.4s, 5 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE d.text CONTAINS 'p", "MATCH (m:Meeting)<-[:DECIDED_IN]-(d:Decision) WHERE m.file CONTAINS 'meeting' AN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) RETURN d.text, d.date, d", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) RETURN d.text, d.dat"]

На митинге под «провижнд конкаренси» имели в виду решение для compute: **Relay moves to Lambda with provisioned concurrency on /deliver**. Это зафиксировано как active decision от **2026-08-03** в файле **meetings/2026-08-03-architecture-committee.txt**; в той же записи сказано, что **PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances**. Источник: **meetings/2026-08-03-architecture-committee.txt**, дата **2026-08-03**.

Почему без этого не проходит SLO: в памяти есть действующее SLO-решение от **2026-10-05** в **meetings/2026-10-05-cutover-planning.txt**: **Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s**. То есть целевой SLO для доставки — **2 s p95** в нормальном режиме, и именно решение с provisioned concurrency связано с тем, чтобы на Lambda держать warm instances и уложиться в этот latency. Источник: **meetings/2026-10-05-cutover-planning.txt**, дата **2026-10-05**.

Если совсем коротко:  
- **что это** — provisioned concurrency для Lambda на `/deliver`;  
- **зачем** — чтобы держать **warm instances** и пройти latency-SLO по p95.  
Источники: **meetings/2026-08-03-architecture-committee.txt** (2026-08-03)

### memory-eval-vector (completed, 6.0s, 3 tool calls)
queries: ['Что на митингах называли «провижнд конкаренси» и почему без этого не проходит SL', 'провижнд конкаренси SLO митинг', 'provisioned concurrency SLO meeting']

На митингах под «провижнд конкаренси» имели в виду **Lambda provisioned concurrency на `/deliver`** — то есть заранее прогретые инстансы для обработчика доставки.

Почему без этого не проходит SLO:
- На PoC-review 2026-07-27 Ваня сказал: **«провижнд конкаренси на deliver обязательно, без него не проходим»**; там же Анна уточнила, что SLO — это **2 секунды до первой попытки доставки**, а не время ответа клиента. Источник: `meetings/2026-07-27-poc-review.txt` (2026-07-27).
- В отчёте PoC-3 за 2026-07-24 прямо сказано: **«Within the 2 s SLO only with provisioned concurrency; without it the SLO is missed.»** Источник: `docs/poc-lambda-report.md` (2026-07-24).
- В ADR-006 от 2026-08-05 это уже закрепили как решение: **provisioned concurrency on /deliver is a condition, not an optimisation: without it the SLO is missed**. Источник: `adr/ADR-006.md` (2026-08-05).

Если коротко: **без provisioned concurrency холодный старт Lambda делает первую попытку доставки слишком медленной, и p95 по SLO не укладывается**. Источники выше это подтверждают; в найденных кусках именно так и формулируется причина.

## m10 [en / crosslingual] What did the team mean by 'дрифт' and what rule came out of it?
**expected:** drift detection: stacks diverging from reality after manual console changes; after the 2026-02-23 incident manual prod changes were frozen and nightly DetectStackDrift runs with alerts  
**expected sources:** {'sources': ['meetings/2026-02-23-incident-review.txt', 'docs/drift-detection.md']}

### memory-eval-both (completed, 6.1s, 3 tool calls)
queries: ['дрифт meaning rule came out of it Relay webhook delivery project', 'дрифт rule change freeze template wins intended not intended Relay', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'iac'}) WHERE d.text STARTS WITH 'Chan"]

Под «дрифт» команда имела в виду расхождение состояния стека AWS с тем, что описано в шаблоне: в обсуждении было сказано, что «stack разошелся с реальностью» после ручного изменения в консоли, а в документе это сформулировано как drift detection and change freeze. Источник: `meetings/2026-02-23-incident-review.txt` от 2026-02-23; `docs/drift-detection.md` от 2026-02-25.

Правило, которое из этого вышло:
1. Нельзя вручную менять production-ресурсы Relay в AWS console.
2. Для проверки дрейфа каждый стек Relay проходит `DetectStackDrift` ночью в 01:00.
3. Если стек в состоянии `DRIFTED`, pipeline блокируется до исправления.

И отдельно для ручных изменений сказано: если изменение было намеренным, его нужно внести в template, задеплоить и подтвердить `IN_SYNC`; если изменение было ненамеренным, нужно redeploy, и шаблон побеждает. Источник: `docs/drift-detection.md` от 2026-02-25.

Если хотите, я могу ещё кратко пересказать, как это правило было сформулировано на встрече.

### memory-eval-graph (completed, 5.4s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'})\nWHERE d.text CONTAINS 'д", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'})\nWHERE d.text CONTAINS 'n"]

By “дрифт” the team meant **configuration drift in IaC/stacks**: the decision says **“Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call”**. Source: **meetings/2026-02-23-incident-review.txt**, date **2026-02-23**.

The rule that came out of it was:
- **No manual console changes**
- **Run nightly drift detection on every stack**
- **Alert on-call on drift**

This is decision **D04** and it is **active**. Source: **meetings/2026-02-23-incident-review.txt**, date **2026-02-23**.

### memory-eval-vector (completed, 5.4s, 3 tool calls)
queries: ["What did the team mean by 'дрифт' and what rule came out of it?", 'дрифт rule came out of it team meaning', 'дрифт']

By **“дрифт”** the team meant an **unintended divergence between the live AWS stack and the declared template/state** — in the incident review, it was when someone changed the load balancer timeout by hand in the console, so the stack “went out of sync” with reality. Source: `meetings/2026-02-23-incident-review.txt` (2026-02-23); also summarized in `docs/drift-detection.md` (updated 2026-02-25).

The rule that came out of it was:

1. **No manual changes in the AWS console for production Relay resources.**  
2. **Run `DetectStackDrift` nightly at 01:00 on every Relay stack.**  
3. **If a stack is `DRIFTED`, block the pipeline until it is reconciled.**  
Source: `docs/drift-detection.md` (updated 2026-02-25).

The reconciliation rule was also recorded as:
- if the change was intended, **put it in the template, deploy, and confirm `IN_SYNC`**;
- if it was not intended, **redeploy the stack; the template wins**.  
Source: `docs/drift-detection.md` (updated 2026-02-25).

## m11 [en / multi_hop] Why were gateway retries on /deliver turned off in August, when they had been turned on in June?
**expected:** June: retries enabled (max 3, budget 15%) once idempotency keys were mandatory; August: Lambda intake is asynchronous and a gateway retry enqueues twice, so retries moved to SQS with a DLQ (ADR-009) and gateway retries were turned off  
**expected sources:** {'sources': ['meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt', 'adr/ADR-009.md']}

### memory-eval-both (completed, 8.7s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.text CONTAIN", 'gateway retries /deliver turned off August turned on June why', 'ретраи gateway /deliver отключили в августе почему в июне включили']

Gateway retries on `/deliver` were turned off in August because the design changed to move retries out of the gateway and into SQS with a dead-letter queue after 5 attempts. The rationale recorded in the memory is that the queue provides better retry behavior: exponential delay, DLQ visibility, and no need for a gateway retry budget.

What was decided:
- 2026-06-15: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%” — `meetings/2026-06-15-weekly-sync.txt` (`D14`, status `superseded`)
- 2026-08-24: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off” — `meetings/2026-08-24-weekly-sync.txt` (`D21`, status `active`)

Why it changed:
- In the August meeting, Ivan said: “очередь ретраит лучше гейтвея это экспоненциальная задержка и видимость в длк” and Lena added that “бюджет ретраев тогда не нужен очередь сама ограничивает.” Source: `meetings/2026-08-24-weekly-sync.txt` on 2026-08-24.
- Earlier rationale for keeping gateway retries off was idempotency risk: a retried `/deliver` could reach a customer twice. Source: `docs/idempotency.md` updated 2026-05-20 and `adr/ADR-002.md` up

### memory-eval-graph (completed, 7.8s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(t:Topic) WHERE t.key IN ['topic:gateway','topic:re"]

Gateway retries on `/deliver` were turned off in August because the team decided to move retries out of the gateway and into SQS with a dead-letter queue after 5 attempts.

What I found:
- On 2026-06-15, the gateway retries on `POST /deliver` were enabled: “max 3 attempts, retry budget 15%” from `meetings/2026-06-15-weekly-sync.txt`. That decision is now superseded. Source: `meetings/2026-06-15-weekly-sync.txt`, date `2026-06-15` (`D14`).
- On 2026-08-24, the active decision changed it to: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off” from `meetings/2026-08-24-weekly-sync.txt`. Source: `meetings/2026-08-24-weekly-sync.txt`, date `2026-08-24` (`D21`).

So the reason, as recorded in memory, is the architectural shift from gateway retries to SQS-based retries + DLQ.

### memory-eval-vector (completed, 5.0s, 3 tool calls)
queries: ['Why were gateway retries on /deliver turned off in August, when they had been tu', 'gateway retries /deliver turned off August turned on June', 'retry /deliver gateway August June turned off turned on']

Not in memory for **August specifically as a change request/decision**. What I retrieved says:

- Gateway retries on `/deliver` were disabled because a retried delivery could reach a customer twice, i.e. the delivery was not idempotent yet. Source: `docs/idempotency.md` (updated 2026-05-20).
- `POST /deliver` retries were described as disabled in gateway docs for the same reason, with the note that they would be enabled later once idempotency keys exist. Source: `adr/ADR-002.md` (updated 2026-03-04) and `docs/gateway.md` (updated 2026-03-18).
- A later ADR chose a different mechanism: retries through SQS with a dead-letter queue, and “gateway retries off on /deliver” was the chosen option. Source: `adr/ADR-009.md` (updated 2026-08-26).
- The later docs say gateway retries are no longer a gateway policy. Source: `docs/retries-dlq.md` (updated 2026-08-27).

So the memory contains the reason for turning them off: to avoid duplicate customer deliveries before idempotency, and later because retries moved to SQS/DLQ. I did not find a separate August note saying “why in August they were turned off” beyond that ADR-009 choice.

## m12 [ru / multi_hop] Какая цепочка событий привела к тому, что сеть осталась в Terraform?
**expected:** январь: решение переехать целиком на CloudFormation (ADR-001, Тимур против); апрель: Серёжа принёс цифры (кастомные ресурсы для пиринга и DNS, 4 недели), Паша возражал, приняли гибрид (ADR-004, заменяет ADR-001)  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-04-13-weekly-sync.txt', 'meetings/2026-04-20-weekly-sync.txt', 'adr/ADR-004.md']}

### memory-eval-both (completed, 10.4s, 3 tool calls)
queries: ['Terraform network remained because chain of events led to network staying in Ter', 'MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision) WHERE (cur)-[:ABOUT', 'ADR-004 Context why networking stays in Terraform hybrid IaC rationale']

Цепочка была такой:

1. **Сначала был принят ADR-001**: мигрировать инфраструктуру Relay из Terraform в CloudFormation по модулям, до конца Q1.  
   Источник: `meetings/2026-01-12-weekly-sync.txt`, дата `2026-01-12`.

2. **Потом выяснилось, что сетевой модуль — последний и самый сложный для переноса**. В контексте ADR-004 прямо сказано, что:
   > “the networking module was the last to move and the hardest: cross-account peering and DNS delegation need custom resources in CloudFormation, while the same networking is already expressed natively in the Terraform the network team maintains for the whole company.”  
   Источник: `adr/ADR-004.md`, дата `2026-04-22`.

3. **На основании этого выбрали гибридный вариант**: сеть оставить в Terraform, а application stacks перенести в CloudFormation.  
   В ADR-004 в разделе Options considered сказано:
   > “Hybrid: networking stays in Terraform, application stacks in CloudFormation (chosen)”  
   Источник: `adr/ADR-004.md`, дата `2026-04-22`.

4. **Это и стало текущим решением, которое supersedes ADR-001**:  
   > “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation.”  
   Источник: `meetings/202

### memory-eval-graph (completed, 8.4s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) RETURN d.id, d.text, d.d", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'}) RETURN d.id, d.text,"]

Цепочка была такой:

1. Сначала решили мигрировать инфраструктуру Relay с Terraform на CloudFormation по модулям, с завершением к концу Q1.  
   Источник: `meetings/2026-01-12-weekly-sync.txt`, 2026-01-12, решение D01: “Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1”.

2. Затем закрепили целевую схему CloudFormation: по одному root stack на окружение и nested stacks для компонентов, включая network.  
   Источник: `meetings/2026-02-09-weekly-sync.txt`, 2026-02-09, решение D03: “One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)”.

3. Потом последовало уточнение по архитектуре gateway, где gateway тоже оказался в CloudFormation nested stack.  
   Источник: `meetings/2026-03-02-weekly-sync.txt`, 2026-03-02, решение D05: “Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack”.

4. Но позже курс изменили: сеть решили оставить в Terraform, а в CloudFormation перевести только application stacks.  
   Источник: `meetings/2026-04-20-weekly-sync.txt`, 2026-04-20, решение D09: “Hybrid IaC: networking (VPC, peering, DNS) sta

### memory-eval-vector (completed, 8.3s, 3 tool calls)
queries: ['Какая цепочка событий привела к тому, что сеть осталась в Terraform?', 'цепочка событий сеть осталась в Terraform', 'network remained in Terraform chain of events']

Цепочка событий в памяти такая:

1. **Сначала был план перевести всю инфраструктуру из Terraform в CloudFormation** — это зафиксировано в **ADR-001** от **2026-01-14**. В контексте сказано, что существующая инфраструктура была в Terraform, а остальная часть AWS-аккаунта уже жила в CloudFormation, поэтому хотели всё унифицировать.  
   **Источник:** `adr/ADR-001.md` / `Context` / **2026-01-14**.

2. **Затем выяснилось, что сетевой модуль — последний и самый сложный для переноса**. В **ADR-004** от **2026-04-22** сказано, что у сети есть **cross-account peering** и **DNS delegation**, которым в CloudFormation нужны custom resources, тогда как та же сеть уже нативно описана в Terraform, который ведёт network team.  
   **Источник:** `adr/ADR-004.md` / `Context` / **2026-04-22**.

3. **Из-за этого приняли новое решение: сеть оставить в Terraform, а application stacks перевести в CloudFormation**. Это текущая активная decision **D09** от **2026-04-20**, записанная в `meetings/2026-04-20-weekly-sync.txt`, и она **supersedes D01**.  
   **Источник:** `meetings/2026-04-20-weekly-sync.txt` / decision `D09` / **2026-04-20**.

4. **Старый план из ADR-001 был фактически заменён** — ADR-004 пом

## m13 [en / multi_hop] Which decision closed the longest-standing open item, who took it, and how many times had it been raised before?
**expected:** D19 on 2026-08-10: Sergey took the DynamoDB dry run (due 2026-09-04); raised 2026-05-04 and again on 05-18, 06-15, 06-29, 07-20 (four times)  
**expected sources:** {'sources': ['meetings/2026-05-04-poc-review.txt', 'meetings/2026-08-10-weekly-sync.txt']}

### memory-eval-both (completed, 5.6s, 2 tool calls)
queries: ["MATCH (o:OpenItem {status:'closed'}) OPTIONAL MATCH (c:Decision)-[:CLOSES]->(o) ", "MATCH (o:OpenItem {status:'closed'})<-[:CLOSES]-(c:Decision) OPTIONAL MATCH (p:P"]

The longest-standing closed open item is **O1: “DynamoDB migration dry run on a production snapshot”**.

- **Decision that closed it:** “DynamoDB migration dry run on a production snapshot is owned by Sergey, due 2026-09-04”
- **Decision date / source:** 2026-08-10, `meetings/2026-08-10-weekly-sync.txt`
- **Who took it:** **no person ownership edge was recorded** on the item itself; the closing decision says it is **owned by Sergey**.
- **How many times it had been raised before:** **5 times total raised dates** were recorded (`2026-05-04` plus `raised_again` on `2026-05-18`, `2026-06-15`, `2026-06-29`, `2026-07-20`), so **4 times after the initial raise**.

Assumption: I treated “how many times had it been raised before” as the number of recorded raise dates, excluding the initial raise.

### memory-eval-graph (completed, 3.9s, 1 tool calls)
queries: ["MATCH (o:OpenItem {status:'closed'}) OPTIONAL MATCH (c:Decision)-[:CLOSES]->(o) "]

The longest-standing closed open item was **“Route drift-detection alerts to on-call”**, raised on **2026-02-23** in **O8**. It was taken by **Lena Kim** on **2026-03-02**.

However, I could not retrieve the closing decision from the graph for this item: the result for the closure fields was null, so the graph does not currently expose a `CLOSES` decision for it.

It had been raised **1 time before** being taken/closed:
- `raised`: 2026-02-23
- `raised_again`: none

Source: **open item O8** (`raised` / `raised_again` / ownership info), and the graph query for `CLOSES` returned no decision rows.

### memory-eval-vector (completed, 4.8s, 3 tool calls)
queries: ['Which decision closed the longest-standing open item, who took it, and how many ', 'longest-standing open item closed by decision raised times', 'open item decision closed raised before how many times']

The longest-standing open item I found is **“DynamoDB migration dry run on a production snapshot”**.

- **Decision that closed it:** **D19**  
- **Who took it:** the item itself says **no owner**; I did **not** find the decision owner in the retrieved chunks, only that it was “Closed by D19”  
- **How many times it had been raised before closing:** **5 times total mentioned** — raised on **2026-05-04**, then again on **2026-05-18, 2026-06-15, 2026-06-29, 2026-07-20**  
  - So it had been **raised again 4 times after the initial raise**.

Sources:
- `meetings/2026-05-04-poc-review.txt` — open item claim O1, dated **2026-05-04**
- `confluence/decision-log.xhtml` — decision log, updated **2026-06-03**
- The retrieved memory did **not** contain the full D19 decision chunk, so the decision’s owner is **not in memory**.

## m14 [ru / multi_hop] Кто возражал против переезда на CloudFormation в январе и какую позицию он занял в апреле, когда обсуждали гибрид?
**expected:** Тимур возражал в январе (ADR-001); в апреле поддержал гибрид Серёжи («тулинг надо выбирать по задаче»); возражал в апреле уже Паша  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 7.4s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'})<-[:OBJECTED_TO]-(p:Perso", 'январь CloudFormation переезд возражал', 'April hybrid discussed position CloudFormation objection', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'})<-[:OBJECTED_TO]-(p:Perso"]

В январе против переезда на CloudFormation возражал **Тимур Алиев**; в апреле на обсуждении гибрида он занял позицию **против чистого завершения миграции и за гибрид**: Terraform для networking, CloudFormation для application stacks.

- Январь: **Timur Aliev** — возражение зафиксировано в ADR-001, датировано **2026-01-12**; источник: `meetings/2026-01-12-weekly-sync.txt` / `adr/ADR-001.md`.
- Апрель: **Pavel Grishin** — возражение записано в ADR-004 от **2026-04-22**; в документе указано, что он возразил против гибрида/смены курса? Нет: по найденному тексту в ADR-004 **объектировал Павел Гришин**, а сама принятая позиция — **Hybrid IaC: networking stays in Terraform, application stacks are CloudFormation**. Источник: `adr/ADR-004.md`.

Если хотите, я могу отдельно разложить это как: **кто именно объектировал в апреле** и **какую сторону поддерживал** — по найденным записям это не одно и то же.

### memory-eval-graph (completed, 5.9s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'})<-[:ABOUT]-(d2:Decision) ", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (p:Person"]

В январе против переезда на CloudFormation возражал Тимур Алиев — источник: `meetings/2026-01-12-weekly-sync.txt`, дата `2026-01-12`. Позиция была зафиксирована в решении: «Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1»; статус `superseded`.

В апреле, когда обсуждали гибрид, его позиция в памяти не помечена как возражение: в решении от `2026-04-20` зафиксировано «Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation»; статус `active`, источник `meetings/2026-04-20-weekly-sync.txt`.

Если хотите, я могу ещё точно сопоставить, было ли это именно возражение Тимура на апрельском обсуждении или он просто снова был связан с этой темой.

### memory-eval-vector (completed, 4.5s, 3 tool calls)
queries: ['Кто возражал против переезда на CloudFormation в январе и какую позицию он занял', 'возражал против переезда на CloudFormation в январе гибрид апрель', 'CloudFormation январь апрель гибрид возражал позицию']

В январе против переезда на CloudFormation возражал **Тимур Аливев** — это зафиксировано в записи встречи **2026-01-12** и в ADR-001 **2026-01-14**.  
Источник: `meetings/2026-01-12-weekly-sync.txt` (2026-01-12), `adr/ADR-001.md` (2026-01-14).

В апреле, когда обсуждали гибрид, **Павел Гришин** занял позицию возражающего: в ADR-004 зафиксировано, что **гибридный вариант принят**, но у него есть возражение; сам вариант такой: **сеть (VPC, peering, DNS) остаётся в Terraform, а application stacks — в CloudFormation**.  
Источник: `adr/ADR-004.md` (2026-04-22), `meetings/2026-04-20-weekly-sync.txt` (2026-04-20).

Если хотите, я могу ещё кратко сопоставить, почему в январе возражал Тимур, а в апреле — Павел, по источникам.

## m15 [en / point_in_time] On 2026-07-01, who owned retries, who owned the serverless PoC, and was the dry run owned?
**expected:** retries: Anna (since 06-01); serverless PoC: Sergey (until 07-13); dry run: no owner  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-06-29-weekly-sync.txt']}

### memory-eval-both (completed, 6.5s, 4 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(x:Topic {key:'topic:retries'}) WHERE o.from <= '2026", "MATCH (p:Person)-[o:OWNS]->(x:PoC {key:'poc:poc-3'}) WHERE o.from <= '2026-07-01", "MATCH (p:Person)-[o:OWNS]->(x:OpenItem {id:'O1'}) WHERE o.from <= '2026-07-01' A", "MATCH (o:OpenItem {id:'O1'}) RETURN o.id, o.text, o.raised, o.raised_again, o.st"]

On 2026-07-01:

- **Retries** was owned by **Anna Sokolova** (`from 2026-06-01` to `2026-09-07`), from the ownership edge on the retries topic. Source: graph query result.
- **The serverless PoC** (`poc:poc-3`) was owned by **Sergey Belov** (`from 2026-06-22` to `2026-07-13`). Source: graph query result.
- **The dry run** (`O1`, “DynamoDB migration dry run on a production snapshot”) was **not owned** on that date: there was no OWNS edge active on 2026-07-01. It was raised on `2026-05-04` and raised again on `2026-05-18`, `2026-06-15`, `2026-06-29`, and `2026-07-20`. Source: graph query result.

If you want, I can also give the exact owning person history for each item.

### memory-eval-graph (completed, 4.9s, 3 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(x:Topic {key:'topic:retries'}) WHERE o.from <= $D AN", "MATCH (p:Person)-[o:OWNS]->(x:PoC {key:'poc:poc-3'}) WHERE o.from <= $D AND (o.t", "MATCH (p:Person)-[o:OWNS]->(x:OpenItem {id:'O1'}) WHERE o.from <= $D AND (o.to I"]

Assumption: “serverless PoC” means `poc:poc-3`, and “the dry run” means open item `O1`.

On 2026-07-01:
- retries was owned by Anna Sokolova, from 2026-06-01 to 2026-09-07. Source: memory graph OWNS edge; no decision file/date applies directly to ownership.  
- the serverless PoC was owned by Sergey Belov, from 2026-06-22 to 2026-07-13. Source: memory graph OWNS edge; no decision file/date applies directly to ownership.  
- the dry run was not owned by anyone on that date. Source: memory graph OWNS lookup for `O1` returned no owner; O1 is the dry run item.

### memory-eval-vector (completed, 5.8s, 3 tool calls)
queries: ['On 2026-07-01, who owned retries, who owned the serverless PoC, and was the dry ', '2026-07-01 retries serverless PoC dry run owner', 'who owned retries who owned the serverless PoC was the dry run owned 2026-07-01']

On 2026-07-01:

- **Retries:** **Anna Sokolova** owned retries. The latest memory I found before or on that date is the ownership claim from **2026-06-01** saying Anna owned retries from 2026-06-01 to 2026-09-07. Source: **memory/decisions.jsonl** and **confluence/team-roster.xhtml** (both reflect ownership as of **2026-07-08**, but the dated ownership claim is the stronger source for 2026-07-01).
- **Serverless PoC:** **Sergey Belov** still owned the serverless PoC on 2026-07-01. The ownership move to **Ivan Melnik** is dated **2026-07-13**, so that later decision supersedes the earlier state. Source: **meetings/2026-07-13-weekly-sync.txt**.
- **Dry run:** **No owner**. The dry run was recorded as open without an owner on **2026-05-04** and was still called out as having no owner on **2026-06-15** and **2026-07-20**. Source: **meetings/2026-05-04-poc-review.txt**; **meetings/2026-06-15-weekly-sync.txt**.

If you want, I can also give this as a one-line table with exact dates and statuses.

## m16 [ru / point_in_time] Какой таймаут на gateway действовал 1 июля 2026 и кто был его владельцем?
**expected:** 30 с (решение 2026-05-18, заменило 10 с), владелец Паша  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt']}

### memory-eval-both (completed, 4.1s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20", "MATCH (p:Person)-[o:OWNS]->(d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}"]

На 2026-07-01 в силе было: **gateway integration timeout 30 s**.

Владелец: **Pavel Grishin**.

Источник: `meetings/2026-05-18-weekly-sync.txt`, решение от `2026-05-18`:
- `Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14`
- статус: `superseded`

Примечание: я использовал последнее решение по теме таймаутов, действовавшее на указанную дату.

### memory-eval-graph (completed, 4.2s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20", "MATCH (p:Person)-[:OWNS]->(d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'})"]

На 2026-07-01 действовало решение: **“Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14”**; дата решения **2026-05-18**, статус **superseded**, источник **meetings/2026-05-18-weekly-sync.txt**. Это и было решение в силе на ту дату по теме таймаутов.  

Владелец: **Pavel Grishin**; источник владения — **meetings/2026-05-18-weekly-sync.txt**, дата **2026-05-18**.

### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['Какой таймаут на gateway действовал 1 июля 2026 и кто был его владельцем?', 'таймаут gateway 1 июля 2026 владелец', 'gateway timeout owner July 1 2026']

На 1 июля 2026 действовал таймаут gateway **30 s**; это решение было принято **2026-05-18** и позже было **superseded** решением от 2026-08-24, где таймаут снизили до 25 s. Источник: `meetings/2026-05-18-weekly-sync.txt` (2026-05-18), `meetings/2026-08-24-weekly-sync.txt` (2026-08-24).

Владельцем gateway был **Pavel Grishin** с **2026-03-02** и без даты окончания, то есть текущий владелец. Источник: `memory/decisions.jsonl` (2026-03-02).

## m17 [en / aggregate] Which decisions were made at the architecture committee on 2026-08-03 and which open item was raised there?
**expected:** D17 Lambda with provisioned concurrency (ADR-006), D18 keep EKS rejected (ADR-007); open item: provisioned concurrency sizing, taken by Ivan on 08-10  
**expected sources:** {'sources': ['meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 6.0s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:DECIDED_IN]->(m:Meeting {date:'2026-08-03'}) RETURN d.id, d", "MATCH (d:Decision)-[:DECIDED_IN]->(m:Meeting {date:'2026-08-03'}) RETURN d.id, d", "MATCH (o:OpenItem)-[:RAISED_IN]->(m:Meeting {date:'2026-08-03'}) RETURN o.id, o."]

At the architecture committee on 2026-08-03, these decisions were made:

- D17 — Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances.  
  Source: `meetings/2026-08-03-architecture-committee.txt`, dated 2026-08-03.

- D18 — Keep Relay on EKS with autoscaling was rejected; the note says p95 0.4 s but 1.7x the monthly cost and a second platform to run.  
  Source: `meetings/2026-08-03-architecture-committee.txt`, dated 2026-08-03.

The open item raised there was:

- O6 — Provisioned concurrency sizing for /deliver.  
  Raised: 2026-08-03  
  Raised again: none  
  Status: closed  
  Source: `meetings/2026-08-03-architecture-committee.txt`, dated 2026-08-03.

### memory-eval-graph (completed, 6.6s, 2 tool calls)
queries: ["MATCH (m:Meeting {date:'2026-08-03'})<-[:DECIDED_IN]-(d:Decision)\nRETURN d.id, d", "MATCH (o:OpenItem)-[:RAISED_IN]->(m:Meeting {date:'2026-08-03'})\nRETURN o.id, o."]

На architecture committee 2026-08-03 были приняты следующие решения:

- **D17** — “Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances”  
  **Дата:** 2026-08-03  
  **Статус:** active  
  **Источник:** `meetings/2026-08-03-architecture-committee.txt`

- **D18** — “Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)”  
  **Дата:** 2026-08-03  
  **Статус:** rejected  
  **Источник:** `meetings/2026-08-03-architecture-committee.txt`

Открытый пункт, поднятый там:

- **O6** — “Provisioned concurrency sizing for /deliver”  
  **Raised:** 2026-08-03  
  **Raised again:** нет  
  **Статус:** closed  
  **Источник:** `meetings/2026-08-03-architecture-committee.txt`

Если хотите, я могу также показать, какое решение сейчас в силе по теме compute.

### memory-eval-vector (completed, 5.4s, 3 tool calls)
queries: ['Which decisions were made at the architecture committee on 2026-08-03 and which ', 'architecture committee 2026-08-03 decisions open item', '2026-08-03 architecture committee meeting decisions open item']

На архитектурном комитете 2026-08-03 было принято решение:

- Relay переезжает на Lambda с provisioned concurrency на `/deliver`; ADR 006 принят, ADR 007 отклонён, владелец — Ваня, возражение Тимура зафиксировано. Источник: `meetings/2026-08-03-architecture-committee.txt`, 2026-08-03.

Также там был поднят открытый вопрос:

- Sizing provisioned concurrency: сколько инстансов держать. Источник: `meetings/2026-08-03-architecture-committee.txt`, 2026-08-03.

Примечание: в найденной памяти есть ещё запись об open item по provisioning concurrency sizing for `/deliver`, но она помечена как `closed` и с владельцем Ivan Melnik с 2026-08-10; для вопроса о том, что было поднято 2026-08-03, актуальна именно формулировка из протокола встречи.

## m18 [ru / aggregate] Сколько раз менялась политика ретраев и кто владел ею на каждом шаге?
**expected:** три решения: 03-30 выключены (Никита), 06-15 включены на gateway, 3 попытки, бюджет 15% (Аня), 08-24 перенесены в SQS с DLQ (Аня, с 09-07 Ваня)  
**expected sources:** {'sources': ['meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 11.2s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) OPTIONAL MATCH (d)<-", 'ретраи retries policy who owned it at each step gateway SQS DLQ', "MATCH (:Person)-[o:OWNS]->(d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) "]

Политика ретраев менялась **3 раза** — то есть есть **3 шага/решения** в истории:

1. **2026-03-30 — D07**  
   `Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice`  
   Источник: `meetings/2026-03-30-weekly-sync.txt`  
   Владелец на этом шаге: **не указан в найденных OWNS-данных для решения**; в памяти по decision-graph есть только сам шаг, а ownership-ребро для него не вернулось отдельным person.

2. **2026-06-15 — D14**  
   `Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%`  
   Источник: `meetings/2026-06-15-weekly-sync.txt`  
   Владелец на этом шаге: **не указан в найденных OWNS-данных для решения**.

3. **2026-08-24 — D21**  
   `Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off`  
   Источник: `meetings/2026-08-24-weekly-sync.txt`  
   Владелец на этом шаге: **Анна Соколова**.  
   Доп. подтверждение из vector memory: `Owner: Anna Sokolova. Proposed by Ivan Melnik; objection from Anna Sokolova.`

Важно: в графе на тему `topic:retries` найдено **3 решения**, но ownership-ребра к первым двум в ответе на запрос 

### memory-eval-graph (completed, 7.9s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) OPTIONAL MATCH (d)-[", "MATCH (p:Person)-[o:OWNS]->(d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})"]

Политика ретраев менялась **3 раза**.  
Я считаю шаги по решениям на topic:retries, а владельца — по OWNS на каждом решении.

1. **2026-03-30** — **Nikita Frolov** владел политикой  
   - Решение: “Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice”  
   - Статус: **superseded**  
   - Источник: `meetings/2026-03-30-weekly-sync.txt`  
   - Дата: `2026-03-30`

2. **2026-06-15** — **Anna Sokolova** владела политикой  
   - Решение: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%”  
   - Статус: **superseded**  
   - Источник: `meetings/2026-06-15-weekly-sync.txt`  
   - Дата: `2026-06-15`

3. **2026-08-24** — **Anna Sokolova** владеет текущей политикой  
   - Решение: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”  
   - Статус: **active**  
   - Источник: `meetings/2026-08-24-weekly-sync.txt`  
   - Дата: `2026-08-24`

Если хотите, могу ещё кратко показать саму эволюцию политики в одной строке.

### memory-eval-vector (completed, 8.7s, 3 tool calls)
queries: ['Сколько раз менялась политика ретраев и кто владел ею на каждом шаге?', 'политика ретраев ownership changes Relay webhook delivery', 'retry policy owner changes Relay webhook delivery']

Найдено **3 изменения** политики ретраев, если считать смены текущего решения по теме `retries`.

1. **2026-03-30** — ретраи на `POST /deliver` были **выключены**; владелец: **Никита**.  
   Источник: `meetings/2026-03-30-weekly-sync.txt` (2026-03-30), а также `meetings/2026-03-30-weekly-sync.txt` / claim `D14` как следующее историческое состояние, где указано, что D14 **supersedes D07**.

2. **2026-06-15** — ретраи на `POST /deliver` в gateway были **включены**: максимум **3 попытки**, budget **15%**; владелец: **Анна**.  
   Источник: `meetings/2026-06-15-weekly-sync.txt` (2026-06-15), claim `D14` в `meetings/2026-06-15-weekly-sync.txt`.

3. **2026-09-07** — ретраи **переехали с Анны на Ваню**; речь уже про **SQS pipeline**, а не gateway policy.  
   Источник: `meetings/2026-09-07-security-review.txt` (2026-09-07).

Важно:
- Более свежий документ `docs/retries-dlq.md` (2026-08-27) говорит: **“Retries are owned by the Relay core lead until the serverless cutover, then by the owner of the SQS pipeline.”** Это соответствует более позднему переходу к SQS, но не отменяет отдельное решение от 2026-09-07 о передаче от Анны к Ване.
- Документ `docs/gateway.md` от 2026-03-18 устарел относ

## m19 [en / unowned] What is still unowned as of 2026-10-05 and how many times has each been raised?
**expected:** 10x load test on Lambda (raised 07-27, again 08-17, 09-14); DocumentDB credential rotation (raised 09-07, again 09-28, 10-05); DocumentDB decommission date (raised 05-18, again 08-10, 10-05) has no date rather than no owner  
**expected sources:** {'sources': ['meetings/2026-07-27-poc-review.txt', 'meetings/2026-09-07-security-review.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 4.4s, 1 tool calls)
queries: ["MATCH (o:OpenItem)\nWHERE o.raised <= '2026-10-05'\n  AND NOT EXISTS { MATCH (o)<-"]

As of 2026-10-05, the unowned open items are:

- O3 — “Load test on Lambda at 10x current volume”  
  Raised 3 times total: 2026-07-27, 2026-08-17, 2026-09-14  
  Source: graph memory, item O3

- O4 — “DocumentDB decommission date”  
  Raised 3 times total: 2026-05-18, 2026-08-10, 2026-10-05  
  Source: graph memory, item O4

- O7 — “Rotate DocumentDB credentials before decommission”  
  Raised 3 times total: 2026-09-07, 2026-09-28, 2026-10-05  
  Source: graph memory, item O7

Counted as raised once plus the dates in `raised_again`.

### memory-eval-graph (completed, 3.8s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

As of 2026-10-05, the unowned open items are:

- O3 — Load test on Lambda at 10x current volume — raised 3 times total: 2026-07-27, 2026-08-17, 2026-09-14. Source: open item O3 from memory graph; raised dates per O3.  
- O4 — DocumentDB decommission date — raised 3 times total: 2026-05-18, 2026-08-10, 2026-10-05. Source: open item O4 from memory graph; raised dates per O4.  
- O7 — Rotate DocumentDB credentials before decommission — raised 3 times total: 2026-09-07, 2026-09-28, 2026-10-05. Source: open item O7 from memory graph; raised dates per O7.  

No owner was found for these items as of 2026-10-05.

### memory-eval-vector (completed, 4.9s, 3 tool calls)
queries: ['What is still unowned as of 2026-10-05 and how many times has each been raised?', 'unowned as of 2026-10-05 raised how many times each', 'open item no owner raised dates Relay webhook delivery']

As of 2026-10-05, I found 3 unowned open items in memory:

- DocumentDB decommission date — raised 3 times  
  Source: `meetings/2026-05-18-weekly-sync.txt` (2026-05-18), with repeats on 2026-08-10 and 2026-10-05 in the same claim.
- Load test on Lambda at 10x current volume — raised 3 times  
  Source: `meetings/2026-07-27-poc-review.txt` (2026-07-27), with repeats on 2026-08-17 and 2026-09-14 in the same claim.
- Rotate DocumentDB credentials before decommission — raised 3 times  
  Source: `meetings/2026-09-07-security-review.txt` (2026-09-07), with repeats on 2026-09-28 and 2026-10-05 in the same claim.

I did not count closed items or items that have an owner. The retrieved memory also contained closed items like the DynamoDB migration dry run, rollback runbook, Terraform state cleanup, and provisioned concurrency sizing, plus a cutover decision assigning ownership, but those are not unowned open items.

## m20 [ru / dependency] Что должно произойти до серверлес-катовера 19 октября и в каком порядке?
**expected:** катовер базы на DynamoDB 12 октября (за неделю), dual write до 26 октября; нагрузочный тест на 10x всё ещё не сделан; runbook отката с владельцем Леной  
**expected sources:** {'sources': ['meetings/2026-10-05-cutover-planning.txt', 'docs/runbook-cutover-serverless.md', 'docs/load-testing.md']}

### memory-eval-both (completed, 5.5s, 3 tool calls)
queries: ['серверлес катовер 19 октября runbook steps order before cutover', 'serverless cutover October 19 runbook steps order before cutover', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202"]

До серверлес-катовера 19 октября должны произойти эти шаги, в таком порядке:

1. За 24 часа заморозить изменения endpoint’ов.  
2. Переключить интеграции gateway для `POST /relay/deliver` и `GET /relay/*` с VPC link на Lambda-интеграции.  
3. Уменьшить EKS deployments до 0 replicas, но оставить кластер ещё на 7 дней.  
4. Наблюдать `delivery p95`, `DLQ depth` и `intake 5xx` в течение 30 минут после переключения.

Источник: `docs/runbook-cutover-serverless.md`, updated `2026-09-29`.

Дополнительно по предкатовымеру:
- Cutover запланирован на `2026-10-19` в `09:00` local.
- По заметке в runbook’е предварительное условие: сначала должен быть выполнен DynamoDB cutover, и между ними должен быть интервал в неделю.
- Из решения от `2026-10-05` в силе также указано: owner rollback для обоих cutover — Lena.  
  Источник: `meetings/2026-10-05-cutover-planning.txt`.

### memory-eval-graph (completed, 9.4s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202", "MATCH (o:OpenItem)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE o.raised <= '2"]

По состоянию на 2026-10-19 в памяти есть только два решения по катоверу, и оба от 2026-10-05; они не образуют явной цепочки зависимостей, поэтому порядок между ними в графе не задан.

Что должно произойти до серверлес-катовера:
1. Назначен владелец отката для обоих катоверов — Лена.  
   Источник: `meetings/2026-10-05-cutover-planning.txt`, дата `2026-10-05`.
2. Сам серверлес-катовер запланирован на `2026-10-19 09:00 local`, и он укладывается в planned-work error budget.  
   Источник: `meetings/2026-10-05-cutover-planning.txt`, дата `2026-10-05`.

Порядок в памяти:
- сначала зафиксировано назначение владельца отката,
- затем зафиксирован сам катовер.  

Но это именно порядок дат решений, а не явный порядок выполнения шагов: в графе нет связки `DEPENDS_ON` между ними, и открытых items по теме `cutover` на эту дату нет.

Если хотите, могу также проверить, есть ли связанные решения по `database` и `compute`, которые должны быть выполнены до этого катовера.

### memory-eval-vector (completed, 5.3s, 3 tool calls)
queries: ['Что должно произойти до серверлес-катовера 19 октября и в каком порядке?', 'до серверлес-катовера 19 октября порядок событий', 'серверлес-катовер 19 октября порядок']

До серверлес-катовера 19 октября в памяти есть такой порядок:

1. **Переключить базу раньше 12 октября** — это должно случиться **до** серверлес-катовера. Источник: `meetings/2026-10-05-cutover-planning.txt`, 2026-10-05.
2. **Выключить dual write 26 октября** — это уже **после** серверлес-катовера 19 октября. Источник: `meetings/2026-10-05-cutover-planning.txt`, 2026-10-05.

То есть, если отвечать строго на вопрос «что должно произойти **до** 19 октября и в каком порядке», в памяти явно зафиксировано только одно событие до этой даты: **переключение базы раньше 12 октября**.

Что я нашёл:
- `meetings/2026-10-05-cutover-planning.txt` (2026-10-05): серверлес-катовер 19 октября в 9:00; база — до 12 октября; dual write — до 26 октября.
- `docs/runbook-cutover-serverless.md` (2026-09-29): preconditions и шаги для serverless cutover, но дата там не назначена и документ старее, чем встреча.

Если хотите, я могу отдельно собрать **полную хронологию всех шагов вокруг cutover** из найденных источников.

## m21 [en / temporal] Has the SLO ever changed? What is it right now?
**expected:** yes: p95 2 s from 2026-01-26; relaxed to 3 s for 30 days after the serverless cutover (decided 2026-10-05, Marat objected), then back to 2 s; success rate 99.5% unchanged  
**expected sources:** {'sources': ['meetings/2026-01-26-weekly-sync.txt', 'meetings/2026-10-05-cutover-planning.txt', 'docs/slo.md']}

### memory-eval-both (completed, 4.8s, 3 tool calls)
queries: ['SLO changed current target Relay webhook delivery project', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE", "MATCH (d:Decision {status:'superseded'})-[:ABOUT]->(t:Topic {key:'topic:slo'}) R"]

Yes — it has changed.

Current SLO on the `slo` topic:
- Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s
- Date: 2026-10-05
- Status: active
- Source: `meetings/2026-10-05-cutover-planning.txt`

Earlier SLO that was superseded:
- Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%
- Date: 2026-01-26
- Status: superseded
- Source: `meetings/2026-01-26-weekly-sync.txt`

So right now, the live SLO is 3 s p95 for 30 days after the cutover, with a planned return to 2 s afterward.

### memory-eval-graph (completed, 4.7s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) OPTIONAL MATCH (d)-[:SUP"]

Yes — the SLO has changed.

- 2026-01-26, `meetings/2026-01-26-weekly-sync.txt`: **“Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%”** — this was `D02` and is now **superseded**.
- 2026-10-05, `meetings/2026-10-05-cutover-planning.txt`: **“Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s”** — this is `D28` and is **active**.

So **right now** the live SLO is:
- **p95 end-to-end delivery latency: 3 s for 30 days after the serverless cutover, then 2 s**
- source: `meetings/2026-10-05-cutover-planning.txt`, date `2026-10-05`

### memory-eval-vector (completed, 4.5s, 3 tool calls)
queries: ['Has the SLO ever changed? What is it right now?', 'SLO changed current SLO Relay webhook delivery project', 'service level objective SLO Relay webhook delivery project history current']

Yes — the SLO has changed.

- **Current SLO:** delivery latency p95 is **3 s for 30 days after the serverless cutover, then back to 2 s**; success rate is still **99.5% monthly**. Source: `meetings/2026-10-05-cutover-planning.txt` (2026-10-05), decision `D28`, active.
- **Previous SLO:** delivery latency p95 was **2 s over 5 minutes** and monthly success rate **99.5%**. Source: `meetings/2026-01-26-weekly-sync.txt` (2026-01-26), decision `D02`, superseded by `D28`.
- The doc `docs/slo.md` (updated 2026-01-28) is stale on the latency part, because it still says **2 s** with no stabilisation window, and the newer decision `D28` supersedes it.

If you want, I can also list the full SLO table including the `GET /deliveries/*` latency metric.

## m22 [ru / fact] Почему ADR-007 отклонили, какие цифры были у EKS?
**expected:** p95 0.4 с, но $6,100 в месяц, в 1.7 раза дороже Lambda, и второй кластер, который платформа не хочет эксплуатировать  
**expected sources:** {'sources': ['adr/ADR-007.md', 'docs/poc-eks-report.md', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 6.6s, 4 tool calls)
queries: ['ADR-007 Context why rejected EKS numbers results report', 'ADR-007 контекст почему отклонили EKS цифры результаты отчет', "MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:'ADR-007'}) RETURN n.id, n.title"]

ADR-007 отклонили потому, что EKS давал лучшую p95, но это не компенсировало рост затрат и операционную сложность.

Что было в памяти:
- В самом ADR сказано: «Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run).»  
  Источник: `adr/ADR-007.md`, дата `2026-08-05`.
- В разделе Consequences уточняется: «p95 is five times better than Lambda but monthly cost is 1.7x and the platform team would have to become a Kubernetes team.»  
  Источник: `adr/ADR-007.md`, дата `2026-08-05`.

Цифры по EKS:
- p95: `0.4 s`
- monthly cost: `1.7x` по сравнению с альтернативой
- дополнительно требовалось поддерживать `a second platform`
- также формулировка из контекста ADR-005: shared EKS cluster costs about `$6,100 a month`  
  Источник: `adr/ADR-005.md`, дата `2026-06-17` — это контекст для сравнения.

Статус ADR-007:
- `Rejected`
- дата: `2026-08-05`
- файл: `adr/ADR-007.md`

Если хотите, я могу ещё кратко сопоставить ADR-007 с ADR-006: что именно было живым решением вместо EKS.

### memory-eval-graph (completed, 7.0s, 6 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (d:Decision {id:'D07'}) RETURN d.id, d.text, d.date, d.status, d.source, d", "MATCH (d:Decision)-[:RECORDED_IN]->(a:ADR {id:'ADR-007'}) RETURN d.text, d.date,", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'compute'}) WHERE d.text STARTS WITH '", "MATCH (c:PoC {name:'Relay on EKS'}) RETURN c.name, c.results, c.report", "MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'Keep Relay on "]

ADR-007 отклонили потому, что для EKS в решении зафиксировали: p95 = 0.4 s, но это было в 1.7 раза дороже по месячной стоимости и добавляло “a second platform to run”. Источник: `meetings/2026-08-03-architecture-committee.txt`, дата `2026-08-03`.

Что по EKS зафиксировано в памяти:
- `p95_s`: `0.4`
- `monthly_cost_usd`: `6100`
- `ops_effort`: `a second platform team`

Источник: `docs/poc-eks-report.md` (PoC-2: Relay on EKS with autoscaling), дата исходного решения/ссылки в решении: `2026-08-03`.

Также сам ADR-007:
- `ADR-007` — `Rejected`
- файл: `adr/ADR-007.md`
- дата: `2026-08-05`

Источник: `adr/ADR-007.md`, дата `2026-08-05`.

Если хотите, могу ещё кратко свести это в одну строку “почему выбрали не EKS, а серверлес”.

### memory-eval-vector (completed, 3.4s, 3 tool calls)
queries: ['Почему ADR-007 отклонили, какие цифры были у EKS?', 'ADR-007 rejected EKS numbers', 'ADR-007 отклонили EKS цифры']

ADR-007 отклонили из-за компромисса по стоимости и операционной сложности: в решении указано, что у EKS была p95 **0.4 s**, но это стоило **в 1.7 раза больше в месяц** и означало **ещё одну платформу в эксплуатации**. Источник: `adr/ADR-007.md`, дата **2026-08-05**.

Ещё в последствиях сказано, что p95 у EKS был **в пять раз лучше, чем у Lambda**, но месячная стоимость всё равно была **1.7x**, и команде платформы пришлось бы стать Kubernetes-командой. Источник: `adr/ADR-007.md`, дата **2026-08-05**.

Если хотите, могу ещё коротко сравнить это с ADR-006 по тем же цифрам.

## t01 [en / current] What is the current decision on infrastructure as code, and when was it made?
**expected:** Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation (decided 2026-04-20, owner Pavel Grishin)  
**expected sources:** {'sources': ['meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 3.5s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERSE"]

The current decision on infrastructure as code is:

- **Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation**
- **Made on:** 2026-04-20
- **Source:** `meetings/2026-04-20-weekly-sync.txt`

If you want, I can also give the decision history on this topic.

### memory-eval-graph (completed, 3.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERSE"]

The current decision on infrastructure as code is: **“Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation”** — **source:** `meetings/2026-04-20-weekly-sync.txt`, **date:** `2026-04-20`, **status:** `active`.

### memory-eval-vector (completed, 3.0s, 3 tool calls)
queries: ['What is the current decision on infrastructure as code, and when was it made?', 'current decision infrastructure as code made date Relay webhook delivery project', 'infrastructure as code decision current status date']

The current decision is **hybrid IaC: networking stays in Terraform, while application stacks move to CloudFormation**. It is recorded as **ADR-004** and marked as superseding ADR-001. Source: **confluence/decision-log.xhtml**, dated **2026-06-03**.

The older decision to **migrate infrastructure code from Terraform to CloudFormation** is now **superseded**. Source: **adr/ADR-001.md**, dated **2026-01-14**.

## t02 [ru / history] Как менялось решение по теме «infrastructure as code»? Перечисли по датам.
**expected:** 2026-01-12: Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1 → 2026-02-09: One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway) → 2026-02-23: Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call → 2026-04-20: Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-02-09-weekly-sync.txt', 'meetings/2026-02-23-incident-review.txt', 'meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 6.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (d)-[:SUP"]

По теме «infrastructure as code» решения менялись так:

- 2026-01-12 — **D01**: «Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1»  
  Статус: superseded  
  Источник: `meetings/2026-01-12-weekly-sync.txt`

- 2026-02-09 — **D03**: «One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)»  
  Статус: active  
  Источник: `meetings/2026-02-09-weekly-sync.txt`

- 2026-02-23 — **D04**: «Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call»  
  Статус: active  
  Источник: `meetings/2026-02-23-incident-review.txt`

- 2026-04-20 — **D09**: «Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation»  
  Статус: active  
  Источник: `meetings/2026-04-20-weekly-sync.txt`

Если хочешь, я могу ещё кратко показать, **какое решение сейчас в силе** по IaC.

### memory-eval-graph (completed, 6.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (d)-[:SUP"]

По теме **infrastructure as code** решения менялись так, по датам:

- **2026-01-12** — **D01**: «Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1»  
  Статус: **superseded**.  
  Источник: `meetings/2026-01-12-weekly-sync.txt`

- **2026-02-09** — **D03**: «One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)»  
  Статус: **active**.  
  Источник: `meetings/2026-02-09-weekly-sync.txt`

- **2026-02-23** — **D04**: «Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call»  
  Статус: **active**.  
  Источник: `meetings/2026-02-23-incident-review.txt`

- **2026-04-20** — **D09**: «Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation»  
  Статус: **active**.  
  Источник: `meetings/2026-04-20-weekly-sync.txt`

Если хочешь, я могу ещё отдельно показать **какое решение сейчас в силе** по теме IaC.

### memory-eval-vector (completed, 8.0s, 3 tool calls)
queries: ['Как менялось решение по теме «infrastructure as code»? Перечисли по датам.', 'infrastructure as code decision dates changes', 'infrastructure as code']

По теме **infrastructure as code** нашёл такую хронологию решений:

- **2026-01-12** — решить **мигрировать Relay infrastructure code с Terraform на CloudFormation**, по модулям, до конца Q1.  
  Источник: `meetings/2026-01-12-weekly-sync.txt` (claim `D01`, статус `superseded`), и зафиксировано в `adr/ADR-001.md` от **2026-01-14**.

- **2026-04-20** — решение **изменено на гибридную схему**: networking остаётся в Terraform, а application stacks — в CloudFormation. Это **переопределяет ADR-001**.  
  Источник: `confluence/decision-log.xhtml` от **2026-06-03** (запись за **2026-04-20**, статус `[ACTIVE]`), также указано в `confluence/migration-roadmap.xhtml` от **2026-06-20**.

- **2026-06-20** — в roadmap тема уже описана как **“Terraform to CloudFormation, revised to a hybrid in April (ADR-004)”**, то есть текущая формулировка подтверждает гибридный вариант.  
  Источник: `confluence/migration-roadmap.xhtml` от **2026-06-20**.

Если кратко:  
**Terraform → CloudFormation (12 янв 2026) → hybrid: Terraform для networking + CloudFormation для application stacks (20 апр 2026).**

Источники:
- `meetings/2026-01-12-weekly-sync.txt` — **2026-01-12**
- `adr/ADR-001.md` — **2026-01-14** (ус

## t03 [en / current] What is the current decision on gateway timeout, and when was it made?
**expected:** Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom (decided 2026-08-24, owner Ivan Melnik)  
**expected sources:** {'sources': ['meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.1s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE NOT (d)<-[:SU"]

The current decision on gateway timeout is:

- **Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom**
- **Date made:** 2026-08-24
- **Status:** active
- **Source:** `meetings/2026-08-24-weekly-sync.txt`



### memory-eval-graph (completed, 3.9s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.text CONTAI", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) RETURN d.text, d.da"]

Current decision: **Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom**.  
It was made on **2026-08-24**.  
Source: **meetings/2026-08-24-weekly-sync.txt**.

### memory-eval-vector (completed, 3.1s, 3 tool calls)
queries: ['What is the current decision on gateway timeout, and when was it made?', 'gateway timeout decision current made date', 'gateway timeout']

The current decision in memory is **gateway integration timeout = 25 s**, and it was made on **2026-08-24**.

Source:
- `meetings/2026-08-24-weekly-sync.txt` — decision **D20**, status **active**, dated **2026-08-24**: “Gateway integration timeout lowered from 30 s to 25 s… Supersedes D12.”

Note:
- There is a newer document `adr/ADR-010.md` updated **2026-09-23**, but it says **no decision recorded** and is marked **Proposed**, so it does not supersede D20.


## t04 [ru / history] Как менялось решение по теме «gateway timeout»? Перечисли по датам.
**expected:** 2026-03-16: Gateway integration timeout 10 s on every Relay route → 2026-05-18: Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14 → 2026-08-24: Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom  
**expected sources:** {'sources': ['meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 6.0s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.text CONTAI", "MATCH (d:Decision)-[:ABOUT]->(t:Topic) WHERE t.name CONTAINS 'timeout' OR t.alia"]

По теме «gateway timeout» решение менялось так:

- **2026-03-16** — «Gateway integration timeout 10 s on every Relay route»  
  Источник: `meetings/2026-03-16-weekly-sync.txt`  
  Статус: `superseded`

- **2026-05-18** — «Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14»  
  Источник: `meetings/2026-05-18-weekly-sync.txt`  
  Статус: `superseded`

- **2026-08-24** — «Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom»  
  Источник: `meetings/2026-08-24-weekly-sync.txt`  
  Статус: `active`

Если хочешь, могу ещё показать, какое решение сейчас в силе и почему оно сменилось.

### memory-eval-graph (completed, 4.7s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'})\nOPTIONAL MATCH (d)-"]

По теме «gateway timeout» решение менялось так:

- 2026-03-16 — «Gateway integration timeout 10 s on every Relay route»  
  source: `meetings/2026-03-16-weekly-sync.txt`

- 2026-05-18 — «Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14»  
  source: `meetings/2026-05-18-weekly-sync.txt`

- 2026-08-24 — «Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom»  
  source: `meetings/2026-08-24-weekly-sync.txt`

Если нужно, могу ещё показать, какое из этих решений сейчас в силе.

### memory-eval-vector (completed, 4.6s, 3 tool calls)
queries: ['Как менялось решение по теме «gateway timeout»? Перечисли по датам.', 'gateway timeout решение по датам', 'gateway timeout decision dates']

Вот хронология решения по теме **gateway timeout** из памяти:

- **2026-03-16** — timeout на всех Relay routes установлен в **10 s**.  
  Источник: `meetings/2026-03-16-weekly-sync.txt` (claim D06, статус: superseded).

- **2026-05-18** — timeout увеличен с **10 s до 30 s** после инцидента со slow target от 2026-05-14.  
  Источник: `meetings/2026-05-18-weekly-sync.txt` (claim D12, статус: superseded).

- **2026-08-24** — timeout снижен с **30 s до 25 s**: у gateway hard limit **29 s**, нужен запас для Lambda.  
  Источник: `meetings/2026-08-24-weekly-sync.txt` (claim D20, статус: active).

Текущее решение в памяти — **25 s**, и оно **не superseded**.  
Если нужно, могу ещё коротко показать, какие документы стали устаревшими из-за этих решений.

## t05 [en / chain] The current decision on gateway timeout replaced an earlier one. What did that earlier decision itself replace, and when?
**expected:** Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom (2026-08-24) replaced 'Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14' (2026-05-18), which replaced 'Gateway integration timeout 10 s on every Relay route' (2026-03-16)  
**expected sources:** {'sources': ['meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.4s, 1 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE NOT (cur)<-"]

The earlier timeout decision replaced this older one:

- **Decision:** “Gateway integration timeout 10 s on every Relay route”
- **When:** **2026-03-16**
- **Source:** `meetings/2026-03-16-weekly-sync.txt`

Assumption: by “the earlier decision” I took the decision immediately superseded by the current gateway timeout decision.

### memory-eval-graph (completed, 5.8s, 3 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE cur.text CO", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.text CONTAI", "MATCH path=(cur:Decision {id:'D12'})-[:SUPERSEDES*1..5]->(old:Decision) RETURN ["]

The earlier decision was **D06**: “Gateway integration timeout 10 s on every Relay route” — dated **2026-03-16** and sourced from **meetings/2026-03-16-weekly-sync.txt**. It was later replaced by **D12** on **2026-05-18**, and then D12 was itself replaced by the current decision.

### memory-eval-vector (completed, 2.7s, 3 tool calls)
queries: ['The current decision on gateway timeout replaced an earlier one. What did that e', 'gateway timeout decision replaced earlier one what did that earlier decision rep', 'gateway timeout current decision earlier decision replaced what did it replace w']

The earlier decision was **D12**, and it **replaced D06** on **2026-05-18**.

Sources:
- **meetings/2026-05-18-weekly-sync.txt** — claim **D12**, dated **2026-05-18**: “Supersedes D06.”
- **meetings/2026-03-16-weekly-sync.txt** — claim **D06**, dated **2026-03-16**: “Gateway integration timeout 10 s on every Relay route.”

## t06 [en / current] What is the current decision on retries, and when was it made?
**expected:** Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off (decided 2026-08-24, owner Anna Sokolova)  
**expected sources:** {'sources': ['meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.1s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (d)<-[:SUP"]

Current decision on retries: **Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off.**  
Status: **active**  
Made on: **2026-08-24**  
Source: **meetings/2026-08-24-weekly-sync.txt**

Note: **docs/gateway.md (updated 2026-03-18) still describes gateway retries at all; ADR-002 section Retries is stale since 2026-08-24**

### memory-eval-graph (completed, 2.9s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (d)<-[:SUP"]

Current decision on retries: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off.” Source: `meetings/2026-08-24-weekly-sync.txt`, date `2026-08-24`, status `active`.

It was made on `2026-08-24`.

### memory-eval-vector (completed, 4.6s, 3 tool calls)
queries: ['What is the current decision on retries, and when was it made?', 'current decision on retries made date', 'retries decision status date']

The current decision is:

- Retries are handled in SQS with a dead-letter queue after 5 attempts.
- Gateway retries on `POST /deliver` are turned off.
- This decision supersedes the earlier gateway-retry decision.

Source:
- `meetings/2026-08-24-weekly-sync.txt` — decision dated **2026-08-24** (claim D21, ADR-009), status **active**
- `adr/ADR-009.md` — updated **2026-08-26**, status **Accepted**
- `docs/retries-dlq.md` — updated **2026-08-27**, notes the decision was made **2026-08-24**

Note: `docs/gateway.md` updated **2026-03-18** still describes gateway retries and is stale relative to the 2026-08-24 decision.

## t07 [ru / history] Как менялось решение по теме «retries»? Перечисли по датам.
**expected:** 2026-03-30: Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice → 2026-06-15: Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15% → 2026-08-24: Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off  
**expected sources:** {'sources': ['meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 5.6s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) OPTIONAL MATCH (d)-["]

Вот как менялось решение по теме «retries», по датам:

- **2026-03-30** — **D07**: “Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice”  
  Статус: **superseded**  
  Источник: `meetings/2026-03-30-weekly-sync.txt`

- **2026-06-15** — **D14**: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%”  
  Статус: **superseded**  
  Источник: `meetings/2026-06-15-weekly-sync.txt`

- **2026-08-24** — **D21**: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”  
  Статус: **active**  
  Источник: `meetings/2026-08-24-weekly-sync.txt`

Если хочешь, я могу ещё коротко показать это как цепочку “что было заменено чем”.

### memory-eval-graph (completed, 4.4s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) OPTIONAL MATCH (d)-["]

По теме **retries** решение менялось так:

- **2026-03-30** — **D07**: «Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice»  
  Статус: superseded. Источник: `meetings/2026-03-30-weekly-sync.txt`

- **2026-06-15** — **D14**: «Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%»  
  Статус: superseded. Источник: `meetings/2026-06-15-weekly-sync.txt`

- **2026-08-24** — **D21**: «Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off»  
  Статус: active. Источник: `meetings/2026-08-24-weekly-sync.txt`

Если нужно, могу ещё показать это как цепочку «что было заменено чем».

### memory-eval-vector (completed, 8.1s, 3 tool calls)
queries: ['Как менялось решение по теме «retries»? Перечисли по датам.', 'retries decision dates changes', 'retry retries policy decision updated date']

По теме **retries** в памяти есть такая хронология:

- **2026-03-04** — retries в gateway-архитектуре: для `POST /deliver` они **disabled until idempotency keys exist**; read routes могут retry twice, и retries тогда были частью **gateway policy**.  
  Источник: `adr/ADR-002.md` (updated **2026-03-04**).

- **2026-03-30** — решение уточнили/переформулировали как: `POST /deliver` **disabled** на gateway **until idempotency keys exist**; read routes retry up to two times.  
  Источник: `meetings/2026-03-30-weekly-sync.txt` (date **2026-03-30**), claim **D07**.

- **2026-06-15** — retries на `POST /deliver` **enabled** на gateway: **max 3 attempts**, retry budget **15%**.  
  Источник: `meetings/2026-06-15-weekly-sync.txt` (date **2026-06-15**), claim **D14**.

- **2026-08-24** — retries **перенесли из gateway в SQS + dead-letter queue**, после **5 attempts**; gateway retries on `/deliver` **turned off**. Это текущая активная версия решения.  
  Источник: `meetings/2026-08-24-weekly-sync.txt` (date **2026-08-24**), claim **D21**.

Что ещё видно из памяти:
- `D07` от **2026-03-30** помечен **superseded** и superseded by `D14`.
- `D14` от **2026-06-15** помечен **superseded** и supersed

## t08 [en / chain] The current decision on retries replaced an earlier one. What did that earlier decision itself replace, and when?
**expected:** Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off (2026-08-24) replaced 'Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%' (2026-06-15), which replaced 'Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice' (2026-03-30)  
**expected sources:** {'sources': ['meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 7.7s, 2 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (cur)<-[", 'MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision) WHERE (cur)-[:ABOUT']

The earlier retries decision replaced this one:

- **“Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice”**
- **Date:** 2026-03-30
- **Source:** `meetings/2026-03-30-weekly-sync.txt`

So, the replacement chain is:

1. **2026-03-30** — retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice  
   Source: `meetings/2026-03-30-weekly-sync.txt`
2. **2026-06-15** — retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%  
   Source: `meetings/2026-06-15-weekly-sync.txt`
3. **2026-08-24** — retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off  
   Source: `meetings/2026-08-24-weekly-sync.txt`

The decision immediately replaced by the current one is the **2026-06-15** decision, and that earlier decision itself replaced the **2026-03-30** decision.

### memory-eval-graph (completed, 4.9s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (d)<-[:SUP", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) OPTIONAL MATCH (d)-["]

The earlier decision was **D14**, and it replaced **D07**.

- **D07**: “Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice”  
  - **Date:** 2026-03-30  
  - **Status:** superseded  
  - **Source:** `meetings/2026-03-30-weekly-sync.txt`

So, the earlier decision itself replaced **D07 on 2026-03-30**.

### memory-eval-vector (completed, 3.8s, 3 tool calls)
queries: ['The current decision on retries replaced an earlier one. What did that earlier d', 'current decision retries replaced earlier one what did earlier decision replace ', 'retries decision replaced earlier decision superseded replaced what when']

The earlier decision was **D14**, dated **2026-06-15**: retries were enabled on `POST /deliver` at the gateway with **max 3 attempts** and a **15% retry budget**. It **superseded D07**.  
Source: **meetings/2026-06-15-weekly-sync.txt** / claim D14, dated **2026-06-15**.

For context, the current decision is **D21** on **2026-08-24**, which says retries moved to SQS with a DLQ and **supersedes D14**.  
Source: **meetings/2026-08-24-weekly-sync.txt** / claim D21, dated **2026-08-24**.

## t09 [en / current] What is the current decision on compute platform, and when was it made?
**expected:** Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances (decided 2026-08-03, owner Ivan Melnik)  
**expected sources:** {'sources': ['meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 3.1s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE NOT (d)<-[:SUP"]

The current compute-platform decision is: **Relay moves to Lambda with provisioned concurrency on `/deliver`; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances**.

It was made on **2026-08-03**.

Source: `meetings/2026-08-03-architecture-committee.txt` (decision date `2026-08-03`).

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE NOT (d)<-[:SUP"]

The current compute-platform decision is: Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances. Source: `meetings/2026-08-03-architecture-committee.txt`, dated `2026-08-03`.

### memory-eval-vector (completed, 3.2s, 3 tool calls)
queries: ['What is the current decision on compute platform, and when was it made?', 'current decision compute platform made date', 'decision on compute platform']

The current decision on compute is: **move Relay to Lambda with provisioned concurrency on `/deliver`**. It was made on **2026-08-03**.

Source:
- `meetings/2026-08-03-architecture-committee.txt` — decision claim dated **2026-08-03**: “Relay moves to Lambda with provisioned concurrency on /deliver … Supersedes D15.”  
- This is recorded as **active** and supersedes the earlier EKS decision.

Note: I also found an ADR-007 document updated **2026-08-05** that says **“Rejected on 2026-08-03”** for keeping Relay on EKS with autoscaling, which aligns with Lambda being the current decision.

## t10 [ru / history] Как менялось решение по теме «compute platform»? Перечисли по датам.
**expected:** 2026-06-15: Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July → 2026-08-03: Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances  
**expected sources:** {'sources': ['meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 5.1s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE d.date <= '999"]

По теме «compute platform» решение менялось так:

- 2026-06-15 — **D15**: «Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July»  
  source: `meetings/2026-06-15-weekly-sync.txt`

- 2026-08-03 — **D18**: «Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)»  
  status: `rejected`  
  source: `meetings/2026-08-03-architecture-committee.txt`

- 2026-08-03 — **D17**: «Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances»  
  status: `active`  
  source: `meetings/2026-08-03-architecture-committee.txt`

Если хочешь, я могу ещё кратко показать, какое из этих решений сейчас в силе и какое предыдущее оно заменило.

### memory-eval-graph (completed, 4.4s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) OPTIONAL MATCH (d)-["]

По теме «compute platform» решение менялось так:

- 2026-06-15 — **D15** — `superseded` — `meetings/2026-06-15-weekly-sync.txt`  
  `Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July`

- 2026-08-03 — **D17** — `active` — `meetings/2026-08-03-architecture-committee.txt`  
  `Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances`

- 2026-08-03 — **D18** — `rejected` — `meetings/2026-08-03-architecture-committee.txt`  
  `Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)`

Если нужно, могу ещё кратко свести это в «что было решено в итоге» и «какое решение заменило какое».

### memory-eval-vector (completed, 9.4s, 4 tool calls)
queries: ['Как менялось решение по теме «compute platform»? Перечисли по датам.', 'compute platform', 'compute platform decision', 'compute platform EKS Lambda ADR']

По теме **compute platform** решение менялось так:

- **2026-06-17** — решили **проводить два PoC параллельно: EKS with autoscaling и Lambda**, а финальное решение отложить до конца июля.  
  Источник: `adr/ADR-005.md` / `Decision` и `docs/confluence`-копия в `ADR-005`, дата 2026-06-17.  
  Это решение позже стало **superseded**.

- **2026-08-03** — после PoC решили **перейти на Lambda с provisioned concurrency на `/deliver`**; указано, что PoC-3 дал **41% меньшую стоимость** и **p95 1.9 s**.  
  Источник: `meetings/2026-08-03-architecture-committee.txt` / claim `decision:compute:2026-08-03`, дата 2026-08-03.  
  Этот decision **active** и **supersedes D15**.

- **2026-08-05** — в ADR-006 зафиксировано то же решение: **Run Relay on Lambda with provisioned concurrency**, статус **Accepted, supersedes ADR-005**.  
  Источник: `adr/ADR-006.md`, дата 2026-08-05.  
  Это подтверждает решение от 2026-08-03.

- **2026-08-05** — отдельно есть **ADR-007: Keep Relay on EKS with autoscaling**, но он **Rejected**; в нём прямо сказано, что отклонён 2026-08-03.  
  Источник: `adr/ADR-007.md`, дата 2026-08-05.  
  Это не текущее решение, а отклонённая альтернатива.

Если нужно, могу ещё свести эт

## t11 [en / current] What is the current decision on SLO, and when was it made?
**expected:** Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s (decided 2026-10-05, owner Lena Kim)  
**expected sources:** {'sources': ['meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 3.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

Current decision on SLO: “Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s”.

It was made on 2026-10-05.

Source: meetings/2026-10-05-cutover-planning.txt, 2026-10-05.

### memory-eval-graph (completed, 2.6s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

Current SLO decision: **Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s**. It was made on **2026-10-05**.  
Source: **meetings/2026-10-05-cutover-planning.txt**.

### memory-eval-vector (completed, 3.8s, 3 tool calls)
queries: ['What is the current decision on SLO, and when was it made?', 'current decision on SLO made date decision', 'SLO decision current status date']

The current SLO decision is: delivery p95 SLO is relaxed from **2 s to 3 s for 30 days after the serverless cutover, then back to 2 s**. It is marked **active** and **supersedes D02**. Source: `meetings/2026-10-05-cutover-planning.txt`, dated **2026-10-05**.

I also found older/stale material:
- `docs/slo.md` says **2 s / 99.5%** and was updated **2026-01-28**; it is stale because the newer decision on the same topic is from **2026-10-05**.
- `meetings/2026-01-26-weekly-sync.txt` records the earlier **2 s / 99.5%** decision, but it is **superseded** by D28.

## t12 [ru / history] Как менялось решение по теме «SLO»? Перечисли по датам.
**expected:** 2026-01-26: Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5% → 2026-10-05: Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s  
**expected sources:** {'sources': ['meetings/2026-01-26-weekly-sync.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 4.4s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) OPTIONAL MATCH (d)-[:SUP"]

По теме **SLO** в памяти есть такие решения, по датам:

- **2026-01-26** — **D02**: “Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%” — **superseded**.  
  Источник: `meetings/2026-01-26-weekly-sync.txt`

- **2026-10-05** — **D28**: “Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s” — **active**.  
  Источник: `meetings/2026-10-05-cutover-planning.txt`

Если нужно, могу ещё кратко показать цепочку, как именно D28 изменил D02.

### memory-eval-graph (completed, 3.6s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) RETURN d.text, d.date, d"]

По теме **SLO** решение менялось так:

- **2026-01-26** — «Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%»; **status:** superseded; **source:** `meetings/2026-01-26-weekly-sync.txt`.
- **2026-10-05** — «Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s»; **status:** active; **source:** `meetings/2026-10-05-cutover-planning.txt`.

Если нужно, могу ещё показать, какое решение было **в силе на конкретную дату**.

### memory-eval-vector (completed, 5.4s, 3 tool calls)
queries: ['Как менялось решение по теме «SLO»? Перечисли по датам.', 'SLO решение по теме по датам', 'изменение решения по теме SLO']

По теме **SLO** в памяти есть два решения, и текущее — более позднее:

- **2026-01-26** — SLO: p95 end-to-end delivery latency **2 s** за окно **5 минут**; monthly delivery success rate **99.5%**.  
  Источник: `meetings/2026-01-26-weekly-sync.txt` (claim `D02`), статус **superseded**.  
- **2026-10-05** — SLO по p95 delivery latency **смягчён с 2 s до 3 s на 30 дней после serverless cutover**, затем вернуть **2 s**.  
  Источник: `meetings/2026-10-05-cutover-planning.txt` (claim `D28`), статус **active**.

Итог: **текущее решение — от 2026-10-05; оно supersedes решение от 2026-01-26**.

Что я нашёл в памяти:
- `meetings/2026-01-26-weekly-sync.txt` — решение `D02` от 2026-01-26
- `meetings/2026-10-05-cutover-planning.txt` — решение `D28` от 2026-10-05
- `docs/slo.md` updated 2026-01-28 — уже **устаревший** относительно решения от 2026-10-05

## t13 [ru / owner_now] Кто сейчас владеет темой «retries» и с какой даты?
**expected:** Ivan Melnik, с 2026-09-07  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 3.0s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.to IS NULL RE"]

Тему «retries» сейчас владеет Ivan Melnik, с 2026-09-07.

Источник: граф памяти (OWNS), дата начала владения: 2026-09-07.

### memory-eval-graph (completed, 3.2s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.to IS NULL RE"]

Темой «retries» сейчас владеет **Ivan Melnik** — с **2026-09-07**.  
Источник: граф памяти, связь OWNS по `topic:retries`; дата начала владения: `2026-09-07`.

### memory-eval-vector (completed, 3.5s, 3 tool calls)
queries: ['Кто сейчас владеет темой «retries» и с какой даты?', 'who owns retries and from what date?', 'ownership retries from date current owner']

Сейчас темой **retries** владеет **Ivan Melnik** — с **2026-09-07**.  
Источник: `memory/decisions.jsonl`, запись `claim ownership | retries | 2026-09-07` (status: active).

Есть ещё более старая запись:
- `Anna Sokolova` — с `2026-06-01` до `2026-09-07` (`memory/decisions.jsonl`, status: superseded).

Также нашёлся документ `docs/retries-dlq.md` (updated `2026-08-27`), где сказано, что retries принадлежат Relay core lead до serverless cutover, но он старее текущей decision-записи и поэтому устарел.

## t14 [en / owner_at] Who owned retries on 2026-06-15?
**expected:** Anna Sokolova (from 2026-06-01 to 2026-09-07)  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 2.7s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.from <= '2026"]

Anna Sokolova owned retries on 2026-06-15. Source: graph ownership edge, effective from 2026-06-01 to 2026-09-07.

### memory-eval-graph (completed, 2.7s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.from <= $D AN"]

Anna Sokolova owned retries on 2026-06-15. Source: graph memory OWNS edge to topic:retries, from 2026-06-01 to 2026-09-07.

### memory-eval-vector (completed, 4.3s, 3 tool calls)
queries: ['Who owned retries on 2026-06-15?', 'retries ownership 2026-06-15', 'owner of retries on 2026-06-15']

On 2026-06-15, **Anna Sokolova** owned retries.

Sources:
- `memory/decisions.jsonl`, 2026-06-01: “Anna Sokolova owns retries from 2026-06-01 to 2026-09-07.” This interval includes 2026-06-15.
- `meetings/2026-06-01-weekly-sync.txt`, 2026-06-01: ownership moved from Nikita to Anna.

I also retrieved a newer ownership decision:
- `memory/decisions.jsonl`, 2026-09-07: “Ivan Melnik owns retries from 2026-09-07 (current).”

So the answer for 2026-06-15 is Anna Sokolova.

## t15 [ru / owner_now] Кто сейчас владеет темой «compute platform» и с какой даты?
**expected:** Ivan Melnik, с 2026-07-13  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt']}

### memory-eval-both (completed, 2.7s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.to IS NULL RE"]

Темой «compute platform» сейчас владеет Ivan Melnik с 2026-07-13.

Источник: граф знаний; дата владения — 2026-07-13.

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.to IS NULL RE"]

Тему «compute platform» сейчас владеет Иван Мельник, с 2026-07-13.  
Источник: граф памяти, тема `topic:compute`, дата владения `2026-07-13`.

### memory-eval-vector (completed, 2.6s, 3 tool calls)
queries: ['Кто сейчас владеет темой «compute platform» и с какой даты?', 'compute platform owner from date current owner', 'ownership compute platform']

Сейчас темой **compute** владеет **Ivan Melnik** с **2026-07-13**.  
Источник: **memory/decisions.jsonl** — запись `ownership:compute:2026-07-13` (active).

Есть более ранняя, уже **superseded** запись: **Sergey Belov** владел compute с **2026-06-15** до **2026-07-13**.  
Источник: **memory/decisions.jsonl** — запись `ownership:compute:2026-06-15`.

Если хотите, могу ещё проверить, есть ли в памяти отдельная тема именно под названием **“compute platform”**.

## t16 [en / owner_at] Who owned compute platform on 2026-06-28?
**expected:** Sergey Belov (from 2026-06-15 to 2026-07-13)  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt']}

### memory-eval-both (completed, 3.4s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.from <= '2026"]

On 2026-06-28, **Sergey Belov** owned **compute platform**.

- Source: graph ownership edge
- Ownership period: **2026-06-15** to **2026-07-13**

Assumption: I matched “compute platform” to the fixed topic **topic:compute**.

### memory-eval-graph (completed, 2.9s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.from <= '2026"]

Sergey Belov owned compute platform on 2026-06-28. Source: memory graph ownership edge to `topic:compute`, from 2026-06-15 to 2026-07-13.

### memory-eval-vector (completed, 3.0s, 3 tool calls)
queries: ['Who owned compute platform on 2026-06-28?', 'compute platform owner 2026-06-28', 'ownership of compute platform on 2026-06-28']

Compute platform was owned by **Sergey Belov** on **2026-06-28**. The claim says Sergey Belov owned compute from **2026-06-15 to 2026-07-13**, so 2026-06-28 falls in that range.  
Source: **memory/decisions.jsonl** (date **2026-06-15**), and the newer ownership claim **memory/decisions.jsonl** (date **2026-07-13**) confirms the later owner changed after that date.

## t17 [ru / owner_now] Кто сейчас владеет темой «idempotency» и с какой даты?
**expected:** Anna Sokolova, с 2026-06-01  
**expected sources:** {'sources': []}

### memory-eval-both (completed, 2.0s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.to IS NUL"]

Темой «idempotency» сейчас владеет Anna Sokolova с 2026-06-01.

Источник: граф знаний; дата владения: 2026-06-01.

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.to IS NUL"]

Темой «idempotency» сейчас владеет **Anna Sokolova** с **2026-06-01**. Источник: граф памяти, связь OWNS к теме `topic:idempotency` (дата владения: 2026-06-01).

### memory-eval-vector (completed, 1.9s, 1 tool calls)
queries: ['Кто сейчас владеет темой «idempotency» и с какой даты?']

Сейчас темой **idempotency** владеет **Anna Sokolova** — **с 2026-06-01**.  
Источник: `memory/decisions.jsonl`, запись `claim ownership | idempotency | 2026-06-01` (active).

## t18 [en / owner_at] Who owned idempotency on 2026-05-28?
**expected:** Nikita Frolov (from 2026-05-18 to 2026-06-01)  
**expected sources:** {'sources': []}

### memory-eval-both (completed, 4.0s, 2 tool calls)
queries: ["MATCH (:Topic {key:'topic:idempotency'})<-[:OWNS]-(p:Person)-[o:OWNS]->(:Topic {", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.from <= '"]

Nikita Frolov owned idempotency on 2026-05-28.

- Source: graph OWNS edge
- Dates: from 2026-05-18 to 2026-06-01

### memory-eval-graph (completed, 3.1s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.from <= $"]

On 2026-05-28, **Nikita Frolov** owned **idempotency**. Source: ownership edge for `topic:idempotency`, effective from **2026-05-18** to **2026-06-01**.

### memory-eval-vector (completed, 3.5s, 3 tool calls)
queries: ['Who owned idempotency on 2026-05-28?', 'idempotency owner 2026-05-28', 'ownership idempotency from date to date owner']

On 2026-05-28, **Nikita Frolov** owned idempotency.

Sources:
- `meetings/2026-05-18-weekly-sync.txt` — 2026-05-18: “Owner: Nikita Frolov.” This ownership runs from 2026-05-18 to 2026-06-01.
- `memory/decisions.jsonl` — 2026-05-18: ownership claim says Nikita Frolov owns idempotency from 2026-05-18 to 2026-06-01.
- `memory/decisions.jsonl` — 2026-06-01: later claim says Anna Sokolova owns idempotency from 2026-06-01 (current).

The 2026-06-01 decision supersedes the earlier ownership starting on 2026-05-28.

## t19 [ru / objector] Кто предложил и кто возражал против решения «Migrate Relay infrastructure code from Terraform to CloudFor…»?
**expected:** proposer Pavel Grishin, objector Timur Aliev, 2026-01-12  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt']}

### memory-eval-both (completed, 2.1s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Migrate Relay infrastructure code f"]

Решение «Migrate Relay infrastructure code from Terraform to CloudFor…»:

- Предложил: Pavel Grishin
- Возражал: Timur Aliev

Источник: `meetings/2026-01-12-weekly-sync.txt`, дата решения: `2026-01-12`.

### memory-eval-graph (completed, 3.2s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Migrate Relay infrastructure code f"]

Предложил **Павел Гришин**; возражал **Тимур Алиев**.

Источник: `meetings/2026-01-12-weekly-sync.txt`, решение от `2026-01-12` — `Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1`.

### memory-eval-vector (completed, 3.9s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Migrate Relay infrastructure code f', 'Кто предложил решение «Migrate Relay infrastructure code from Terraform to Cloud', 'Migrate Relay infrastructure code from Terraform to CloudFormation proposer obje']

Решение **предложил Pavel Grishin**, а **возражал Timur Aliev**.

Источники:
- `meetings/2026-01-12-weekly-sync.txt` — 2026-01-12: “Proposed by Pavel Grishin; objection from Timur Aliev.”
- `adr/ADR-001.md` — 2026-01-14: “Objection recorded from Timur Aliev.”  
- Это решение сейчас **superseded**: `ADR-001` superseded by `ADR-004` (источник: `meetings/2026-01-12-weekly-sync.txt`, 2026-01-12; `adr/ADR-001.md`, 2026-01-14).



## t20 [en / objector] Who proposed and who objected to the decision 'Gateway integration timeout 10 s on every Relay route…'?
**expected:** proposer Pavel Grishin, objector Anna Sokolova, 2026-03-16  
**expected sources:** {'sources': ['meetings/2026-03-16-weekly-sync.txt']}

### memory-eval-both (completed, 2.9s, 1 tool calls)
queries: ['"Gateway integration timeout 10 s on every Relay route" proposed objected']

Proposed by **Pavel Grishin**; objected to by **Anna Sokolova**.

Source: `meetings/2026-03-16-weekly-sync.txt`, decision dated `2026-03-16` (`D06`, status `superseded`).

Assumption: you meant the decision text that starts with “Gateway integration timeout 10 s on every Relay route…”.

### memory-eval-graph (completed, 3.6s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout 10 s on"]

Proposed by Pavel Grishin, objected to by Anna Sokolova.

- Decision: “Gateway integration timeout 10 s on every Relay route”
- Date: 2026-03-16
- Status: superseded
- Source: meetings/2026-03-16-weekly-sync.txt

### memory-eval-vector (completed, 2.9s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'Gateway integration timeout 10 s ", 'Gateway integration timeout 10 s on every Relay route proposed objected', '"Gateway integration timeout 10 s on every Relay route" proposed objected']

Proposed by **Pavel Grishin** and objected to by **Anna Sokolova**.

Source:
- `meetings/2026-03-16-weekly-sync.txt` — `D06`, dated **2026-03-16**
- The same claim is also reflected in the source chunk from the meeting transcript dated **2026-03-16**.

Note: this decision is marked **superseded** by `D12`.

## t21 [ru / objector] Кто предложил и кто возражал против решения «Hybrid IaC: networking (VPC, peering, DNS) stays in Terrafor…»?
**expected:** proposer Sergey Belov, objector Pavel Grishin, 2026-04-20  
**expected sources:** {'sources': ['meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 1.9s, 1 tool calls)
queries: ['MATCH (d:Decision) WHERE d.text STARTS WITH $prefix OPTIONAL MATCH (a:Person)-[:']

Предложил **Сергей Белов**, возражал **Павел Гришин**.

Источник: `meetings/2026-04-20-weekly-sync.txt`, дата решения: `2026-04-20`.

### memory-eval-graph (completed, 2.9s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Hybrid IaC: networking (VPC, peerin"]

Предложил **Sergey Belov**, возражал **Pavel Grishin**.  
Источник: решение **“Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation”**, дата **2026-04-20**, файл **meetings/2026-04-20-weekly-sync.txt**.

### memory-eval-vector (completed, 3.4s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Hybrid IaC: networking (VPC, peerin', 'Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform proposed objected', 'Hybrid IaC networking VPC peering DNS stays in Terraform']

Решение предложил **Sergey Belov**, а возражал против него **Pavel Grishin** — это указано в записи о решении.  
Источник: `meetings/2026-04-20-weekly-sync.txt`, дата **2026-04-20**. В ADR это же подтверждено как objection recorded from Pavel Grishin. Источник: `adr/ADR-004.md`, дата **2026-04-22**.

Дополнительно: в памяти есть указание, что это решение **supersedes D01 / ADR-001**, то есть это текущая версия решения.

## t22 [en / objector] Who proposed and who objected to the decision 'DynamoDB single-table design, chosen on PoC-1 results (p99 r…'?
**expected:** proposer Denis Orlov, objector Timur Aliev, 2026-05-04  
**expected sources:** {'sources': ['meetings/2026-05-04-poc-review.txt']}

### memory-eval-both (completed, 2.4s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'DynamoDB single-table design, chose", '"DynamoDB single-table design, chosen on PoC-1 results" proposed objected']

Proposed by Denis Orlov; objected by Timur Aliev.

- Decision date: 2026-05-04
- Source: `meetings/2026-05-04-poc-review.txt`

### memory-eval-graph (completed, 2.5s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'DynamoDB single-table design, chose"]

Proposed by Denis Orlov and objected to by Timur Aliev.  
Source: `meetings/2026-05-04-poc-review.txt`, dated `2026-05-04`.

### memory-eval-vector (completed, 2.8s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'DynamoDB single-table design, cho", 'DynamoDB single-table design, chosen on PoC-1 results p99 read latency proposed ', 'single-table design PoC-1 p99 read latency proposer objector']

Proposed by **Denis Orlov** and objected to by **Timur Aliev**. Source: **meetings/2026-05-04-poc-review.txt** / **ADR-003**; date **2026-05-04**.

## t23 [en / objector] Who proposed and who objected to the decision 'Gateway integration timeout raised from 10 s to 30 s after t…'?
**expected:** proposer Anna Sokolova, objector Lena Kim, 2026-05-18  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt']}

### memory-eval-both (completed, 2.7s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout raised ", '"Gateway integration timeout raised from 10 s to 30 s after t" proposer objected']

Proposed by **Anna Sokolova** and objected to by **Lena Kim**.

Source: `meetings/2026-05-18-weekly-sync.txt`, 2026-05-18.

### memory-eval-graph (completed, 4.0s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout raised ", "MATCH (d:Decision) WHERE d.text CONTAINS 'Gateway integration timeout raised fro"]

Anna Sokolova proposed and Lena Kim objected to the decision “Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14” (D12, 2026-05-18, source: `meetings/2026-05-18-weekly-sync.txt`).

### memory-eval-vector (completed, 2.6s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'Gateway integration timeout raise", 'Gateway integration timeout raised from 10 s to 30 s after t', 'proposed objected Gateway integration timeout raised from 10 s to 30 s after t']

The decision was **proposed by Anna Sokolova** and **objected to by Lena Kim**.

Source: **meetings/2026-05-18-weekly-sync.txt** — **2026-05-18** (`claim D12`, status: superseded).

## t24 [ru / objector] Кто предложил и кто возражал против решения «Relay moves to Lambda with provisioned concurrency on /deliv…»?
**expected:** proposer Olga Petrova, objector Timur Aliev, 2026-08-03  
**expected sources:** {'sources': ['meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 2.6s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio"]

Решение «Relay moves to Lambda with provisioned concurrency on /deliv…»:

- Предложила: **Ольга Петрова**  
- Возражал: **Тимур Алиев**

Источник: `meetings/2026-08-03-architecture-committee.txt`, дата **2026-08-03**.

### memory-eval-graph (completed, 2.7s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio"]

Предложила: **Olga Petrova** — решение от **2026-08-03**, статус **active**, источник **meetings/2026-08-03-architecture-committee.txt**.  
Возражал: **Timur Aliev** — то же решение и источник.

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Relay moves to Lambda with provisio', 'Who proposed and who objected to the decision "Relay moves to Lambda with provis', 'Relay moves to Lambda with provisioned concurrency on /deliv decision proposed o']

Предложила **Ольга Петрова**, возражал **Тимур Алиев**.

Источники:
- `meetings/2026-08-03-architecture-committee.txt` — 2026-08-03: в claim D17 указано “Proposed by Olga Petrova; objection from Timur Aliev.”
- `adr/ADR-006.md` — 2026-08-05: в разделе Decision написано “Objection recorded from Timur Aliev.”

Если нужно, могу также процитировать фрагмент из протокола собрания.

## t25 [ru / objector] Кто предложил и кто возражал против решения «Retries move out of the gateway into SQS with a dead-letter …»?
**expected:** proposer Ivan Melnik, objector Anna Sokolova, 2026-08-24  
**expected sources:** {'sources': ['meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 2.0s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Retries move out of the gateway int"]

Решение «Retries move out of the gateway into SQS with a dead-letter …»:

- Предложил: Ivan Melnik
- Возражала: Anna Sokolova

Дата: 2026-08-24  
Источник: `meetings/2026-08-24-weekly-sync.txt`

### memory-eval-graph (completed, 3.9s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Retries move out of the gateway int", "MATCH (d:Decision) WHERE d.text CONTAINS 'Retries move out of the gateway into S"]

Предложил **Ivan Melnik** и возражала **Anna Sokolova**.

Источник: `meetings/2026-08-24-weekly-sync.txt`, дата `2026-08-24`.

### memory-eval-vector (completed, 4.2s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Retries move out of the gateway int', "Who proposed and who objected to the decision 'Retries move out of the gateway i", 'Retries move out of the gateway into SQS with a dead-letter']

Предложил **Ivan Melnik**; возражала **Anna Sokolova**.

Источник:
- `meetings/2026-08-24-weekly-sync.txt` — 2026-08-24: “Proposed by Ivan Melnik; objection from Anna Sokolova.”
- `adr/ADR-009.md` — 2026-08-26: “Objection recorded from Anna Sokolova.”

Также в памяти есть запись, что это решение было принято 2026-08-24 и оформлено в ADR-009.

## t26 [en / objector] Who proposed and who objected to the decision 'Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after t…'?
**expected:** proposer Lena Kim, objector Marat Yusupov, 2026-10-05  
**expected sources:** {'sources': ['meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 3.5s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Delivery p95 SLO relaxed from 2 s t", "MATCH (d:Decision) WHERE d.text CONTAINS 'Delivery p95 SLO relaxed from 2 s to 3"]

Proposed by Lena Kim; objected to by Marat Yusupov.

- Decision date: 2026-10-05
- Source: `meetings/2026-10-05-cutover-planning.txt`

### memory-eval-graph (completed, 4.2s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Delivery p95 SLO relaxed from 2 s t", "MATCH (d:Decision) WHERE d.text CONTAINS 'Delivery p95 SLO relaxed from 2 s to 3"]

Proposed by **Lena Kim** and objected to by **Marat Yusupov**.

Source: `meetings/2026-10-05-cutover-planning.txt`, decision dated `2026-10-05`:
- “Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s” (`active`)

### memory-eval-vector (completed, 3.3s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'Delivery p95 SLO relaxed from 2 s", 'Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after t… proposed objected', 'Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after t']

Lena Kim proposed it, and Marat Yusupov objected.  
Source: `meetings/2026-10-05-cutover-planning.txt` via claim `D28`, dated `2026-10-05`.

I also found a matching meeting excerpt in the same file showing:
- Lena: “I propose relaxing SLO p95 to three seconds for thirty days after cutover…”
- Marat: “I oppose…”

There is a contradiction with an older SLO doc:
- `docs/slo.md`, updated `2026-01-28`, still says the p95 delivery SLO is `2 s`.
- But the newer decision `D28` on `2026-10-05` supersedes the older decision `D02`, so `D28` is the current one.



## t27 [en / aggregate] How many decisions have been superseded, and on which topics?
**expected:** 7: D01 (infrastructure as code, 2026-01-12); D02 (SLO, 2026-01-26); D06 (gateway timeout, 2026-03-16); D07 (retries, 2026-03-30); D12 (gateway timeout, 2026-05-18); D14 (retries, 2026-06-15); D15 (compute platform, 2026-06-15)  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-01-26-weekly-sync.txt', 'meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt']}

### memory-eval-both (completed, 2.8s, 1 tool calls)
queries: ["MATCH (d:Decision {status:'superseded'})-[:ABOUT]->(t:Topic)\nRETURN count(d) AS "]

There are 7 superseded decisions.

Topics:
- topic:iac
- topic:slo
- topic:timeouts
- topic:retries
- topic:compute

Source: graph query over Decision nodes with status `superseded`.

### memory-eval-graph (completed, 10.6s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:SUPERSEDES]->(old:Decision)\nRETURN count(DISTINCT old) AS s', 'MATCH (d:Decision)-[:SUPERSEDES]->(old:Decision)-[:ABOUT]->(t:Topic)\nRETURN coun']

There are 7 superseded decisions. Source: graph memory query result, 2026-01-12 to 2026-06-15.

Topics with superseded decisions:
- topic:iac — infrastructure as code
- topic:timeouts — gateway timeout
- topic:retries — retries
- topic:compute — compute platform
- topic:slo — SLO

Details from the superseded decisions:
- D01, 2026-01-12, superseded, `Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1` — topic:iac — `meetings/2026-01-12-weekly-sync.txt`
- D02, 2026-01-26, superseded, `Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%` — topic:slo — `meetings/2026-01-26-weekly-sync.txt`
- D06, 2026-03-16, superseded, `Gateway integration timeout 10 s on every Relay route` — topic:timeouts — `meetings/2026-03-16-weekly-sync.txt`
- D07, 2026-03-30, superseded, `Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice` — topic:retries — `meetings/2026-03-30-weekly-sync.txt`
- D12, 2026-05-18, superseded, `Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14` — topic:timeouts — `meeting

### memory-eval-vector (completed, 8.9s, 3 tool calls)
queries: ['How many decisions have been superseded, and on which topics?', 'superseded decisions topics Relay webhook delivery project', 'decisions marked superseded topics']

I found **5 superseded decisions** in memory, on these topics:

1. **retries** — D07 (2026-03-30) superseded by D14, and D14 (2026-06-15) is itself superseded by D21.  
   - Source: `meetings/2026-03-30-weekly-sync.txt` (2026-03-30)  
   - Source: `meetings/2026-06-15-weekly-sync.txt` (2026-06-15)

2. **timeouts** — D06 (2026-03-16) superseded by D12, and D12 (2026-05-18) is itself superseded by D20.  
   - Source: `meetings/2026-03-16-weekly-sync.txt` (2026-03-16)  
   - Source: `meetings/2026-05-18-weekly-sync.txt` (2026-05-18)

3. **compute** — D15 (2026-06-15) superseded by D17.  
   - Source: `meetings/2026-06-15-weekly-sync.txt` (2026-06-15)

4. **ADR-005 / compute PoCs** — the ADR page for “Evaluate EKS and Lambda with two proofs of concept” is marked **Superseded by ADR-006**.  
   - Source: `adr/ADR-005.md` (updated 2026-06-17)

5. **ADR-006 / Lambda with provisioned concurrency** — this is not superseded; it is shown as **accepted** and supersedes ADR-005, so I did **not** count it as superseded.  
   - Source: `adr/ADR-006.md` (updated 2026-08-05)

So the count is **5 superseded decision records/topics found**, but note that **one topic appears twice** in superseded hist

## t28 [ru / aggregate] Какими действующими решениями владеет Anna Sokolova? Сколько их?
**expected:** 2: D13 Retries and idempotency ownership moves from Nikit; D21 Retries move out of the gateway into SQS with a de  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.5s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:anna-sokolova'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

У Anna Sokolova **2 действующих решения**.

- **D13** — “Retries and idempotency ownership moves from Nikita to Anna (Nikita leaves on 2026-06-01)” — 2026-06-01 — `meetings/2026-06-01-weekly-sync.txt`
- **D21** — “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off” — 2026-08-24 — `meetings/2026-08-24-weekly-sync.txt`

Если нужно, могу также перечислить, какие темы это затрагивает.

### memory-eval-graph (completed, 4.4s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:anna-sokolova'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

У Anna Sokolova 2 действующих решения. Источники: `meetings/2026-06-01-weekly-sync.txt` (2026-06-01) и `meetings/2026-08-24-weekly-sync.txt` (2026-08-24).

- `D13`: “Retries and idempotency ownership moves from Nikita to Anna (Nikita leaves on 2026-06-01)” — 2026-06-01, `active`, `meetings/2026-06-01-weekly-sync.txt`
- `D21`: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off” — 2026-08-24, `active`, `meetings/2026-08-24-weekly-sync.txt`

Если хотите, могу также перечислить их по темам.

### memory-eval-vector (completed, 4.5s, 3 tool calls)
queries: ['Какими действующими решениями владеет Anna Sokolova? Сколько их?', 'Anna Sokolova owns current decisions how many', 'Anna Sokolova ownership decisions current active']

Действующие решения, которыми владеет Anna Sokolova, в памяти есть только одно: **idempotency**.

- **idempotency** — Anna Sokolova, **active**, с **2026-06-01**.  
  Source: `memory/decisions.jsonl`, `2026-06-01`.

Важно: в памяти есть и запись про **retries**, но она **superseded** и значит не действующая:
- **retries** — Anna Sokolova, **superseded**, с **2026-06-01** до **2026-09-07**.  
  Source: `memory/decisions.jsonl`, `2026-06-01`.

Итого действующих решений у Anna Sokolova: **1**.  
Источник для текущего владения: `memory/decisions.jsonl`, `2026-06-01`.

Дополнительно, более общий документ `confluence/team-roster.xhtml` от **2026-07-08** пишет, что Anna owns “core service; retries and idempotency”, но он старее, чем решение от **2026-09-07**, по которому retries уже перешли к Ivan Melnik, поэтому по retries этот документ устарел.

## t29 [ru / aggregate] Какими действующими решениями владеет Pavel Grishin? Сколько их?
**expected:** 3: D03 One CloudFormation root stack per environment with; D05 Front Relay with the API gateway; the gateway and ; D09 Hybrid IaC: networking (VPC, peering, DNS) stays i  
**expected sources:** {'sources': ['meetings/2026-02-09-weekly-sync.txt', 'meetings/2026-03-02-weekly-sync.txt', 'meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 4.1s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:pavel-grishin'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

У Pavel Grishin сейчас 3 действующих решения.

- D03 — «One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)» — 2026-02-09 — source: `meetings/2026-02-09-weekly-sync.txt`
- D05 — «Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack» — 2026-03-02 — source: `meetings/2026-03-02-weekly-sync.txt`
- D09 — «Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation» — 2026-04-20 — source: `meetings/2026-04-20-weekly-sync.txt`

Итого: 3.

### memory-eval-graph (completed, 3.9s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:pavel-grishin'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

Павел Гришин владеет 3 действующими решениями.

- D03 — “One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)” — 2026-02-09 — `meetings/2026-02-09-weekly-sync.txt`
- D05 — “Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack” — 2026-03-02 — `meetings/2026-03-02-weekly-sync.txt`
- D09 — “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation” — 2026-04-20 — `meetings/2026-04-20-weekly-sync.txt`

Источник: граф памяти, по действующим `OWNS`-связям от `person:pavel-grishin`.

### memory-eval-vector (completed, 4.3s, 3 tool calls)
queries: ['Какими действующими решениями владеет Pavel Grishin? Сколько их?', 'Pavel Grishin owner active decisions', 'Pavel Grishin действующие решения']

У Павла Grishin в памяти **2 действующих решения**:

1. **iac** — «One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)»; владелец: Pavel Grishin; **active**; источник: `meetings/2026-02-09-weekly-sync.txt` — **2026-02-09**.  
2. **gateway** — «Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack»; владелец: Pavel Grishin; **active**; источник: `meetings/2026-03-02-weekly-sync.txt` — **2026-03-02**.

Есть ещё решение по **timeouts** от **2026-03-16**, но оно помечено как **superseded**, поэтому в число действующих не входит: `meetings/2026-03-16-weekly-sync.txt`.

Если хотите, я могу также перечислить **все** решения Павла с указанием, какие из них уже устарели.

## t30 [ru / aggregate] Какими действующими решениями владеет Ivan Melnik? Сколько их?
**expected:** 5: D16 Serverless PoC ownership moves from Sergey to Ivan; D17 Relay moves to Lambda with provisioned concurrency; D20 Gateway integration timeout lowered from 30 s to 2; D22 Retries ownership moves from Anna to Ivan, who own; D25 Serverless cutover on 2026-10-19 at 09:00 local, i  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt', 'meetings/2026-08-03-architecture-committee.txt', 'meetings/2026-08-24-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 5.5s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:ivan-melnik'})-[o:OWNS]->(d:Decision) WHERE o.to IS "]

Ivan Melnik владеет 5 действующими решениями.

- `Serverless PoC ownership moves from Sergey to Ivan` — 2026-07-13, `meetings/2026-07-13-weekly-sync.txt`
- `Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances` — 2026-08-03, `meetings/2026-08-03-architecture-committee.txt`
- `Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom` — 2026-08-24, `meetings/2026-08-24-weekly-sync.txt`
- `Retries ownership moves from Anna to Ivan, who owns the SQS pipeline` — 2026-09-07, `meetings/2026-09-07-security-review.txt`
- `Serverless cutover on 2026-10-19 at 09:00 local, inside the planned-work error budget` — 2026-10-05, `meetings/2026-10-05-cutover-planning.txt`

Если хотите, могу ещё разложить их по темам.

### memory-eval-graph (completed, 5.4s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:ivan-melnik'})-[o:OWNS]->(d:Decision)\nWHERE o.to IS "]

Ivan Melnik владеет 5 действующими решениями.

- D16 — “Serverless PoC ownership moves from Sergey to Ivan” — 2026-07-13 — `meetings/2026-07-13-weekly-sync.txt`
- D17 — “Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances” — 2026-08-03 — `meetings/2026-08-03-architecture-committee.txt`
- D20 — “Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom” — 2026-08-24 — `meetings/2026-08-24-weekly-sync.txt`
- D22 — “Retries ownership moves from Anna to Ivan, who owns the SQS pipeline” — 2026-09-07 — `meetings/2026-09-07-security-review.txt`
- D25 — “Serverless cutover on 2026-10-19 at 09:00 local, inside the planned-work error budget” — 2026-10-05 — `meetings/2026-10-05-cutover-planning.txt`

Источник: записи OWNS к активным решениям; дата вопроса не уточнялась, поэтому я взял текущее состояние.

### memory-eval-vector (completed, 3.8s, 3 tool calls)
queries: ['Какими действующими решениями владеет Ivan Melnik? Сколько их?', 'Ivan Melnik current decisions ownership', 'Ivan Melnik owns decision active current']

По памяти Ivan Melnik владеет 3 действующими решениями:

1. retries — с 2026-09-07, current  
   Источник: `memory/decisions.jsonl` / `meetings/2026-09-07-security-review.txt` (2026-09-07)

2. compute — с 2026-07-13, current  
   Источник: `memory/decisions.jsonl` / `meetings/2026-07-13-weekly-sync.txt` (2026-07-13)

3. serverless PoC / ownership — с 2026-07-13, current  
   Источник: `meetings/2026-07-13-weekly-sync.txt` (2026-07-13)

Итого: 3.

Примечание: в выдаче есть также отдельная активная запись D22 про retries/SQS pipeline, но она по сути подтверждает ту же текущую ownership-решение про retries, поэтому я не считаю её отдельным решением.

## t31 [ru / aggregate] Какими действующими решениями владеет Lena Kim? Сколько их?
**expected:** 3: D04 Manual console changes are frozen; nightly drift d; D27 Rollback owner for both cutovers is Lena; D28 Delivery p95 SLO relaxed from 2 s to 3 s for 30 da  
**expected sources:** {'sources': ['meetings/2026-02-23-incident-review.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 4.9s, 1 tool calls)
queries: ["MATCH (p:Person {key:'person:lena-kim'})-[o:OWNS]->(d:Decision) WHERE o.to IS NU"]

У Lena Kim сейчас 3 действующих решения.

1. **Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call**  
   Дата: 2026-02-23  
   Статус: active  
   Источник: `meetings/2026-02-23-incident-review.txt`

2. **Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s**  
   Дата: 2026-10-05  
   Статус: active  
   Источник: `meetings/2026-10-05-cutover-planning.txt`

3. **Rollback owner for both cutovers is Lena**  
   Дата: 2026-10-05  
   Статус: active  
   Источник: `meetings/2026-10-05-cutover-planning.txt`

Если нужно, могу также перечислить, за какие темы эти решения отвечают.

### memory-eval-graph (completed, 4.1s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:lena-kim'})-[o:OWNS]->(d:Decision) WHERE o.to IS NUL"]

Lena Kim владеет 3 действующими решениями.

1. **D04** — “Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call”  
   Дата: **2026-02-23**  
   Статус: **active**  
   Источник: **meetings/2026-02-23-incident-review.txt**

2. **D28** — “Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s”  
   Дата: **2026-10-05**  
   Статус: **active**  
   Источник: **meetings/2026-10-05-cutover-planning.txt**

3. **D27** — “Rollback owner for both cutovers is Lena”  
   Дата: **2026-10-05**  
   Статус: **active**  
   Источник: **meetings/2026-10-05-cutover-planning.txt**

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['Какими действующими решениями владеет Lena Kim? Сколько их?', 'Lena Kim owner active decisions count', 'Lena Kim owns current decisions']

У Lena Kim **3 действующих решения**:

1. **slo** — Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s.  
   Источник: `meetings/2026-10-05-cutover-planning.txt`, **2026-10-05**.

2. **cutover** — Rollback owner for both cutovers is Lena.  
   Источник: `meetings/2026-10-05-cutover-planning.txt`, **2026-10-05**.

3. **iac** — Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call.  
   Источник: `meetings/2026-02-23-incident-review.txt`, **2026-02-23**.

Итого: **3**.

Примечание: в памяти есть ещё запись про `slo` как ownership (`memory/decisions.jsonl`, **2026-01-26**), но это отдельная запись-ownership; если считать именно **действующие решения**, то выше — 3.

## t32 [en / aggregate] Which ADRs are not Accepted, and what is their status?
**expected:** Superseded: ADR-001, ADR-005; Rejected: ADR-007; Proposed: ADR-010  
**expected sources:** {'sources': ['adr/ADR-001.md', 'adr/ADR-005.md', 'adr/ADR-007.md', 'adr/ADR-010.md']}

### memory-eval-both (completed, 3.7s, 1 tool calls)
queries: ["MATCH (a:ADR) WHERE a.status <> 'Accepted' RETURN a.id, a.title, a.status, a.dat"]

The ADRs not Accepted are:

- ADR-001 — status: Superseded — file: adr/ADR-001.md — date: 2026-01-14
- ADR-005 — status: Superseded — file: adr/ADR-005.md — date: 2026-06-17
- ADR-007 — status: Rejected — file: adr/ADR-007.md — date: 2026-08-05
- ADR-010 — status: Proposed — file: adr/ADR-010.md — date: 2026-09-23

If you want, I can also tell you which ADR is currently live on each of their topics.

### memory-eval-graph (completed, 3.3s, 1 tool calls)
queries: ["MATCH (a:ADR) WHERE a.status <> 'Accepted' RETURN a.id, a.title, a.status, a.fil"]

The ADRs that are not Accepted are:

- **ADR-001** — **Superseded** — `adr/ADR-001.md`  
- **ADR-005** — **Superseded** — `adr/ADR-005.md`  
- **ADR-007** — **Rejected** — `adr/ADR-007.md`  
- **ADR-010** — **Proposed** — `adr/ADR-010.md`

Source: each ADR record in memory (`adr/*.md`; ADR status fields, no date field returned in this query).

### memory-eval-vector (completed, 4.1s, 3 tool calls)
queries: ['Which ADRs are not Accepted, and what is their status?', 'ADRs not Accepted status', 'Accepted ADR status superseded proposed rejected draft']

I found these ADRs that are not Accepted:

- **ADR-007: Keep Relay on EKS with autoscaling** — **Rejected**  
  Source: `adr/ADR-007.md`, updated **2026-08-05**.
- **ADR-005: Evaluate EKS and Lambda with two proofs of concept** — **Superseded (superseded by ADR-006)**  
  Source: `adr/ADR-005.md`, updated **2026-06-17**.
- **ADR-010: Gateway timeout policy for Lambda integrations** — **Proposed**  
  Source: `adr/ADR-010.md`, updated **2026-09-23**.

Notes:
- The memory also contains several **Accepted** ADR chunks, but those do not match your question.
- For ADR-005, the chunk explicitly says it is superseded by ADR-006, so its current status is **Superseded**.

## t33 [ru / unowned_at] Какие открытые вопросы были без владельца на 2026-06-15?
**expected:** O1 DynamoDB migration dry run on a production snapshot (raised 2026-05-04); O4 DocumentDB decommission date (raised 2026-05-18)  
**expected sources:** {'sources': ['meetings/2026-05-04-poc-review.txt', 'meetings/2026-05-18-weekly-sync.txt']}

### memory-eval-both (completed, 4.3s, 1 tool calls)
queries: ["MATCH (o:OpenItem) WHERE o.raised <= '2026-06-15' AND NOT EXISTS { MATCH (o)<-[w"]

На 2026-06-15 без владельца были:

- **O1** — “DynamoDB migration dry run on a production snapshot”  
  raised: **2026-05-04**; raised_again: **2026-05-18, 2026-06-15, 2026-06-29, 2026-07-20**  
  status: **closed**  
  source: граф памяти; дата среза **2026-06-15**

- **O4** — “DocumentDB decommission date”  
  raised: **2026-05-18**; raised_again: **2026-08-10, 2026-10-05**  
  status: **open**  
  source: граф памяти; дата среза **2026-06-15**

Если хотите, я могу отдельно показать, кто позже взял каждый из этих вопросов.

### memory-eval-graph (completed, 4.1s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На 2026-06-15 без владельца были 2 открытых вопроса:

- O1 — “DynamoDB migration dry run on a production snapshot”; raised: 2026-05-04, raised_again: 2026-05-18, 2026-06-15, 2026-06-29, 2026-07-20. Источник: граф памяти, дата: 2026-06-15.
- O4 — “DocumentDB decommission date”; raised: 2026-05-18, raised_again: 2026-08-10, 2026-10-05. Источник: граф памяти, дата: 2026-06-15.

Примечание: я отфильтровал только те открытые вопросы, которые на эту дату не имели владельца и ещё не были закрыты.

### memory-eval-vector (completed, 5.0s, 3 tool calls)
queries: ['Какие открытые вопросы были без владельца на 2026-06-15?', 'открытые вопросы без владельца 2026-06-15', 'open questions without owner on 2026-06-15']

На **2026-06-15** в памяти есть **один открытый вопрос без владельца**:

- **Dry run миграции базы** — в встрече сказано, что он **«без владельца»**.  
  Источник: `meetings/2026-06-15-weekly-sync.txt`, **2026-06-15**.  
  Также это соответствует более ранней записи о том же вопросе: `meetings/2026-05-18-weekly-sync.txt`, **2026-05-18**, где он тоже отмечен как **без владельца**.

Что я нашёл в памяти:
- `meetings/2026-06-15-weekly-sync.txt` — 2026-06-15
- `meetings/2026-05-18-weekly-sync.txt` — 2026-05-18
- `meetings/2026-05-04-poc-review.txt` — 2026-05-04

Если хотите, я могу ещё перечислить все открытые вопросы **без владельца, которые были известны именно на эту дату**, с их статусом и последними упоминаниями.

## t34 [ru / unowned_at] Какие открытые вопросы были без владельца на 2026-08-17?
**expected:** O3 Load test on Lambda at 10x current volume (raised 2026-07-27); O4 DocumentDB decommission date (raised 2026-05-18)  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-07-27-poc-review.txt']}

### memory-eval-both (completed, 3.8s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На 2026-08-17 без владельца были 2 открытых вопроса:

- **O3** — «Load test on Lambda at 10x current volume»  
  raised: 2026-07-27; raised_again: 2026-08-17, 2026-09-14  
  status: open

- **O4** — «DocumentDB decommission date»  
  raised: 2026-05-18; raised_again: 2026-08-10, 2026-10-05  
  status: open

Источник: graph query, open items without owner on 2026-08-17.

### memory-eval-graph (completed, 4.7s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На 2026-08-17 без владельца были такие открытые вопросы:

- **O3** — “Load test on Lambda at 10x current volume”; raised: **2026-07-27**; raised_again: **2026-08-17, 2026-09-14**; status: **open**.  
  Источник: граф памяти, дата вопроса **2026-08-17**.

- **O4** — “DocumentDB decommission date”; raised: **2026-05-18**; raised_again: **2026-08-10, 2026-10-05**; status: **open**.  
  Источник: граф памяти, дата вопроса **2026-08-17**.

Если хотите, могу также перечислить **все открытые вопросы на эту дату**, включая те, у которых был владелец.

### memory-eval-vector (completed, 6.5s, 3 tool calls)
queries: ['Какие открытые вопросы были без владельца на 2026-08-17?', 'открытые вопросы без владельца 2026-08-17', 'open items with no owner as of 2026-08-17']

На **2026-08-17** в памяти есть один явно открытый вопрос **без владельца**:

- **Load test on Lambda at 10x current volume** — raised **2026-07-27**, **no owner**.  
  Источник: `meetings/2026-07-27-poc-review.txt` / claim `O3` (`openitem:compute:2026-07-27`), дата: **2026-07-27**.

Что я дополнительно нашёл, но это не отвечает точно на дату **2026-08-17**:
- Встреча **2026-08-10**: `dry run миграции базы` был **без владельца** на тот момент, но там уже фигурирует, что **Серёжа** его берёт, так что к 2026-08-17 это, вероятно, уже не “без владельца”. Источник: `meetings/2026-08-10-weekly-sync.txt`, дата: **2026-08-10**.
- Встреча **2026-09-14**: `нагрузочный на десять икс` всё ещё без владельца, но это уже позже запрошенной даты. Источник: `meetings/2026-09-14-weekly-sync.txt`, дата: **2026-09-14**.

Если хотите, я могу отдельно перечислить **все open items без владельца, которые были актуальны вокруг 2026-08-17**, с пометкой что именно подтверждено на эту дату, а что только до/после неё.

## t35 [en / unowned_at] Which open items had no owner on 2026-10-05?
**expected:** O3 Load test on Lambda at 10x current volume (raised 2026-07-27); O4 DocumentDB decommission date (raised 2026-05-18); O7 Rotate DocumentDB credentials before decommission (raised 2026-09-07)  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-07-27-poc-review.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 3.7s, 1 tool calls)
queries: ["MATCH (o:OpenItem) WHERE o.raised <= '2026-10-05' AND NOT EXISTS { MATCH (o)<-[w"]

On 2026-10-05, the open items with no owner were:

- O3 — “Load test on Lambda at 10x current volume”  
  Raised: 2026-07-27; raised again: 2026-08-17, 2026-09-14

- O4 — “DocumentDB decommission date”  
  Raised: 2026-05-18; raised again: 2026-08-10, 2026-10-05

- O7 — “Rotate DocumentDB credentials before decommission”  
  Raised: 2026-09-07; raised again: 2026-09-28, 2026-10-05

Source: graph query over OpenItem ownership as of 2026-10-05.

### memory-eval-graph (completed, 4.8s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

On 2026-10-05, the open items with no owner were:

- O3 — “Load test on Lambda at 10x current volume” — raised 2026-07-27, raised again 2026-08-17 and 2026-09-14. Source: graph memory (OpenItem O3); no owner edge as of 2026-10-05.
- O4 — “DocumentDB decommission date” — raised 2026-05-18, raised again 2026-08-10 and 2026-10-05. Source: graph memory (OpenItem O4); no owner edge as of 2026-10-05.
- O7 — “Rotate DocumentDB credentials before decommission” — raised 2026-09-07, raised again 2026-09-28 and 2026-10-05. Source: graph memory (OpenItem O7); no owner edge as of 2026-10-05.

Assumption: “no owner” means no OWNS edge active on or before 2026-10-05.

### memory-eval-vector (completed, 2.9s, 3 tool calls)
queries: ['Which open items had no owner on 2026-10-05?', 'open items no owner 2026-10-05', 'items with no owner raised 2026-10-05 open']

On 2026-10-05, the open item with no owner in memory was:

- **DocumentDB decommission date** — raised 2026-05-18, raised again on 2026-08-10 and 2026-10-05, **no owner**. Source: `meetings/2026-05-18-weekly-sync.txt` (dated 2026-05-18).

What I retrieved also included several items with owners or closed status, so I excluded them.

## t36 [en / stale_docs] Which documents were out of date on 2026-07-01, and why?
**expected:** docs/iac-cloudformation.md (updated 2026-02-11): says all infrastructure including networking moves to CloudFormation, changed by D09 on 2026-04-20; docs/gateway.md (updated 2026-03-18): says the integration timeout is 10 s, changed by D12 on 2026-05-18; docs/gateway.md (updated 2026-03-18): says retries are disabled on /deliver, changed by D14 on 2026-06-15; docs/onboarding.md (updated 2026-03-10): lists Nikita as retries owner and does not list Sergey or Ivan, changed by D13 on 2026-06-01; confluence/architecture.xhtml (updated 2026-03-12): shows DocumentDB, changed by D10 on 2026-05-04; confluence/decision-log.xhtml (updated 2026-06-03): stops at 2026-06-01, changed by D14 on 2026-06-15  
**expected sources:** {'sources': ['confluence/architecture.xhtml', 'confluence/decision-log.xhtml', 'docs/gateway.md', 'docs/iac-cloudformation.md', 'docs/onboarding.md']}

### memory-eval-both (completed, 11.3s, 2 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ', '2026-07-01 stale document architecture decision log gateway retries timeout Clou']

On 2026-07-01, these documents were out of date:

- `confluence/architecture.xhtml` — updated `2026-03-12`
  - Stale because a later decision on `2026-05-04` changed the documented fact: it now **shows DocumentDB**.
  - Source for the stale fact: `meetings/2026-05-04-poc-review.txt`

- `confluence/decision-log.xhtml` — updated `2026-06-03`
  - Stale because a later decision on `2026-06-15` changed the ownership/status details it records: it **stops at 2026-06-01**.
  - Source: `meetings/2026-06-15-weekly-sync.txt`

- `docs/gateway.md` — updated `2026-03-18`
  - Stale because later decisions changed two facts in it:
    - on `2026-06-15`, the doc’s claim that it **says retries are disabled on /deliver** became outdated
    - on `2026-05-18`, the doc’s claim that it **says the integration timeout is 10 s** became outdated
  - Source: `meetings/2026-06-15-weekly-sync.txt` and `meetings/2026-05-18-weekly-sync.txt`

- `docs/iac-cloudformation.md` — updated `2026-02-11`
  - Stale because a later decision on `2026-04-20` changed the IaC arrangement: it **says all infrastructure including networking moves to CloudFormation**.
  - Source: `meetings/2026-04-20-weekly-sync.txt`

- `docs/onboa

### memory-eval-graph (completed, 14.6s, 1 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D AND dec']

On 2026-07-01, these documents were out of date because later decisions changed facts they stated.

- `confluence/architecture.xhtml` — updated `2026-03-12`  
  It was stale because a later decision on `2026-05-04` changed the database fact it still showed: the document said “DocumentDB,” but the decision in force changed it to “DynamoDB single-table design.”  
  Source: `meetings/2026-05-04-poc-review.txt` (`2026-05-04`)

- `confluence/decision-log.xhtml` — updated `2026-06-03`  
  It was stale because a later decision on `2026-06-15` changed the retry policy it still described. The old fact was that retries “stop at 2026-06-01”; the new decision enabled retries on `POST /deliver` with max 3 attempts and a 15% retry budget.  
  Source: `meetings/2026-06-15-weekly-sync.txt` (`2026-06-15`)

- `docs/gateway.md` — updated `2026-03-18`  
  It was stale for two reasons:
  1. A decision on `2026-05-18` changed the gateway integration timeout from 10 s to 30 s.  
     Source: `meetings/2026-05-18-weekly-sync.txt` (`2026-05-18`)
  2. A decision on `2026-06-15` changed retry behavior: retries were enabled on `POST /deliver` with max 3 attempts and a 15% retry budget.  
     Source: `meeting

### memory-eval-vector (completed, 9.4s, 3 tool calls)
queries: ['Which documents were out of date on 2026-07-01, and why?', 'documents out of date on 2026-07-01 why stale updated date newer decision', 'out of date documents as of 2026-07-01 stale document decision newer updated dat']

Not in memory as a complete list of “documents out of date on 2026-07-01”.

What I did retrieve:
- `docs/db-migration-plan.md` — updated 2026-05-26. It was already stale by 2026-07-01 because it still said DocumentDB decommission had no date / cutover not dated, and a newer decision later set the DynamoDB cutover on 2026-10-12.  
  Source: `docs/db-migration-plan.md` (2026-05-26) and `meetings/2026-10-05-cutover-planning.txt` (2026-10-05).
- `docs/documentdb-runbook.md` — updated 2026-02-02. It was later superseded on the same topic by the 2026-10-05 decision noting it still described DocumentDB as the system of record after the cutover plan changed.  
  Source: `docs/documentdb-runbook.md` (2026-02-02) and `meetings/2026-10-05-cutover-planning.txt` (2026-10-05).
- `docs/secrets.md` — updated 2026-09-10. This is not out of date on 2026-07-01 by its own update date, but it does mention the later 2026-09-07 security review decision.  
  Source: `docs/secrets.md` (2026-09-10) and `meetings/2026-09-07-security-review.txt` (2026-09-07).
- `confluence/decision-log.xhtml` — updated 2026-06-03. I found no direct newer superseding decision for the whole page, but it contains older entries a

## t37 [en / stale_docs] Which documents were out of date on 2026-10-05, and why?
**expected:** docs/iac-cloudformation.md (updated 2026-02-11): says all infrastructure including networking moves to CloudFormation, changed by D09 on 2026-04-20; docs/gateway.md (updated 2026-03-18): says the integration timeout is 10 s, changed by D12 on 2026-05-18; docs/gateway.md (updated 2026-03-18): says retries are disabled on /deliver, changed by D14 on 2026-06-15; docs/gateway.md (updated 2026-03-18): describes gateway retries at all, changed by D21 on 2026-08-24; docs/slo.md (updated 2026-01-28): says p95 2 s with no stabilisation window, changed by D28 on 2026-10-05; docs/documentdb-runbook.md (updated 2026-02-02): describes DocumentDB as the system of record, changed by D26 on 2026-10-05; docs/db-migration-plan.md (updated 2026-05-26): says the dry run has no owner, changed by D19 on 2026-08-10; docs/db-migration-plan.md (updated 2026-05-26): has no cutover date, changed by D26 on 2026-10-05; docs/runbook-cutover-serverless.md (updated 2026-09-29): says rollback owner TBD, changed by D27 on 2026-10-05; docs/runbook-cutover-serverless.md (updated 2026-09-29): has no cutover date, changed by D25 on 2026-10-05; docs/onboarding.md (updated 2026-03-10): lists Nikita as retries owner and does not list Sergey or Ivan, changed by D13 on 2026-06-01; confluence/architecture.xhtml (updated 2026-03-12): shows EKS as the runtime, changed by D17 on 2026-08-03; confluence/architecture.xhtml (updated 2026-03-12): shows DocumentDB, changed by D10 on 2026-05-04; confluence/decision-log.xhtml (updated 2026-06-03): stops at 2026-06-01, changed by D14 on 2026-06-15; confluence/team-roster.xhtml (updated 2026-07-08): lists Anna as retries owner, changed by D22 on 2026-09-07; confluence/migration-roadmap.xhtml (updated 2026-06-20): lists compute decision as pending PoC, changed by D17 on 2026-08-03  
**expected sources:** {'sources': ['confluence/architecture.xhtml', 'confluence/decision-log.xhtml', 'confluence/migration-roadmap.xhtml', 'confluence/team-roster.xhtml', 'docs/db-migration-plan.md', 'docs/documentdb-runbook.md', 'docs/gateway.md', 'docs/iac-cloudformation.md', 'docs/onboarding.md', 'docs/runbook-cutover-serverless.md', 'docs/slo.md']}

### memory-eval-both (completed, 27.1s, 2 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ', '"2026-10-05" out of date document why stale decision changed fact Relay webhook ']

On 2026-10-05, these documents were out of date:

- `confluence/architecture.xhtml` — updated `2026-03-12`. It was stale because later decisions changed it twice:
  - `2026-05-04`: the fact “shows DocumentDB” changed.
  - `2026-08-03`: the fact “shows EKS as the runtime” changed.
  Source for the stale facts: `meetings/2026-05-04-poc-review.txt` and `meetings/2026-08-03-architecture-committee.txt`.

- `confluence/decision-log.xhtml` — updated `2026-06-03`. It was stale because a later decision on `2026-06-15` changed the fact “stops at 2026-06-01” in the log.
  Source: `meetings/2026-06-15-weekly-sync.txt`.

- `confluence/migration-roadmap.xhtml` — updated `2026-06-20`. It was stale because the `2026-08-03` decision changed the fact “lists compute decision as pending PoC”.
  Source: `meetings/2026-08-03-architecture-committee.txt`.

- `confluence/team-roster.xhtml` — updated `2026-07-08`. It was stale because the `2026-09-07` decision changed the fact “lists Anna as retries owner”.
  Source: `meetings/2026-09-07-security-review.txt`.

- `docs/db-migration-plan.md` — updated `2026-05-26`. It was stale because later decisions on `2026-08-10` and `2026-10-05` changed facts in it:
  - 

### memory-eval-graph (completed, 22.2s, 1 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ']

On 2026-10-05, these documents were out of date:

- `confluence/architecture.xhtml` — updated 2026-03-12, but later decisions changed it:
  - 2026-05-04: “shows DocumentDB” was made stale by `meetings/2026-05-04-poc-review.txt`
  - 2026-08-03: “shows EKS as the runtime” was made stale by `meetings/2026-08-03-architecture-committee.txt`

- `confluence/decision-log.xhtml` — updated 2026-06-03, but a later decision changed a fact in it:
  - 2026-06-15: “stops at 2026-06-01” was made stale by `meetings/2026-06-15-weekly-sync.txt`

- `confluence/migration-roadmap.xhtml` — updated 2026-06-20, but later decisions changed it:
  - 2026-08-03: “lists compute decision as pending PoC” was made stale by `meetings/2026-08-03-architecture-committee.txt`

- `confluence/team-roster.xhtml` — updated 2026-07-08, but later decisions changed it:
  - 2026-09-07: “lists Anna as retries owner” was made stale by `meetings/2026-09-07-security-review.txt`

- `docs/db-migration-plan.md` — updated 2026-05-26, but later decisions changed it:
  - 2026-10-05: “has no cutover date” was made stale by `meetings/2026-10-05-cutover-planning.txt`
  - 2026-08-10: “says the dry run has no owner” was made stale by `meetin

### memory-eval-vector (completed, 12.2s, 3 tool calls)
queries: ['Which documents were out of date on 2026-10-05, and why?', 'documents out of date on 2026-10-05 stale updated date newer decision why', '2026-10-05 documents stale superseded decision updated date']

On 2026-10-05, I found these documents/sections called out as out of date:

1. **`docs/documentdb-runbook.md`** — updated **2026-02-02**
   - Why stale: the 2026-10-05 cutover decision says it “still describes DocumentDB as the system of record,” but DynamoDB cutover had been decided for **2026-10-12**.
   - Source: `meetings/2026-10-05-cutover-planning.txt` (2026-10-05), claim **D26**.

2. **`docs/db-migration-plan.md`** — updated **2026-05-26**
   - Why stale: the same 2026-10-05 decision says it “still has no cutover date,” while the actual cutover date was decided as **2026-10-12**.
   - Source: `meetings/2026-10-05-cutover-planning.txt` (2026-10-05), claim **D26**.

3. **`docs/gateway.md`** — updated **2026-03-18**
   - Why stale: it still says the integration timeout is **10 s**, but the timeout was raised to **30 s** on **2026-05-18**.
   - Source: `meetings/2026-05-18-weekly-sync.txt` (2026-05-18), claim **D12**.
   - Note: the claim explicitly says `ADR-002`’s Timeouts section is stale since 2026-05-18.

4. **`ADR-002` / `ADR-002` section “Timeouts”** — stale since **2026-05-18**
   - Why stale: same timeout decision as above; it was superseded by the later decision to use

## t38 [ru / poc_basis] На каком PoC и на каких цифрах основано решение «DynamoDB single-table design, chosen on PoC-1 results (p99 r…»?
**expected:** PoC-1: DynamoDB single-table vs multi-table: {"single_table_p99_read_ms": 4, "multi_table_p99_read_ms": 11, "single_table_cost_delta_pct": -38, "documentdb_p99_read_ms": 9}; report docs/poc-dynamodb-report.md  
**expected sources:** {'sources': ['docs/poc-dynamodb-report.md', 'meetings/2026-05-04-poc-review.txt']}

### memory-eval-both (completed, 4.7s, 3 tool calls)
queries: ['"DynamoDB single-table design, chosen on PoC-1 results" PoC-1 results p99 reads ', 'PoC-1 DynamoDB single-table multi-table p99 reads writes results', "MATCH (d:Decision)-[:BASED_ON]->(p:PoC) WHERE d.text STARTS WITH 'DynamoDB singl"]

Решение основано на PoC-1: **«PoC-1: DynamoDB single-table vs multi-table»**.  
Источник решения: **meetings/2026-05-04-poc-review.txt**, дата **2026-05-04**.

Цифры, на которых оно основано:
- **p99 read**: **4 ms** у single-table против **11 ms** у multi-table
- **стоимость при прогнозируемом объёме**: **на 38% ниже** у single-table
- в данных PoC также указан **DocumentDB p99 read = 9 ms**

Источник цифр: **docs/poc-dynamodb-report.md**, дата **2026-05-01**.

### memory-eval-graph (completed, 4.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(c:PoC)\nWHERE d.text STARTS WITH 'DynamoDB singl"]

Решение основано на **PoC-1: DynamoDB single-table vs multi-table**.  
Источник решения: `meetings/2026-05-04-poc-review.txt`, дата `2026-05-04`.

Цифры из PoC:
- `single_table_p99_read_ms = 4`
- `multi_table_p99_read_ms = 11`
- `single_table_cost_delta_pct = -38`
- `documentdb_p99_read_ms = 9`

Также в тексте решения зафиксировано: **p99 read 4 ms vs 11 ms; 38% lower cost at projected volume**.  
Источник: `meetings/2026-05-04-poc-review.txt`, дата `2026-05-04`.

Отдельно в записи PoC указан отчёт: `docs/poc-dynamodb-report.md`, но сам выбор решения ссылается на результаты PoC-1 и на этот review meeting.

### memory-eval-vector (completed, 5.0s, 3 tool calls)
queries: ['На каком PoC и на каких цифрах основано решение «DynamoDB single-table design, c', 'DynamoDB single-table design, chosen on PoC-1 results (p99 r…', 'PoC-1 p99 DynamoDB single-table design results цифры']

Решение основано на **PoC-1**.

Цифры, на которых оно основано:
- **p99 read 4 ms** у DynamoDB single-table
- **p99 read 11 ms** у DynamoDB multi-table
- **38% lower cost at projected volume**
- В отчёте PoC-1 также указано:  
  - DocumentDB baseline: **9 ms read p99**, **$5,200/month**
  - DynamoDB multi-table: **11 ms read p99**, **$5,100/month**
  - DynamoDB single-table: **4 ms read p99**, **$3,200/month (-38%)**

Источники:
- `meetings/2026-05-04-poc-review.txt` — 2026-05-04, decision claim D10 / ADR-003
- `docs/poc-dynamodb-report.md` — 2026-05-01, section “Results”
- `adr/ADR-003.md` — updated 2026-05-06, section “Decision”

Если хотите, могу ещё кратко собрать это в формате: **«PoC -> метрика -> вывод»**.

## t39 [ru / poc_basis] На каком PoC и на каких цифрах основано решение «Relay moves to Lambda with provisioned concurrency on /deliv…»?
**expected:** PoC-3: Relay on Lambda: {"p95_warm_s": 1.9, "p95_cold_s": 3.4, "cold_start_s": 1.2, "monthly_cost_usd": 3600, "cost_delta_vs_eks_pct": -41}; report docs/poc-lambda-report.md  
**expected sources:** {'sources': ['docs/poc-lambda-report.md', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 3.9s, 2 tool calls)
queries: ['"Relay moves to Lambda with provisioned concurrency on /deliv…" PoC numbers resu', "MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio"]

Решение основано на **PoC-3: Relay on Lambda**.

Цифры, на которых оно основано:
- **p95 latency с provisioned concurrency на `/deliver` — 1.9 s**
- **p95 latency без provisioned concurrency — 3.4 s**
- **cold start — 1.2 s**
- **monthly cost — $3,600**
- **cost delta vs EKS — -41%**

Источник:
- `docs/poc-lambda-report.md` — обновлено **2026-07-24**
- `meetings/2026-08-03-architecture-committee.txt` — решение от **2026-08-03**

Короткая формулировка из памяти:
- PoC-3 показал **41% lower monthly cost** и **p95 1.9 s with warm instances**.

Если нужно, могу ещё показать, **что именно было записано в ADR-006 как обоснование и последствия**.

### memory-eval-graph (completed, 3.5s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio"]

Решение основано на PoC-3: **Relay on Lambda**; это указано в решении от **2026-08-03** в файле **meetings/2026-08-03-architecture-committee.txt**.

Цифры, на которых оно основано, из результатов PoC:
- **p95 warm = 1.9 s**
- **p95 cold = 3.4 s**
- **cold start = 1.2 s**
- **monthly cost = 3600 USD**
- **cost delta vs EKS = -41%**

Источник PoC: **docs/poc-lambda-report.md**.

Если нужно, могу ещё показать формулировку решения целиком и его note из памяти.

### memory-eval-vector (completed, 5.0s, 3 tool calls)
queries: ['На каком PoC и на каких цифрах основано решение «Relay moves to Lambda with prov', 'Relay moves to Lambda with provisioned concurrency on /deliv… PoC цифры решение', 'PoC и цифры для решения Relay moves to Lambda with provisioned concurrency on /d']

Решение основано на **PoC-3**.

Что именно использовали для решения:
- **p95 delivery latency = 1.9 s** при **provisioned concurrency on `/deliver`**
- **monthly cost = $3,600**, что на **41% ниже EKS**
- из PoC-3 также видно, что без provisioned concurrency p95 был **3.4 s**, а cold start — **1.2 s**

Источники:
- `adr/ADR-006.md` — **2026-08-05**: decision “Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances.”
- `docs/poc-lambda-report.md` — **2026-07-24**: таблица результатов PoC-3 с цифрами **1.9 s**, **3.4 s**, **1.2 s**, **$3,600 (-41% vs EKS)**
- `meetings/2026-08-03-architecture-committee.txt` — **2026-08-03**: decision claim “Based on poc-3.”

Если хотите, могу ещё коротко сопоставить, **какие именно цифры из PoC-3 стали аргументами за Lambda, а какие были возражением против неё**.

## t40 [ru / poc_basis] На каком PoC и на каких цифрах основано решение «Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but …»?
**expected:** PoC-2: Relay on EKS with autoscaling: {"p95_s": 0.4, "monthly_cost_usd": 6100, "ops_effort": "a second platform team"}; report docs/poc-eks-report.md  
**expected sources:** {'sources': ['docs/poc-eks-report.md', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 4.5s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'Keep Relay on ", '"Keep Relay on EKS with autoscaling" p95 0.4 s цифры PoC', '"Keep Relay on EKS with autoscaling" PoC numbers p95 0.4 s']

Основано на **PoC-2: Relay on EKS with autoscaling**.  
Источник: `docs/poc-eks-report.md`, дата `2026-07-24`.

Цифры из PoC:
- **p95 latency:** `0.4 s`
- **monthly cost at current volume:** `6,100 USD`
- **scale-out to 3x volume:** `90 s`
- **operations burden:** `a second cluster: upgrades, node images, Karpenter, 24/7 on-call`

Это же и цитируется в решении:
- `ADR-007: Keep Relay on EKS with autoscaling`
- `adr/ADR-007.md`, дата `2026-08-05`
- текст: `Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run).`

Если нужно, могу ещё показать, откуда взялась фраза про **“1.7x the monthly cost”** в сравнении с альтернативой.

### memory-eval-graph (completed, 4.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(p:PoC) WHERE d.text STARTS WITH 'Keep Relay on "]

Решение основано на PoC-2: Relay on EKS with autoscaling; источник — `meetings/2026-08-03-architecture-committee.txt`, дата решения `2026-08-03` (статус: `rejected`).

Цифры, на которых оно основано, из PoC:
- `p95_s = 0.4`
- `monthly_cost_usd = 6100`
- `ops_effort = "a second platform team"`

Само решение в графе сформулировано так:  
`Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)`  
Источник: `meetings/2026-08-03-architecture-committee.txt`, дата `2026-08-03`.

PoC-отчёт: `docs/poc-eks-report.md` (PoC-2).

### memory-eval-vector (completed, 6.0s, 3 tool calls)
queries: ['На каком PoC и на каких цифрах основано решение «Keep Relay on EKS with autoscal', 'Keep Relay on EKS with autoscaling rejected p95 0.4 s PoC цифры', 'PoC цифры Keep Relay on EKS with autoscaling p95 0.4 s']

Решение основано на **PoC-2: “Relay on EKS with autoscaling”**.

Цифры, на которых оно основано:
- **p95 delivery latency = 0.4 s**
- **monthly cost at current volume = $6,100**
- **scale-out to 3x volume = 90 s**
- **operations burden = второй кластер, upgrades, node images, Karpenter, 24/7 on-call**

Источники:
- `docs/poc-eks-report.md` — **2026-07-24**: результат PoC-2 с p95 0.4 s и cost $6,100.
- `meetings/2026-07-27-poc-review.txt` — **2026-07-27**: обсуждение PoC-2 с теми же цифрами и акцентом на второй кластер/платформенную команду.
- `meetings/2026-08-03-architecture-committee.txt` — **2026-08-03**: решение в ADR-007, где прямо сказано, что оно **based on poc-2**.
- `adr/ADR-007.md` — **updated 2026-08-05**: формулировка решения “rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run”.

Если хотите, я могу ещё коротко сопоставить эти цифры с альтернативой на Lambda из PoC-3.

## t41 [en / adr_status] What is the status of ADR-001 ('Migrate infrastructure code from Terraform to CloudFormation')?
**expected:** Superseded, superseded by ADR-004  
**expected sources:** {'sources': ['adr/ADR-001.md']}

### memory-eval-both (completed, 4.1s, 3 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'ADR-001 Migrate infrastructure code from Terraform to CloudFormation status']

ADR-001 is **Superseded**.

- **ID:** ADR-001
- **Title:** Migrate infrastructure code from Terraform to CloudFormation
- **Date:** 2026-01-14
- **File:** `adr/ADR-001.md`

Source:
- `adr/ADR-001.md` — status `Superseded`
- The memory text says it was **superseded by ADR-004**.

### memory-eval-graph (completed, 4.1s, 2 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:$id}) RETURN n.id, n.title']

ADR-001 is **Superseded**.  
- **Source:** `adr/ADR-001.md`, dated `2026-01-14`
- It was superseded by **ADR-004**: “Hybrid IaC: Terraform for networking, CloudFormation for application stacks”
  - **Source:** ADR record via the `SUPERSEDES` relationship, dated `2026-01-14` for ADR-001; the newer ADR is `ADR-004`.



### memory-eval-vector (completed, 2.7s, 3 tool calls)
queries: ["What is the status of ADR-001 ('Migrate infrastructure code from Terraform to Cl", 'ADR-001 Migrate infrastructure code from Terraform to CloudFormation status', 'status of ADR-001 Terraform to CloudFormation']

ADR-001 is **Superseded (superseded by ADR-004)**. Source: `adr/ADR-001.md`, updated **2026-01-14**.

## t42 [en / adr_status] What is the status of ADR-005 ('Evaluate EKS and Lambda with two proofs of concept')?
**expected:** Superseded, superseded by ADR-006  
**expected sources:** {'sources': ['adr/ADR-005.md']}

### memory-eval-both (completed, 5.0s, 3 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-005'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:'ADR-005'}) RETURN n.id, n.title", 'ADR-005 Context Evaluate EKS and Lambda with two proofs of concept']

ADR-005 is **Superseded**.

- **ADR-005: “Evaluate EKS and Lambda with two proofs of concept”**
- Date: **2026-06-17**
- Status: **Superseded**
- Source: **adr/ADR-005.md**

It is superseded by **ADR-006: “Run Relay on Lambda with provisioned concurrency”**.

Source files:
- **adr/ADR-005.md** — 2026-06-17
- **adr/ADR-006.md** — superseding ADR found in graph

### memory-eval-graph (completed, 3.6s, 2 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-005'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:'ADR-005'}) RETURN n.id, n.title"]

ADR-005 is **Superseded**.  
- **ADR-005**: “Evaluate EKS and Lambda with two proofs of concept” — **Superseded**, dated **2026-06-17**, file **adr/ADR-005.md**.  
- It was superseded by **ADR-006**: “Run Relay on Lambda with provisioned concurrency” — file **adr/ADR-006.md**.

### memory-eval-vector (completed, 2.8s, 3 tool calls)
queries: ["What is the status of ADR-005 ('Evaluate EKS and Lambda with two proofs of conce", 'ADR-005 Evaluate EKS and Lambda with two proofs of concept status', 'status of ADR-005 EKS Lambda two proofs of concept']

ADR-005 is **Superseded (superseded by ADR-006)**.

Source: `adr/ADR-005.md`, dated **2026-06-17**. The ADR header explicitly says: **“Status: Superseded (superseded by ADR-006)”**.

## t43 [en / adr_status] What is the status of ADR-007 ('Keep Relay on EKS with autoscaling')?
**expected:** Rejected  
**expected sources:** {'sources': ['adr/ADR-007.md']}

### memory-eval-both (completed, 2.2s, 2 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:$id}) RETURN n.id, n.title']

ADR-007 is **Rejected**.

- **ADR-007** — “Keep Relay on EKS with autoscaling”
- **Status:** Rejected
- **Date:** 2026-08-05
- **Source:** `adr/ADR-007.md`

No newer ADR was found that supersedes it.

### memory-eval-graph (completed, 3.5s, 2 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.date, a.file;", "MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:'ADR-007'}) RETURN n.id, n.title;"]

ADR-007 is **Rejected**. Source: `adr/ADR-007.md`, dated `2026-08-05`.

There is **no newer ADR recorded as superseding it** in memory.

### memory-eval-vector (completed, 3.2s, 3 tool calls)
queries: ["What is the status of ADR-007 ('Keep Relay on EKS with autoscaling')?", 'ADR-007 Keep Relay on EKS with autoscaling status', 'Keep Relay on EKS with autoscaling ADR-007']

ADR-007 is **Rejected**.

Sources:
- `adr/ADR-007.md` — updated **2026-08-05** — “**Status:** Rejected”
- `adr/ADR-007.md` — updated **2026-08-05** — Decision section says “Keep Relay on EKS with autoscaling (rejected …)”



## t44 [en / adr_status] What is the status of ADR-010 ('Gateway timeout policy for Lambda integrations')?
**expected:** Proposed; Never accepted; D20 (25 s) is the live decision and the ADR still proposes 20 s  
**expected sources:** {'sources': ['adr/ADR-010.md']}

### memory-eval-both (completed, 3.5s, 3 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:$id}) RETURN n.id, n.title, n.status, n.d']

ADR-010 is **Proposed**.

- **ADR-010** — *Gateway timeout policy for Lambda integrations*
- **Status:** Proposed
- **Date:** 2026-09-23
- **Source:** `adr/ADR-010.md`

No newer ADR was found to supersede it.

### memory-eval-graph (completed, 6.8s, 2 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:'ADR-010'}) RETURN n.id, n.title"]

ADR-010 is **Proposed**. Source: `adr/ADR-010.md` dated `2026-09-23`.

I also checked whether another ADR supersedes it; none was found in memory.

### memory-eval-vector (completed, 2.7s, 3 tool calls)
queries: ["What is the status of ADR-010 ('Gateway timeout policy for Lambda integrations')", 'ADR-010 Gateway timeout policy for Lambda integrations status', 'status of ADR-010 Gateway timeout policy for Lambda integrations']

ADR-010 is **Proposed**.

Sources:
- `adr/ADR-010.md`, updated **2026-09-23**: “Status: Proposed” in the ADR header.
- `adr/ADR-010.md`, updated **2026-09-23**: “No decision recorded; see Status.”
- `adr/ADR-010.md`, updated **2026-09-23**: “Proposed, not accepted.”

Retrieved hits all agree on **Proposed**.

## t45 [en / dependency] What did the decision 'Front Relay with the API gateway; the gateway and its routes…' depend on?
**expected:** One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway) (2026-02-09)  
**expected sources:** {'sources': ['meetings/2026-02-09-weekly-sync.txt', 'meetings/2026-03-02-weekly-sync.txt']}

### memory-eval-both (completed, 2.2s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Front Relay with the API gateway; t"]

The decision **“Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack”** depended on:

- **“One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)”**
  - **Date:** 2026-02-09
  - **Status:** active
  - **Source:** `meetings/2026-02-09-weekly-sync.txt`

So the dependency was the earlier CloudFormation stack-structure decision.

### memory-eval-graph (completed, 4.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'}) WHERE d.text STARTS "]

The decision **“Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack”** depended on:

- **“One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)”** — date **2026-02-09**, status **active**, source **meetings/2026-02-09-weekly-sync.txt**.  
  Source of the dependent decision: **meetings/2026-03-02-weekly-sync.txt**, date **2026-03-02**.



### memory-eval-vector (completed, 3.0s, 3 tool calls)
queries: ["What did the decision 'Front Relay with the API gateway; the gateway and its rou", 'Front Relay with the API gateway; the gateway and its routes depend on', 'Front Relay with the API gateway; the gateway and its routes… depend on']

The decision appears to depend on the context in **ADR-002: Front Relay with the API gateway**:

- Callers were reaching Relay directly through an internal load balancer with a shared API key.
- The goals were **authentication per caller**, **per-route timeouts and retries**, and **one place to see traffic**.
- The account’s API gateway already fronted two other services.

Source: **adr/ADR-002.md**, **2026-03-04**.

I did not find any explicit “depends on” statement beyond that context, so this is the closest memory-backed basis for the decision.
