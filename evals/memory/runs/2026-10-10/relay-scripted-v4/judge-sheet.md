
## m01 [en / fact] What is the delivery latency SLO and what exactly does it measure?
**expected:** p95 2 s over 5 minutes, from POST /deliver accepted to the first delivery attempt sent, not to the customer's answer; success rate 99.5% monthly  
**expected sources:** {'sources': ['docs/slo.md', 'meetings/2026-01-26-weekly-sync.txt']}

### memory-eval-both (completed, 5.2s, 3 tool calls)
queries: ['delivery latency SLO what does it measure latency delivery SLO Relay', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE", '"The latency SLO measures Relay, not the customer" delivery latency measures Rel']

The delivery latency SLO is **2 s p95 over a 5-minute window**.

What it measures:
- **From `POST /deliver` accepted**
- **To the first delivery attempt being sent**
- It measures **Relay’s internal delivery latency**, **not** the customer’s response time.

Source:
- `docs/slo.md`, updated `2026-01-28`
- Decision in force on this topic: `2026-10-05` says the p95 SLO was **relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s** (`meetings/2026-10-05-cutover-planning.txt`)

Assumption: you meant the **delivery latency** SLO on the SLO page, not the `GET /deliveries/*` latency SLO.

### memory-eval-graph (completed, 5.9s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE d.text CONTAINS 'd", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE d.status <> 'rejec"]

The current delivery latency SLO is: **p95 end-to-end delivery latency 3 s for 30 days after the serverless cutover, then back to 2 s**.  
Source: `meetings/2026-10-05-cutover-planning.txt`, dated `2026-10-05`.

What it measures: the graph only gives the wording **“p95 end-to-end delivery latency”** and does not further decompose the metric. So, in memory, it measures **end-to-end delivery latency at the 95th percentile**.  
Source: `meetings/2026-01-26-weekly-sync.txt`, dated `2026-01-26` (superseded wording) and `meetings/2026-10-05-cutover-planning.txt`, dated `2026-10-05`.

Note: the older decision said **p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%**, but that decision is superseded. Source: `meetings/2026-01-26-weekly-sync.txt`, dated `2026-01-26`.

### memory-eval-vector (completed, 3.9s, 3 tool calls)
queries: ['What is the delivery latency SLO and what exactly does it measure?', 'delivery latency SLO measures what exactly', 'latency SLO delivery webhook what does it measure']

The delivery latency SLO is **p95 = 2 s over a 5-minute window**. It measures **Relay-side latency from when `POST /deliver` is accepted until the first delivery attempt is sent**.

It **does not** measure customer response time; the SLO “ends when the first attempt is sent, not when the customer answers.”

Sources:
- `docs/slo.md`, updated **2026-01-28**: “Delivery latency, p95: from `POST /deliver` accepted to the first delivery attempt sent | 2 s | 5 minutes” and “The latency SLO measures Relay, not the customer…”
- `meetings/2026-01-26-weekly-sync.txt`, **2026-01-26**: older decision D02 says “end-to-end delivery latency,” but it is marked **superseded**.

## m02 [ru / fact] Сколько попыток доставки делает очередь до dead-letter и с какими задержками?
**expected:** 5 попыток, экспоненциально: 30 с, 2 мин, 10 мин, 30 мин, 2 ч; потом DLQ и алерт  
**expected sources:** {'sources': ['docs/retries-dlq.md', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 2.6s, 2 tool calls)
queries: ['очередь до dead-letter сколько попыток доставки задержки retry budget DLQ', 'delivery attempts to dead-letter delays retry budget DLQ queue']

Очередь делает **5 попыток** доставки, после чего сообщение уходит в **dead-letter queue**.

Задержки между попытками: **30 s, 2 min, 10 min, 30 min, 2 h**.

Источники:
- `docs/retries-dlq.md`, updated `2026-08-27`
- `adr/ADR-009.md`, updated `2026-08-26`

### memory-eval-graph (completed, 4.7s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.text CONTAIN"]

Очередь делает **5 попыток доставки** до перехода в dead-letter queue. Источник: **meetings/2026-08-24-weekly-sync.txt**, дата **2026-08-24**.

По задержкам в памяти **не указаны конкретные значения**. В найденном решении сказано только, что ретраи перенесены в SQS и после 5 попыток идёт DLQ; про интервалы/бэкофф там нет сведений. Источник: **meetings/2026-08-24-weekly-sync.txt**, дата **2026-08-24**.

### memory-eval-vector (completed, 3.6s, 1 tool calls)
queries: ['Сколько попыток доставки делает очередь до dead-letter и с какими задержками?']

Очередь делает **5 попыток** до dead-letter queue. Задержки по ретраям: **30 s, 2 min, 10 min, 30 min, 2 h**.

Источники:
- `docs/retries-dlq.md`, updated **2026-08-27** — механизм retries through SQS and DLQ.
- `adr/ADR-009.md`, updated **2026-08-26** — решение: retries move out of gateway into SQS with a dead-letter queue after 5 attempts.

Если нужно, могу ещё сказать, на какой именно попытке сообщение уходит в DLQ и как это влияет на статус delivery.

## m03 [en / fact] Why does the hybrid IaC layout keep networking in Terraform?
**expected:** cross-account peering and DNS delegation need custom resources in CloudFormation but are native in the Terraform the network team already maintains; moving network was 30% of the effort  
**expected sources:** {'sources': ['adr/ADR-004.md', 'meetings/2026-04-20-weekly-sync.txt', 'docs/iac-hybrid.md']}

### memory-eval-both (completed, 6.0s, 3 tool calls)
queries: ['hybrid IaC layout keep networking in Terraform why networking kept in Terraform ', 'hybrid IaC networking stays in Terraform rationale because Terraform owns VPC pe', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.text STARTS WITH"]

Because the live decision on the IaC topic says networking stays in Terraform while application stacks move to CloudFormation.

What the memory says:
- “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation.”  
  Source: `meetings/2026-04-20-weekly-sync.txt`, date `2026-04-20`
- ADR-004 confirms the boundary: “VPC, peering and DNS in Terraform; data, compute and gateway stacks in CloudFormation. Both sides run drift detection.”  
  Source: `adr/ADR-004.md`, date `2026-04-22`

So the rationale in memory is that Terraform remains responsible for the networking boundary, and CloudFormation owns the application stacks; the handoff is done through exported network values, and both sides use drift detection.  
Source: `docs/iac-hybrid.md`, date `2026-04-24`



### memory-eval-graph (completed, 4.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.text CONTAINS 'n"]

The graph says the hybrid IaC layout keeps networking in Terraform because the active decision on the IaC topic states:

- “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation”
  - date: 2026-04-20
  - status: active
  - source: `meetings/2026-04-20-weekly-sync.txt`

It also notes why this is called out: `docs/iac-cloudformation.md` was still saying all infrastructure, including networking, moves to CloudFormation, but that document is stale relative to the 2026-04-20 decision.
- source note on the decision: `docs/iac-cloudformation.md (updated 2026-02-11) still says all infrastructure including networking moves to CloudFormation`

So, in-memory reason: networking remains in Terraform because the later hybrid decision split responsibilities, leaving networking in Terraform and moving application stacks to CloudFormation.


### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['Why does the hybrid IaC layout keep networking in Terraform?', 'hybrid IaC layout keep networking in Terraform', 'networking in Terraform hybrid IaC layout']

The memory says **networking stays in Terraform because ADR-004 fixed the hybrid boundary**: VPC, peering, and DNS are kept in Terraform, while data/compute/gateway application stacks move to CloudFormation. The recorded consequence is that **both sides run drift detection**, and Terraform state was cleaned of resources already imported into stacks. Source: **adr/ADR-004.md** and **meetings/2026-04-20-weekly-sync.txt** (2026-04-22, 2026-04-20).

There is also a hand-off reason in the docs: Terraform exports network outputs to SSM Parameter Store, and CloudFormation reads them with dynamic references; changing a network output requires a Terraform apply and then a CloudFormation deploy, with no automatic trigger. Source: **docs/iac-hybrid.md** (2026-04-24).

If you want, I can also summarize the **full hybrid layout boundary** from memory.

## m04 [ru / contradiction] В gateway.md написано, что таймаут интеграции 10 секунд. Это актуально?
**expected:** нет; документ от 2026-03-18, таймаут менялся на 30 с (2026-05-18) и на 25 с (2026-08-24); текущее значение 25 с  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 4.3s, 2 tool calls)
queries: ["MATCH (doc:Document) WHERE doc.file ENDS WITH 'gateway.md' RETURN doc.file, doc.", 'gateway.md timeout integration 10 seconds актуально current stale integration ti']

Да — по текущему состоянию памяти `docs/gateway.md` уже не актуален по этому месту.

- В `docs/gateway.md` (updated `2026-03-18`) написано, что integration timeout — **10 seconds**.
- Но в найденной записи решения по topic `timeouts` сказано, что **gateway integration timeout raised from 10 s to 30 s** после инцидента `2026-05-14`, и это решение датировано `2026-05-18`.

Итог: `gateway.md` по этому факту **устарел**.

Источник:
- `docs/gateway.md`, `2026-03-18`
- `meetings/2026-05-18-weekly-sync.txt`, `2026-05-18`

### memory-eval-graph (completed, 4.4s, 2 tool calls)
queries: ["MATCH (doc:Document) WHERE doc.file ENDS WITH 'gateway.md' OR doc.title CONTAINS", "MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document {file:'docs/gateway.md'}) RE"]

Нет, это уже не актуально.

- `docs/gateway.md` обновлён `2026-03-18`, а позже его утверждение про `10 s` стало stale из-за решения **D12**: “Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14” — источник `meetings/2026-05-18-weekly-sync.txt`, дата `2026-05-18`.
- В памяти есть более позднее решение по gateway таймаутам: **D12**.

Итог: таймаут интеграции не 10 секунд; документ устарел.

### memory-eval-vector (completed, 4.1s, 3 tool calls)
queries: ['В gateway.md написано, что таймаут интеграции 10 секунд. Это актуально?', 'gateway.md integration timeout 10 seconds current status', 'таймаут интеграции 10 секунд gateway.md актуально']

Нет, не актуально.

По памяти:
- `docs/gateway.md`, updated `2026-03-18`, говорит, что timeout интеграции на каждом Relay route — **10 секунд**.
- Но более новая decision из `meetings/2026-05-18-weekly-sync.txt` от `2026-05-18` говорит, что gateway integration timeout **подняли с 10 s до 30 s**; этот claim помечен как `superseded`, и в нём прямо сказано, что `docs/gateway.md` устарел с `2026-05-18`.

Итого: `gateway.md` в части timeout'а устарел; текущая запись в памяти — изменение на 30 секунд.

## m05 [en / contradiction] The team roster page says Anna owns retries. Is that right today?
**expected:** no; roster updated 2026-07-08, retries moved from Anna to Ivan on 2026-09-07  
**expected sources:** {'sources': ['confluence/team-roster.xhtml', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 2.3s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.to IS NULL RE"]

No — today the current owner of retries is Ivan Melnik, starting 2026-09-07. Source: ownership edge query; Anna is not the live owner.

### memory-eval-graph (completed, 5.9s, 3 tool calls)
queries: ["MATCH (p:Person {key:'person:anna-sokolova'})-[o:OWNS]->(t:Topic {key:'topic:ret", "MATCH (p:Person {key:'person:anna-sokolova'})-[o:OWNS]->(t:Topic {key:'topic:ret", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) RETURN p.name AS pers"]

No — Anna does **not** own retries today.

- **Retries ownership on 2026-10-09:** **Ivan Melnik** owns `topic:retries` now, since **2026-09-07**.  
  Source: `topic:retries` ownership edge, graph memory query result.

- **Anna’s ownership period:** Anna Sokolova owned `topic:retries` from **2026-06-01** until **2026-09-07**.  
  Source: `topic:retries` ownership edge, graph memory query result.

So the roster page is stale on this point.

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['The team roster page says Anna owns retries. Is that right today?', 'Anna owns retries', 'retries owner Anna']

No — Anna does **not** own retries today. The current decision says **Ivan Melnik** owns retries from **2026-09-07**. Source: **meetings/2026-09-07-security-review.txt** (2026-09-07).

The team roster page is stale on this point: it still lists **Anna Sokolova** as retries owner, but it was updated on **2026-07-08**, and the newer ownership decision supersedes it. Source: **confluence/team-roster.xhtml** (2026-07-08) and **meetings/2026-09-07-security-review.txt** (2026-09-07).

## m06 [ru / contradiction] Decision log в Confluence актуален?
**expected:** нет; последняя версия 2026-06-03, в нём нет решений после 1 июня: ретраи на gateway (06-15), два PoC (06-15), передача PoC Ване (07-13), выбор Lambda (08-03), таймаут 25 с и ретраи через SQS (08-24), SSM (09-07), бюджет (09-21), даты катовера (10-05)  
**expected sources:** {'sources': ['confluence/decision-log.xhtml', 'memory/decisions.jsonl']}

### memory-eval-both (completed, 4.1s, 2 tool calls)
queries: ['Decision log Confluence актуален current stale updated decision log', "MATCH (doc:Document) WHERE doc.file = 'confluence/decision-log.xhtml' OPTIONAL M"]

Нет, не актуален.

Decision log в Confluence обновлён **2026-06-03**, но после этого есть решение от **2026-06-15**:  
- **D14** — “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%”  
  source: `meetings/2026-06-15-weekly-sync.txt`, date: `2026-06-15`

То есть страница уже устарела: она пропускает изменение факта “stops at 2026-06-01”, зафиксированное решением от 2026-06-15.

### memory-eval-graph (completed, 23.0s, 2 tool calls)
queries: ["MATCH (doc:Document) WHERE doc.file CONTAINS 'decision-log' OR toLower(doc.title", "MATCH (doc:Document {file:'confluence/decision-log.xhtml'}) OPTIONAL MATCH (dec:"]

Нет, **decision log в Confluence уже не актуален**: документ `confluence/decision-log.xhtml` обновлён **2026-06-03**, а после этого в памяти есть решения, которые его изменяют.

Что именно он пропускает:
- **D14** — `Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%` — **2026-06-15** — `meetings/2026-06-15-weekly-sync.txt`
- **D15** — `Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July` — **2026-06-15** — `meetings/2026-06-15-weekly-sync.txt`
- **D16** — `Serverless PoC ownership moves from Sergey to Ivan` — **2026-07-13** — `meetings/2026-07-13-weekly-sync.txt`
- **D17** — `Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances` — **2026-08-03** — `meetings/2026-08-03-architecture-committee.txt`
- **D18** — `Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)` — **2026-08-03** — `meetings/2026-08-03-architecture-committee.txt`
- **D19** — `DynamoDB migration dry run on a production snapshot is owned by Sergey, due 2026-09-04` — **2026-08-10** 

### memory-eval-vector (completed, 5.1s, 3 tool calls)
queries: ['Decision log в Confluence актуален?', 'Decision log Confluence актуален', 'актуален ли decision log в Confluence']

Да, **decision log в Confluence актуален**: найден документ **“Decision log”**, updated **2026-06-03**; в нём прямо указано, что решения из weekly sync записываются туда и страница обновляется после встречи. Источник: `confluence/decision-log.xhtml` от **2026-06-03**.

Но есть важная оговорка: в самом log указано, что **если страница расходится с записью встречи, запись встречи важнее**. То есть как рабочий источник он актуален, но при расхождениях приоритет у записи. Источник: `confluence/decision-log.xhtml` от **2026-06-03**.

Что я нашёл:
- `confluence/decision-log.xhtml` — updated **2026-06-03**
- `docs/onboarding.md` — updated **2026-03-10**, где сказано, что решения фиксируются в Confluence decision log

Если хотите, я могу ещё проверить, **нет ли более свежего решения, которое делает сам decision log устаревшим** — но по текущим данным в памяти он актуален.

## m07 [en / contradiction] ADR-010 says the gateway timeout for Lambda should be 20 s. Is that the policy?
**expected:** no; ADR-010 is Proposed and was never accepted; the live decision of 2026-08-24 is 25 s  
**expected sources:** {'sources': ['adr/ADR-010.md', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 5.2s, 3 tool calls)
queries: ['ADR-010 gateway timeout Lambda 20 s policy', 'ADR-010 таймаут gateway Lambda 20 сек policy', "MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.date, a.file"]

No — that is not the live policy.

ADR-010 is **Proposed** and says it is only a proposal:
- **adr/ADR-010.md**, updated **2026-09-23**: “**20 s on every route, with per-route overrides**” in the options, but also “**Proposed, not accepted**.”
- The same ADR says: “**The live value was set by the team on 2026-08-24 at 25 s; this document still says 20 s.**”
- Graph confirms ADR-010 status is **Proposed** on **2026-09-23**.

So the policy in force is **not 20 s**; the memory says **25 s** was the live decision as of 2026-08-24, and ADR-010 was still a proposal.

### memory-eval-graph (completed, 5.2s, 2 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20"]

No. ADR-010 is only a **Proposed** ADR, not the policy. The live policy in memory is the newer active decision dated **2026-08-24**, which says: **“Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom”**. Source: `meetings/2026-08-24-weekly-sync.txt`, dated **2026-08-24**.

ADR-010 itself is `adr/ADR-010.md`, dated **2026-09-23**, status **Proposed**, titled **“Gateway timeout policy for Lambda integrations”**. It is not the current policy unless and until it is accepted and there is no newer decision superseding the live one.

### memory-eval-vector (completed, 6.6s, 3 tool calls)
queries: ['ADR-010 says the gateway timeout for Lambda should be 20 s. Is that the policy?', 'gateway timeout Lambda 20 s policy ADR-010', 'ADR-010 Lambda gateway timeout 20 seconds']

No — ADR-010 is **not** the current policy. The memory says ADR-010 is **Proposed** and has **no decision recorded**. It also says the ADR still proposes **20 s**, but that is **not accepted**. Source: `adr/ADR-010.md`, updated **2026-09-23**.

The retrieved memory also says the live decision is **25 s** from **2026-08-24**, and that ADR-010 is stale on that point. Source: `adr/ADR-010.md`, updated **2026-09-23**.

Retrieved hits:
- `adr/ADR-010.md` — Context: hard limit 29 s; ADR proposes Lambda policy, **2026-09-23**
- `adr/ADR-010.md` — Options considered: “20 s on every route, with per-route overrides,” **2026-09-23**
- `adr/ADR-010.md` — Consequences: “Proposed, not accepted… live value… 25 s,” **2026-09-23**
- `adr/ADR-010.md` — Decision: “No decision recorded,” **2026-09-23**

## m08 [ru / contradiction] В runbook катовера написано, что владелец отката TBD. Кто на самом деле?
**expected:** Лена, решение 2026-10-05; runbook от 2026-09-29 устарел  
**expected sources:** {'sources': ['docs/runbook-cutover-serverless.md', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 6.7s, 4 tool calls)
queries: ["MATCH (doc:Document) WHERE doc.file ENDS WITH 'runbook' OR doc.title CONTAINS 'r", 'runbook катовера владелец отката TBD кто на самом деле', "MATCH (p:Person {name:'Lena Kim'})-[o:OWNS]->(x {key:'topic:cutover'}) RETURN p.", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:cutover'}) RETURN p.name, o.from"]

По факту владелец отката — **Lena Kim**.

Источник:
- **meetings/2026-10-05-cutover-planning.txt**, **2026-10-05** — решение: “Rollback owner for both cutovers is Lena. Owner: Lena Kim.”
- При этом в старом runbook это действительно было **TBD**:
  - **docs/runbook-cutover-serverless.md**, **2026-09-29**
  - **meetings/2026-09-21-weekly-sync.txt**, **2026-09-21**: “ранбук катовера выложил владелец отката там пока tbd”

Примечание: в графе не нашлось актуальной OWNS-связи на topic:cutover, поэтому опираюсь на зафиксированное решение из встречи.

### memory-eval-graph (completed, 4.3s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.text CONTAIN", "MATCH (o:OpenItem)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE o.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) RETURN d.text, d.dat"]

На самом деле владельец отката — **Лена**.

Источник: `meetings/2026-10-05-cutover-planning.txt`, решение от `2026-10-05` — **“Rollback owner for both cutovers is Lena”**.

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['В runbook катовера написано, что владелец отката TBD. Кто на самом деле?', 'runbook катовера владелец отката TBD кто владелец', 'rollback owner cutover runbook TBD who owns rollback']

На самом деле владелец отката — **Lena Kim**. Это зафиксировано в решении от **2026-10-05**: “Rollback owner for both cutovers is Lena. Owner: Lena Kim.”  
Источник: `meetings/2026-10-05-cutover-planning.txt` — **2026-10-05**.

Замечание: runbook с `TBD` уже устарел по сравнению с этим решением. В найденных материалах runbook `docs/runbook-cutover-serverless.md` упомянут как обновлённый **2026-09-29**, но решение новее.

## m09 [ru / crosslingual] Что на митингах называли «провижнд конкаренси» и почему без этого не проходит SLO?
**expected:** provisioned concurrency: прогретые инстансы Lambda на /deliver; без них p95 3.4 с при SLO 2 с, с ними 1.9 с (PoC-3)  
**expected sources:** {'sources': ['docs/poc-lambda-report.md', 'meetings/2026-07-27-poc-review.txt', 'adr/ADR-006.md']}

### memory-eval-both (completed, 5.6s, 2 tool calls)
queries: ['"провижнд конкаренси" SLO почему без этого не проходит', '"provisioned concurrency" SLO why without it does not pass']

Под «провижнд конкаренси» на митингах имели в виду **provisioned concurrency на `/deliver`**.

Почему без этого не проходит SLO:
- в отчёте PoC сказано: **“Within the 2 s SLO only with provisioned concurrency; without it the SLO is missed.”**  
  Источник: `docs/poc-lambda-report.md`, `2026-07-24`.
- в ADR это закреплено как решение: **“Provisioned concurrency on /deliver is a condition, not an optimisation: without it the SLO is missed.”**  
  Источник: `adr/ADR-006.md`, `2026-08-05`.
- на встрече Иван формулировал это по-русски: **“провижнд конкаренси на deliver обязательно без него не проходим”**.  
  Источник: `meetings/2026-07-27-poc-review.txt`, `2026-07-27`.

Смысл SLO здесь — latency до **первой попытки доставки**; в записи встречи Анна уточнила, что это не про ответ клиента:  
**“SLO две секунды это про первую попытку доставки а не про ответ клиента”**.  
Источник: `meetings/2026-07-27-poc-review.txt`, `2026-07-27`.

Если хотите, могу ещё коротко объяснить, **почему именно Lambda без provisioned concurrency не укладывается в эти 2 секунды по записям**.

### memory-eval-graph (completed, 8.1s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE d.date <= '2026-08"]

На митингах под «провижнд конкаренси» имели в виду **provisioned concurrency в Lambda** для маршрута **`/deliver`**: это прямо сказано в решении от **2026-08-03** — «Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances»; источник: **`meetings/2026-08-03-architecture-committee.txt`**.

Почему без этого не проходит SLO: в памяти есть SLO по доставке с требованием **p95 end-to-end delivery latency 2 s over 5 minutes**; оно зафиксировано в решении от **2026-01-26** в **`meetings/2026-01-26-weekly-sync.txt`**. Для серверлесс-варианта отдельно зафиксировано, что с **warm instances** p95 был **1.9 s** в PoC-3, то есть смысл provisioned concurrency — держать инстансы тёплыми, чтобы уложиться в этот p95-порог. Если без неё, из памяти не видно отдельного решения с цифрой «не проходит», но связь в решениях именно такая: provisioned concurrency нужна, чтобы обеспечить warm instances и тем самым выполнить SLO.

Сводка по источникам:
- **`meetings/2026-08-03-architecture-committee.txt`**, **2026-08-03** — Lambda + provisioned concurrency on `/deliver`, PoC-3, p95 1.9 s.
- **`meetings/2026-01-26-weekly-sync.txt`**, *

### memory-eval-vector (completed, 8.6s, 3 tool calls)
queries: ['Что на митингах называли «провижнд конкаренси» и почему без этого не проходит SL', 'провижнд конкаренси SLO митинг Relay webhook delivery', 'provisioned concurrency SLO meeting Relay webhook delivery']

На митингах под «провижнд конкаренси» имели в виду **provisioned concurrency для Lambda на `/deliver`** — то есть держать заранее прогретые инстансы, чтобы первый вызов не попадал на cold start. Источники: meeting `meetings/2026-07-27-poc-review.txt` от **2026-07-27** и meeting `meetings/2026-08-03-architecture-committee.txt` от **2026-08-03**.

Почему без этого не проходит SLO:
- На PoC review сказали, что **без provisioned concurrency SLO не проходит**; при этом p95 сравнивали как **0.4 vs 1.9**, и `1.9` — это **на грани SLO**. Источник: `meetings/2026-07-27-poc-review.txt`, **2026-07-27**.
- В документах это зафиксировано как решение: **“Provisioned concurrency on /deliver is a condition, not an optimisation: without it the SLO is missed.”** Источник: `adr/ADR-006.md`, **2026-08-05**.
- Сам SLO по latency — это **2 s до первой попытки доставки**, а не до ответа клиента. Источник: `docs/slo.md`, **updated 2026-01-28**.
- На комитете также сказали, что **Lambda проходит SLO только с прогревом**. Источник: `meetings/2026-08-03-architecture-committee.txt`, **2026-08-03**.

Коротко: речь была о **предварительно прогретой concurrency на Lambda**, и без неё **p95 latency первой попытки

## m10 [en / crosslingual] What did the team mean by 'дрифт' and what rule came out of it?
**expected:** drift detection: stacks diverging from reality after manual console changes; after the 2026-02-23 incident manual prod changes were frozen and nightly DetectStackDrift runs with alerts  
**expected sources:** {'sources': ['meetings/2026-02-23-incident-review.txt', 'docs/drift-detection.md']}

### memory-eval-both (completed, 5.5s, 3 tool calls)
queries: ['дрифт what did the team mean by drift and what rule came out of it', 'drift what did the team mean by drift and what rule came out of it', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:iac'}) WHERE d.text STARTS WIT"]

By “дрифт” the team meant a stack/state mismatch: something was changed manually, so the live AWS resource no longer matched the template.

The rule that came out of it was:
- no manual changes in the AWS console for production resources that belong to a Relay stack;
- nightly `DetectStackDrift` on every Relay stack at 01:00;
- if a stack is `DRIFTED`, the pipeline is blocked until it’s reconciled.

Source: `docs/drift-detection.md`, updated `2026-02-25`.

The incident review also framed the cause as “a manual load balancer change was reverted by the nightly deploy,” and the meeting note says Lena proposed banning manual console changes and enabling nightly drift detection with alerts. Source: `meetings/2026-02-23-incident-review.txt`, `2026-02-23`.

### memory-eval-graph (completed, 4.0s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.text CONTAINS 'д", "MATCH (o:OpenItem)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE o.text CONTAINS 'д"]

By “дрифт” the team meant **configuration drift**: manual console changes that make stacks differ from the intended state. The rule that came out of it was:

- **Manual console changes are frozen; nightly drift detection runs on every stack with alerts to on-call** — source: `meetings/2026-02-23-incident-review.txt`, date `2026-02-23` (Decision D04, active).

Related follow-up:
- **Route drift-detection alerts to on-call** — source: the open item `O8` raised on `2026-02-23`, now closed.



### memory-eval-vector (completed, 5.2s, 3 tool calls)
queries: ["What did the team mean by 'дрифт' and what rule came out of it?", 'дрифт rule team mean', 'дрифт came out of it rule']

By **“дрифт”** the team meant **configuration drift**: a stack had been changed manually in the console so it no longer matched the expected real state. In the incident review, Lena said, “мы не видим дрифт пока не наступим” after a manual load balancer timeout change caused the stack to diverge from reality. Source: `meetings/2026-02-23-incident-review.txt`, 2026-02-23.

The rule that came out of it was:

1. **No manual changes in the AWS console for production Relay stack resources.**
2. **Every Relay stack runs `DetectStackDrift` nightly at 01:00.**
3. **A stack in `DRIFTED` state blocks the pipeline until it is reconciled.**

Source: `docs/drift-detection.md`, updated 2026-02-25.

The reconciliation rule says: if the change was intended, put it in the template, deploy, and confirm `IN_SYNC`; if it was not intended, redeploy the stack and let the template win. Source: `docs/drift-detection.md`, updated 2026-02-25.

## m11 [en / multi_hop] Why were gateway retries on /deliver turned off in August, when they had been turned on in June?
**expected:** June: retries enabled (max 3, budget 15%) once idempotency keys were mandatory; August: Lambda intake is asynchronous and a gateway retry enqueues twice, so retries moved to SQS with a DLQ (ADR-009) and gateway retries were turned off  
**expected sources:** {'sources': ['meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt', 'adr/ADR-009.md']}

### memory-eval-both (completed, 7.1s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.text CONTAIN", 'gateway retries /deliver turned off August turned on June why', 'ретраи шлюза /deliver отключили в августе включили в июне почему']

In August, gateway retries on `/deliver` were turned off because the retry mechanism was moved out of the gateway and into SQS with a dead-letter queue after 5 attempts.

The relevant decision says:
- 2026-08-24, active: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off” — source: `meetings/2026-08-24-weekly-sync.txt`

The earlier June decision had retries on at the gateway:
- 2026-06-15, superseded: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%” — source: `meetings/2026-06-15-weekly-sync.txt`

Why they were turned off:
- The docs and meeting notes tie gateway retries to the non-idempotency risk: a retried delivery could reach a customer twice.
- By August, the chosen alternative was queue-based retries, which provide retry handling in SQS and visibility via the DLQ instead of gateway policy.
- Sources:
  - `docs/idempotency.md` updated 2026-05-20: “Gateway retries on `/deliver` were disabled on 2026-03-30 because a retried delivery could reach a customer twice.”
  - `adr/ADR-009.md` updated 2026-08-26: “Retries in SQS with a dead-letter queue after 5 attempts; gateway

### memory-eval-graph (completed, 8.3s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'})\nWHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'})\nWHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'})\nWHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nRETURN d.id, d.text,"]

Gateway retries on `/deliver` were turned off in August because the retry mechanism was moved out of the gateway and into SQS with a dead-letter queue after 5 attempts.

What I found:
- On 2026-06-15, the gateway retries on `POST /deliver` were enabled: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%” (`meetings/2026-06-15-weekly-sync.txt`).
- On 2026-08-24, that decision was changed to: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off” (`meetings/2026-08-24-weekly-sync.txt`).

So the August change was a redesign of retry handling, not just a toggle.

Source and dates:
- `meetings/2026-06-15-weekly-sync.txt`, 2026-06-15
- `meetings/2026-08-24-weekly-sync.txt`, 2026-08-24

### memory-eval-vector (completed, 5.6s, 3 tool calls)
queries: ['Why were gateway retries on /deliver turned off in August, when they had been tu', 'gateway retries /deliver turned off in August turned on in June', 'gateway retries on /deliver August June turned off on']

Gateway retries on `/deliver` were turned off because a retried delivery could reach a customer twice, and the endpoint was not idempotent yet. The later August decision moved retries away from the gateway entirely and into SQS/DLQ, so retries were “no longer a gateway policy.”  
Sources:
- `docs/idempotency.md` (updated 2026-05-20): gateway retries on `/deliver` were disabled because a retried delivery could reach a customer twice.
- `adr/ADR-009.md` (updated 2026-08-26): “Retries through SQS with a dead-letter queue” was chosen; gateway retries off on `/deliver`.
- `docs/retries-dlq.md` (updated 2026-08-27): “Decided 2026-08-24 (ADR-009). Retries are no longer a gateway policy.”

I did not find anything saying they were turned on in June in the retrieved memory, so I can only explain the off decision, not the June-on decision.

## m12 [ru / multi_hop] Какая цепочка событий привела к тому, что сеть осталась в Terraform?
**expected:** январь: решение переехать целиком на CloudFormation (ADR-001, Тимур против); апрель: Серёжа принёс цифры (кастомные ресурсы для пиринга и DNS, 4 недели), Паша возражал, приняли гибрид (ADR-004, заменяет ADR-001)  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-04-13-weekly-sync.txt', 'meetings/2026-04-20-weekly-sync.txt', 'adr/ADR-004.md']}

### memory-eval-both (completed, 8.1s, 3 tool calls)
queries: ['MATCH path=(cur:Decision)-[:SUPERSEDES*1..6]->(old:Decision) WHERE cur.status <>', 'Terraform network stayed in Terraform chain of events why', 'сеть осталась в Terraform почему цепочка событий']

Цепочка такая:

1. **Сначала приняли решение мигрировать всю инфраструктуру из Terraform в CloudFormation** — это было решение **D01** от **2026-01-12**.  
   Источник: `meetings/2026-01-12-weekly-sync.txt`  
   Текст: “Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1”.

2. **Потом это решение было пересмотрено** — в **D09** от **2026-04-20** решили:  
   “**Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation**.”  
   Источник: `meetings/2026-04-20-weekly-sync.txt`

3. **Почему именно сеть осталась в Terraform:** в ADR-004 сказано, что  
   “the networking module was the last to move and the hardest: cross-account peering and DNS delegation need custom resources in CloudFormation, while the same networking is already expressed natively in the Terraform the network team maintains for the whole company.”  
   Источник: `adr/ADR-004.md`  
   Дата: **2026-04-22**

Итого: **исходный план полного переезда на CloudFormation (D01) столкнулся с тем, что сетевой слой оказался последним и самым сложным для переноса, плюс он уже нативно поддерживался командой сети в Terraform; поэтому в

### memory-eval-graph (completed, 7.8s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.text CONTAINS 'T", 'MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision) WHERE (cur)-[:ABOUT', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (d)-[:SUP"]

Цепочка, которая привела к тому, что сеть осталась в Terraform, такая:

1. Сначала решили мигрировать Relay с Terraform на CloudFormation по частям, до конца Q1.  
   Источник: `meetings/2026-01-12-weekly-sync.txt`, дата `2026-01-12`  
   Текст решения: “Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1”.

2. Потом приняли более детальную схему CloudFormation: один root stack на окружение и nested stacks по компонентам, включая network.  
   Источник: `meetings/2026-02-09-weekly-sync.txt`, дата `2026-02-09`  
   Текст решения: “One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)”.

3. Затем финально скорректировали курс: сеть, то есть VPC/peering/DNS, оставили в Terraform, а application stacks перевели в CloudFormation.  
   Источник: `meetings/2026-04-20-weekly-sync.txt`, дата `2026-04-20`  
   Текст решения: “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation”.

Итог: сеть осталась в Terraform из-за решения о гибридной модели IaC, которое заменило более ранний план полной миграции.

### memory-eval-vector (completed, 8.6s, 1 tool calls)
queries: ['Какая цепочка событий привела к тому, что сеть осталась в Terraform?']

Цепочка событий, которая привела к тому, что сеть осталась в Terraform:

1. Сначала был принят курс на миграцию всей инфраструктуры из Terraform в CloudFormation. В ADR-001 сказано, что Terraform-описание инфраструктуры устарело, а остальной AWS-ландшафт уже был на CloudFormation.  
   Источник: `adr/ADR-001.md`, 2026-01-14.

2. При реализации миграции выяснилось, что сеть — последний и самый сложный модуль для переноса, потому что:
   - cross-account peering,
   - DNS delegation,
   - необходимость custom resources в CloudFormation,
   - при этом та же сеть уже была нативно описана в Terraform, которым управляла network team.  
   Источник: `adr/ADR-004.md`, 2026-04-22.

3. На weekly sync 2026-04-20 приняли новое решение: сделать гибридную схему — networking оставить в Terraform, а application stacks перевести в CloudFormation. Это решение записано как активное и оно supersedes ADR-001.  
   Источник: `meetings/2026-04-20-weekly-sync.txt`, 2026-04-20.

4. В ADR-004 зафиксировано итоговое решение: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation. Там же отмечено возражение Павла Гришина.  
   Источник: `adr/ADR-004.md`, 2026-04-22.

Итог: сет

## m13 [en / multi_hop] Which decision closed the longest-standing open item, who took it, and how many times had it been raised before?
**expected:** D19 on 2026-08-10: Sergey took the DynamoDB dry run (due 2026-09-04); raised 2026-05-04 and again on 05-18, 06-15, 06-29, 07-20 (four times)  
**expected sources:** {'sources': ['meetings/2026-05-04-poc-review.txt', 'meetings/2026-08-10-weekly-sync.txt']}

### memory-eval-both (completed, 9.3s, 4 tool calls)
queries: ['MATCH (o:OpenItem) WHERE NOT EXISTS { MATCH (o)<-[:CLOSES]-(:Decision) } AND o.r', "MATCH (d:Decision)-[:CLOSES]->(o:OpenItem {id:'O8'}) OPTIONAL MATCH (p:Person)-[", 'O8 Route drift-detection alerts to on-call closed by decision who proposed or ow', 'raised again open item closed by decision how many times raised O8 route drift-d']

Assumption: I treated “longest-standing open item” as the open item with the earliest raised date among items that were later closed.

The open item was **“Route drift-detection alerts to on-call”**:
- Raised: **2026-02-23**
- Closed by decision **D04**
- Decision text: **“Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call.”**
- Decision date/source: **2026-02-23, meetings/2026-02-23-incident-review.txt**

Who took it:
- **Lena Kim**
- Source says: **Owner: Lena Kim since 2026-03-02**  
  Source file/date: **meetings/2026-02-23-incident-review.txt, 2026-02-23**

How many times it had been raised before closing:
- The memory shows **no raised_again entries** for this item, so it had been raised **1 time total** before closure.
- Source file/date: **meetings/2026-02-23-incident-review.txt, 2026-02-23**

### memory-eval-graph (completed, 5.6s, 2 tool calls)
queries: ['MATCH (o:OpenItem)\nWHERE EXISTS { MATCH (:Decision)-[:CLOSES]->(o) }\nWITH o, siz', 'MATCH (o:OpenItem)\nWHERE EXISTS { MATCH (:Decision)-[:CLOSES]->(o) }\nWITH o, siz']

Assumption: “longest-standing open item” means the open item with the earliest `raised` date among items that were eventually closed.

The decision was **“DynamoDB migration dry run on a production snapshot is owned by Sergey, due 2026-09-04”**, dated **2026-08-10**, source **`meetings/2026-08-10-weekly-sync.txt`**. It closed open item **O1: “DynamoDB migration dry run on a production snapshot”**, which was first raised on **2026-05-04** and raised again on **2026-05-18, 2026-06-15, 2026-06-29, and 2026-07-20**. The item had been raised **5 times total**. Source for the open item: the item’s `raised` and `raised_again` dates from the graph; source file shown via the closing decision row above.

### memory-eval-vector (completed, 8.9s, 3 tool calls)
queries: ['Which decision closed the longest-standing open item, who took it, and how many ', 'longest-standing open item closed decision raised before who took it', 'decision closed open item raised before times who took it longest-standing']

The decision is **D19**, which closed the **database** open item “DynamoDB migration dry run on a production snapshot.” The item was **raised 5 times before closure**: on 2026-05-04, 2026-05-18, 2026-06-15, 2026-06-29, and 2026-07-20. Source: **meetings/2026-05-04-poc-review.txt** (2026-05-04), claim **O1**.

What I retrieved suggests this was the longest-standing closed open item among the hits:
- **O1 / database** — raised 2026-05-04, closed by D19, raised again 4 times afterward. Source: **meetings/2026-05-04-poc-review.txt** (2026-05-04)
- **O8 / iac** — raised 2026-02-23, closed, but only one raised-again date is visible in the retrieved chunk. Source: **meetings/2026-02-23-incident-review.txt** (2026-02-23)
- **O6 / compute** — raised 2026-08-03, closed. Source: **meetings/2026-08-03-architecture-committee.txt** (2026-08-03)
- **O2 / cutover** — raised 2026-08-24, closed. Source: **meetings/2026-08-24-weekly-sync.txt** (2026-08-24)

I can’t fully prove “longest-standing” from the retrieved chunks alone, but among the retrieved closed items, **O1** is the oldest and the only one explicitly marked as closed by **D19**.

## m14 [ru / multi_hop] Кто возражал против переезда на CloudFormation в январе и какую позицию он занял в апреле, когда обсуждали гибрид?
**expected:** Тимур возражал в январе (ADR-001); в апреле поддержал гибрид Серёжи («тулинг надо выбирать по задаче»); возражал в апреле уже Паша  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 5.4s, 3 tool calls)
queries: ['возражал против переезда на CloudFormation январе гибрид апреле кто возражал поз', 'CloudFormation migration January objected hybrid April who objected position tak', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'iac'}) OPTIONAL MATCH (a:Person)-[:OB"]

В январе против переезда на CloudFormation возражал **Тимур Алиев**; это было в решении от **2026-01-12** из `meetings/2026-01-12-weekly-sync.txt`.

В апреле, когда обсуждали **гибрид**, он занял позицию **«объектовал/возражение не снимал»** — но на этот раз возражение было записано уже за **Павлом Гришиным**, а итоговая позиция стала такой: **Terraform для сети, CloudFormation для application stacks**. Это зафиксировано в `adr/ADR-004.md` от **2026-04-22**.

Источники:
- `meetings/2026-01-12-weekly-sync.txt`, 2026-01-12
- `adr/ADR-004.md`, 2026-04-22

### memory-eval-graph (completed, 7.6s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.date STARTS WITH", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.date STARTS WITH", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.date STARTS WITH", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.date STARTS WITH"]

В январе против переезда на CloudFormation возражал **Тимур А.**: он objected to decision от **2026-01-12** про миграцию Relay infrastructure code from Terraform to CloudFormation; decision сейчас **superseded**. Источник: **meetings/2026-01-12-weekly-sync.txt**, дата **2026-01-12**.

В апреле, когда обсуждали гибрид, позицию занял **Павел Г.**: он objected to decision от **2026-04-20** — **“Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation”**. Это decision **active**. Источник: **meetings/2026-04-20-weekly-sync.txt**, дата **2026-04-20**.

Предположение: под «Кто возражал» я взял единственного возражавшего, найденного в январском решении.

### memory-eval-vector (completed, 5.7s, 3 tool calls)
queries: ['Кто возражал против переезда на CloudFormation в январе и какую позицию он занял', 'возражал против переезда на CloudFormation в январе hybrid апрель позиция', 'January CloudFormation opposed April hybrid position']

В январе против переезда на CloudFormation возражал **Тимур Алиев**: в weekly sync от **2026-01-12** он сказал «я против, но не блокирую», и его возражение записали. Источник: `meetings/2026-01-12-weekly-sync.txt` (2026-01-12).

В апреле, когда обсуждали гибрид, в ADR-004 зафиксирована позиция **объединённая**: **сеть остаётся в Terraform, а application stacks — в CloudFormation**. Там же записано, что возражение было от **Pavel Grishin**. Источник: `adr/ADR-004.md` (2026-04-22).

Если вы имели в виду одного и того же человека, то в памяти есть несостыковка: январское возражение относится к Тимуру, а апрельское — к Павлу.

## m15 [en / point_in_time] On 2026-07-01, who owned retries, who owned the serverless PoC, and was the dry run owned?
**expected:** retries: Anna (since 06-01); serverless PoC: Sergey (until 07-13); dry run: no owner  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-06-29-weekly-sync.txt']}

### memory-eval-both (completed, 3.4s, 3 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(x {key:'topic:retries'}) WHERE o.from <= '2026-07-01", "MATCH (p:Person)-[o:OWNS]->(x {key:'poc:poc-3'}) WHERE o.from <= '2026-07-01' AN", "MATCH (p:Person)-[o:OWNS]->(x {key:'topic:database'}) WHERE o.from <= '2026-07-0"]

On 2026-07-01:

- retries was owned by Anna Sokolova, from 2026-06-01 to 2026-09-07. Source: graph ownership edge; date: 2026-06-01.
- the serverless PoC was owned by Ivan Melnik, from 2026-06-22 onward. Source: graph ownership edge; date: 2026-06-22.
- the dry run was owned by Denis Orlov, from 2026-04-06 onward. Source: graph ownership edge; date: 2026-04-06.

### memory-eval-graph (completed, 6.3s, 4 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.from <= $D AN", "MATCH (p:Person)-[o:OWNS]->(poc:PoC {key:'poc:poc-3'}) WHERE o.from <= $D AND (o", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:cutover'}) WHERE t.name CONTAINS", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:cutover'}) WHERE o.from <= $D AN"]

On 2026-07-01:

- Retries was owned by **Anna Sokolova**; the OWNS edge was active from **2026-06-01** to **2026-09-07**. Source: graph ownership edge for `topic:retries` (no document file; ownership edge, dated by the edge interval).
- The serverless PoC (`poc:poc-3`) was owned by **Ivan Melnik**; the OWNS edge was active from **2026-06-22** and had no end date. Source: graph ownership edge for `poc:poc-3` (no document file; ownership edge, dated by the edge interval).
- I found **no owned “dry run” topic/item on 2026-07-01** in the graph. Source: ownership lookup returned no matching node/edge on that date.

Assumption: I interpreted “the dry run” as the cutover-related dry-run item/topic, but there was no matching owned topic/item in memory.

### memory-eval-vector (completed, 13.6s, 3 tool calls)
queries: ['On 2026-07-01, who owned retries, who owned the serverless PoC, and was the dry ', '2026-07-01 retries owner serverless PoC owner dry run owner', 'retries serverless PoC dry run ownership 2026-07-01']

On 2026-07-01, the memory does **not** contain a direct decision for all three items, but it does contain these relevant records:

- **Retries**: the closest ownership record says retries were owned by **Anna Sokolova** since **2026-06-01** in `confluence/team-roster.xhtml` (updated **2026-07-08**). It also says retries are owned by the Relay core lead until serverless cutover in `docs/retries-dlq.md` (updated **2026-08-27**), which is newer and therefore the roster line is stale on that point.
- **Serverless PoC**: `meetings/2026-07-13-weekly-sync.txt` has an active ownership decision dated **2026-07-13** saying ownership moves from Sergey to **Ivan Melnik**. In `confluence/team-roster.xhtml` updated **2026-07-08**, Ivan is listed as owning the serverless PoC, but that table also says it was still being handed over; the **2026-07-13** decision is newer.
- **Dry run**: `meetings/2026-05-04-poc-review.txt` records the dry run as **open without an owner**. `meetings/2026-08-10-weekly-sync.txt` later assigns it to **Sergey Belov**, so the older note is stale after that. For **2026-07-01**, the memory supports **no owner**.

So, for **2026-07-01**:
- retries: **Anna Sokolova**
- server

## m16 [ru / point_in_time] Какой таймаут на gateway действовал 1 июля 2026 и кто был его владельцем?
**expected:** 30 с (решение 2026-05-18, заменило 10 с), владелец Паша  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt']}

### memory-eval-both (completed, 6.4s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20", "MATCH (p:Person)-[o:OWNS]->(x {key:'topic:timeouts'}) WHERE o.from <= '2026-07-0", "MATCH (p:Person)-[o:OWNS]->(x {key:'topic:gateway'}) WHERE o.from <= '2026-07-01"]

На 2026-07-01 для **gateway** действовало решение: **таймаут интеграции увеличен с 10 с до 30 с**.  
Источник: `meetings/2026-05-18-weekly-sync.txt`, дата решения `2026-05-18` — но статус у него **superseded**, то есть позже оно было заменено.

**Владелец gateway на 2026-07-01:** **Павел Гришин**.  
Источник: OWNS на `topic:gateway`, начало `2026-03-02`, без даты окончания.

Если хотите, я могу ещё проверить, **какое именно решение было в силе на 2026-07-01 после superseded-замены**.

### memory-eval-graph (completed, 6.8s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= $D ", "MATCH (p:Person)-[o:OWNS]->(x {key:'topic:timeouts'}) WHERE o.from <= $D AND (o.", "MATCH (p:Person)-[o:OWNS]->(x {key:'topic:gateway'}) WHERE o.from <= $D AND (o.t"]

На 2026-07-01 в памяти есть такой факт по таймауту gateway: **10 s → 30 s**; это решение от **2026-05-18** со статусом **superseded** из файла **meetings/2026-05-18-weekly-sync.txt**.  
Но по топику **timeout** у меня **нет владельца на эту дату** в графе памяти.

Если вы имели в виду владельца **gateway** как топика целиком, то на **2026-07-01** его владелец был **Pavel Grishin** — файл/источник владения в графе не хранится, но дата владения начинается с **2026-03-02** и не заканчивается.

Сводка:
- **Таймаут:** 30 s, действовало решение от **2026-05-18**, источник: **meetings/2026-05-18-weekly-sync.txt**
- **Владелец timeout:** **не найден**
- **Владелец gateway:** **Pavel Grishin**, с **2026-03-02**

### memory-eval-vector (completed, 7.2s, 3 tool calls)
queries: ['Какой таймаут на gateway действовал 1 июля 2026 и кто был его владельцем?', 'таймаут gateway 1 июля 2026 владелец', 'gateway timeout owner 2026-07-01']

На **1 июля 2026** в памяти есть текущая история по таймауту gateway через решения:

- **10 s** — было в решении **D06** от **2026-03-16**; это решение **superseded**.
- **30 s** — стало в решении **D12** от **2026-05-18**; оно тоже помечено **superseded**, но на **1 июля 2026** это был последний найденный действующий на тот момент лимит.
- Позже, **2026-08-24**, решение **D20** снизило таймаут до **25 s** и **supersedes D12**, но это уже после 1 июля.

**Владелец gateway**: **Pavel Grishin** с **2026-03-02**; запись активна и текущая.  
Источник: `memory/decisions.jsonl` от **2026-03-02**.

Итого: **на 1 июля 2026 таймаут gateway был 30 s, владелец — Pavel Grishin**.  
Источники:  
- `meetings/2026-05-18-weekly-sync.txt` — **2026-05-18** (D12, timeout 30 s)  
- `memory/decisions.jsonl` — **2026-03-02** (ownership gateway: Pavel Grishin)  
- `meetings/2026-08-24-weekly-sync.txt` — **2026-08-24** (D20, позже снизил до 25 s)



## m17 [en / aggregate] Which decisions were made at the architecture committee on 2026-08-03 and which open item was raised there?
**expected:** D17 Lambda with provisioned concurrency (ADR-006), D18 keep EKS rejected (ADR-007); open item: provisioned concurrency sizing, taken by Ivan on 08-10  
**expected sources:** {'sources': ['meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 4.2s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:DECIDED_IN]->(m:Meeting {date:'2026-08-03'}) RETURN d.id, d", "MATCH (o:OpenItem)-[:RAISED_IN]->(m:Meeting {date:'2026-08-03'}) OPTIONAL MATCH "]

At the architecture committee on 2026-08-03, these decisions were made:

- D17: “Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances” — status: active  
  Source: `meetings/2026-08-03-architecture-committee.txt`, date `2026-08-03`

- D18: “Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)” — status: rejected  
  Source: `meetings/2026-08-03-architecture-committee.txt`, date `2026-08-03`

The open item raised there was:

- O6: “Provisioned concurrency sizing for /deliver”  
  Raised: `2026-08-03`  
  Status: closed  
  Owner: Ivan Melnik  
  Source: meeting date `2026-08-03`

### memory-eval-graph (completed, 6.2s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:DECIDED_IN]->(m:Meeting {date:$date}) RETURN d.id, d.text, ', 'MATCH (o:OpenItem)-[:RAISED_IN]->(m:Meeting {date:$date}) OPTIONAL MATCH (p:Pers']

At the architecture committee on 2026-08-03, these decisions were made:

- **D17** — “Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances” — **active** — source: `meetings/2026-08-03-architecture-committee.txt` — date: 2026-08-03.
- **D18** — “Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)” — **rejected** — source: `meetings/2026-08-03-architecture-committee.txt` — date: 2026-08-03.

The open item raised there was:

- **O6** — “Provisioned concurrency sizing for /deliver” — raised: 2026-08-03 — raised again: [] — status: closed — source meeting: `meetings/2026-08-03-architecture-committee.txt`.

Assumption: I treated “made at the architecture committee on 2026-08-03” as decisions linked to the meeting dated 2026-08-03.

### memory-eval-vector (completed, 9.4s, 3 tool calls)
queries: ['Which decisions were made at the architecture committee on 2026-08-03 and which ', 'architecture committee 2026-08-03 decisions open item raised', '2026-08-03 architecture committee decision open item']

На архитектурном комитете **2026-08-03** были зафиксированы такие решения:

1. **Relay переезжает на Lambda с provisioned concurrency для /deliver.**  
   - **ADR 006 принят**, **ADR 007 отклонён**, **владелец — Ваня**, возражение Тимура записано.  
   - Источник: `meetings/2026-08-03-architecture-committee.txt` (2026-08-03), фрагмент `00:01:11–00:01:55`.

2. **По compute рассматривали Lambda и EKS, затем проголосовали за Lambda с provisioned concurrency для /deliver**; это подтверждает то же решение выше.  
   - Источник: `meetings/2026-08-03-architecture-committee.txt` (2026-08-03), фрагменты `00:00:06–00:00:39` и `00:00:39–00:01:11`.

Открытый вопрос, поднятый там:
- **Sizing provisioned concurrency: сколько инстансов держать для /deliver.**  
  - В одном фрагменте это явно названо открытым вопросом.  
  - Источник: `meetings/2026-08-03-architecture-committee.txt` (2026-08-03), фрагмент `00:01:11–00:01:55`.

Дополнительно в памяти есть отдельная карточка open item:
- **Provisioned concurrency sizing for /deliver** — raised **2026-08-03**.  
  - Источник: `meetings/2026-08-03-architecture-committee.txt` (2026-08-03), claim `O6`.  
  - Но эта карточка помечена **closed** и у неё у

## m18 [ru / aggregate] Сколько раз менялась политика ретраев и кто владел ею на каждом шаге?
**expected:** три решения: 03-30 выключены (Никита), 06-15 включены на gateway, 3 попытки, бюджет 15% (Аня), 08-24 перенесены в SQS с DLQ (Аня, с 09-07 Ваня)  
**expected sources:** {'sources': ['meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 7.6s, 3 tool calls)
queries: ['MATCH path=(cur:Decision)-[:SUPERSEDES*0..10]->(old:Decision) WHERE (cur)-[:ABOU', "MATCH (p:Person)-[o:OWNS]->(d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})", 'política de reintentos ownership retries who owned each change']

Политика ретраев менялась **3 раза** по найденной цепочке решений.

Шаги и владельцы на каждом шаге:

1. **2026-03-30 — D07**
   - Текст: “Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice”
   - Владелец на тот момент: **Nikita Frolov**
   - Источник: `meetings/2026-03-30-weekly-sync.txt`

2. **2026-06-15 — D14**
   - Текст: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%”
   - Владелец на тот момент: **Anna Sokolova**
   - Источник: `meetings/2026-06-15-weekly-sync.txt`

3. **2026-08-24 — D21**
   - Текст: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”
   - Владелец на тот момент: **Anna Sokolova**
   - Источник: `meetings/2026-08-24-weekly-sync.txt`

Примечание: в памяти также есть отдельная запись об изменении владения retries от Anna к Ivan на **2026-09-07**, но это уже **про ownership**, а не новая смена самой политики ретраев.

### memory-eval-graph (completed, 6.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) OPTIONAL MATCH (p:Pe"]

Политика ретраев менялась **2 раза**: было **3 решения** по теме, из них **2 раза политика менялась**.

Шаги и владельцы:

1. **2026-03-30 — D07**  
   `Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice`  
   Владелец: **Nikita Frolov**  
   Источник: `meetings/2026-03-30-weekly-sync.txt`

2. **2026-06-15 — D14**  
   `Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%`  
   Владелец: **Anna Sokolova**  
   Источник: `meetings/2026-06-15-weekly-sync.txt`

3. **2026-08-24 — D21**  
   `Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off`  
   Владелец: **Anna Sokolova**  
   Источник: `meetings/2026-08-24-weekly-sync.txt`

Итого по владельцам на каждом шаге:
- D07 — **Nikita Frolov**
- D14 — **Anna Sokolova**
- D21 — **Anna Sokolova**

Если хотите, могу ещё показать, **какое решение сейчас в силе** и **кто владеет темой retries сейчас**.

### memory-eval-vector (completed, 8.0s, 3 tool calls)
queries: ['Сколько раз менялась политика ретраев и кто владел ею на каждом шаге?', 'политика ретраев owner changes decisions Relay webhook delivery', 'retry policy ownership change Relay webhook delivery']

В памяти есть **2 смены** политики ретраев, если считать только явно зафиксированные решения по этому же topic:

1. **2026-03-30** — политика ретраев за **Никитой**.  
   Источник: `meetings/2026-03-30-weekly-sync.txt` (meeting, 2026-03-30).  
   Формулировка: «политика ретраев за никитой».

2. **2026-06-15** — ретраи на `deliver` за **Аней**.  
   Источник: `meetings/2026-06-15-weekly-sync.txt` (meeting, 2026-06-15).  
   Формулировка: «ретраи аня».

3. **2026-08-27** — в документе зафиксировано, что ретраи принадлежат **Relay core lead** до serverless cutover, а потом владельцу **SQS pipeline**.  
   Источник: `docs/retries-dlq.md` (docs-md, updated 2026-08-27).  
   Это выглядит как более новая текущая формулировка владения.  
   Сама механика в том же документе тоже обновлена на 2026-08-27: gateway retries on `POST /relay/deliver` are off, SQS redrive with backoff, 5 attempts, then DLQ.

Итого:  
- **Если считать смены владельца по хронологии, то их 2**: Никита → Аня → Relay core lead / SQS pipeline.  
- **Но есть несостыковка** между meeting-решениями и документом 2026-08-27: документ дает более свежую схему владения, чем ранние встречи, поэтому это, скорее всего, уже новое со

## m19 [en / unowned] What is still unowned as of 2026-10-05 and how many times has each been raised?
**expected:** 10x load test on Lambda (raised 07-27, again 08-17, 09-14); DocumentDB credential rotation (raised 09-07, again 09-28, 10-05); DocumentDB decommission date (raised 05-18, again 08-10, 10-05) has no date rather than no owner  
**expected sources:** {'sources': ['meetings/2026-07-27-poc-review.txt', 'meetings/2026-09-07-security-review.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 5.4s, 1 tool calls)
queries: ["MATCH (o:OpenItem) WHERE o.raised <= '2026-10-05' AND NOT EXISTS { MATCH (o)<-[w"]

As of 2026-10-05, the unowned open items are:

- O4 — “DocumentDB decommission date” — raised 0 times in the graph results shown here  
  Source: graph query result; raised on 2026-05-18, raised_again on 2026-08-10 and 2026-10-05

- O3 — “Load test on Lambda at 10x current volume” — raised 0 times in the graph results shown here  
  Source: graph query result; raised on 2026-07-27, raised_again on 2026-08-17 and 2026-09-14

- O7 — “Rotate DocumentDB credentials before decommission” — raised 0 times in the graph results shown here  
  Source: graph query result; raised on 2026-09-07, raised_again on 2026-09-28

Assumption: I treated “how many times has each been raised” as the count of RAISED_IN meetings found in the graph query. The query returned no matching RAISED_IN meetings for these items, so the count is 0 for each.

### memory-eval-graph (completed, 7.8s, 2 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ', 'MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

As of 2026-10-05, the unowned open items are:

- O3 — “Load test on Lambda at 10x current volume” — raised 3 times  
  Source: not in a source file for the count; item details from graph memory. Dates: raised 2026-07-27, raised_again 2026-08-17 and 2026-09-14.

- O4 — “DocumentDB decommission date” — raised 3 times  
  Source: not in a source file for the count; item details from graph memory. Dates: raised 2026-05-18, raised_again 2026-08-10 and 2026-10-05.

- O7 — “Rotate DocumentDB credentials before decommission” — raised 2 times  
  Source: not in a source file for the count; item details from graph memory. Dates: raised 2026-09-07, raised_again 2026-09-28.

Assumption: “how many times has each been raised” means 1 initial raise plus each entry in `raised_again`.

### memory-eval-vector (completed, 6.1s, 3 tool calls)
queries: ['What is still unowned as of 2026-10-05 and how many times has each been raised?', 'unowned open items raised how many times as of 2026-10-05', 'no owner open item raised date count 2026-10-05']

As of 2026-10-05, I found **3 still-unowned open items** in memory:

1. **database — DocumentDB decommission date**  
   - **Raised 3 times**: 2026-05-18, 2026-08-10, 2026-10-05  
   - Source: `meetings/2026-05-18-weekly-sync.txt` / claim O4, dated 2026-05-18

2. **compute — Load test on Lambda at 10x current volume**  
   - **Raised 3 times**: 2026-07-27, 2026-08-17, 2026-09-14  
   - Source: `meetings/2026-07-27-poc-review.txt` / claim O3, dated 2026-07-27

3. **security — Rotate DocumentDB credentials before decommission**  
   - **Raised 2 times**: 2026-09-07, 2026-09-28  
   - Source: `meetings/2026-09-07-security-review.txt` / claim O7, dated 2026-09-07

I did not count closed items that had no owner earlier, because they are no longer still unowned.

## m20 [ru / dependency] Что должно произойти до серверлес-катовера 19 октября и в каком порядке?
**expected:** катовер базы на DynamoDB 12 октября (за неделю), dual write до 26 октября; нагрузочный тест на 10x всё ещё не сделан; runbook отката с владельцем Леной  
**expected sources:** {'sources': ['meetings/2026-10-05-cutover-planning.txt', 'docs/runbook-cutover-serverless.md', 'docs/load-testing.md']}

### memory-eval-both (completed, 12.6s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.text CONTAIN", 'серверлес катовер 19 октября что должно произойти до него и в каком порядке', 'serverless cutover 19 October before that in what order steps', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202"]

Предполагаю, что вы спрашиваете про серверлес-катовер из решения по cutover.

До катовера 19 октября должны произойти такие шаги, в таком порядке:

1. За 24 часа заморозить изменения эндпоинтов.  
   Источник: `docs/runbook-cutover-serverless.md`, updated `2026-09-29`.

2. Переключить интеграцию gateway для `POST /relay/deliver` и `GET /relay/*` с VPC link на Lambda-интеграции.  
   Источник: `docs/runbook-cutover-serverless.md`, updated `2026-09-29`.

3. Уменьшить EKS deployments до 0 replicas, но оставить кластер на 7 дней.  
   Источник: `docs/runbook-cutover-serverless.md`, updated `2026-09-29`.

4. Наблюдать `delivery p95`, `DLQ depth` и `intake 5xx` в течение 30 минут.  
   Источник: `docs/runbook-cutover-serverless.md`, updated `2026-09-29`.

Есть ещё предусловия, которые должны быть выполнены до катовера:
- staging на Lambda должен быть без инцидентов неделю;
- provisioned concurrency на `relay-deliver` должен быть 4;
- 10x load test ещё не сделан;
- DynamoDB cutover должен быть раньше, и между ними должна быть неделя.  
Источник: `docs/runbook-cutover-serverless.md`, updated `2026-09-29`.

Отдельно по решению о катовере:
- серверлес-катовер запланирован на `2026-10-19` в `

### memory-eval-graph (completed, 6.7s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202"]

К 19 октября до серверлес-катовера должно быть выполнено следующее, и из памяти видно только два решения по этой теме:

1. **Назначен ответственный за rollback** — **Лена**.  
   Источник: `meetings/2026-10-05-cutover-planning.txt`, дата решения `2026-10-05`.

2. **Сам serverless cutover запланирован на 2026-10-19, 09:00 local**, и он должен укладываться в planned-work error budget.  
   Источник: `meetings/2026-10-05-cutover-planning.txt`, дата решения `2026-10-05`.

Порядок в памяти такой: оба решения имеют одну и ту же дату `2026-10-05`, поэтому явного последовательного порядка между ними нет; можно лишь сказать, что перед катовером должны быть определены **rollback owner** и **само время катовера**.

### memory-eval-vector (completed, 9.7s, 3 tool calls)
queries: ['Что должно произойти до серверлес-катовера 19 октября и в каком порядке?', 'до серверлес-катовера 19 октября порядок действий', 'serverless cutover 19 October order of steps']

До серверлес-катовера 19 октября нужно сделать следующее, в таком порядке:

1. **Переключить базу раньше 12 октября** — это должно случиться **до** серверлес-катовера, и в обсуждении сказано, что база переключается **раньше 12 октября**, то есть примерно за неделю до катовера.  
   Источник: `meetings/2026-10-05-cutover-planning.txt` — 2026-10-05.

2. **Выключить dual write 26 октября** — это тоже было названо как отдельная веха, но она **после** 19 октября, поэтому к вопросу “до катовера 19 октября” не относится как предшаг.  
   Источник: `meetings/2026-10-05-cutover-planning.txt` — 2026-10-05.

3. **Сам серверлес-катовер запланирован на 19 октября в 09:00**.  
   Источник: `meetings/2026-10-05-cutover-planning.txt` — 2026-10-05; подтверждено решением `decision:cutover:2026-10-05` в `meetings/2026-10-05-cutover-planning.txt` — 2026-10-05.

Если вам нужен именно **полный порядок предкатовера по ранбуку**, то в памяти есть только общий runbook от 2026-09-29:
1. заморозить изменения endpoint за 24 часа,
2. переключить gateway integrations на Lambda,
3. опустить EKS до 0 replicas,
4. наблюдать 30 минут.  
Источник: `docs/runbook-cutover-serverless.md` — 2026-09-29.

Но здесь есть важ

## m21 [en / temporal] Has the SLO ever changed? What is it right now?
**expected:** yes: p95 2 s from 2026-01-26; relaxed to 3 s for 30 days after the serverless cutover (decided 2026-10-05, Marat objected), then back to 2 s; success rate 99.5% unchanged  
**expected sources:** {'sources': ['meetings/2026-01-26-weekly-sync.txt', 'meetings/2026-10-05-cutover-planning.txt', 'docs/slo.md']}

### memory-eval-both (completed, 4.9s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE", 'MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision) WHERE (cur)-[:ABOUT']

Yes — it has changed.

Current SLO in force:
- Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s
- Date: 2026-10-05
- Source: `meetings/2026-10-05-cutover-planning.txt`

What it changed from:
- Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%
- Date: 2026-01-26
- Source: `meetings/2026-01-26-weekly-sync.txt`

Assumption: by “right now” I used the latest active decision on the SLO topic.

### memory-eval-graph (completed, 5.3s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) OPTIONAL MATCH (d)-[:SUP"]

Yes — the SLO has changed.

Current SLO in force:
- Delivery p95 SLO is relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s.  
  Source: `meetings/2026-10-05-cutover-planning.txt`, dated `2026-10-05` (`D28`, active)

History:
- Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%.  
  Source: `meetings/2026-01-26-weekly-sync.txt`, dated `2026-01-26` (`D02`, superseded)

Note: the document `docs/slo.md` was already stale as of `2026-10-05`; it still says p95 2 s with no stabilisation window.

### memory-eval-vector (completed, 5.7s, 3 tool calls)
queries: ['Has the SLO ever changed? What is it right now?', 'SLO changed current SLO Relay webhook delivery project', 'service level objective SLO Relay webhook delivery current decision']

Yes — the SLO has changed.

- On **2026-01-26**, the current SLO was set to **p95 delivery latency 2 s over 5 minutes** and **monthly delivery success rate 99.5%**. Source: **meetings/2026-01-26-weekly-sync.txt** (decision **D02**, now **superseded**) and **docs/slo.md** updated **2026-01-28**.
- On **2026-10-05**, the latency SLO was **relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s**. This decision **supersedes D02** and is the current decision on SLO. Source: **meetings/2026-10-05-cutover-planning.txt** (decision **D28**, active).

So **right now**, the SLO is:
- **Delivery latency p95: 3 s for 30 days after the serverless cutover, then 2 s**
- **Delivery success rate: 99.5% monthly**

Sources:
- **meetings/2026-10-05-cutover-planning.txt**, **2026-10-05** — current active decision D28
- **docs/slo.md**, **2026-01-28** — this doc is stale on latency because it still says **2 s** and predates the newer decision

I also retrieved:
- **meetings/2026-01-26-weekly-sync.txt**, **2026-01-26** — superseded decision D02
- **docs/slo.md**, **2026-01-28** — current success-rate doc, but stale on latency


## m22 [ru / fact] Почему ADR-007 отклонили, какие цифры были у EKS?
**expected:** p95 0.4 с, но $6,100 в месяц, в 1.7 раза дороже Lambda, и второй кластер, который платформа не хочет эксплуатировать  
**expected sources:** {'sources': ['adr/ADR-007.md', 'docs/poc-eks-report.md', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 6.1s, 3 tool calls)
queries: ['ADR-007 rejected why EKS numbers costs results report', 'ADR-007 отклонили почему цифры EKS результаты отчёт', "MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.file"]

ADR-007 отклонили потому, что, хотя EKS давал очень хорошую задержку, он был дороже и добавлял операционную сложность.

- В ADR и отчёте PoC сказано, что latency была отличной: `p95 0.4 s`, а также `p95 is five times better than Lambda`.
- Но у решения был минус: `1.7x the monthly cost` / `monthly cost is 1.7x`.
- Ещё одна причина: `a second platform to run` и `the platform team would have to become a Kubernetes team`.

По цифрам EKS, которые есть в памяти:
- `p95 0.4 s`
- `1.7x` месячной стоимости относительно альтернативы
- в раннем контексте EKS-кластер стоил около `$6,100/month` для общего кластера, большая часть относилась к Relay

Источник:
- `adr/ADR-007.md` — 2026-08-05, статус `Rejected`
- `docs/poc-eks-report.md` — 2026-07-24, оценка PoC-2

### memory-eval-graph (completed, 6.7s, 5 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (d:Decision)-[:RECORDED_IN]->(a:ADR {id:'ADR-007'}) OPTIONAL MATCH (d)-[:B", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'compute'}) WHERE d.text CONTAINS 'EKS", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'compute'}) WHERE d.text STARTS WITH '", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'compute'}) WHERE d.text CONTAINS 'Kee"]

ADR-007 отклонили, потому что по решению от 2026-08-03 EKS давал **p95 0.4 s**, но при этом был **в 1.7 раза дороже по месячной стоимости** и требовал **“a second platform to run”**. Источник: `meetings/2026-08-03-architecture-committee.txt`, 2026-08-03.

Что есть в памяти про EKS:
- `p95_s = 0.4`
- `monthly_cost_usd = 6100`
- `ops_effort = "a second platform team"`

Дополнительно: ADR-007 имеет статус **Rejected**; файл `adr/ADR-007.md`, дата `2026-08-05`.

### memory-eval-vector (completed, 4.7s, 3 tool calls)
queries: ['Почему ADR-007 отклонили, какие цифры были у EKS?', 'ADR-007 отклонили EKS цифры', 'ADR-007 rejected EKS numbers']

ADR-007 отклонили из‑за стоимости и операционной сложности: в решении указано, что p95 был **0.4 s**, но это стоило **в 1.7x дороже в месяц** и требовало **вторую платформу для сопровождения**. Источник: `adr/ADR-007.md`, дата `2026-08-05`.

По цифрам для EKS в памяти есть такие формулировки:
- **p95 0.4 s** — в секции Decision. Источник: `adr/ADR-007.md`, `2026-08-05`.
- **p95 в 5 раз лучше, чем Lambda** — в секции Consequences. Источник: `adr/ADR-007.md`, `2026-08-05`.
- **monthly cost 1.7x** — в секции Decision и Consequences. Источник: `adr/ADR-007.md`, `2026-08-05`.

Если хотите, могу ещё проверить, есть ли в памяти более точные числа по сравнению EKS vs Lambda/другим вариантам.

## t01 [en / current] What is the current decision on infrastructure as code, and when was it made?
**expected:** Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation (decided 2026-04-20, owner Pavel Grishin)  
**expected sources:** {'sources': ['meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 3.1s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERSE"]

Current decision on infrastructure as code: **Hybrid IaC — networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation**.

It was made on **2026-04-20**.

Source: `meetings/2026-04-20-weekly-sync.txt` — decision date `2026-04-20`.

### memory-eval-graph (completed, 3.4s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERSE"]

The current decision on infrastructure as code is: “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation” — dated 2026-04-20, source `meetings/2026-04-20-weekly-sync.txt`.

Assumption: by “current decision” you meant the latest active decision on the IaC topic.

### memory-eval-vector (completed, 4.4s, 3 tool calls)
queries: ['What is the current decision on infrastructure as code, and when was it made?', 'current decision infrastructure as code made date', 'infrastructure as code decision']

The current decision on infrastructure as code is **hybrid IaC**: **networking stays in Terraform, and application stacks use CloudFormation**. This decision was made in **ADR-004 on 2026-04-20** and is recorded as superseding ADR-001. Source: **confluence/decision-log.xhtml** (updated **2026-06-03**) and **adr/ADR-004.md** (updated **2026-04-22**).

The earlier decision to migrate everything from Terraform to CloudFormation exists in **ADR-001** but it is **superseded**, so it is not the current decision. Source: **adr/ADR-001.md** (updated **2026-01-14**).



## t02 [ru / history] Как менялось решение по теме «infrastructure as code»? Перечисли по датам.
**expected:** 2026-01-12: Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1 → 2026-02-09: One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway) → 2026-02-23: Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call → 2026-04-20: Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-02-09-weekly-sync.txt', 'meetings/2026-02-23-incident-review.txt', 'meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 5.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (d)-[:SUP"]

По теме «infrastructure as code» в памяти есть такие решения, по датам:

- 2026-01-12 — D01: «Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1»  
  Источник: `meetings/2026-01-12-weekly-sync.txt`

- 2026-02-09 — D03: «One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)»  
  Источник: `meetings/2026-02-09-weekly-sync.txt`

- 2026-02-23 — D04: «Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call»  
  Источник: `meetings/2026-02-23-incident-review.txt`

- 2026-04-20 — D09: «Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation»  
  Источник: `meetings/2026-04-20-weekly-sync.txt`

Если нужно, могу ещё отдельно показать, какое из этих решений сейчас в силе и какое что именно отменяло.

### memory-eval-graph (completed, 4.7s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERSE"]

По теме «infrastructure as code» решение менялось так:

- **2026-02-09** — **active**: *One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)*.  
  **Источник:** `meetings/2026-02-09-weekly-sync.txt`

- **2026-02-23** — **active**: *Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call*.  
  **Источник:** `meetings/2026-02-23-incident-review.txt`

- **2026-04-20** — **active**: *Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation*.  
  **Источник:** `meetings/2026-04-20-weekly-sync.txt`

Если нужно, могу ещё показать, **какое из этих решений сейчас в силе как текущее** и есть ли у них цепочка supersedes.

### memory-eval-vector (completed, 7.2s, 3 tool calls)
queries: ['Как менялось решение по теме «infrastructure as code»? Перечисли по датам.', 'infrastructure as code decision history dates', 'решение по теме infrastructure as code по датам']

По теме **infrastructure as code** в памяти есть такая цепочка решений:

- **2026-01-12** — принято решение **мигрировать инфраструктурный код с Terraform на CloudFormation**; миграция должна идти по модулям до конца Q1. Источник: `meetings/2026-01-12-weekly-sync.txt` (claim D01, status: superseded).  
- **2026-01-14** — это решение оформлено в **ADR-001**, но сам ADR уже помечен как **Superseded (superseded by ADR-004)**. Источник: `adr/ADR-001.md` (updated 2026-01-14).  
- **2026-04-20** — принято новое решение: **hybrid IaC** — networking остаётся в Terraform, application stacks переводятся в CloudFormation; это **supersedes ADR-001**. Источник: `confluence/decision-log.xhtml` (updated 2026-06-03), также подтверждено `adr/ADR-004.md` (updated 2026-04-22).  

Итог: **сначала был полный переход Terraform → CloudFormation, затем решение изменили на гибридную схему**. Если хочешь, могу ещё свести это в компактную таблицу «дата / решение / статус / источник».

## t03 [en / current] What is the current decision on gateway timeout, and when was it made?
**expected:** Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom (decided 2026-08-24, owner Ivan Melnik)  
**expected sources:** {'sources': ['meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE NOT (d)<-[:SU"]

Current decision: **Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom**.  
It was made on **2026-08-24**.  
Source: **meetings/2026-08-24-weekly-sync.txt**.

### memory-eval-graph (completed, 5.5s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.text CONTAI"]

The current decision is: “Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom” — status active, dated 2026-08-24, source `meetings/2026-08-24-weekly-sync.txt`.

Assumption: by “gateway timeout” you meant the timeout decision on the `topic:timeouts` topic, since the `topic:gateway` search returned nothing.

### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['What is the current decision on gateway timeout, and when was it made?', 'current decision gateway timeout made date', 'gateway timeout decision']

The current decision is: **gateway integration timeout is 25 s**. It was made on **2026-08-24**. Source: **meetings/2026-08-24-weekly-sync.txt** (`D20`, status active).

I also found a newer document, **ADR-010: Gateway timeout policy for Lambda integrations** updated **2026-09-23**, but it says **“No decision recorded”** in the Decision section and is therefore stale on this point relative to the meeting decision. Source: **adr/ADR-010.md** (`Decision`, updated 2026-09-23).

## t04 [ru / history] Как менялось решение по теме «gateway timeout»? Перечисли по датам.
**expected:** 2026-03-16: Gateway integration timeout 10 s on every Relay route → 2026-05-18: Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14 → 2026-08-24: Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom  
**expected sources:** {'sources': ['meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 5.7s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.text CONTAI", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) RETURN d.id, d.text"]

По теме «gateway timeout» решение менялось так:

- 2026-03-16 — **Gateway integration timeout 10 s on every Relay route**  
  Источник: `meetings/2026-03-16-weekly-sync.txt`  
  Статус: `superseded`

- 2026-05-18 — **Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14**  
  Источник: `meetings/2026-05-18-weekly-sync.txt`  
  Статус: `superseded`

- 2026-08-24 — **Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom**  
  Источник: `meetings/2026-08-24-weekly-sync.txt`  
  Статус: `active`

Если хочешь, я могу ещё кратко показать, какое решение сейчас в силе.

### memory-eval-graph (completed, 4.8s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:$T}) OPTIONAL MATCH (d)-[:SUPERSEDES]']

По теме «gateway timeout» решение менялось так:

- 2026-03-16 — **D06**: `Gateway integration timeout 10 s on every Relay route`  
  источник: `meetings/2026-03-16-weekly-sync.txt`  
  статус: `superseded`

- 2026-05-18 — **D12**: `Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14`  
  источник: `meetings/2026-05-18-weekly-sync.txt`  
  статус: `superseded`

- 2026-08-24 — **D20**: `Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom`  
  источник: `meetings/2026-08-24-weekly-sync.txt`  
  статус: `active`

Если нужно, могу ещё показать это как цепочку «что действовало на каждую дату».

### memory-eval-vector (completed, 9.0s, 3 tool calls)
queries: ['Как менялось решение по теме «gateway timeout»? Перечисли по датам.', 'gateway timeout decision timeline', 'решение gateway timeout по датам']

По теме **gateway timeout** в памяти есть такая хронология решений:

- **2026-03-16** — таймаут интеграции Gateway на всех маршрутах установлен на **10 s**.  
  Источник: `meetings/2026-03-16-weekly-sync.txt` (decision **D06**, статус `superseded`).

- **2026-05-18** — таймаут поднят с **10 s до 30 s** после инцидента с медленным target’ом.  
  Источник: `meetings/2026-05-18-weekly-sync.txt` (decision **D12**, статус `superseded`).

- **2026-08-24** — таймаут снижен с **30 s до 25 s**, потому что у gateway жёсткий лимит **29 s** и нужен запас для Lambda.  
  Источник: `meetings/2026-08-24-weekly-sync.txt` (decision **D20**, статус `active`).

Важно: текущим решением в памяти является **D20 от 2026-08-24**; более ранние решения **D06** и **D12** помечены как `superseded`.  
Источники: `meetings/2026-03-16-weekly-sync.txt` (2026-03-16), `meetings/2026-05-18-weekly-sync.txt` (2026-05-18), `meetings/2026-08-24-weekly-sync.txt` (2026-08-24).

Также найдено, что документ `docs/gateway.md` обновлён **2026-03-18** и уже устарел относительно более поздних решений: он всё ещё говорит про **10 s**.  
Источник: `docs/gateway.md` (updated 2026-03-18) + решения **D12** и **D20** выше.

## t05 [en / chain] The current decision on gateway timeout replaced an earlier one. What did that earlier decision itself replace, and when?
**expected:** Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom (2026-08-24) replaced 'Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14' (2026-05-18), which replaced 'Gateway integration timeout 10 s on every Relay route' (2026-03-16)  
**expected sources:** {'sources': ['meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 4.5s, 1 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE NOT (cur)<-"]

The earlier decision replaced this one:

- **“Gateway integration timeout 10 s on every Relay route”** — **2026-03-16** — source: `meetings/2026-03-16-weekly-sync.txt`

So the chain is:
- current: lowered from 30 s to 25 s — **2026-08-24**
- earlier: raised from 10 s to 30 s — **2026-05-18**
- which itself replaced: 10 s on every Relay route — **2026-03-16**



### memory-eval-graph (completed, 3.9s, 1 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE NOT (cur)<-"]

The earlier decision was **“Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14”**, dated **2026-05-18**. It itself replaced **“Gateway integration timeout 10 s on every Relay route”**, dated **2026-03-16**.  
Source: **meetings/2026-05-18-weekly-sync.txt** (D12) and **meetings/2026-03-16-weekly-sync.txt** (D06).

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['The current decision on gateway timeout replaced an earlier one. What did that e', 'gateway timeout decision replaced earlier decision replace when', 'gateway timeout decision superseded by earlier decision what did it replace']

The earlier decision was **D06**, dated **2026-03-16**: “Gateway integration timeout 10 s on every Relay route.” It was later **superseded by D12**.  
Source: **meetings/2026-03-16-weekly-sync.txt** via claim **D06**.

So the chain is:

- **D06** — 2026-03-16 — set timeout to **10 s**
- **D12** — 2026-05-18 — raised it to **30 s**, and **superseded D06**
- **D20** — 2026-08-24 — lowered it to **25 s**, and **superseded D12**

If you want, I can also summarize the full timeout decision history in one line.

## t06 [en / current] What is the current decision on retries, and when was it made?
**expected:** Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off (decided 2026-08-24, owner Anna Sokolova)  
**expected sources:** {'sources': ['meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 5.6s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (d)<-[:SUP"]

The current decision on retries is: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off.”

It was made on 2026-08-24, from `meetings/2026-08-24-weekly-sync.txt`.

### memory-eval-graph (completed, 2.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (d)<-[:SUP"]

Current decision on retries: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off” — status **active**, made on **2026-08-24**. Source: **meetings/2026-08-24-weekly-sync.txt**.

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['What is the current decision on retries, and when was it made?', 'current decision retries made date', 'retries decision status date superseded']

The current decision on retries is:

- Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on `/deliver` are turned off.  
  Source: `meetings/2026-08-24-weekly-sync.txt` (claim D21), date `2026-08-24`.

This supersedes the earlier gateway-retry decision:

- On `2026-06-15`, retries had been enabled on `POST /deliver` at the gateway with max 3 attempts and a 15% retry budget.  
  Source: `meetings/2026-06-15-weekly-sync.txt` (claim D14), date `2026-06-15`, now superseded.

So the current decision was made on `2026-08-24`.

## t07 [ru / history] Как менялось решение по теме «retries»? Перечисли по датам.
**expected:** 2026-03-30: Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice → 2026-06-15: Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15% → 2026-08-24: Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off  
**expected sources:** {'sources': ['meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.9s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) RETURN d.id, d.text,"]

По теме «retries» решение менялось так:

- 2026-03-30 — **D07**: `Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice`  
  источник: `meetings/2026-03-30-weekly-sync.txt`

- 2026-06-15 — **D14**: `Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%`  
  источник: `meetings/2026-06-15-weekly-sync.txt`

- 2026-08-24 — **D21**: `Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off`  
  источник: `meetings/2026-08-24-weekly-sync.txt`

Если нужно, могу ещё показать, какое из них сейчас в силе и какие решения оно заменило.

### memory-eval-graph (completed, 3.9s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$T}) OPTIONAL MATCH (d)-[:SUPERSEDES]-']

По теме «retries» решение менялось так, по датам:

- 2026-03-30 — D07: “Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice”  
  source: `meetings/2026-03-30-weekly-sync.txt`

- 2026-06-15 — D14: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%”  
  source: `meetings/2026-06-15-weekly-sync.txt`

- 2026-08-24 — D21: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”  
  source: `meetings/2026-08-24-weekly-sync.txt`

Если хочешь, могу ещё показать, какое из этих решений сейчас в силе.

### memory-eval-vector (completed, 6.7s, 3 tool calls)
queries: ['Как менялось решение по теме «retries»? Перечисли по датам.', 'retries decision by date', 'решение retries даты']

По теме **retries** в памяти есть такие решения, по датам:

- **2026-03-30** — ретраи на `POST /deliver` в gateway **отключены** до появления idempotency keys; read routes могут ретраить дважды. Источник: `meetings/2026-03-30-weekly-sync.txt` (`D07`), статус: `superseded`.  
- **2026-06-15** — ретраи на `POST /deliver` в gateway **включены**: максимум 3 попытки, retry budget 15%. Источник: `meetings/2026-06-15-weekly-sync.txt` (`D14`), статус: `superseded`.  
- **2026-08-24** — ретраи **убраны из gateway** и перенесены в **SQS + DLQ**: после 5 попыток сообщение идет в dead-letter queue, gateway retries на `/deliver` выключены. Источник: `meetings/2026-08-24-weekly-sync.txt` (`D21` / ADR-009), статус: `active`.

Итог: текущее решение — **ретраи не на gateway, а через SQS с DLQ после 5 попыток**. Источник: `meetings/2026-08-24-weekly-sync.txt` (`D21`), 2026-08-24.

Если хочешь, я могу еще сделать **короткую хронологию “было → стало” одной строкой**.

## t08 [en / chain] The current decision on retries replaced an earlier one. What did that earlier decision itself replace, and when?
**expected:** Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off (2026-08-24) replaced 'Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%' (2026-06-15), which replaced 'Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice' (2026-03-30)  
**expected sources:** {'sources': ['meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.8s, 1 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (cur)<-["]

The earlier retries decision replaced this one:

- “Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice”
- Date: 2026-03-30
- Source: meetings/2026-03-30-weekly-sync.txt

So the current decision on retries replaced that 2026-03-30 decision, which is the one in the chain immediately before the 2026-06-15 decision.

### memory-eval-graph (completed, 4.0s, 1 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (cur)<-["]

The earlier decision replaced the one from **2026-03-30**.

- **Earlier decision:** “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%”
- **It replaced:** “Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice”
- **Date of the replaced decision:** **2026-03-30**
- **Source:** `meetings/2026-06-15-weekly-sync.txt` for the earlier decision; `meetings/2026-03-30-weekly-sync.txt` for the decision it replaced.

The current retries decision chain is:
1. **2026-08-24** current active decision
2. **2026-06-15** earlier decision
3. **2026-03-30** decision it replaced

### memory-eval-vector (completed, 4.5s, 3 tool calls)
queries: ['The current decision on retries replaced an earlier one. What did that earlier d', 'current decision retries replaced earlier decision replaced what and when', 'retries decision superseded replaced earlier decision what did it replace when']

The earlier retries decision was **D14**, from **2026-06-15**. It **replaced D07**.  
- **D14**: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%.”  
  Source: **meetings/2026-06-15-weekly-sync.txt** / claim D14, dated **2026-06-15**.  
- **D07**: “Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice.”  
  Source: **meetings/2026-03-30-weekly-sync.txt** / claim D07, dated **2026-03-30**.

So, the earlier decision replaced **D07 on 2026-03-30**.

## t09 [en / current] What is the current decision on compute platform, and when was it made?
**expected:** Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances (decided 2026-08-03, owner Ivan Melnik)  
**expected sources:** {'sources': ['meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 3.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE NOT (d)<-[:SUP"]

The current decision on compute platform is: **Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances**.

It was made on **2026-08-03**.

Source: `meetings/2026-08-03-architecture-committee.txt` (decision date 2026-08-03).

### memory-eval-graph (completed, 3.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE NOT (d)<-[:SUP"]

Current compute-platform decision: Relay moves to Lambda with provisioned concurrency on `/deliver`; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances. Source: `meetings/2026-08-03-architecture-committee.txt`, date `2026-08-03`.

Assumption: by “current decision” you meant the active decision on the `compute` topic.

### memory-eval-vector (completed, 3.4s, 3 tool calls)
queries: ['What is the current decision on compute platform, and when was it made?', 'current decision compute platform made date', 'compute platform decision']

The current decision on compute is: **Relay moves to Lambda with provisioned concurrency on `/deliver`**. It was made on **2026-08-03**. Source: `meetings/2026-08-03-architecture-committee.txt` / claim `D17` (recorded in ADR-006), dated **2026-08-03**.

I also found an older document saying to **keep Relay on EKS with autoscaling**, but it is **rejected/superseded** by the 2026-08-03 decision. Sources: `adr/ADR-007.md` dated **2026-08-05** and `meetings/2026-08-03-architecture-committee.txt` dated **2026-08-03**.

## t10 [ru / history] Как менялось решение по теме «compute platform»? Перечисли по датам.
**expected:** 2026-06-15: Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July → 2026-08-03: Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances  
**expected sources:** {'sources': ['meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 4.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE d.date <= '999"]

По теме **compute platform** решение менялось так:

- **2026-06-15** — **D15**: «Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July» — **статус: superseded**. Источник: `meetings/2026-06-15-weekly-sync.txt`
- **2026-08-03** — **D17**: «Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances» — **статус: active**. Источник: `meetings/2026-08-03-architecture-committee.txt`

Если коротко: сначала решили **сравнить EKS и Lambda**, затем окончательно выбрали **Lambda с provisioned concurrency**.

### memory-eval-graph (completed, 3.7s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'})\nWHERE NOT (d)<-[:SUP"]

По теме «compute platform» в памяти есть одно актуальное решение:

- 2026-08-03 — «Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances»; статус: active; источник: `meetings/2026-08-03-architecture-committee.txt`  
  Примечание: `confluence/architecture.xhtml` (updated 2026-03-12) всё ещё показывает EKS как runtime, а `confluence/migration-roadmap.xhtml` (updated 2026-06-20) всё ещё считает решение по compute pending PoC.

Я не нашёл в графе более ранних решений по этой теме, которые бы сейчас считались в силе или образовывали цепочку supersedes.

### memory-eval-vector (completed, 6.0s, 3 tool calls)
queries: ['Как менялось решение по теме «compute platform»? Перечисли по датам.', 'compute platform decision dates changes', 'решение compute platform по датам']

По теме **compute platform** в памяти есть такие решения по датам:

- **2026-06-15** — запустить **два PoC параллельно**: EKS с autoscaling и Lambda; решение должно было быть принято по cost и p95 к концу июля. Это решение позже помечено как **superseded**.  
  **Источник:** `meetings/2026-06-15-weekly-sync.txt` / ADR-005, дата 2026-06-15.

- **2026-08-03** — перейти на **Lambda с provisioned concurrency** для `/deliver`; это решение **supersedes D15** и является текущим. В качестве аргументов указаны **41% меньшая месячная стоимость** и **p95 1.9 s** на warm instances.  
  **Источник:** `meetings/2026-08-03-architecture-committee.txt` / ADR-006, дата 2026-08-03.

Если нужно, я могу еще отдельно показать, как это решение менялось в виде цепочки: **D15 → D17**.

## t11 [en / current] What is the current decision on SLO, and when was it made?
**expected:** Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s (decided 2026-10-05, owner Lena Kim)  
**expected sources:** {'sources': ['meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 3.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

The current SLO decision is: “Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s.”

It was made on 2026-10-05.

Source: meetings/2026-10-05-cutover-planning.txt, 2026-10-05.

### memory-eval-graph (completed, 3.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

The current SLO decision is: “Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s.” It is **active** and was made on **2026-10-05**. Source: `meetings/2026-10-05-cutover-planning.txt` (decision date 2026-10-05).

Note: the decision’s note says `docs/slo.md` was updated on 2026-01-28 and was already stale relative to this decision.

### memory-eval-vector (completed, 4.2s, 3 tool calls)
queries: ['What is the current decision on SLO, and when was it made?', 'current decision on SLO made date decision status', 'SLO decision current status date']

The current SLO decision is:

- Delivery p95 SLO is relaxed from **2 s to 3 s for 30 days after the serverless cutover, then back to 2 s**.
- This decision is **active** and **supersedes D02**.
- Source: `meetings/2026-10-05-cutover-planning.txt` / claim `D28`, dated **2026-10-05**.

There is a newer decision than the SLO doc:
- `docs/slo.md` says **2 s p95** and was updated **2026-01-28**, but it is stale because `D28` on **2026-10-05** supersedes it.
- Source: `docs/slo.md` and `meetings/2026-10-05-cutover-planning.txt`.

If you want, I can also summarize the older superseded SLO decision from 2026-01-26.

## t12 [ru / history] Как менялось решение по теме «SLO»? Перечисли по датам.
**expected:** 2026-01-26: Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5% → 2026-10-05: Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s  
**expected sources:** {'sources': ['meetings/2026-01-26-weekly-sync.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 3.6s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) RETURN d.id, d.text, d.d"]

По теме SLO в памяти есть 2 решения, по датам:

- 2026-01-26 — **D02**: `Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%`  
  Статус: superseded  
  Источник: `meetings/2026-01-26-weekly-sync.txt`

- 2026-10-05 — **D28**: `Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s`  
  Статус: active  
  Источник: `meetings/2026-10-05-cutover-planning.txt`

Если нужно, могу ещё показать, какое решение сейчас в силе и чем именно оно заменило предыдущее.

### memory-eval-graph (completed, 4.7s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) OPTIONAL MATCH (d)-[:SUP"]

По теме «SLO» изменения такие, по датам:

- **2026-01-26** — «Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%»  
  **Источник:** `meetings/2026-01-26-weekly-sync.txt`  
  **Статус решения:** `superseded`  
  **Примечание:** это более раннее решение; позже оно было заменено.

- **2026-10-05** — «Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s»  
  **Источник:** `meetings/2026-10-05-cutover-planning.txt`  
  **Статус решения:** `active`

Если нужно, могу ещё кратко показать, какое решение по SLO действует сейчас.

### memory-eval-vector (completed, 6.3s, 3 tool calls)
queries: ['Как менялось решение по теме «SLO»? Перечисли по датам.', 'SLO решение по датам', 'изменения решения по теме SLO']

По теме **SLO** в памяти есть **два решения**, и более новое **заменяет** старое:

1. **2026-01-26** — решено: delivery SLO = **p95 end-to-end delivery latency 2 s over 5 minutes** и **monthly delivery success rate 99.5%**.  
   Источник: `meetings/2026-01-26-weekly-sync.txt` / claim D02, дата **2026-01-26**.  
   Это решение сейчас **superseded**.

2. **2026-10-05** — решено: delivery p95 SLO **ослабить с 2 s до 3 s на 30 дней после serverless cutover, затем вернуть 2 s**.  
   Источник: `meetings/2026-10-05-cutover-planning.txt` / claim D28, дата **2026-10-05**.  
   Это **текущее** решение; оно **supersedes D02**.

Дополнительно: документ `docs/slo.md` был обновлён **2026-01-28** и всё ещё содержит старое значение **2 s**, поэтому он **устарел** относительно решения от **2026-10-05**.  
Источник: `docs/slo.md`, дата **2026-01-28**.

Если хочешь, могу ещё свести это в таблицу «дата → что поменялось → статус».

## t13 [ru / owner_now] Кто сейчас владеет темой «retries» и с какой даты?
**expected:** Ivan Melnik, с 2026-09-07  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 2.5s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.to IS NULL RE"]

Темой «retries» сейчас владеет Ivan Melnik, с 2026-09-07.

Источник: граф памяти; дата начала владения — 2026-09-07.

### memory-eval-graph (completed, 3.2s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.to IS NULL RE"]

Темой «retries» сейчас владеет **Иван Мельник** с **2026-09-07**. Источник: граф памяти, связь `OWNS` для `topic:retries` на дату `2026-09-07`.

### memory-eval-vector (completed, 2.7s, 3 tool calls)
queries: ['Кто сейчас владеет темой «retries» и с какой даты?', 'Who owns retries and since when?', 'ownership retries from date owner current']

Сейчас тему **retries** владеет **Ivan Melnik** — **с 2026-09-07**. Источник: `memory/decisions.jsonl`, запись `claim ownership | retries | 2026-09-07` (статус `active`).

## t14 [en / owner_at] Who owned retries on 2026-06-15?
**expected:** Anna Sokolova (from 2026-06-01 to 2026-09-07)  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 4.2s, 2 tool calls)
queries: ["MATCH (t:Topic {key:'topic:retries'})<-[:OWNS]-(p:Person) WHERE p.key IS NOT NUL", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.from <= '2026"]

On 2026-06-15, **Anna Sokolova** owned retries.

Source: graph ownership edge; queried as of 2026-06-15.

### memory-eval-graph (completed, 2.9s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.from <= $D AN"]

Anna Sokolova owned retries on 2026-06-15. Source: not in the returned fields for ownership edges; the ownership record is dated 2026-06-01 and runs until 2026-09-07.

### memory-eval-vector (completed, 4.3s, 3 tool calls)
queries: ['Who owned retries on 2026-06-15?', 'retries ownership 2026-06-15', 'owner retries 2026-06-15']

On 2026-06-15, **Anna Sokolova** owned retries. The active ownership decision is from **2026-06-01** and says “Anna Sokolova owns retries from 2026-06-01 to 2026-09-07.” Source: **memory/decisions.jsonl** dated **2026-06-01**.

I also retrieved a meeting note from **2026-06-15** that says “без владельца” (“without an owner”), but it appears to be about a different item in that sync, not the retries ownership decision. Source: **meetings/2026-06-15-weekly-sync.txt** dated **2026-06-15**.



## t15 [ru / owner_now] Кто сейчас владеет темой «compute platform» и с какой даты?
**expected:** Ivan Melnik, с 2026-07-13  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt']}

### memory-eval-both (completed, 2.6s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.to IS NULL RE"]

Темой «compute platform» сейчас владеет Ivan Melnik, с 2026-07-13.

Источник: граф памяти; дата владения из связи OWNS.

### memory-eval-graph (completed, 2.8s, 1 tool calls)
queries: ['MATCH (p:Person)-[o:OWNS]->(t:Topic {key:$k}) WHERE o.from <= $d AND (o.to IS NU']

Сейчас темой «compute platform» владеет **Ivan Melnik** — с **2026-07-13**.  
Источник: граф памяти, связь OWNS к теме `topic:compute`; дата владения: `2026-07-13`.

### memory-eval-vector (completed, 2.5s, 1 tool calls)
queries: ['Кто сейчас владеет темой «compute platform» и с какой даты?']

Сейчас темой **compute** владеет **Ivan Melnik** с **2026-07-13**. Источник: `memory/decisions.jsonl` (claim ownership | compute | 2026-07-13).

Нашёл также более старую, уже неактуальную запись: **Sergey Belov** владел compute с **2026-06-15** по **2026-07-13**. Источник: `memory/decisions.jsonl` (claim ownership | compute | 2026-06-15).

## t16 [en / owner_at] Who owned compute platform on 2026-06-28?
**expected:** Sergey Belov (from 2026-06-15 to 2026-07-13)  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt']}

### memory-eval-both (completed, 3.0s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(x:Topic {key:'topic:compute'}) WHERE o.from <= '2026"]

On 2026-06-28, compute platform was owned by Sergey Belov.

Source: graph ownership edge, effective 2026-06-15 to 2026-07-13.

### memory-eval-graph (completed, 3.1s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(x:Topic {key:'topic:compute'}) WHERE o.from <= $D AN"]

On 2026-06-28, **Sergey Belov** owned **compute platform**. Source: ownership edge, date **2026-06-15 to 2026-07-13**.

### memory-eval-vector (completed, 4.1s, 3 tool calls)
queries: ['Who owned compute platform on 2026-06-28?', 'compute platform owner 2026-06-28', 'ownership of compute platform on 2026-06-28']

On 2026-06-28, **Sergey Belov** owned compute. Source: **memory/decisions.jsonl** — claim dated **2026-06-15**: “Sergey Belov owns compute from 2026-06-15 to 2026-07-13.”

I also found a newer ownership decision for compute dated **2026-07-13** saying **Ivan Melnik** owns compute from that date onward, so the 2026-06-15 decision is the applicable one for 2026-06-28. Source: **memory/decisions.jsonl** — decision dated **2026-07-13**.

## t17 [ru / owner_now] Кто сейчас владеет темой «idempotency» и с какой даты?
**expected:** Anna Sokolova, с 2026-06-01  
**expected sources:** {'sources': []}

### memory-eval-both (completed, 3.5s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.to IS NUL"]

Темой «idempotency» сейчас владеет **Anna Sokolova** — с **2026-06-01**.

Источник: граф памяти, связь OWNS к `topic:idempotency`.

### memory-eval-graph (completed, 3.2s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.to IS NUL"]

Темой «idempotency» сейчас владеет Anna Sokolova, с 2026-06-01. Источник: граф памяти, связь OWNS по теме `topic:idempotency` (дата владения: 2026-06-01).

### memory-eval-vector (completed, 3.0s, 3 tool calls)
queries: ['Кто сейчас владеет темой «idempotency» и с какой даты?', 'idempotency ownership current owner from date', 'владелец idempotency дата']

Сейчас темой **idempotency** владеет **Anna Sokolova** — с **2026-06-01**.  
Источник: `memory/decisions.jsonl`, запись `ownership:idempotency:2026-06-01` (дата 2026-06-01).

## t18 [en / owner_at] Who owned idempotency on 2026-05-28?
**expected:** Nikita Frolov (from 2026-05-18 to 2026-06-01)  
**expected sources:** {'sources': []}

### memory-eval-both (completed, 2.5s, 1 tool calls)
queries: ["MATCH (t:Topic {key:'topic:idempotency'})<- [o:OWNS]-(p:Person) WHERE o.from <= "]

Nikita Frolov owned idempotency on 2026-05-28.

Source: graph ownership edge; effective from 2026-05-18 to 2026-06-01.

### memory-eval-graph (completed, 3.8s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.from <= '"]

Nikita Frolov owned idempotency on 2026-05-28. Source: not a document; ownership edge in the graph, effective from 2026-05-18 to 2026-06-01.

### memory-eval-vector (completed, 3.0s, 3 tool calls)
queries: ['Who owned idempotency on 2026-05-28?', 'idempotency owner 2026-05-28', 'ownership of idempotency on 2026-05-28']

Nikita Frolov owned idempotency on 2026-05-28. Source: `meetings/2026-05-18-weekly-sync.txt` and `memory/decisions.jsonl`, dated 2026-05-18. The newer ownership decision says Anna Sokolova owns idempotency from 2026-06-01, so that does not apply yet. Source: `meetings/2026-06-01-weekly-sync.txt` and `memory/decisions.jsonl`, dated 2026-06-01.

## t19 [ru / objector] Кто предложил и кто возражал против решения «Migrate Relay infrastructure code from Terraform to CloudFor…»?
**expected:** proposer Pavel Grishin, objector Timur Aliev, 2026-01-12  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt']}

### memory-eval-both (completed, 3.4s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Migrate Relay infrastructure code f"]

Предложил: Павел Гришин; возражал: Тимур Алиев.

Источник: `meetings/2026-01-12-weekly-sync.txt`, дата `2026-01-12`.  
Решение: `Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1` (статус: `superseded`).

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Migrate Relay infrastructure code f"]

Предложил **Павел Гришин**; возражал **Тимур Алиев**.  
Источник: `meetings/2026-01-12-weekly-sync.txt`, решение от `2026-01-12` — «Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1».

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Migrate Relay infrastructure code f', 'Who proposed and who objected to the decision “Migrate Relay infrastructure code', 'Migrate Relay infrastructure code from Terraform to CloudFor… proposed objected']

Решение **предложил Pavel Grishin**, а **возражал Timur Aliev**.

Источники:
- **meetings/2026-01-12-weekly-sync.txt** — 2026-01-12: “Proposed by Pavel Grishin; objection from Timur Aliev.”  
- **adr/ADR-001.md** — 2026-01-14: “Objection recorded from Timur Aliev.”  

Примечание: найденное решение **ADR-001** помечено как **Superseded by ADR-004**, то есть это уже историческая версия.

## t20 [en / objector] Who proposed and who objected to the decision 'Gateway integration timeout 10 s on every Relay route…'?
**expected:** proposer Pavel Grishin, objector Anna Sokolova, 2026-03-16  
**expected sources:** {'sources': ['meetings/2026-03-16-weekly-sync.txt']}

### memory-eval-both (completed, 2.9s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout 10 s on"]

Proposed by **Pavel Grishin** and objected to by **Anna Sokolova**.

Source: `meetings/2026-03-16-weekly-sync.txt`, dated `2026-03-16`  
Decision status: `superseded`

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.text STARTS"]

Павел Гришин предложил, а Анна Соколова возразила по решению “Gateway integration timeout 10 s on every Relay route”.

Источник: `meetings/2026-03-16-weekly-sync.txt`, 2026-03-16.

### memory-eval-vector (completed, 3.5s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'Gateway integration timeout 10 s ", 'Gateway integration timeout 10 s on every Relay route', 'relay route gateway integration timeout 10 s proposed objected']

Proposed by Pavel Grishin and objected by Anna Sokolova. Source: `meetings/2026-03-16-weekly-sync.txt` / claim D06, dated 2026-03-16.

Note: this decision is marked superseded in the same source, with later related decisions existing.

## t21 [ru / objector] Кто предложил и кто возражал против решения «Hybrid IaC: networking (VPC, peering, DNS) stays in Terrafor…»?
**expected:** proposer Sergey Belov, objector Pavel Grishin, 2026-04-20  
**expected sources:** {'sources': ['meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 3.2s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Hybrid IaC: networking (VPC, peerin"]

Решение «Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation» предложил **Сергей Белов**, возражал **Павел Гришин**.

Источник: `meetings/2026-04-20-weekly-sync.txt`, дата решения `2026-04-20`.

### memory-eval-graph (completed, 3.2s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Hybrid IaC: networking (VPC, peerin"]

Решение «Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation» предложил **Sergey Belov**, а возражал против него **Pavel Grishin**. Источник: `meetings/2026-04-20-weekly-sync.txt`, дата решения `2026-04-20`.

### memory-eval-vector (completed, 4.9s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Hybrid IaC: networking (VPC, peerin', 'Кто предложил и кто возражал против решения Hybrid IaC networking VPC peering DN', 'Hybrid IaC networking VPC peering DNS stays in Terraform proposed opposed']

Предложил: **Sergey Belov** — source: `meetings/2026-04-20-weekly-sync.txt` (2026-04-20), также подтверждено в `adr/ADR-004.md` (updated 2026-04-22).

Возражал: **Pavel Grishin** — source: `meetings/2026-04-20-weekly-sync.txt` (2026-04-20), также подтверждено в `adr/ADR-004.md` (updated 2026-04-22).

Найдены записи:
- `meetings/2026-04-20-weekly-sync.txt` (2026-04-20)
- `adr/ADR-004.md` (updated 2026-04-22)



## t22 [en / objector] Who proposed and who objected to the decision 'DynamoDB single-table design, chosen on PoC-1 results (p99 r…'?
**expected:** proposer Denis Orlov, objector Timur Aliev, 2026-05-04  
**expected sources:** {'sources': ['meetings/2026-05-04-poc-review.txt']}

### memory-eval-both (completed, 2.2s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'DynamoDB single-table design, chose"]

Proposed by Denis Orlov and objected to by Timur Aliev.

Source: `meetings/2026-05-04-poc-review.txt`, dated `2026-05-04`.

### memory-eval-graph (completed, 2.7s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'DynamoDB single-table design, chose"]

Proposed by **Denis Orlov** and objected to by **Timur Aliev**.  
Source: `meetings/2026-05-04-poc-review.txt`, `2026-05-04`.

### memory-eval-vector (completed, 3.2s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'DynamoDB single-table design, cho", 'DynamoDB single-table design, chosen on PoC-1 results p99 proposed objected', 'single-table design PoC-1 results p99 proposed objected DynamoDB']

Proposed by **Denis Orlov** and objected by **Timur Aliev**.  
Source: `meetings/2026-05-04-poc-review.txt` via claim D10, dated **2026-05-04**.

## t23 [en / objector] Who proposed and who objected to the decision 'Gateway integration timeout raised from 10 s to 30 s after t…'?
**expected:** proposer Anna Sokolova, objector Lena Kim, 2026-05-18  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt']}

### memory-eval-both (completed, 2.1s, 1 tool calls)
queries: ['MATCH (d:Decision) WHERE d.text STARTS WITH "Gateway integration timeout raised ']

Proposed by **Anna Sokolova** and objected to by **Lena Kim**.  
Source: `meetings/2026-05-18-weekly-sync.txt`, dated **2026-05-18**.

### memory-eval-graph (completed, 4.4s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout raised ", "MATCH (d:Decision) WHERE d.text CONTAINS 'Gateway integration timeout raised fro"]

Anna Sokolova proposed it, and Lena Kim objected. Source: `meetings/2026-05-18-weekly-sync.txt`, decision dated `2026-05-18` (`Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14`).

### memory-eval-vector (completed, 2.4s, 1 tool calls)
queries: ["Who proposed and who objected to the decision 'Gateway integration timeout raise"]

Proposed by **Anna Sokolova** and objected to by **Lena Kim**. Source: **meetings/2026-05-18-weekly-sync.txt** (2026-05-18).

## t24 [ru / objector] Кто предложил и кто возражал против решения «Relay moves to Lambda with provisioned concurrency on /deliv…»?
**expected:** proposer Olga Petrova, objector Timur Aliev, 2026-08-03  
**expected sources:** {'sources': ['meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 3.2s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio"]

Предложила Olga Petrova, возразил Timur Aliev.

Источник: `meetings/2026-08-03-architecture-committee.txt`, 2026-08-03.

### memory-eval-graph (completed, 3.2s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio"]

Предложила **Ольга Петрова**, возражал **Тимур Алиев**.  
Источник: `meetings/2026-08-03-architecture-committee.txt`, решение от `2026-08-03`.

### memory-eval-vector (completed, 4.8s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Relay moves to Lambda with provisio', 'Кто предложил и кто возражал против решения Relay moves to Lambda with provision', 'Relay moves to Lambda with provisioned concurrency on /deliv… proposed opposed']

Предложила **Olga Petrova**; возражал **Timur Aliev**.  
Источник: `meetings/2026-08-03-architecture-committee.txt` (2026-08-03), а также `adr/ADR-006.md` (2026-08-05), где это повторено.

Найденные записи:
- `meetings/2026-08-03-architecture-committee.txt` (2026-08-03): «proposed by Olga Petrova; objection from Timur Aliev»
- `adr/ADR-006.md` (2026-08-05): «Objection recorded from Timur Aliev»

## t25 [ru / objector] Кто предложил и кто возражал против решения «Retries move out of the gateway into SQS with a dead-letter …»?
**expected:** proposer Ivan Melnik, objector Anna Sokolova, 2026-08-24  
**expected sources:** {'sources': ['meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.0s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Retries move out of the gateway int"]

Предложил: Ivan Melnik. Возражала: Anna Sokolova.

Источник: `meetings/2026-08-24-weekly-sync.txt`, дата `2026-08-24`.

### memory-eval-graph (completed, 3.8s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Retries move out of the gateway int"]

Решение **«Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off»**:

- **Предложил:** Иван Мельник — **2026-08-24**, `meetings/2026-08-24-weekly-sync.txt`
- **Возражала:** Анна Соколова — **2026-08-24**, `meetings/2026-08-24-weekly-sync.txt`

Источник: decision/meeting запись с датой **2026-08-24** в файле `meetings/2026-08-24-weekly-sync.txt`.

### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Retries move out of the gateway int', 'Who proposed and who objected to the decision "Retries move out of the gateway i', 'Retries move out of the gateway into SQS with a dead-letter']

Решение предложил **Ivan Melnik**, а возражала **Anna Sokolova**.  
Источник: **meetings/2026-08-24-weekly-sync.txt**; решение зафиксировано в **ADR-009: Retries through SQS with a dead-letter queue**. Дата: **2026-08-24**.

## t26 [en / objector] Who proposed and who objected to the decision 'Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after t…'?
**expected:** proposer Lena Kim, objector Marat Yusupov, 2026-10-05  
**expected sources:** {'sources': ['meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 2.3s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Delivery p95 SLO relaxed from 2 s t"]

Proposed by Lena Kim and objected to by Marat Yusupov.

Source: `meetings/2026-10-05-cutover-planning.txt`, date `2026-10-05`.

### memory-eval-graph (completed, 4.5s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Delivery p95 SLO relaxed from 2 s t", "MATCH (d:Decision) WHERE d.text CONTAINS 'Delivery p95 SLO relaxed from 2 s to 3"]

Proposed by **Lena Kim** and objected by **Marat Yusupov** for the decision **“Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s”**. Source: `meetings/2026-10-05-cutover-planning.txt`, dated `2026-10-05`.

### memory-eval-vector (completed, 2.4s, 1 tool calls)
queries: ["Who proposed and who objected to the decision 'Delivery p95 SLO relaxed from 2 s"]

Proposed by **Lena Kim** and objected to by **Marat Yusupov**. Source: `meetings/2026-10-05-cutover-planning.txt` (2026-10-05), claim D28.

## t27 [en / aggregate] How many decisions have been superseded, and on which topics?
**expected:** 7: D01 (infrastructure as code, 2026-01-12); D02 (SLO, 2026-01-26); D06 (gateway timeout, 2026-03-16); D07 (retries, 2026-03-30); D12 (gateway timeout, 2026-05-18); D14 (retries, 2026-06-15); D15 (compute platform, 2026-06-15)  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-01-26-weekly-sync.txt', 'meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt']}

### memory-eval-both (completed, 2.9s, 1 tool calls)
queries: ["MATCH (d:Decision {status:'superseded'})-[:ABOUT]->(t:Topic) RETURN count(d) AS "]

7 decisions have been superseded.

Topics involved:
- infrastructure as code
- SLO
- gateway timeout
- retries
- compute platform

Source: graph query over `Decision {status:'superseded'}` and their `ABOUT` topics.

### memory-eval-graph (completed, 5.4s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:SUPERSEDES]->(old:Decision)\nRETURN count(DISTINCT old) AS s', 'MATCH (d:Decision)-[:SUPERSEDES]->(old:Decision)-[:ABOUT]->(t:Topic)\nRETURN coun']

There are **7 superseded decisions**.  
They are on these topics:

- **infrastructure as code**  
- **gateway timeout**  
- **retries**  
- **compute platform**  
- **SLO**

Source: graph query over `Decision` → `SUPERSEDES` → `Decision` → `ABOUT` → `Topic` returned count and topic names.

### memory-eval-vector (completed, 7.1s, 3 tool calls)
queries: ['How many decisions have been superseded, and on which topics?', 'decisions superseded topics', 'superseded decision topic date source status']

I found 5 superseded decision topics in memory:

1. retries — D07 superseded by D14, and D14 superseded by D21  
   Source: `meetings/2026-03-30-weekly-sync.txt` (2026-03-30), `meetings/2026-06-15-weekly-sync.txt` (2026-06-15)

2. timeouts — D06 superseded by D12, and D12 superseded by D20  
   Source: `meetings/2026-03-16-weekly-sync.txt` (2026-03-16), `meetings/2026-05-18-weekly-sync.txt` (2026-05-18)

3. compute — D15 superseded by D17  
   Source: `meetings/2026-06-15-weekly-sync.txt` (2026-06-15)

4. iac — D01 superseded by D09  
   Source: `meetings/2026-01-12-weekly-sync.txt` (2026-01-12)

5. slo — D02 superseded by D28  
   Source: `meetings/2026-01-26-weekly-sync.txt` (2026-01-26)

I also retrieved `adr/ADR-005.md` (updated 2026-06-17), which is itself marked superseded by ADR-006, but that is an ADR document rather than one of the decision topics above.

## t28 [ru / aggregate] Какими действующими решениями владеет Anna Sokolova? Сколько их?
**expected:** 2: D13 Retries and idempotency ownership moves from Nikit; D21 Retries move out of the gateway into SQS with a de  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.2s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:anna-sokolova'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

Anna Sokolova владеет 2 действующими решениями.

1. **D13** — “Retries and idempotency ownership moves from Nikita to Anna (Nikita leaves on 2026-06-01)”  
   Дата: **2026-06-01**  
   Источник: **meetings/2026-06-01-weekly-sync.txt**

2. **D21** — “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”  
   Дата: **2026-08-24**  
   Источник: **meetings/2026-08-24-weekly-sync.txt**

Итого: **2**.

### memory-eval-graph (completed, 3.7s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:anna-sokolova'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

У Anna Sokolova 2 действующих решения.

- D13 — “Retries and idempotency ownership moves from Nikita to Anna (Nikita leaves on 2026-06-01)” — 2026-06-01 — active — source: `meetings/2026-06-01-weekly-sync.txt`
- D21 — “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off” — 2026-08-24 — active — source: `meetings/2026-08-24-weekly-sync.txt`

Источник: граф памяти, по связям OWNS от `person:anna-sokolova` к Decision с `status = active` и без даты окончания.

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['Какими действующими решениями владеет Anna Sokolova? Сколько их?', 'Anna Sokolova owner current decisions active decisions', 'Who owns current decisions Anna Sokolova']

У Anna Sokolova в памяти есть **1 действующее решение**: **idempotency**.  
- **idempotency** — Anna Sokolova owns idempotency from **2026-06-01**; статус **active**. Источник: `memory/decisions.jsonl` / `ownership:idempotency:2026-06-01`, дата **2026-06-01**.

По `retries` есть более новая запись, и она **не у Anna**:
- **retries** — ownership moves from Anna to Ivan; статус **active**. Источник: `meetings/2026-09-07-security-review.txt`, дата **2026-09-07**.

Итого: **1** действующее решение.

## t29 [ru / aggregate] Какими действующими решениями владеет Pavel Grishin? Сколько их?
**expected:** 3: D03 One CloudFormation root stack per environment with; D05 Front Relay with the API gateway; the gateway and ; D09 Hybrid IaC: networking (VPC, peering, DNS) stays i  
**expected sources:** {'sources': ['meetings/2026-02-09-weekly-sync.txt', 'meetings/2026-03-02-weekly-sync.txt', 'meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 3.7s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:pavel-grishin'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

Pavel Grishin владеет 3 действующими решениями.

- D03 — “One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)” — 2026-02-09 — `meetings/2026-02-09-weekly-sync.txt`
- D05 — “Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack” — 2026-03-02 — `meetings/2026-03-02-weekly-sync.txt`
- D09 — “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation” — 2026-04-20 — `meetings/2026-04-20-weekly-sync.txt`

### memory-eval-graph (completed, 3.8s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:pavel-grishin'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

Pavel Grishin владеет 3 действующими решениями.

1. 2026-02-09 — `One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)`  
   Источник: `meetings/2026-02-09-weekly-sync.txt`

2. 2026-03-02 — `Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack`  
   Источник: `meetings/2026-03-02-weekly-sync.txt`

3. 2026-04-20 — `Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation`  
   Источник: `meetings/2026-04-20-weekly-sync.txt`

### memory-eval-vector (completed, 4.2s, 3 tool calls)
queries: ['Какими действующими решениями владеет Pavel Grishin? Сколько их?', 'Pavel Grishin current decisions owns how many', 'Павел Гришин действующие решения сколько']

У Pavel Grishin есть 2 действующих решения:

1. **gateway** — с **2026-03-02**  
   Источник: `meetings/2026-03-02-weekly-sync.txt` (запись `D05`), статус **active**.

2. **iac** — с **2026-02-09**  
   Источник: `meetings/2026-02-09-weekly-sync.txt` (запись `D03`), статус **active**.

Итого: **2**.

Примечание: найдено также решение по **timeouts** от **2026-03-16**, но оно помечено как **superseded**, поэтому не считается действующим. Источник: `meetings/2026-03-16-weekly-sync.txt` (`D06`).

## t30 [ru / aggregate] Какими действующими решениями владеет Ivan Melnik? Сколько их?
**expected:** 5: D16 Serverless PoC ownership moves from Sergey to Ivan; D17 Relay moves to Lambda with provisioned concurrency; D20 Gateway integration timeout lowered from 30 s to 2; D22 Retries ownership moves from Anna to Ivan, who own; D25 Serverless cutover on 2026-10-19 at 09:00 local, i  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt', 'meetings/2026-08-03-architecture-committee.txt', 'meetings/2026-08-24-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 4.9s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:ivan-melnik'})-[o:OWNS]->(d:Decision) WHERE o.to IS "]

По состоянию в памяти у Ivan Melnik 5 действующих решений.

- Serverless PoC ownership moves from Sergey to Ivan — 2026-07-13, `meetings/2026-07-13-weekly-sync.txt`
- Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances — 2026-08-03, `meetings/2026-08-03-architecture-committee.txt`
- Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom — 2026-08-24, `meetings/2026-08-24-weekly-sync.txt`
- Retries ownership moves from Anna to Ivan, who owns the SQS pipeline — 2026-09-07, `meetings/2026-09-07-security-review.txt`
- Serverless cutover on 2026-10-19 at 09:00 local, inside the planned-work error budget — 2026-10-05, `meetings/2026-10-05-cutover-planning.txt`

### memory-eval-graph (completed, 4.9s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:ivan-melnik'})-[o:OWNS]->(d:Decision)\nWHERE o.to IS "]

Ivan Melnik владеет 5 действующими решениями. Источники и даты:

1. **Serverless PoC ownership moves from Sergey to Ivan** — 2026-07-13, `meetings/2026-07-13-weekly-sync.txt`
2. **Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances** — 2026-08-03, `meetings/2026-08-03-architecture-committee.txt`
3. **Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom** — 2026-08-24, `meetings/2026-08-24-weekly-sync.txt`
4. **Retries ownership moves from Anna to Ivan, who owns the SQS pipeline** — 2026-09-07, `meetings/2026-09-07-security-review.txt`
5. **Serverless cutover on 2026-10-19 at 09:00 local, inside the planned-work error budget** — 2026-10-05, `meetings/2026-10-05-cutover-planning.txt`

### memory-eval-vector (completed, 6.5s, 3 tool calls)
queries: ['Какими действующими решениями владеет Ivan Melnik? Сколько их?', 'Ivan Melnik current decisions ownership count', 'Ivan Melnik owns decisions active current']

По памяти у Ivan Melnik **3 действующих владения**:

1. **retries** — с 2026-09-07, current.  
   Источник: `memory/decisions.jsonl`, 2026-09-07 (`own-retries-2026-09-07`).

2. **compute** — с 2026-07-13, current.  
   Источник: `memory/decisions.jsonl`, 2026-07-13 (`own-compute-2026-07-13`).

3. **serverless PoC** — ownership moved from Sergey to Ivan, active.  
   Источник: `meetings/2026-07-13-weekly-sync.txt`, 2026-07-13 (`D16`).

Есть также более общий `ownership`-запись от 2026-07-13 и отдельная запись про retries от 2026-09-07; они не добавляют нового владения, а подтверждают те же темы.  
Итого: **3**.

## t31 [ru / aggregate] Какими действующими решениями владеет Lena Kim? Сколько их?
**expected:** 3: D04 Manual console changes are frozen; nightly drift d; D27 Rollback owner for both cutovers is Lena; D28 Delivery p95 SLO relaxed from 2 s to 3 s for 30 da  
**expected sources:** {'sources': ['meetings/2026-02-23-incident-review.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 3.8s, 1 tool calls)
queries: ["MATCH (p:Person {key:'person:lena-kim'})-[o:OWNS]->(d:Decision)\nWHERE o.to IS NU"]

Lena Kim владеет 3 действующими решениями.

- `Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call` — 2026-02-23, `meetings/2026-02-23-incident-review.txt`
- `Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s` — 2026-10-05, `meetings/2026-10-05-cutover-planning.txt`
- `Rollback owner for both cutovers is Lena` — 2026-10-05, `meetings/2026-10-05-cutover-planning.txt`

### memory-eval-graph (completed, 4.0s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:lena-kim'})-[o:OWNS]->(d:Decision)\nWHERE o.to IS NUL"]

Lena Kim владеет 3 действующими решениями.

- «Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call» — 2026-02-23 — active — `meetings/2026-02-23-incident-review.txt`
- «Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s» — 2026-10-05 — active — `meetings/2026-10-05-cutover-planning.txt`
- «Rollback owner for both cutovers is Lena» — 2026-10-05 — active — `meetings/2026-10-05-cutover-planning.txt`

Источники: решение о владении найдено по связи OWNS для `person:lena-kim`; статус `active` взят из самих узлов Decision.

### memory-eval-vector (completed, 6.3s, 3 tool calls)
queries: ['Какими действующими решениями владеет Lena Kim? Сколько их?', 'Lena Kim owns active decisions count', 'Какие решения сейчас принадлежат Lena Kim']

У Lena Kim есть 3 действующих решения:

1. **cutover** — rollback owner для обоих cutover’ов назначен Lena Kim.  
   Источник: `meetings/2026-10-05-cutover-planning.txt`, 2026-10-05.

2. **iac** — manual console changes frozen; nightly drift detection на всех стэках с алертами on-call.  
   Источник: `meetings/2026-02-23-incident-review.txt`, 2026-02-23.

3. **slo** — p95 SLO ослаблен с 2 s до 3 s на 30 дней после serverless cutover, затем обратно до 2 s.  
   Источник: `meetings/2026-10-05-cutover-planning.txt`, 2026-10-05.

Итого: **3**.

Примечание: в памяти также есть более старое решение по **slo** от 2026-01-26, но оно **superseded** решением от 2026-10-05, поэтому не считается действующим. Источник: `meetings/2026-01-26-weekly-sync.txt` и `meetings/2026-10-05-cutover-planning.txt`.

## t32 [en / aggregate] Which ADRs are not Accepted, and what is their status?
**expected:** Superseded: ADR-001, ADR-005; Rejected: ADR-007; Proposed: ADR-010  
**expected sources:** {'sources': ['adr/ADR-001.md', 'adr/ADR-005.md', 'adr/ADR-007.md', 'adr/ADR-010.md']}

### memory-eval-both (completed, 3.7s, 1 tool calls)
queries: ["MATCH (a:ADR) WHERE a.status <> 'Accepted' RETURN a.id, a.title, a.status, a.fil"]

The ADRs that are not Accepted are:

- ADR-001 — Superseded — “Migrate infrastructure code from Terraform to CloudFormation” — source: `adr/ADR-001.md`
- ADR-005 — Superseded — “Evaluate EKS and Lambda with two proofs of concept” — source: `adr/ADR-005.md`
- ADR-007 — Rejected — “Keep Relay on EKS with autoscaling” — source: `adr/ADR-007.md`
- ADR-010 — Proposed — “Gateway timeout policy for Lambda integrations” — source: `adr/ADR-010.md`

Source query date: not explicitly dated in the graph; these are the current ADR statuses from memory.

### memory-eval-graph (completed, 4.2s, 1 tool calls)
queries: ["MATCH (a:ADR) WHERE a.status <> 'Accepted' RETURN a.id, a.title, a.status, a.fil"]

The ADRs that are not Accepted are:

- ADR-001 — Superseded — `adr/ADR-001.md`  
  Source file: `adr/ADR-001.md`  
  Date: not in the retrieved ADR row

- ADR-005 — Superseded — `adr/ADR-005.md`  
  Source file: `adr/ADR-005.md`  
  Date: not in the retrieved ADR row

- ADR-007 — Rejected — `adr/ADR-007.md`  
  Source file: `adr/ADR-007.md`  
  Date: not in the retrieved ADR row

- ADR-010 — Proposed — `adr/ADR-010.md`  
  Source file: `adr/ADR-010.md`  
  Date: not in the retrieved ADR row

I retrieved each ADR’s `id`, `title`, `status`, and `file`; the graph query did not return their dates.

### memory-eval-vector (completed, 8.8s, 3 tool calls)
queries: ['Which ADRs are not Accepted, and what is their status?', 'ADRs not Accepted status', 'accepted ADR status list']

Not in memory as a complete list of all ADRs that are not Accepted.

What I retrieved:
- **ADR-007: Keep Relay on EKS with autoscaling** — **Rejected** — `adr/ADR-007.md` — updated **2026-08-05**.
- **ADR-010: Gateway timeout policy for Lambda integrations** — **Proposed** / **No decision recorded** — `adr/ADR-010.md` — updated **2026-09-23**.
- **ADR-002: Front Relay with the API gateway** — **Accepted** — `adr/ADR-002.md` — updated **2026-03-04**.
- **ADR-006: Run Relay on Lambda with provisioned concurrency** — **Accepted, supersedes ADR-005** — `adr/ADR-006.md` — updated **2026-08-05**.
- **ADR-008: Secrets from SSM Parameter Store** — **Accepted** — `adr/ADR-008.md` — updated **2026-09-09**.
- **ADR-004: Hybrid IaC...** — **Accepted, supersedes ADR-001** — `adr/ADR-004.md` — updated **2026-04-22**.

So the only clearly **not Accepted** ADRs I found are:
- **ADR-007** — Rejected — `adr/ADR-007.md` — 2026-08-05
- **ADR-010** — Proposed / no decision recorded — `adr/ADR-010.md` — 2026-09-23

If you want, I can search more broadly for any other ADRs with statuses like Draft, Proposed, or Rejected.

## t33 [ru / unowned_at] Какие открытые вопросы были без владельца на 2026-06-15?
**expected:** O1 DynamoDB migration dry run on a production snapshot (raised 2026-05-04); O4 DocumentDB decommission date (raised 2026-05-18)  
**expected sources:** {'sources': ['meetings/2026-05-04-poc-review.txt', 'meetings/2026-05-18-weekly-sync.txt']}

### memory-eval-both (completed, 4.5s, 1 tool calls)
queries: ["MATCH (o:OpenItem) WHERE o.raised <= '2026-06-15' AND NOT EXISTS { MATCH (o)<-[w"]

На 2026-06-15 без владельца были 2 открытых вопроса.

- O1 — «DynamoDB migration dry run on a production snapshot»  
  raised: 2026-05-04; raised_again: 2026-05-18, 2026-06-15, 2026-06-29, 2026-07-20; status: closed.  
  source: данных о владельце нет в памяти для этой даты.

- O4 — «DocumentDB decommission date»  
  raised: 2026-05-18; raised_again: 2026-08-10, 2026-10-05; status: open.  
  source: данных о владельце нет в памяти для этой даты.

Если хотите, могу отдельно показать, когда у каждого из них появился владелец или был закрыт.

### memory-eval-graph (completed, 4.1s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На 2026-06-15 без владельца были 2 открытых вопроса:

- O1 — “DynamoDB migration dry run on a production snapshot”; raised: 2026-05-04; raised_again: 2026-05-18, 2026-06-15, 2026-06-29, 2026-07-20. Источник: граф памяти, дата вопроса/среза 2026-06-15.
- O4 — “DocumentDB decommission date”; raised: 2026-05-18; raised_again: 2026-08-10, 2026-10-05. Источник: граф памяти, дата вопроса/среза 2026-06-15.

Если нужно, могу также показать, как именно это следует из условий “без владельца” и “на дату”.

### memory-eval-vector (completed, 9.4s, 3 tool calls)
queries: ['Какие открытые вопросы были без владельца на 2026-06-15?', 'open items without owner on 2026-06-15', 'вопросы без владельца открытые 2026-06-15']

На **2026-06-15** в памяти есть один открытый вопрос **без владельца**:

- **DynamoDB migration dry run on a production snapshot** — raised 2026-05-04, **no owner**; на 2026-06-15 он всё ещё упоминается как без владельца.  
  Источник: `meetings/2026-05-04-poc-review.txt` (2026-05-04), и подтверждение в `meetings/2026-06-15-weekly-sync.txt` (2026-06-15).  
  Примечание: в записи от 2026-06-15 сказано только «dry run … знаю без владельца», без явного названия, но это тот же open item из более ранней записи.

Что я нашёл в поиске:
- `meetings/2026-05-04-poc-review.txt` — open item про DynamoDB migration dry run, no owner.
- `meetings/2026-05-18-weekly-sync.txt` — два вопроса по базе, оба open, дата декома неизвестна, без владельца.
- `meetings/2026-06-15-weekly-sync.txt` — упоминание dry run как «без владельца».

Если хотите, я могу ещё перечислить **все** open items без владельца, которые существовали **на или до** 2026-06-15, а не только тот, что прямо подтверждён на эту дату.

## t34 [ru / unowned_at] Какие открытые вопросы были без владельца на 2026-08-17?
**expected:** O3 Load test on Lambda at 10x current volume (raised 2026-07-27); O4 DocumentDB decommission date (raised 2026-05-18)  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-07-27-poc-review.txt']}

### memory-eval-both (completed, 3.9s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На 2026-08-17 без владельца были такие открытые вопросы:

- **O3** — “Load test on Lambda at 10x current volume”  
  raised: 2026-07-27; raised_again: 2026-08-17, 2026-09-14  
  status: open  
  source: неизвестно из этой выборки; дата: 2026-07-27

- **O4** — “DocumentDB decommission date”  
  raised: 2026-05-18; raised_again: 2026-08-10, 2026-10-05  
  status: open  
  source: неизвестно из этой выборки; дата: 2026-05-18

Если хотите, могу ещё показать, из каких встреч они были подняты.

### memory-eval-graph (completed, 4.4s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $d AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На 2026-08-17 без владельца были такие открытые вопросы:

- O3 — “Load test on Lambda at 10x current volume”, raised: 2026-07-27, raised_again: 2026-08-17 / 2026-09-14, status: open. Источник: не указан в найденных полях; дата из графа: 2026-07-27.
- O4 — “DocumentDB decommission date”, raised: 2026-05-18, raised_again: 2026-08-10 / 2026-10-05, status: open. Источник: не указан в найденных полях; дата из графа: 2026-05-18.

Основание: по состоянию на 2026-08-17 у них не было владельца и они не были закрыты.

### memory-eval-vector (completed, 11.4s, 3 tool calls)
queries: ['Какие открытые вопросы были без владельца на 2026-08-17?', 'открытые вопросы без владельца 2026-08-17', 'open items with no owner as of 2026-08-17']

На **2026-08-17** в памяти есть следующее по **открытым вопросам без владельца**:

1. **Load test on Lambda at 10x current volume** — raised **2026-07-27**, помечен как **open**, **No owner**.  
   Источник: `meetings/2026-07-27-poc-review.txt` (документ/claim `O3`), дата **2026-07-27**.

2. **DocumentDB decommission date** — raised **2026-05-18**, помечен как **open**, **No owner**.  
   Источник: `meetings/2026-05-18-weekly-sync.txt` (claim `O4`), дата **2026-05-18**.

3. **DynamoDB migration dry run on a production snapshot** — raised **2026-05-04**, позже повторно поднимался, но в записи указан **No owner**; статус там **closed**.  
   Источник: `meetings/2026-05-04-poc-review.txt` (claim `O1`), дата **2026-05-04**.  
   Это не открытый вопрос на 2026-08-17, но он был найден среди безвладельных.

Что я также нашёл, но это **позже 2026-08-17** и потому не относится к указанной дате:
- `cutover` rollback runbook — 2026-08-24, closed, с владельцем.
- `security` rotate DocumentDB credentials — 2026-09-07, open, без владельца.

Если хотите, я могу дальше отфильтровать именно **все open items без owner, которые существовали на 2026-08-17**, строго исключив всё, что появилось позже эт

## t35 [en / unowned_at] Which open items had no owner on 2026-10-05?
**expected:** O3 Load test on Lambda at 10x current volume (raised 2026-07-27); O4 DocumentDB decommission date (raised 2026-05-18); O7 Rotate DocumentDB credentials before decommission (raised 2026-09-07)  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-07-27-poc-review.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 2.8s, 1 tool calls)
queries: ["MATCH (o:OpenItem) WHERE o.raised <= '2026-10-05' AND NOT EXISTS { MATCH (o)<-[w"]

On 2026-10-05, the open items with no owner were:

- O3 — “Load test on Lambda at 10x current volume”  
  Raised: 2026-07-27; raised again: 2026-08-17, 2026-09-14

- O4 — “DocumentDB decommission date”  
  Raised: 2026-05-18; raised again: 2026-08-10, 2026-10-05

- O7 — “Rotate DocumentDB credentials before decommission”  
  Raised: 2026-09-07; raised again: 2026-09-28

Source: graph query against open items as of 2026-10-05.

### memory-eval-graph (completed, 4.3s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

On 2026-10-05, the open items with no owner were:

- O3 — “Load test on Lambda at 10x current volume” — raised 2026-07-27; raised again 2026-08-17 and 2026-09-14 — status open. Source: graph memory, no source file stored on the node fields returned.
- O4 — “DocumentDB decommission date” — raised 2026-05-18; raised again 2026-08-10 and 2026-10-05 — status open. Source: graph memory, no source file stored on the node fields returned.
- O7 — “Rotate DocumentDB credentials before decommission” — raised 2026-09-07; raised again 2026-09-28 — status open. Source: graph memory, no source file stored on the node fields returned.

Assumption: “no owner” means no OWNS edge in force on 2026-10-05, and the item was not already closed by that date.

### memory-eval-vector (completed, 8.5s, 3 tool calls)
queries: ['Which open items had no owner on 2026-10-05?', 'open items no owner 2026-10-05', 'items with no owner raised on 2026-10-05']

On 2026-10-05, the open items with no owner in memory are:

- DocumentDB decommission date — raised 2026-05-18, raised again on 2026-08-10 and 2026-10-05, no owner. Source: `meetings/2026-05-18-weekly-sync.txt` (2026-05-18).
- Rotate DocumentDB credentials before decommission — raised 2026-09-07, raised again on 2026-09-28, no owner. Source: `meetings/2026-09-07-security-review.txt` (2026-09-07).
- Load test on Lambda at 10x current volume — raised 2026-07-27, raised again on 2026-08-17 and 2026-09-14, no owner. Source: `meetings/2026-07-27-poc-review.txt` (2026-07-27).

What I retrieved:
- `meetings/2026-05-18-weekly-sync.txt` (2026-05-18)
- `meetings/2026-09-07-security-review.txt` (2026-09-07)
- `meetings/2026-07-27-poc-review.txt` (2026-07-27)
- Also retrieved several items that had owners or were closed, but they do not meet your filter.

I did not find a separate item explicitly *dated* 2026-10-05 with no owner beyond the Database item that was raised again on that date.

## t36 [en / stale_docs] Which documents were out of date on 2026-07-01, and why?
**expected:** docs/iac-cloudformation.md (updated 2026-02-11): says all infrastructure including networking moves to CloudFormation, changed by D09 on 2026-04-20; docs/gateway.md (updated 2026-03-18): says the integration timeout is 10 s, changed by D12 on 2026-05-18; docs/gateway.md (updated 2026-03-18): says retries are disabled on /deliver, changed by D14 on 2026-06-15; docs/onboarding.md (updated 2026-03-10): lists Nikita as retries owner and does not list Sergey or Ivan, changed by D13 on 2026-06-01; confluence/architecture.xhtml (updated 2026-03-12): shows DocumentDB, changed by D10 on 2026-05-04; confluence/decision-log.xhtml (updated 2026-06-03): stops at 2026-06-01, changed by D14 on 2026-06-15  
**expected sources:** {'sources': ['confluence/architecture.xhtml', 'confluence/decision-log.xhtml', 'docs/gateway.md', 'docs/iac-cloudformation.md', 'docs/onboarding.md']}

### memory-eval-both (completed, 7.8s, 1 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ']

As of 2026-07-01, these documents were out of date:

- `confluence/architecture.xhtml` — updated `2026-03-12`
  - It missed a later decision from `2026-05-04` saying the architecture **shows DocumentDB**.
  - Source: `meetings/2026-05-04-poc-review.txt`

- `confluence/decision-log.xhtml` — updated `2026-06-03`
  - It missed a later decision from `2026-06-15` saying the log **stops at 2026-06-01**.
  - Source: `meetings/2026-06-15-weekly-sync.txt`

- `docs/gateway.md` — updated `2026-03-18`
  - It missed a later decision from `2026-06-15` saying **retries are disabled on /deliver**.
  - It also missed a later decision from `2026-05-18` saying **the integration timeout is 10 s**.
  - Sources: `meetings/2026-06-15-weekly-sync.txt`, `meetings/2026-05-18-weekly-sync.txt`

- `docs/iac-cloudformation.md` — updated `2026-02-11`
  - It missed a later decision from `2026-04-20` saying **all infrastructure including networking moves to CloudFormation**.
  - Source: `meetings/2026-04-20-weekly-sync.txt`

- `docs/onboarding.md` — updated `2026-03-10`
  - It missed a later decision from `2026-06-01` saying **Nikita is the retries owner and Sergey or Ivan are not listed**.
  - Source: `meetings/2

### memory-eval-graph (completed, 15.2s, 1 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D AND dec']

On 2026-07-01, these documents were out of date because later decisions changed facts they contained.

- `confluence/architecture.xhtml` — updated `2026-03-12`  
  It was made stale by a decision on `2026-05-04` that changed the database choice: “DynamoDB single-table design, chosen on PoC-1 results (p99 read 4 ms vs 11 ms; 38% lower cost at projected volume)” from `meetings/2026-05-04-poc-review.txt`.  
  The document’s stale fact is noted as “shows DocumentDB”.

- `confluence/decision-log.xhtml` — updated `2026-06-03`  
  It was made stale by a decision on `2026-06-15` that changed the retries policy: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%” from `meetings/2026-06-15-weekly-sync.txt`.  
  The document’s stale fact is noted as “stops at 2026-06-01”.

- `docs/gateway.md` — updated `2026-03-18`  
  It was made stale twice by later decisions:
  - `2026-05-18`: “Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14” from `meetings/2026-05-18-weekly-sync.txt`, which makes the document’s “integration timeout is 10 s” stale.
  - `2026-06-15`: “Retries enabled on POST /deliver at the gateway: max 3 atte

### memory-eval-vector (completed, 9.2s, 3 tool calls)
queries: ['Which documents were out of date on 2026-07-01, and why?', 'documents out of date on 2026-07-01 why', 'out of date documents 2026-07-01 stale because newer decision']

Not in memory for a complete list of “documents out of date on 2026-07-01.”

What I retrieved:
- `docs/documentdb-runbook.md` — updated 2026-02-02. Retrieved claims indicate it was stale because the newer decision on 2026-10-05 said it “still describes DocumentDB as the system of record” after the DynamoDB cutover decision. Source: `meetings/2026-10-05-cutover-planning.txt` (2026-10-05).
- `docs/db-migration-plan.md` — updated 2026-05-26. Retrieved claims indicate it was stale because the newer decision on 2026-10-05 said it “still has no cutover date.” Source: `meetings/2026-10-05-cutover-planning.txt` (2026-10-05).
- `docs/secrets.md` — updated 2026-09-10. Retrieved claims say `/relay/prod/docdb/credentials` was overdue and must be rotated before DocumentDB decommission. Source: `docs/secrets.md` (2026-09-10), plus security review item from `meetings/2026-09-07-security-review.txt` (2026-09-07).

Why I’m not giving a dated list for 2026-07-01:
- The retrieved memory chunks are either earlier than 2026-07-01 or later than it, and I don’t have a chunk that explicitly answers “which documents were out of date on 2026-07-01.”
- I can only cite what the memory contains; I don’t want t

## t37 [en / stale_docs] Which documents were out of date on 2026-10-05, and why?
**expected:** docs/iac-cloudformation.md (updated 2026-02-11): says all infrastructure including networking moves to CloudFormation, changed by D09 on 2026-04-20; docs/gateway.md (updated 2026-03-18): says the integration timeout is 10 s, changed by D12 on 2026-05-18; docs/gateway.md (updated 2026-03-18): says retries are disabled on /deliver, changed by D14 on 2026-06-15; docs/gateway.md (updated 2026-03-18): describes gateway retries at all, changed by D21 on 2026-08-24; docs/slo.md (updated 2026-01-28): says p95 2 s with no stabilisation window, changed by D28 on 2026-10-05; docs/documentdb-runbook.md (updated 2026-02-02): describes DocumentDB as the system of record, changed by D26 on 2026-10-05; docs/db-migration-plan.md (updated 2026-05-26): says the dry run has no owner, changed by D19 on 2026-08-10; docs/db-migration-plan.md (updated 2026-05-26): has no cutover date, changed by D26 on 2026-10-05; docs/runbook-cutover-serverless.md (updated 2026-09-29): says rollback owner TBD, changed by D27 on 2026-10-05; docs/runbook-cutover-serverless.md (updated 2026-09-29): has no cutover date, changed by D25 on 2026-10-05; docs/onboarding.md (updated 2026-03-10): lists Nikita as retries owner and does not list Sergey or Ivan, changed by D13 on 2026-06-01; confluence/architecture.xhtml (updated 2026-03-12): shows EKS as the runtime, changed by D17 on 2026-08-03; confluence/architecture.xhtml (updated 2026-03-12): shows DocumentDB, changed by D10 on 2026-05-04; confluence/decision-log.xhtml (updated 2026-06-03): stops at 2026-06-01, changed by D14 on 2026-06-15; confluence/team-roster.xhtml (updated 2026-07-08): lists Anna as retries owner, changed by D22 on 2026-09-07; confluence/migration-roadmap.xhtml (updated 2026-06-20): lists compute decision as pending PoC, changed by D17 on 2026-08-03  
**expected sources:** {'sources': ['confluence/architecture.xhtml', 'confluence/decision-log.xhtml', 'confluence/migration-roadmap.xhtml', 'confluence/team-roster.xhtml', 'docs/db-migration-plan.md', 'docs/documentdb-runbook.md', 'docs/gateway.md', 'docs/iac-cloudformation.md', 'docs/onboarding.md', 'docs/runbook-cutover-serverless.md', 'docs/slo.md']}

### memory-eval-both (completed, 24.0s, 1 tool calls)
queries: ["MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= '2026-10-0"]

As of 2026-10-05, these documents were out of date because later decisions had changed facts they stated:

- `confluence/architecture.xhtml` — updated `2026-03-12`
  - `2026-05-04` decision changed the fact “shows DocumentDB”  
    source: `meetings/2026-05-04-poc-review.txt`
  - `2026-08-03` decision changed the fact “shows EKS as the runtime”  
    source: `meetings/2026-08-03-architecture-committee.txt`

- `confluence/decision-log.xhtml` — updated `2026-06-03`
  - `2026-06-15` decision changed the fact “stops at 2026-06-01”  
    source: `meetings/2026-06-15-weekly-sync.txt`

- `confluence/migration-roadmap.xhtml` — updated `2026-06-20`
  - `2026-08-03` decision changed the fact “lists compute decision as pending PoC”  
    source: `meetings/2026-08-03-architecture-committee.txt`

- `confluence/team-roster.xhtml` — updated `2026-07-08`
  - `2026-09-07` decision changed the fact “lists Anna as retries owner”  
    source: `meetings/2026-09-07-security-review.txt`

- `docs/db-migration-plan.md` — updated `2026-05-26`
  - `2026-10-05` decision changed the fact “has no cutover date”  
    source: `meetings/2026-10-05-cutover-planning.txt`
  - `2026-08-10` decision changed the fact “

### memory-eval-graph (completed, 21.8s, 1 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ']

On 2026-10-05, these documents were out of date:

- confluence/architecture.xhtml — updated 2026-03-12. It was stale because later decisions changed what it says about the architecture:
  - 2026-05-04: the project shows DocumentDB
  - 2026-08-03: the project shows EKS as the runtime  
  Source: meetings/2026-05-04-poc-review.txt; meetings/2026-08-03-architecture-committee.txt

- confluence/decision-log.xhtml — updated 2026-06-03. It was stale because a later decision changed the ownership/history it records:
  - 2026-06-15: it stops at 2026-06-01  
  Source: meetings/2026-06-15-weekly-sync.txt

- confluence/migration-roadmap.xhtml — updated 2026-06-20. It was stale because later decisions changed the compute status it describes:
  - 2026-08-03: it lists the compute decision as pending PoC  
  Source: meetings/2026-08-03-architecture-committee.txt

- confluence/team-roster.xhtml — updated 2026-07-08. It was stale because a later decision changed the retries owner it lists:
  - 2026-09-07: it lists Anna as retries owner  
  Source: meetings/2026-09-07-security-review.txt

- docs/db-migration-plan.md — updated 2026-05-26. It was stale because later decisions changed the migration plan

### memory-eval-vector (completed, 13.0s, 3 tool calls)
queries: ['Which documents were out of date on 2026-10-05, and why?', 'documents out of date on 2026-10-05 why', 'out of date documents 2026-10-05']

The memory contains **three documents that were out of date by 2026-10-05**:

1. **`docs/documentdb-runbook.md`** — updated **2026-02-02**  
   It was out of date because the **2026-10-05 decision on database cutover** says DocumentDB was still described there as the system of record, but the active decision had moved to a **DynamoDB cutover on 2026-10-12**.  
   **Source:** `meetings/2026-10-05-cutover-planning.txt` / decision claim `D26` (**2026-10-05**).

2. **`docs/db-migration-plan.md`** — updated **2026-05-26**  
   It was out of date because the same **2026-10-05 database decision** says this plan still had **no cutover date**, while the new decision set the cutover to **2026-10-12**.  
   **Source:** `meetings/2026-10-05-cutover-planning.txt` / decision claim `D26` (**2026-10-05**).

3. **`docs/runbook-cutover-serverless.md`** — updated **2026-09-29**  
   It was out of date because the **2026-10-05 cutover decision** says it still had **no cutover date**, while the new decision set **serverless cutover on 2026-10-19 at 09:00 local**.  
   **Source:** `meetings/2026-10-05-cutover-planning.txt` / decision claim `D25` (**2026-10-05**).

I also retrieved related but not direct

## t38 [ru / poc_basis] На каком PoC и на каких цифрах основано решение «DynamoDB single-table design, chosen on PoC-1 results (p99 r…»?
**expected:** PoC-1: DynamoDB single-table vs multi-table: {"single_table_p99_read_ms": 4, "multi_table_p99_read_ms": 11, "single_table_cost_delta_pct": -38, "documentdb_p99_read_ms": 9}; report docs/poc-dynamodb-report.md  
**expected sources:** {'sources': ['docs/poc-dynamodb-report.md', 'meetings/2026-05-04-poc-review.txt']}

### memory-eval-both (completed, 7.3s, 3 tool calls)
queries: ['"DynamoDB single-table design, chosen on PoC-1 results" p99 requests latency thr', '"DynamoDB single-table design" "PoC-1" results numbers p99 rps latency', "MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'DynamoDB singl"]

Решение основано на PoC-1: **PoC-1: DynamoDB single-table vs multi-table**.  
Цифры из результатов:

- **p99 read**: single-table **4 ms** vs multi-table **11 ms**
- **p99 read**: single-table **4 ms** vs DocumentDB **9 ms**
- **стоимость при projected volume**: single-table **на 38% ниже** DocumentDB

Источник решения: **meetings/2026-05-04-poc-review.txt**, дата **2026-05-04**.  
Источник цифр: **docs/poc-dynamodb-report.md**, дата **2026-05-01**.

Если хотите, я могу ещё коротко показать полную цепочку: какое именно решение, кто его предложил и кто возражал.

### memory-eval-graph (completed, 4.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'DynamoDB singl"]

Решение основано на PoC-1: **PoC-1: DynamoDB single-table vs multi-table**.

Цифры, на которых оно основано:
- **p99 read = 4 ms** для single-table
- **p99 read = 11 ms** для multi-table
- **38% lower cost** at projected volume

Источник решения:
- **meetings/2026-05-04-poc-review.txt**, дата **2026-05-04**: `DynamoDB single-table design, chosen on PoC-1 results (p99 read 4 ms vs 11 ms; 38% lower cost at projected volume)`

Источник PoC:
- **docs/poc-dynamodb-report.md**
- `c.results`: `{"single_table_p99_read_ms": 4, "multi_table_p99_read_ms": 11, "single_table_cost_delta_pct": -38, "documentdb_p99_read_ms": 9}`

Если хотите, я могу ещё кратко сопоставить, какие именно варианты сравнивались в PoC-1 и что было выбрано в итоге.

### memory-eval-vector (completed, 8.3s, 3 tool calls)
queries: ['На каком PoC и на каких цифрах основано решение «DynamoDB single-table design, c', 'DynamoDB single-table design, chosen on PoC-1 results p99 r', 'PoC-1 results p99 DynamoDB single-table design']

Решение основано на **PoC-1**. В памяти есть два согласующихся источника:

- **ADR-003** — `adr/ADR-003.md`, дата **2026-05-06**:  
  «DynamoDB single-table design, chosen on PoC-1 results (p99 read 4 ms vs 11 ms; 38% lower cost at projected volume).»
- **Отчёт PoC-1** — `docs/poc-dynamodb-report.md`, дата **2026-05-01**, раздел **Results**:  
  - DocumentDB (baseline): **read p99 9 ms**, write p99 14 ms, cost **$5,200**
  - DynamoDB multi-table: **read p99 11 ms**, write p99 9 ms, cost **$5,100**
  - DynamoDB single-table: **read p99 4 ms**, write p99 8 ms, cost **$3,200 (-38%)**

То есть решение основано на **PoC-1**, а ключевые цифры — **p99 read 4 ms vs 11 ms** и **38% lower cost at projected volume**.  
Дополнительно из отчёта PoC-1 видно, что сравнение шло на **90 days of production-shaped deliveries (14 M items)** и нагрузке **на six Relay access patterns at 1x and 3x current volume**.

Если нужно, могу отдельно выписать:
1. какие именно сравнивались варианты,  
2. какие были p99 write/cost у каждого,  
3. или почему multi-table проиграл по чтению.

## t39 [ru / poc_basis] На каком PoC и на каких цифрах основано решение «Relay moves to Lambda with provisioned concurrency on /deliv…»?
**expected:** PoC-3: Relay on Lambda: {"p95_warm_s": 1.9, "p95_cold_s": 3.4, "cold_start_s": 1.2, "monthly_cost_usd": 3600, "cost_delta_vs_eks_pct": -41}; report docs/poc-lambda-report.md  
**expected sources:** {'sources': ['docs/poc-lambda-report.md', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 5.6s, 3 tool calls)
queries: ['"Relay moves to Lambda with provisioned concurrency on /deliv…" PoC цифры основа', '"Relay moves to Lambda with provisioned concurrency" PoC numbers basis decision', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE d.text STARTS "]

Решение основано на **PoC-3**.

Цифры, которые прямо указаны в памяти для этого решения:
- **p95 1.9 s** с provisioned concurrency на `/deliver`
- **3.4 s** без provisioned concurrency
- **$3,600/мес**, что составляет **-41% vs EKS**

Источник:
- `docs/poc-lambda-report.md` — updated **2026-07-24**
- `adr/ADR-006.md` — updated **2026-08-05**
- само решение: `meetings/2026-08-03-architecture-committee.txt` — date **2026-08-03**, status **active**

Формулировка в решении:  
“Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances.”

Если хотите, могу ещё коротко перечислить, чем PoC-3 отличался от PoC-2.

### memory-eval-graph (completed, 5.6s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE d.text STARTS ", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE d.text STARTS ", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE d.text STARTS "]

Решение **«Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances»** основано на **PoC-3: Relay on Lambda**.

Цифры из PoC:
- **p95 warm**: **1.9 s**
- **p95 cold**: **3.4 s**
- **cold start**: **1.2 s**
- **monthly cost**: **3600 USD**
- **cost delta vs EKS**: **-41%**

Источник:
- решение: **meetings/2026-08-03-architecture-committee.txt**, **2026-08-03**
- PoC: **docs/poc-lambda-report.md**, результат PoC-3

Если нужно, могу ещё показать, какие именно формулировки в решении и отчёте PoC связаны между собой.

### memory-eval-vector (completed, 8.7s, 3 tool calls)
queries: ['На каком PoC и на каких цифрах основано решение «Relay moves to Lambda with prov', 'Relay moves to Lambda with provisioned concurrency on /deliv PoC цифры', 'decision Relay moves to Lambda with provisioned concurrency on /deliv evidence P']

Решение основано на **PoC-3**.

Что именно было в цифрах:
- **p95 1.9 s** с provisioned concurrency на `/deliver`  
- **p95 3.4 s** без provisioned concurrency  
- **Monthly cost $3,600**, что **на 41% ниже EKS**  
- В ADR также указано, что **within the 2 s SLO only with provisioned concurrency; without it the SLO is missed**

Источники:
- **adr/ADR-006.md**, updated **2026-08-05** — решение: “Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances.”
- **docs/poc-lambda-report.md**, updated **2026-07-24** — таблица результатов PoC-3: p95 1.9 s, 3.4 s без provisioned concurrency, cost $3,600 (-41% vs EKS)
- **docs/poc-lambda-report.md**, updated **2026-07-24** — assessment: “Within the 2 s SLO only with provisioned concurrency; without it the SLO is missed.”
- **meetings/2026-08-03-architecture-committee.txt**, date **2026-08-03** — decision claim: “Based on poc-3.”

Если хотите, я могу ещё отдельно выписать, чем **PoC-2** отличался от **PoC-3** по цифрам.

## t40 [ru / poc_basis] На каком PoC и на каких цифрах основано решение «Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but …»?
**expected:** PoC-2: Relay on EKS with autoscaling: {"p95_s": 0.4, "monthly_cost_usd": 6100, "ops_effort": "a second platform team"}; report docs/poc-eks-report.md  
**expected sources:** {'sources': ['docs/poc-eks-report.md', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 5.6s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'Keep Relay on ", '"Keep Relay on EKS with autoscaling" PoC p95 0.4 s numbers results', '"Keep Relay on EKS with autoscaling" ПоC цифры p95 0.4 с результаты']

Решение основано на **PoC-2: Relay on EKS with autoscaling**.

Цифры и выводы из памяти:
- **p95 latency:** **0.4 s**
- **monthly cost at current volume:** **$6,100**
- **scale-out to 3x volume:** **90 s**
- **operations burden:** **“a second cluster: upgrades, node images, Karpenter, 24/7 on-call”**

Именно это и легло в формулировку решения:  
**“rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run”**

Источник:
- `docs/poc-eks-report.md` — **2026-07-24**
- `adr/ADR-007.md` — **2026-08-05**
- решение: `meetings/2026-08-03-architecture-committee.txt` — **2026-08-03**

Если хотите, могу ещё коротко показать, **как именно p95 0.4 s сравнили с ценой Lambda/другими PoC**.

### memory-eval-graph (completed, 4.6s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(c:PoC)\nWHERE d.text STARTS WITH 'Keep Relay on "]

Решение основано на **PoC-2: Relay on EKS with autoscaling**.

Цифры и вывод из PoC:
- **p95 = 0.4 s**
- **monthly_cost_usd = 6100**
- **ops_effort = "a second platform team"**

Источник решения:
- `meetings/2026-08-03-architecture-committee.txt`, **2026-08-03**
- Текст решения: `Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)`

Источник PoC:
- `docs/poc-eks-report.md`
- `c.results` = `{"p95_s": 0.4, "monthly_cost_usd": 6100, "ops_effort": "a second platform team"}`

Если хотите, могу ещё показать, **какое именно решение это заменило или с чем сравнивали EKS vs Lambda**.

### memory-eval-vector (completed, 10.0s, 3 tool calls)
queries: ['На каком PoC и на каких цифрах основано решение «Keep Relay on EKS with autoscal', 'Keep Relay on EKS with autoscaling rejected p95 0.4 s PoC цифры', 'Relay on EKS autoscaling rejected p95 0.4 s PoC']

Решение основано на **PoC-2**.

Что есть в памяти по цифрам:

- **PoC-2 report: Relay on EKS** — `docs/poc-eks-report.md`, обновлён **2026-07-24**:
  - delivery latency **p95 = 0.4 s**
  - delivery latency **p99 = 0.9 s**
  - monthly cost at current volume **$6,100**
  - scale-out to 3x volume: **90 s**
  - operations: нужен **second cluster** с upgrades, node images, Karpenter, 24/7 on-call

- **ADR-007: Keep Relay on EKS with autoscaling** — `adr/ADR-007.md`, обновлён **2026-08-05**:
  - решение сформулировано как: **“rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run”**

- **Meeting / claim D18** — `meetings/2026-08-03-architecture-committee.txt`, дата **2026-08-03**:
  - прямо сказано: **“Based on poc-2”**
  - то же решение: **rejected**
  - те же аргументы: **p95 0.4 s**, **1.7x the monthly cost**, **a second platform to run**

Итого:  
решение опирается на **PoC-2**, где ключевые числа — **p95 0.4 s** и **monthly cost $6,100**, а в самом решении это сведено к сравнению с альтернативой: **1.7x monthly cost** и **вторая платформа/кластер в эксплуатации**.

Если хотите, могу ещё отдельно вытащить, **с чем именно сравнивали 1.7x** и откуда взялась эта проп

## t41 [en / adr_status] What is the status of ADR-001 ('Migrate infrastructure code from Terraform to CloudFormation')?
**expected:** Superseded, superseded by ADR-004  
**expected sources:** {'sources': ['adr/ADR-001.md']}

### memory-eval-both (completed, 3.4s, 3 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-001'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (a:ADR {id:'ADR-001'})-[:SUPERSEDES]->(sup:ADR) RETURN a.id, a.status, sup", 'ADR-001 Migrate infrastructure code from Terraform to CloudFormation status supe']

ADR-001 is **Superseded**.  
Source: `adr/ADR-001.md`, updated `2026-01-14`.

It is superseded by **ADR-004**. Source text says: “Superseded (superseded by ADR-004)”.

### memory-eval-graph (completed, 5.1s, 3 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-001'}) RETURN a.id, a.title, a.status, a.file", "MATCH (a:ADR {id:'ADR-001'})-[:SUPERSEDES]->(b:ADR) RETURN b.id, b.title, b.stat", "MATCH (x:ADR)-[:SUPERSEDES]->(a:ADR {id:'ADR-001'}) RETURN x.id, x.title, x.stat"]

ADR-001 is **Superseded**.  
Source: `adr/ADR-001.md` — ADR-001 “Migrate infrastructure code from Terraform to CloudFormation” has status **Superseded** as of the record in memory.

The ADR that supersedes it is ADR-004, “Hybrid IaC: Terraform for networking, CloudFormation for application stacks,” dated **2026-04-22** in `adr/ADR-004.md`.

### memory-eval-vector (completed, 4.8s, 3 tool calls)
queries: ["What is the status of ADR-001 ('Migrate infrastructure code from Terraform to Cl", 'ADR-001 Migrate infrastructure code from Terraform to CloudFormation status', 'status ADR-001 Terraform CloudFormation']

ADR-001 is **Superseded (superseded by ADR-004)**. Source: `adr/ADR-001.md` (updated **2026-01-14**). The ADR header explicitly says “Status: Superseded (superseded by ADR-004)”.

I also found ADR-004, which is **Accepted, supersedes ADR-001** in `adr/ADR-004.md` (updated **2026-04-22**). Since it is newer, ADR-004 is the current decision on this topic.

## t42 [en / adr_status] What is the status of ADR-005 ('Evaluate EKS and Lambda with two proofs of concept')?
**expected:** Superseded, superseded by ADR-006  
**expected sources:** {'sources': ['adr/ADR-005.md']}

### memory-eval-both (completed, 3.1s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-005'}) RETURN a.id, a.title, a.status, a.date, a.file"]

ADR-005 is **Superseded**.

- **ADR-005**: “Evaluate EKS and Lambda with two proofs of concept”
- **Status**: Superseded
- **Date**: 2026-06-17
- **Source file**: `adr/ADR-005.md`

If you want, I can also tell you what superseded it or what is currently live on that topic.

### memory-eval-graph (completed, 5.2s, 3 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-005'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (a:ADR {id:'ADR-005'})-[:SUPERSEDES]->(b:ADR) RETURN b.id, b.title, b.stat", "MATCH (d:Decision)-[:RECORDED_IN]->(a:ADR {id:'ADR-005'}) RETURN d.text, d.date,"]

ADR-005 is **Superseded**.

- **ADR-005** — “Evaluate EKS and Lambda with two proofs of concept”  
  **Status:** Superseded  
  **Date:** 2026-06-17  
  **Source file:** `adr/ADR-005.md`

The live decision recorded in that ADR’s topic area is:
- **Decision:** “Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July”  
  **Status:** superseded  
  **Date:** 2026-06-15  
  **Source file:** `meetings/2026-06-15-weekly-sync.txt`

I did not find a successor ADR linked by `SUPERSEDES` for ADR-005 in memory.

### memory-eval-vector (completed, 3.1s, 3 tool calls)
queries: ["What is the status of ADR-005 ('Evaluate EKS and Lambda with two proofs of conce", 'ADR-005 Evaluate EKS and Lambda with two proofs of concept status', 'status of ADR-005 Evaluate EKS and Lambda with two proofs of concept']

ADR-005 is **Superseded (superseded by ADR-006)**.

Sources:
- `adr/ADR-005.md`, updated **2026-06-17**: status line says **“Superseded (superseded by ADR-006)”**.
- `adr/ADR-005.md`, updated **2026-06-17**: the ADR header and decision chunks also show the same superseded status.

I did not find any newer non-superseded status for ADR-005 in memory.

## t43 [en / adr_status] What is the status of ADR-007 ('Keep Relay on EKS with autoscaling')?
**expected:** Rejected  
**expected sources:** {'sources': ['adr/ADR-007.md']}

### memory-eval-both (completed, 3.4s, 2 tool calls)
queries: ['ADR-007 Keep Relay on EKS with autoscaling status', "MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.date, a.file"]

ADR-007 is **Rejected**.

- **Source:** `adr/ADR-007.md`
- **Date:** `2026-08-05`

The ADR record says:
- `ADR-007`
- title: `Keep Relay on EKS with autoscaling`
- status: `Rejected`

### memory-eval-graph (completed, 2.7s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.file"]

ADR-007 is **Rejected**. Source: `adr/ADR-007.md`, dated `not in memory for the ADR file date` — the graph returns `ADR-007`, title `Keep Relay on EKS with autoscaling`, status `Rejected`.

### memory-eval-vector (completed, 3.9s, 3 tool calls)
queries: ["What is the status of ADR-007 ('Keep Relay on EKS with autoscaling')?", 'ADR-007 Keep Relay on EKS with autoscaling status', 'status ADR-007 Keep Relay on EKS autoscaling']

ADR-007 is **Rejected**. The ADR record shows **Status: Rejected** and **Date: 2026-08-05**. Source: `adr/ADR-007.md` (updated 2026-08-05).

I also found a supporting decision chunk stating “Keep Relay on EKS with autoscaling (rejected…)” in `adr/ADR-007.md` (updated 2026-08-05).

## t44 [en / adr_status] What is the status of ADR-010 ('Gateway timeout policy for Lambda integrations')?
**expected:** Proposed; Never accepted; D20 (25 s) is the live decision and the ADR still proposes 20 s  
**expected sources:** {'sources': ['adr/ADR-010.md']}

### memory-eval-both (completed, 2.5s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.date, a.file"]

ADR-010 is **Proposed**.

Source: `adr/ADR-010.md`, dated **2026-09-23**.

### memory-eval-graph (completed, 2.4s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.date, a.file"]

ADR-010 is **Proposed**. Source: `adr/ADR-010.md`, dated `2026-09-23`.

### memory-eval-vector (completed, 4.5s, 3 tool calls)
queries: ["What is the status of ADR-010 ('Gateway timeout policy for Lambda integrations')", 'ADR-010 Gateway timeout policy for Lambda integrations status', 'status ADR-010 Gateway timeout policy for Lambda integrations']

ADR-010 is **Proposed**. The ADR document shows:

- **Status: Proposed** in `adr/ADR-010.md` (updated **2026-09-23**)
- It also says **“No decision recorded; see Status.”** in the Decision section of the same file (**2026-09-23**)

One chunk adds that it is **“Proposed, not accepted”** and notes the live decision is elsewhere, but the ADR itself remains **Proposed**.

Sources:
- `adr/ADR-010.md` — **2026-09-23** — Status section: Proposed
- `adr/ADR-010.md` — **2026-09-23** — Decision section: No decision recorded; see Status
- `adr/ADR-010.md` — **2026-09-23** — Consequences section: Proposed, not accepted

## t45 [en / dependency] What did the decision 'Front Relay with the API gateway; the gateway and its routes…' depend on?
**expected:** One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway) (2026-02-09)  
**expected sources:** {'sources': ['meetings/2026-02-09-weekly-sync.txt', 'meetings/2026-03-02-weekly-sync.txt']}

### memory-eval-both (completed, 35.7s, 4 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Front Relay with the API gateway; t", '"Front Relay with the API gateway; the gateway and its routes" depend on decisio', 'Front Relay with the API gateway gateway routes depended on', "MATCH (d:Decision) WHERE d.text STARTS WITH 'Front Relay with the API gateway; t"]

The decision depended on:

- **One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)**  
  - **Date:** 2026-02-09  
  - **Source:** `meetings/2026-02-09-weekly-sync.txt`

That dependency was attached to the decision:

- **Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack**  
  - **Date:** 2026-03-02  
  - **Source:** `meetings/2026-03-02-weekly-sync.txt`



### memory-eval-graph (completed, 4.0s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Front Relay with the API gateway; t", "MATCH (d:Decision) WHERE d.text STARTS WITH 'Front Relay with the API gateway; t"]

The decision **“Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack”** depended on:

- **“One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)”**  
  - **Date:** 2026-02-09  
  - **Status:** active  
  - **Source:** `meetings/2026-02-09-weekly-sync.txt`

This is the only dependency linked to that decision in memory.

### memory-eval-vector (completed, 4.5s, 3 tool calls)
queries: ["What did the decision 'Front Relay with the API gateway; the gateway and its rou", 'Front Relay with the API gateway; the gateway and its routes', 'decision Front Relay with the API gateway gateway routes depend on']

The decision “Front Relay with the API gateway; the gateway and its routes…” depended on the context/requirements in ADR-002:

- callers were reaching Relay through an internal load balancer with a shared API key,
- the team wanted authentication per caller,
- per-route timeouts and retries,
- and one place to see traffic,
- plus the account’s API gateway already fronted two other services.

Source: `adr/ADR-002.md` — Context section, updated `2026-03-04`.

I also found the decision itself and the chosen option:
- `adr/ADR-002.md` — Decision section, updated `2026-03-04`
- `adr/ADR-002.md` — Options considered section, updated `2026-03-04`

If you want, I can also quote the exact supporting lines from the ADR.
