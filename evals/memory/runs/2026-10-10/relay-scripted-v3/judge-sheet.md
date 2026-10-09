
## m01 [en / fact] What is the delivery latency SLO and what exactly does it measure?
**expected:** p95 2 s over 5 minutes, from POST /deliver accepted to the first delivery attempt sent, not to the customer's answer; success rate 99.5% monthly  
**expected sources:** {'sources': ['docs/slo.md', 'meetings/2026-01-26-weekly-sync.txt']}

### memory-eval-both (completed, 3.9s, 2 tool calls)
queries: ['delivery latency SLO what exactly does it measure delivery latency defined as me', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

The delivery latency SLO is:

- **p95 of 2 s** over a **5-minute window**  
  **Source:** `docs/slo.md` — updated **2026-01-28**

What it measures:
- It measures **Relay’s latency from `POST /deliver` being accepted to the first delivery attempt being sent**.
- It **does not** measure the customer’s response time.
- In other words, the SLO ends when Relay sends the first attempt, **not** when the customer answers.

There is also a later decision:
- **2026-10-05** — delivery p95 SLO was **relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s**  
  **Source:** `meetings/2026-10-05-cutover-planning.txt`

If you want, I can also give the matching delivery success SLO from the same document.

### memory-eval-graph (completed, 6.1s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE d.text CONTAINS 'd", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE d.text CONTAINS 'e", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE d.date <= '2026-10"]

The current delivery latency SLO is:

- **p95 delivery latency: 3 seconds for 30 days after the serverless cutover, then back to 2 seconds**  
  Source: `meetings/2026-10-05-cutover-planning.txt`  
  Date: `2026-10-05`

What it measures:

- The earlier decision spells it out as **“p95 end-to-end delivery latency”**.  
  Source: `meetings/2026-01-26-weekly-sync.txt`  
  Date: `2026-01-26`

So, in memory, this SLO measures **end-to-end delivery latency at the 95th percentile**. The current decision only states the relaxed threshold and the 30-day post-cutover window; it does not redefine the metric itself.

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

### memory-eval-both (completed, 3.9s, 2 tool calls)
queries: ['очередь до dead-letter сколько попыток доставки делает и с какими задержками ret', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.date <= '202"]

Очередь делает **5 попыток** доставки, после чего сообщение уходит в **dead-letter queue**.

Задержки между redrive-попытками:
- **30 s**
- **2 min**
- **10 min**
- **30 min**
- **2 h**

Источник: `docs/retries-dlq.md`, обновлено **2026-08-27**.  
Подтверждающее решение: `meetings/2026-08-24-weekly-sync.txt`, **2026-08-24**.

### memory-eval-graph (completed, 4.1s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.text CONTAIN"]

Очередь делает **5 попыток** до попадания в dead-letter queue; в найденном решении **задержки между попытками не указаны**.

Источник: `meetings/2026-08-24-weekly-sync.txt`, решение от `2026-08-24`:
- “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”

Если хотите, я могу ещё проверить, есть ли в памяти отдельное решение про **backoff / retry delays** для этой очереди.

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

### memory-eval-both (completed, 3.6s, 2 tool calls)
queries: ['Why does the hybrid IaC layout keep networking in Terraform? networking Terrafor', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.text CONTAINS 'n"]

Because the current decided boundary is that networking stays in Terraform while application stacks move to CloudFormation.

Sources:
- `meetings/2026-04-20-weekly-sync.txt` — 2026-04-20: “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation”
- `adr/ADR-004.md` — 2026-04-22: “Hybrid: networking stays in Terraform, application stacks in CloudFormation (chosen)”

The remembered rationale in the docs is that the hybrid layout is the chosen boundary, but I don’t have a more detailed why beyond that from memory.

### memory-eval-graph (completed, 3.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.text CONTAINS 'n"]

Because the hybrid IaC decision keeps networking where the existing Terraform estate already is, while moving application stacks to CloudFormation: “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation” (meetings/2026-04-20-weekly-sync.txt, 2026-04-20, active).

The linked note says the docs were still stale and incorrectly claimed “all infrastructure including networking moves to CloudFormation” (docs/iac-cloudformation.md, updated 2026-02-11), so the decision corrects that.

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['Why does the hybrid IaC layout keep networking in Terraform?', 'hybrid IaC layout keep networking in Terraform', 'networking in Terraform hybrid IaC layout']

The memory says **networking stays in Terraform because ADR-004 fixed the hybrid boundary**: VPC, peering, and DNS are kept in Terraform, while data/compute/gateway application stacks move to CloudFormation. The recorded consequence is that **both sides run drift detection**, and Terraform state was cleaned of resources already imported into stacks. Source: **adr/ADR-004.md** and **meetings/2026-04-20-weekly-sync.txt** (2026-04-22, 2026-04-20).

There is also a hand-off reason in the docs: Terraform exports network outputs to SSM Parameter Store, and CloudFormation reads them with dynamic references; changing a network output requires a Terraform apply and then a CloudFormation deploy, with no automatic trigger. Source: **docs/iac-hybrid.md** (2026-04-24).

If you want, I can also summarize the **full hybrid layout boundary** from memory.

## m04 [ru / contradiction] В gateway.md написано, что таймаут интеграции 10 секунд. Это актуально?
**expected:** нет; документ от 2026-03-18, таймаут менялся на 30 с (2026-05-18) и на 25 с (2026-08-24); текущее значение 25 с  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 5.9s, 2 tool calls)
queries: ["MATCH (doc:Document {file:'gateway.md'}) OPTIONAL MATCH (dec:Decision)-[s:MAKES_", 'gateway.md timeout integration 10 seconds актуально current stale decision timeo']

Да, в памяти это актуально.

Что найдено:
- `docs/gateway.md` — `updated 2026-03-18`
- Векторный фрагмент из этого документа говорит: **“The integration timeout on every Relay route is 10 seconds”** и помечает это как **decided 2026-03-16**.
- Я не нашёл в графе более позднего решения, которое бы делало этот факт stale для `gateway.md`.

Итого: **да, 10 секунд — актуально**.  
Источник: `docs/gateway.md`, дата обновления `2026-03-18`; подтверждающий фрагмент памяти датирован `2026-03-18`.

### memory-eval-graph (completed, 3.4s, 1 tool calls)
queries: ["MATCH (doc:Document {file:'gateway.md'}) OPTIONAL MATCH (dec:Decision)-[s:MAKES_"]

Не могу подтвердить, что это актуально: для `gateway.md` в памяти нет данных о документе и, соответственно, не найдено решений, которые помечают его устаревшим.

Что удалось проверить:
- `gateway.md` не вернулось в графе как документ с датой обновления.
- Не нашлось решений `MAKES_STALE`, которые указывали бы, что этот документ устарел.

Источник: память графа Relay; дата документа и решений не доступны, потому что запись для `gateway.md` не найдена.

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

### memory-eval-both (completed, 4.6s, 2 tool calls)
queries: ["MATCH (p:Person {key:'person:anna-sokolova'})-[o:OWNS]->(t:Topic {key:'topic:ret", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) RETURN p.name, o.from"]

No. Today, Anna does not own retries.

Ownership history for **topic:retries**:
- **Anna Sokolova** owned it from **2026-06-01** to **2026-09-07**.
- **Ivan Melnik** owns it now, from **2026-09-07** onward.

Source: graph ownership edges for `topic:retries` (no document file).

### memory-eval-graph (completed, 3.7s, 2 tool calls)
queries: ["MATCH (p:Person {key:'person:anna-sokolova'})-[o:OWNS]->(t:Topic {key:'topic:ret", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) RETURN p.name, o.from"]

No — Anna does **not** own retries today.

The current owner of **topic:retries** is **Ivan Melnik**, from **2026-09-07** onward; Anna owned it only from **2026-06-01** to **2026-09-07**.  
Source: graph ownership edges for **topic:retries**; retrieved via query results, no document file applies here.

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['The team roster page says Anna owns retries. Is that right today?', 'Anna owns retries', 'retries owner Anna']

No — Anna does **not** own retries today. The current decision says **Ivan Melnik** owns retries from **2026-09-07**. Source: **meetings/2026-09-07-security-review.txt** (2026-09-07).

The team roster page is stale on this point: it still lists **Anna Sokolova** as retries owner, but it was updated on **2026-07-08**, and the newer ownership decision supersedes it. Source: **confluence/team-roster.xhtml** (2026-07-08) and **meetings/2026-09-07-security-review.txt** (2026-09-07).

## m06 [ru / contradiction] Decision log в Confluence актуален?
**expected:** нет; последняя версия 2026-06-03, в нём нет решений после 1 июня: ретраи на gateway (06-15), два PoC (06-15), передача PoC Ване (07-13), выбор Lambda (08-03), таймаут 25 с и ретраи через SQS (08-24), SSM (09-07), бюджет (09-21), даты катовера (10-05)  
**expected sources:** {'sources': ['confluence/decision-log.xhtml', 'memory/decisions.jsonl']}

### memory-eval-both (input-required, 0.9s, 1 tool calls)
queries: ["{'questions': [{'multiple': False, 'question': 'Какой именно файл/страницу из de"]



### memory-eval-graph (completed, 5.9s, 2 tool calls)
queries: ["MATCH (doc:Document) WHERE toLower(doc.title) CONTAINS 'decision log' OR toLower", "MATCH (doc:Document {file:'confluence/decision-log.xhtml'}) OPTIONAL MATCH (dec:"]

Нет, **decision log в Confluence уже не актуален**.

Он был обновлён **2026-06-03** (`confluence/decision-log.xhtml`), но после этого в памяти есть решения с более поздними датами, которые он не учитывает, например:

- **D14** — `Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%` — **2026-06-15** — `meetings/2026-06-15-weekly-sync.txt`
- **D17** — `Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances` — **2026-08-03** — `meetings/2026-08-03-architecture-committee.txt`
- **D25** — `Serverless cutover on 2026-10-19 at 09:00 local, inside the planned-work error budget` — **2026-10-05** — `meetings/2026-10-05-cutover-planning.txt`

Итого: документ **устарел**, потому что есть более поздние решения после его даты обновления.

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

### memory-eval-both (completed, 3.6s, 2 tool calls)
queries: ['ADR-010 gateway timeout Lambda 20 s policy', "MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.file"]

No — in memory, ADR-010 is **Proposed**, not accepted policy.

- **Source:** `adr/ADR-010.md`
- **Date:** `2026-09-23`
- The ADR itself says: **“Proposed, not accepted. The live value was set by the team on 2026-08-24 at 25 s; this document still says 20 s.”**
- The graph also shows ADR-010 status as **Proposed**.

So **20 s is not the policy in force**.

### memory-eval-graph (completed, 5.9s, 3 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (d:Decision)-[:RECORDED_IN]->(a:ADR {id:'ADR-010'}) RETURN d.text, d.date,", "MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway timeout policy for Lambda i"]

I can’t confirm that as policy from memory.

What I retrieved:
- ADR-010 is **“Gateway timeout policy for Lambda integrations”** with status **Proposed**, dated **2026-09-23**, file **adr/ADR-010.md**.
- I did **not** find any decision recorded in that ADR, and I did **not** find a decision text matching that ADR title.

So, based on the graph memory, **“20 s” is not established as the policy**. The only thing I can say from memory is that ADR-010 exists as a proposed ADR, not an accepted policy, per **adr/ADR-010.md (2026-09-23)**.

If you want, I can look for the current gateway timeout decision under the **timeouts** topic and tell you the in-force policy with source and date.

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

### memory-eval-both (completed, 4.9s, 2 tool calls)
queries: ['runbook cutover rollback owner TBD who is the actual owner', "MATCH (p:Person)-[o:OWNS]->(oi:OpenItem {id:'O2'}) WHERE o.from <= '2026-09-29' "]

На самом деле владелец отката — **Lena Kim**.

- В памяти есть запись, что в runbook ещё стоит “TBD”, но решение по катоверу назначило владельца отката на Lena.
- Для open item по rollback runbook владелец указан с **2026-09-21** и на **2026-09-29** это уже Lena Kim.

Источники:
- `meetings/2026-10-05-cutover-planning.txt` — 2026-10-05
- `meetings/2026-08-24-weekly-sync.txt` — 2026-08-24

### memory-eval-graph (input-required, 6.5s, 5 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.text CONTAIN", "MATCH (o:OpenItem)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE o.text CONTAIN", "MATCH (d:Decision)-[:MAKES_STALE]->(doc:Document) WHERE doc.file CONTAINS 'runbo", "MATCH (doc:Document) WHERE doc.file CONTAINS 'runbook' RETURN doc.file, doc.upda", "{'questions': [{'choices': ['docs/runbook-cutover-serverless.md', 'docs/runbook-"]



### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['В runbook катовера написано, что владелец отката TBD. Кто на самом деле?', 'runbook катовера владелец отката TBD кто владелец', 'rollback owner cutover runbook TBD who owns rollback']

На самом деле владелец отката — **Lena Kim**. Это зафиксировано в решении от **2026-10-05**: “Rollback owner for both cutovers is Lena. Owner: Lena Kim.”  
Источник: `meetings/2026-10-05-cutover-planning.txt` — **2026-10-05**.

Замечание: runbook с `TBD` уже устарел по сравнению с этим решением. В найденных материалах runbook `docs/runbook-cutover-serverless.md` упомянут как обновлённый **2026-09-29**, но решение новее.

## m09 [ru / crosslingual] Что на митингах называли «провижнд конкаренси» и почему без этого не проходит SLO?
**expected:** provisioned concurrency: прогретые инстансы Lambda на /deliver; без них p95 3.4 с при SLO 2 с, с ними 1.9 с (PoC-3)  
**expected sources:** {'sources': ['docs/poc-lambda-report.md', 'meetings/2026-07-27-poc-review.txt', 'adr/ADR-006.md']}

### memory-eval-both (completed, 5.6s, 2 tool calls)
queries: ['«провижнд конкаренси» SLO митинг why without it SLO not met Relay webhook delive', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE d.text STARTS "]

На митингах под «провижнд конкаренси» имели в виду **provisioned concurrency для `/deliver`** — то есть это было условие для Lambda-варианта Relay, а не просто оптимизация.

Почему без него не проходит SLO:
- в PoC review сказали: **«без этого не проходим»**;
- в отчёте по PoC-3 и в ADR-006 зафиксировано: **в пределах 2 s SLO Relay укладывается только с provisioned concurrency; без него SLO нарушается**;
- SLO здесь про **первую попытку доставки**, а не про ответ клиента, поэтому речь именно о latency на `/deliver`.

Источник:
- `meetings/2026-07-27-poc-review.txt` — 2026-07-27
- `docs/poc-lambda-report.md` — 2026-07-24
- `adr/ADR-006.md` — 2026-08-05

Если хотите, я могу ещё кратко собрать **буквальную цитату с таймкодом** и **связать это с решением/ADR**, которое это закрепило.

### memory-eval-graph (completed, 7.4s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE d.text CONTAINS 'S"]

На митингах под «провижнд конкаренси» имели в виду **Lambda с provisioned concurrency на `/deliver`**. В графе есть решение:

- **«Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances»** — `meetings/2026-08-03-architecture-committee.txt`, **2026-08-03**.

Почему без этого «не проходит SLO»: в памяти есть SLO по доставке:

- **«Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%»** — `meetings/2026-01-26-weekly-sync.txt`, **2026-01-26**.
- Позже он был временно смягчён:
  - **«Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s»** — `meetings/2026-10-05-cutover-planning.txt`, **2026-10-05**.

Из этого в памяти следует только то, что provisioned concurrency связывали с warm instances и p95 1.9 s, то есть с укладыванием в latency SLO. Но **прямой формулировки “почему без этого не проходит SLO” в графе нет**, поэтому точнее сказать: в памяти есть связь, что без warm instances p95 было бы хуже, а SLO требовал 2 s или позже 3 s на переходный период.

Если хотите, я могу ещё показать все связанные решения и где и

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

### memory-eval-both (completed, 7.6s, 5 tool calls)
queries: ['дрифт meaning team discussion rule came out of it Relay webhook delivery', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:database'}) WHERE d.text STARTS", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:ownership'}) WHERE d.text START", "MATCH (d:Decision) WHERE d.text STARTS WITH 'не видим дрифт' OR d.text STARTS WI", 'дрифт means rule came out of it nightly drift detection no manual changes in con']

Под «дрифт» команда имела в виду расхождение между тем, что описано в шаблоне/конфигурации, и тем, что реально изменили руками в консоли. Это всплыло после инцидента, когда ручное изменение таймаута на балансере разошлось с реальностью и ночной деплой потом откатил изменение.

Правило, которое из этого вывели:
- ручные изменения в проде запрещены;
- включить ночной drift detection на всех стеках;
- алерты должны уходить в on-call.

Источник:
- `meetings/2026-02-23-incident-review.txt` — 2026-02-23
- `docs/drift-detection.md` — updated 2026-02-25

Если хотите, я могу ещё показать, кто это предложил и кто владеет этим правилом.

### memory-eval-graph (completed, 5.6s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.text CONTAINS 'д", "MATCH (d:Decision)-[:ABOUT]->(:Topic) WHERE d.text CONTAINS 'дрифт' OR d.text CO", "MATCH (o:OpenItem) WHERE o.text CONTAINS 'дрифт' OR o.text CONTAINS 'drift' RETU", "MATCH (d:Decision)-[:ABOUT]->(t:Topic) WHERE t.name CONTAINS 'drift' OR t.name C"]

By “дрифт” the team meant infrastructure drift: manual console changes diverging from the declared stack state. The rule that came out of it was: **manual console changes are frozen, and nightly drift detection must run on every stack with alerts sent to on-call**.

Sources:
- `meetings/2026-02-23-incident-review.txt` — decision dated `2026-02-23`: “Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call”
- `meetings/2026-02-23-incident-review.txt` — open item dated `2026-02-23`: “Route drift-detection alerts to on-call” (`O8`, later closed)



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

### memory-eval-both (completed, 7.2s, 2 tool calls)
queries: ['gateway retries /deliver turned off in August turned on in June why rationale de', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.text STARTS "]

The memory does not show a June decision to turn gateway retries on for `/deliver`; what it does show is that retries on `POST /deliver` were disabled because the delivery was not idempotent yet, and a retried request could reach a customer twice.

Relevant records:
- `docs/idempotency.md` — updated `2026-05-20`: “Gateway retries on `/deliver` were disabled on `2026-03-30` because a retried delivery could reach a customer twice. Once every caller sends keys, retries can be enabled at the gateway with a limit and a budget set in the gateway policy.”
- `adr/ADR-002.md` — updated `2026-03-04`, status `Accepted`: “Retries are disabled on POST /deliver until idempotency keys exist, because a retried delivery can reach a customer twice. Read routes may retry twice. When retries are enabled they will be governed by a retry budget set in the gateway policy.”
- `adr/ADR-009.md` — updated `2026-08-26`, status `Accepted`: “Retries in SQS with a dead-letter queue after 5 attempts; gateway retries off on /deliver (chosen).”

So the reason in memory is: retries were turned off because `/deliver` was not idempotent and could duplicate deliveries; by August, the chosen approach was to keep gateway

### memory-eval-graph (completed, 6.3s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.date <= '202", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'}) WHERE d.date <= '202"]

Gateway retries on `/deliver` were turned off in August because the retry responsibility was moved out of the gateway and into SQS with a dead-letter queue after 5 attempts.

What the graph shows:
- On 2026-06-15, retries were enabled at the gateway for `POST /deliver`: “max 3 attempts, retry budget 15%” — source `meetings/2026-06-15-weekly-sync.txt`.
- On 2026-08-24, that decision was replaced by: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off” — source `meetings/2026-08-24-weekly-sync.txt`.

So the August change was a move to queue-based retries rather than gateway-based retries.

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

### memory-eval-both (completed, 7.5s, 2 tool calls)
queries: ['сеть осталась в Terraform why, chain of events, Terraform network remained in Te', 'MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision) WHERE (cur)-[:ABOUT']

Цепочка такая:

1. **Сначала решили полностью мигрировать инфраструктуру из Terraform в CloudFormation**.  
   - **D01** — “Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1”  
   - Дата: **2026-01-12**  
   - Статус: **superseded**  
   - Источник: **meetings/2026-01-12-weekly-sync.txt**

2. **Потом это решение пересмотрели и зафиксировали гибридный вариант**:  
   - **D09** — “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation”  
   - Дата: **2026-04-20**  
   - Статус: **active**  
   - Источник: **meetings/2026-04-20-weekly-sync.txt**

То есть сеть осталась в Terraform потому, что более позднее решение **D09** сузило миграцию: **сетевой слой (VPC, peering, DNS) оставили в Terraform**, а в CloudFormation перенесли только прикладные стеки.

Если кратко по цепочке влияния:
- **D01**: планировали перенести всё.
- **D09**: позже приняли гибридный подход и **сетевую часть оставили в Terraform**.

Источник для формулировки причины: **ADR-004 / D09**, дата **2026-04-20**; в vector store также зафиксировано, что это решение **supersedes D01** и было с возражением Паши Гришина.

### memory-eval-graph (completed, 11.2s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.text CONTAINS 'T", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.date <= '2026-04", 'MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision) WHERE (cur)-[:ABOUT', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (a:Person"]

Цепочка в памяти такая:

1. **2026-01-12** — решили мигрировать инфраструктурный код Relay **с Terraform на CloudFormation** по модулям, с завершением к концу Q1.  
   Источник: `meetings/2026-01-12-weekly-sync.txt`  
   Решение: D01 — `Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1`

2. **2026-02-09** — уточнили целевую схему: **один root stack CloudFormation на окружение** и nested stacks по компонентам, включая **network**.  
   Источник: `meetings/2026-02-09-weekly-sync.txt`  
   Решение: D03 — `One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)`

3. **2026-04-20** — после этого общий курс изменили на **гибридный IaC**: **сеть (VPC, peering, DNS) остаётся в Terraform**, а application stacks идут в CloudFormation. Это и есть текущая причина, почему сеть осталась в Terraform.  
   Источник: `meetings/2026-04-20-weekly-sync.txt`  
   Решение: D09 — `Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation`

Дополнительно по связке решений:
- Текущая цепочка по теме IaC в памяти: **D09 → D01**.  
  Источники: `meetin

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

### memory-eval-both (completed, 8.1s, 3 tool calls)
queries: ['MATCH (o:OpenItem)<-[:CLOSES]-(d:Decision)\nWITH o, d\nORDER BY o.raised ASC\nWITH ', 'MATCH (o:OpenItem)<-[:CLOSES]-(d:Decision)\nWITH o, d\nORDER BY o.raised ASC\nLIMIT', 'MATCH (o:OpenItem)<-[:CLOSES]-(d:Decision)\nWITH o, d\nORDER BY o.raised ASC\nLIMIT']

The longest-standing open item that was closed is:

- Decision: “DynamoDB migration dry run on a production snapshot is owned by Sergey, due 2026-09-04”
- Date: 2026-08-10
- Status: active
- Source: `meetings/2026-08-10-weekly-sync.txt`

Open item:
- `O1` — “DynamoDB migration dry run on a production snapshot”
- Raised: 2026-05-04
- Raised again: 4 times (`2026-05-18`, `2026-06-15`, `2026-06-29`, `2026-07-20`)

Owner/taker:
- No owner could be resolved from the ownership edge at the decision date in memory.

If you want, I can also check whether this open item has a later ownership assignment that would explain the missing owner.

### memory-eval-graph (completed, 4.0s, 1 tool calls)
queries: ['MATCH (o:OpenItem)<-[:CLOSES]-(d:Decision)\nWITH o, d, size(coalesce(o.raised_aga']

The longest-standing open item that was closed was **O1, “DynamoDB migration dry run on a production snapshot”**, first raised on **2026-05-04** and raised again **4** times.  
It was closed by **D19, “DynamoDB migration dry run on a production snapshot is owned by Sergey, due 2026-09-04”** on **2026-08-10**. Source: **meetings/2026-08-10-weekly-sync.txt**.

So, in short:
- **Decision:** D19
- **Taken in / source:** **meetings/2026-08-10-weekly-sync.txt**
- **Closed open item:** O1
- **Raised again:** **4 times**

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

### memory-eval-both (completed, 5.0s, 2 tool calls)
queries: ['CloudFormation hybrid January objected against move to CloudFormation April hybr', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (p:Person"]

Против переезда на CloudFormation в январе возражал **Timur Aliev** — в записи от **2026-01-12** это решение про миграцию Terraform → CloudFormation помечено как **superseded**. Источник: `meetings/2026-01-12-weekly-sync.txt`.

В апреле, когда обсуждали **hybrid**, он уже **не возражал против гибридной схемы**: в силе была позиция **“Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation”** от **2026-04-20**, а затем она была зафиксирована в ADR-004. Источники: `meetings/2026-04-20-weekly-sync.txt` и `adr/ADR-004.md` (2026-04-22).

Если хотите, я могу ещё коротко показать цепочку: **январская позиция → февральские изменения → апрельский гибрид**.

### memory-eval-graph (completed, 6.3s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (b:Person", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (a:Person"]

Против переезда на CloudFormation в январе возражал **Тимур Алиев** — это видно в решении от **2026-01-12** из `meetings/2026-01-12-weekly-sync.txt`, где зафиксирован переход Terraform → CloudFormation; Тимур указан как возражавший к этому решению.

В апреле, когда обсуждали гибрид, он занял позицию **в поддержку гибридного IaC-подхода**: решение от **2026-04-20** в `meetings/2026-04-20-weekly-sync.txt` фиксирует, что **сетевой слой остаётся в Terraform, а application stacks — в CloudFormation**.

Если хотите, я могу ещё показать, **какое именно январское решение было позже superseded** и чем.

### memory-eval-vector (completed, 5.7s, 3 tool calls)
queries: ['Кто возражал против переезда на CloudFormation в январе и какую позицию он занял', 'возражал против переезда на CloudFormation в январе hybrid апрель позиция', 'January CloudFormation opposed April hybrid position']

В январе против переезда на CloudFormation возражал **Тимур Алиев**: в weekly sync от **2026-01-12** он сказал «я против, но не блокирую», и его возражение записали. Источник: `meetings/2026-01-12-weekly-sync.txt` (2026-01-12).

В апреле, когда обсуждали гибрид, в ADR-004 зафиксирована позиция **объединённая**: **сеть остаётся в Terraform, а application stacks — в CloudFormation**. Там же записано, что возражение было от **Pavel Grishin**. Источник: `adr/ADR-004.md` (2026-04-22).

Если вы имели в виду одного и того же человека, то в памяти есть несостыковка: январское возражение относится к Тимуру, а апрельское — к Павлу.

## m15 [en / point_in_time] On 2026-07-01, who owned retries, who owned the serverless PoC, and was the dry run owned?
**expected:** retries: Anna (since 06-01); serverless PoC: Sergey (until 07-13); dry run: no owner  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-06-29-weekly-sync.txt']}

### memory-eval-both (completed, 3.5s, 3 tool calls)
queries: ['MATCH (p:Person)-[o:OWNS]->(x {key:$retryKey}) WHERE o.from <= $d AND (o.to IS N', 'MATCH (p:Person)-[o:OWNS]->(x {key:$pocKey}) WHERE o.from <= $d AND (o.to IS NUL', 'MATCH (p:Person)-[o:OWNS]->(x {key:$dryRunKey}) WHERE o.from <= $d AND (o.to IS ']

On 2026-07-01:

- Retries was owned by **Anna Sokolova** from **2026-06-01** to **2026-09-07**. Source: ownership graph data.
- The serverless PoC was owned by **Ivan Melnik** from **2026-06-22** onward. Source: ownership graph data.
- The dry run was **owned** by **Denis Orlov** from **2026-04-06** onward. Source: ownership graph data.

If you want, I can also check whether the dry run here refers to a decision or a topic and give the exact object it maps to.

### memory-eval-graph (completed, 5.6s, 3 tool calls)
queries: ['MATCH (p:Person)-[o:OWNS]->(x {key:$retries}) WHERE o.from <= $d AND (o.to IS NU', 'MATCH (p:Person)-[o:OWNS]->(x {key:$poc}) WHERE o.from <= $d AND (o.to IS NULL O', 'MATCH (p:Person)-[o:OWNS]->(x {key:$dry}) WHERE o.from <= $d AND (o.to IS NULL O']

On 2026-07-01:

- **Retries** was owned by **Anna Sokolova** from **2026-06-01** to **2026-09-07**. Source: ownership edge in memory for `topic:retries` (no file field is stored on ownership edges), dated by the edge interval.
- **Serverless PoC** (`poc:poc-3`) was owned by **Ivan Melnik** from **2026-06-22** onward. Source: ownership edge in memory for `poc:poc-3` (no file field is stored on ownership edges), dated by the edge interval.
- **Dry run**: I found **no ownership record** for the dry run on 2026-07-01, so it was **unowned**. Source: no matching ownership edge in memory for `topic:cutover` on that date.



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

### memory-eval-both (completed, 4.8s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20"]

На 1 июля 2026 действовал таймаут **30 s** на gateway.

Владелец: **Pavel Grishin**.

Источник:
- `meetings/2026-05-18-weekly-sync.txt` — решение от `2026-05-18`: “Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14”
- Владелец по OWNS на `2026-07-01`: Pavel Grishin, с `2026-05-18` и без даты окончания.

### memory-eval-graph (completed, 7.1s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20", "MATCH (p:Person)-[o:OWNS]->(x {key:'topic:timeouts'}) WHERE o.from <= '2026-07-0", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20"]

На **1 июля 2026** в памяти есть решение по таймауту gateway:

- **Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14** — дата **2026-05-18**, статус **superseded**, источник **meetings/2026-05-18-weekly-sync.txt**.
- Владельцем этого решения на эту дату был **Pavel Grishin** — OWNS с **2026-05-18** и без даты окончания; источник тот же: **meetings/2026-05-18-weekly-sync.txt**.

Важно: это именно решение по таймауту gateway, которое действовало на 2026-07-01; в найденной записи оно уже помечено как **superseded**, но на указанную дату это была последняя найденная запись в силе до 1 июля.

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

### memory-eval-both (completed, 4.9s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:DECIDED_IN]->(m:Meeting {date:'2026-08-03'}) RETURN d.id, d", "MATCH (o:OpenItem)-[:RAISED_IN]->(m:Meeting {date:'2026-08-03'}) OPTIONAL MATCH "]

At the architecture committee on 2026-08-03, these decisions were made:

- D17: “Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances” — active  
  Source: `meetings/2026-08-03-architecture-committee.txt`  
  Date: 2026-08-03

- D18: “Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)” — rejected  
  Source: `meetings/2026-08-03-architecture-committee.txt`  
  Date: 2026-08-03

The open item raised there was:

- O6: “Provisioned concurrency sizing for /deliver” — raised 2026-08-03, status closed  
  Source: `meetings/2026-08-03-architecture-committee.txt`  
  Date: 2026-08-03



### memory-eval-graph (completed, 5.7s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:DECIDED_IN]->(m:Meeting {date:$date}) RETURN d.id, d.text, ', 'MATCH (o:OpenItem)-[:RAISED_IN]->(m:Meeting {date:$date}) RETURN o.id, o.text, o']

At the architecture committee on 2026-08-03, the decisions were:

- **D17** — “Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances” — **active**  
  Source: `meetings/2026-08-03-architecture-committee.txt`  
  Date: `2026-08-03`

- **D18** — “Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)” — **rejected**  
  Source: `meetings/2026-08-03-architecture-committee.txt`  
  Date: `2026-08-03`

The open item raised there was:

- **O6** — “Provisioned concurrency sizing for /deliver” — **closed**  
  Raised: `2026-08-03`  
  Raised again: `[]`  
  Source: `meetings/2026-08-03-architecture-committee.txt`



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

### memory-eval-both (completed, 6.3s, 1 tool calls)
queries: ['MATCH path=(cur:Decision)-[:SUPERSEDES*0..5]->(old:Decision) WHERE (cur)-[:ABOUT']

Политика ретраев менялась **2 раза** (всего 3 версии).

Шаги владения и решений:

1. **2026-03-30 — D07**  
   *«Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice»*  
   Статус: **superseded**  
   Источник: `meetings/2026-03-30-weekly-sync.txt`  
   Владелец на этом шаге: **в памяти графа для этого ответа не найдено**.

2. **2026-06-15 — D14**  
   *«Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%»*  
   Статус: **superseded**  
   Источник: `meetings/2026-06-15-weekly-sync.txt`  
   Владелец на этом шаге: **в памяти графа для этого ответа не найдено**.

3. **2026-08-24 — D21**  
   *«Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off»*  
   Статус: **active**  
   Источник: `meetings/2026-08-24-weekly-sync.txt`  
   Владелец на этом шаге: **в памяти графа для этого ответа не найдено**.

Я смог подтвердить цепочку изменений, но по владельцам именно этой политики на каждом шаге в графе ответ не извлёкся. Если хотите, я могу отдельно проверить владельцев по датам для `topic:retries`.

### memory-eval-graph (completed, 8.1s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) OPTIONAL MATCH (old:", 'MATCH (p:Person)-[o:OWNS]->(d:Decision) WHERE d.key IS NOT NULL AND (d)-[:ABOUT]']

Политика ретраев менялась **2 раза**: было **3 решения** по теме `topic:retries`, из них текущее и два предыдущих.  
Источники: `meetings/2026-03-30-weekly-sync.txt` (2026-03-30), `meetings/2026-06-15-weekly-sync.txt` (2026-06-15), `meetings/2026-08-24-weekly-sync.txt` (2026-08-24).

По шагам владение было такое:

1. **2026-03-30** — `D07`: “Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice”  
   Владелец: **Nikita Frolov**.  
   Источник: `meetings/2026-03-30-weekly-sync.txt` (2026-03-30)

2. **2026-06-15** — `D14`: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%”  
   Владелец: **Anna Sokolova**.  
   Источник: `meetings/2026-06-15-weekly-sync.txt` (2026-06-15)

3. **2026-08-24** — `D21`: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”  
   Владелец: **Anna Sokolova**.  
   Источник: `meetings/2026-08-24-weekly-sync.txt` (2026-08-24)

Если хочешь, я могу ещё показать **цепочку supersedes** или отдельно сказать, **кто владеет текущей политикой сейчас**.

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

### memory-eval-both (completed, 5.7s, 1 tool calls)
queries: ["MATCH (o:OpenItem) WHERE o.raised <= '2026-10-05' AND NOT EXISTS { MATCH (o)<-[w"]

As of 2026-10-05, these open items are still unowned:

- O3 — “Load test on Lambda at 10x current volume”  
  Raised: 2026-07-27  
  Raised again: 2026-08-17, 2026-09-14  
  Total raises: 3  
  Source: open item record; date 2026-07-27

- O4 — “DocumentDB decommission date”  
  Raised: 2026-05-18  
  Raised again: 2026-08-10, 2026-10-05  
  Total raises: 3  
  Source: open item record; date 2026-05-18

- O7 — “Rotate DocumentDB credentials before decommission”  
  Raised: 2026-09-07  
  Raised again: 2026-09-28  
  Total raises: 2  
  Source: open item record; date 2026-09-07

If you want, I can also group them by topic or show which meeting each was raised in.

### memory-eval-graph (completed, 5.4s, 1 tool calls)
queries: ['MATCH (o:OpenItem)\nWHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

As of 2026-10-05, the unowned open items in memory are:

- **O4** — “DocumentDB decommission date”  
  Raised: **2026-05-18**; raised again: **2026-08-10, 2026-10-05**  
  Raised count in memory: **0**  
  Source: **not available in the retrieved fields for this query**; date: **2026-10-05**

- **O3** — “Load test on Lambda at 10x current volume”  
  Raised: **2026-07-27**; raised again: **2026-08-17, 2026-09-14**  
  Raised count in memory: **0**  
  Source: **not available in the retrieved fields for this query**; date: **2026-10-05**

- **O7** — “Rotate DocumentDB credentials before decommission”  
  Raised: **2026-09-07**; raised again: **2026-09-28**  
  Raised count in memory: **0**  
  Source: **not available in the retrieved fields for this query**; date: **2026-10-05**

Note: the query result did not include the item source file, and the graph fields returned here show these open items as unowned and not closed by 2026-10-05.

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

### memory-eval-both (completed, 14.5s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202", 'serverless cutover 19 October sequence before it order what must happen', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202"]

До серверлес-катовера 19 октября в памяти есть такие шаги и условия, в таком порядке:

1. **Заморозить изменения endpoint’ов за 24 часа до катовера.**  
   Источник: `docs/runbook-cutover-serverless.md`, обновлено **2026-09-29**.

2. **Проверить, что staging на Lambda уже неделю без инцидентов.**  
   Это указано как выполненное на **2026-09-28**.  
   Источник: `docs/runbook-cutover-serverless.md`, обновлено **2026-09-29**.

3. **Иметь настроенный provisioned concurrency для `relay-deliver`: 4 инстанса.**  
   Источник: `docs/runbook-cutover-serverless.md`, обновлено **2026-09-29**.

4. **Сделать load test на 10x.**  
   В runbook’е он отмечен как **not done**.  
   Источник: `docs/runbook-cutover-serverless.md`, обновлено **2026-09-29**.

5. **Сначала провести DynamoDB cutover, а серверлес-катовер — через неделю после него.**  
   Это прямое условие из runbook’а: “DynamoDB cutover first; the two must be a week apart.”  
   Источник: `docs/runbook-cutover-serverless.md`, обновлено **2026-09-29**.

6. **В день катовера переключить gateway integration** для `POST /relay/deliver` и `GET /relay/*` **с VPC link на Lambda integrations**.  
   Источник: `docs/runbook-cutover-serverless.m

### memory-eval-graph (completed, 3.8s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:DECIDED_IN]->(m:Meeting {date:'2026-10-19'}) RETURN d.id, d", "MATCH (o:OpenItem)-[:RAISED_IN]->(m:Meeting {date:'2026-10-19'}) OPTIONAL MATCH "]

В памяти нет записей о встрече или решениях на **2026-10-19** (серверлес-катовер): запрос по решениям и открытым пунктам на эту дату вернул пусто.  

Что я проверил:
- решения, принятые на встрече **2026-10-19** — **нет данных**;
- открытые пункты, поднятые на встрече **2026-10-19**, и их владельцы — **нет данных**.

Источник: память графа проекта Relay; дата проверки: **2026-10-19**.

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

### memory-eval-both (completed, 4.0s, 2 tool calls)
queries: ['SLO changed current right now decision Relay webhook delivery project', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

Yes — the SLO has changed.

Current SLO in force:
- Delivery p95 SLO is **3 s for 30 days after the serverless cutover, then back to 2 s**
- Date: **2026-10-05**
- Status: **active**
- Source: **meetings/2026-10-05-cutover-planning.txt**

Evidence from docs:
- **docs/slo.md** was updated **2026-01-28** and still says **p95 2 s** with no stabilisation window, so it is stale relative to the later decision.

Source comparison:
- Decision: **2026-10-05**, `meetings/2026-10-05-cutover-planning.txt`
- Document: **docs/slo.md**, updated **2026-01-28**

### memory-eval-graph (completed, 3.6s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

Да — SLO менялся.

- **Текущее SLO:** доставка **p95 3 s на 30 дней после serverless cutover, затем обратно 2 s**. Это активное решение от **2026-10-05** из `meetings/2026-10-05-cutover-planning.txt`.  
- В примечании к решению указано, что `docs/slo.md` (updated **2026-01-28**) всё ещё говорит **p95 2 s** без stabilisation window, то есть документ уже устарел. Источник: `meetings/2026-10-05-cutover-planning.txt`, дата **2026-10-05**.

Если хотите, я могу ещё показать, **какое SLO было в силе на любую конкретную дату** и кратко перечислить историю изменений.

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

### memory-eval-both (completed, 3.1s, 2 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.file", 'ADR-007 rejected why EKS numbers figures team memory']

ADR-007 отклонили, потому что у EKS:
- p95 latency был **0.4 s**
- но ежемесячная стоимость была **в 1.7 раза выше**
- и это означало **ещё одну платформу для поддержки**; в формулировке PoC — платформа должна была фактически стать Kubernetes-командой.

Источник: `adr/ADR-007.md`, дата `2026-08-05`  
Доп. источник с причиной: `docs/poc-eks-report.md`, дата `2026-07-24`

Если хотите, могу ещё кратко сопоставить это с ADR-006 и сказать, что именно сравнивали по EKS vs Lambda.

### memory-eval-graph (completed, 7.5s, 5 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.file", "MATCH (d:Decision {id:'D07'}) OPTIONAL MATCH (a:Person)-[:OBJECTED_TO]->(d) OPTI", "MATCH (d:Decision)-[:BASED_ON]->(c:PoC {key:'poc:poC-2'}) RETURN d.id, d.text, d", "MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE c.key='poc:2' RETURN d.id, d.text,", "MATCH (a:ADR {id:'ADR-007'})<-[:RECORDED_IN]-(d:Decision) RETURN d.id, d.text, d"]

ADR-007 отклонили, потому что связанное с ним решение было отклонено за стоимость и операционную сложность:  
- «Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)» — это решение D18 от 2026-08-03 из `meetings/2026-08-03-architecture-committee.txt`.  
- Сам ADR-007: `ADR-007`, статус `Rejected`, `adr/ADR-007.md` от 2026-08-03.

Про EKS цифры, которые есть в памяти:
- p95: `0.4 s`
- monthly cost: `1.7x` текущей месячной стоимости

Источник: `meetings/2026-08-03-architecture-committee.txt` / `D18` от 2026-08-03.

Если хотите, я могу ещё показать, какое именно решение в цепочке записано как обосновавшее ADR-007 и кто был против/за него.

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

### memory-eval-both (completed, 3.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERSE"]

The current infrastructure-as-code decision is:

- **Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation**
- **Made on 2026-04-20**
- Source: `meetings/2026-04-20-weekly-sync.txt`

There are older active decisions in the topic too, but this is the current one because it is the newest active decision on `topic:iac`.

### memory-eval-graph (completed, 2.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERSE"]

Current decision on infrastructure as code: **Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation**.  
It was made on **2026-04-20**.  
Source: **meetings/2026-04-20-weekly-sync.txt** (decision date 2026-04-20).

### memory-eval-vector (completed, 4.4s, 3 tool calls)
queries: ['What is the current decision on infrastructure as code, and when was it made?', 'current decision infrastructure as code made date', 'infrastructure as code decision']

The current decision on infrastructure as code is **hybrid IaC**: **networking stays in Terraform, and application stacks use CloudFormation**. This decision was made in **ADR-004 on 2026-04-20** and is recorded as superseding ADR-001. Source: **confluence/decision-log.xhtml** (updated **2026-06-03**) and **adr/ADR-004.md** (updated **2026-04-22**).

The earlier decision to migrate everything from Terraform to CloudFormation exists in **ADR-001** but it is **superseded**, so it is not the current decision. Source: **adr/ADR-001.md** (updated **2026-01-14**).



## t02 [ru / history] Как менялось решение по теме «infrastructure as code»? Перечисли по датам.
**expected:** 2026-01-12: Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1 → 2026-02-09: One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway) → 2026-02-23: Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call → 2026-04-20: Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-02-09-weekly-sync.txt', 'meetings/2026-02-23-incident-review.txt', 'meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 5.9s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (d)-[:SUP"]

По теме «infrastructure as code» в памяти есть такие решения, по датам:

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

Если хочешь, я могу ещё показать, **какое решение сейчас в силе** по этой теме.

### memory-eval-graph (completed, 5.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) RETURN d.text, d.date, d"]

По теме infrastructure as code решения менялись так, по датам:

- 2026-01-12 — «Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1» — статус: superseded.  
  Источник: `meetings/2026-01-12-weekly-sync.txt`  
  Это решение затем было изменено более поздними решениями в теме.

- 2026-02-09 — «One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)» — статус: active.  
  Источник: `meetings/2026-02-09-weekly-sync.txt`

- 2026-02-23 — «Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call» — статус: active.  
  Источник: `meetings/2026-02-23-incident-review.txt`

- 2026-04-20 — «Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation» — статус: active.  
  Источник: `meetings/2026-04-20-weekly-sync.txt`

Если хочешь, я могу ещё отдельно показать **цепочку supersedes** для этой темы или выделить **текущее решение**.

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

### memory-eval-both (completed, 2.9s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE NOT (d)<-[:SU"]

Current decision: Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom.  
Made on: 2026-08-24.

Source: `meetings/2026-08-24-weekly-sync.txt`  
Status: active

### memory-eval-graph (completed, 2.9s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE NOT (d)<-[:SU"]

Current decision on gateway timeout: **Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom**. Source: `meetings/2026-08-24-weekly-sync.txt`, dated **2026-08-24**.

### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['What is the current decision on gateway timeout, and when was it made?', 'current decision gateway timeout made date', 'gateway timeout decision']

The current decision is: **gateway integration timeout is 25 s**. It was made on **2026-08-24**. Source: **meetings/2026-08-24-weekly-sync.txt** (`D20`, status active).

I also found a newer document, **ADR-010: Gateway timeout policy for Lambda integrations** updated **2026-09-23**, but it says **“No decision recorded”** in the Decision section and is therefore stale on this point relative to the meeting decision. Source: **adr/ADR-010.md** (`Decision`, updated 2026-09-23).

## t04 [ru / history] Как менялось решение по теме «gateway timeout»? Перечисли по датам.
**expected:** 2026-03-16: Gateway integration timeout 10 s on every Relay route → 2026-05-18: Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14 → 2026-08-24: Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom  
**expected sources:** {'sources': ['meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 5.2s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.text CONTAI", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) RETURN d.text, d.da"]

По теме «gateway timeout» в памяти есть такие решения, по датам:

- 2026-03-16 — «Gateway integration timeout 10 s on every Relay route»  
  Источник: `meetings/2026-03-16-weekly-sync.txt`  
  Статус: `superseded`

- 2026-05-18 — «Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14»  
  Источник: `meetings/2026-05-18-weekly-sync.txt`  
  Статус: `superseded`

- 2026-08-24 — «Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom»  
  Источник: `meetings/2026-08-24-weekly-sync.txt`  
  Статус: `active`

Если хочешь, я могу ещё кратко показать, какое решение было в силе на любую конкретную дату.

### memory-eval-graph (completed, 4.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'})\nOPTIONAL MATCH (d)-"]

По датам решение по теме «gateway timeout» менялось так:

- **2026-03-16** — **D06**: «Gateway integration timeout 10 s on every Relay route» — `superseded`  
  source: `meetings/2026-03-16-weekly-sync.txt`

- **2026-05-18** — **D12**: «Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14» — `superseded`  
  source: `meetings/2026-05-18-weekly-sync.txt`

- **2026-08-24** — **D20**: «Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom» — `active`  
  source: `meetings/2026-08-24-weekly-sync.txt`

Если хочешь, я могу ещё кратко показать цепочку изменений как «10 s → 30 s → 25 s».

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

### memory-eval-both (completed, 3.2s, 1 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE NOT (cur)<-"]

The earlier decision was **“Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14”**.

It replaced:
- **“Gateway integration timeout 10 s on every Relay route”** — **2026-03-16**  
  Source: `meetings/2026-03-16-weekly-sync.txt`

For the earlier decision itself:
- Decision text: `Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14`
- Date: `2026-05-18`
- Source: `meetings/2026-05-18-weekly-sync.txt`

### memory-eval-graph (completed, 5.0s, 2 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE cur.text CO", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) RETURN d.id, d.text"]

The earlier decision was **“Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14”**.

- It **replaced** **“Gateway integration timeout 10 s on every Relay route”**
- That earlier decision is **D06**, dated **2026-03-16**
- Source: **meetings/2026-03-16-weekly-sync.txt**

The replacement chain in memory is:
- **D06** → replaced by **D12** on **2026-05-18**
- Source for D12: **meetings/2026-05-18-weekly-sync.txt**



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

### memory-eval-both (completed, 2.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (d)<-[:SUP"]

Current decision on retries: retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on `/deliver` are turned off.  
Made on: 2026-08-24.  

Source: `meetings/2026-08-24-weekly-sync.txt` — `2026-08-24`

### memory-eval-graph (completed, 3.4s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (d)<-[:SUP"]

The current decision on retries is:

- “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off” — source: `meetings/2026-08-24-weekly-sync.txt`, dated `2026-08-24`, status `active`.

So it was made on `2026-08-24` (`meetings/2026-08-24-weekly-sync.txt`).

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

### memory-eval-both (completed, 4.9s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.status <> 'r"]

По теме **retries** решение менялось так:

1. **2026-03-30** — **D07**  
   *“Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice”*  
   Статус: **superseded**  
   Source: `meetings/2026-03-30-weekly-sync.txt`

2. **2026-06-15** — **D14**  
   *“Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%”*  
   Статус: **superseded**  
   Source: `meetings/2026-06-15-weekly-sync.txt`

3. **2026-08-24** — **D21**  
   *“Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”*  
   Статус: **active**  
   Source: `meetings/2026-08-24-weekly-sync.txt`

Если хочешь, могу ещё кратко показать **цепочку supersedes** или сказать, **какое решение сейчас в силе**.

### memory-eval-graph (completed, 5.0s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$T}) OPTIONAL MATCH (old:Decision)<-[:']

По теме **«retries»** решение менялось так:

- **2026-03-30** — **D07**: «Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice»  
  Источник: `meetings/2026-03-30-weekly-sync.txt`  
  Статус: `superseded`

- **2026-06-15** — **D14**: «Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%»  
  Источник: `meetings/2026-06-15-weekly-sync.txt`  
  Статус: `superseded`

- **2026-08-24** — **D21**: «Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off»  
  Источник: `meetings/2026-08-24-weekly-sync.txt`  
  Статус: `active`

Если хочешь, я могу ещё кратко показать, **какое решение сейчас в силе** и **чем оно отличается от предыдущих**.

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

### memory-eval-both (completed, 3.3s, 1 tool calls)
queries: ['MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision) WHERE (cur)-[:ABOUT']

The earlier decision was **D14**: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%” — **2026-06-15** — source: `meetings/2026-06-15-weekly-sync.txt`.

That decision itself replaced **D07**: “Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice” — **2026-03-30** — source: `meetings/2026-03-30-weekly-sync.txt`.

### memory-eval-graph (completed, 5.6s, 2 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})-[:ABOUT]?(x) RETUR", "MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (cur)<-["]

The earlier decision was **D14**, and it replaced **nothing** I can show before it in the retry chain from memory.

- **D14**: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%”  
  - **Date:** 2026-06-15  
  - **Source:** `meetings/2026-06-15-weekly-sync.txt`

The current retry decision is **D21**, which supersedes D14:
- **D21**: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”  
  - **Date:** 2026-08-24  
  - **Source:** `meetings/2026-08-24-weekly-sync.txt`

I don’t have a prior decision before D14 in the retry supersession chain in the graph.

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

### memory-eval-both (completed, 3.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE NOT (d)<-[:SUP"]

The current decision on compute platform is:

- **Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances**
- **Made on:** 2026-08-03
- **Status:** active
- **Source:** `meetings/2026-08-03-architecture-committee.txt`



### memory-eval-graph (completed, 3.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE NOT (d)<-[:SUP"]

The current compute-platform decision is: **Relay moves to Lambda with provisioned concurrency on `/deliver`**. It was made on **2026-08-03**.  
Source: **meetings/2026-08-03-architecture-committee.txt** (decision date 2026-08-03).

Supporting note from the same decision: the note says **PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances**.

### memory-eval-vector (completed, 3.4s, 3 tool calls)
queries: ['What is the current decision on compute platform, and when was it made?', 'current decision compute platform made date', 'compute platform decision']

The current decision on compute is: **Relay moves to Lambda with provisioned concurrency on `/deliver`**. It was made on **2026-08-03**. Source: `meetings/2026-08-03-architecture-committee.txt` / claim `D17` (recorded in ADR-006), dated **2026-08-03**.

I also found an older document saying to **keep Relay on EKS with autoscaling**, but it is **rejected/superseded** by the 2026-08-03 decision. Sources: `adr/ADR-007.md` dated **2026-08-05** and `meetings/2026-08-03-architecture-committee.txt` dated **2026-08-03**.

## t10 [ru / history] Как менялось решение по теме «compute platform»? Перечисли по датам.
**expected:** 2026-06-15: Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July → 2026-08-03: Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances  
**expected sources:** {'sources': ['meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 5.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) OPTIONAL MATCH (d)-["]

По теме **compute platform** решение менялось так:

- **2026-06-15** — **D15**: *Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July* — `superseded`  
  Source: `meetings/2026-06-15-weekly-sync.txt`

- **2026-08-03** — **D18**: *Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)* — `rejected`  
  Source: `meetings/2026-08-03-architecture-committee.txt`

- **2026-08-03** — **D17**: *Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances* — `active`  
  Source: `meetings/2026-08-03-architecture-committee.txt`

Если хочешь, я могу ещё показать **цепочку, какое решение кого supersedes**, или кратко объяснить **текущее решение в силе**.

### memory-eval-graph (completed, 4.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) OPTIONAL MATCH (d)-["]

По теме **compute platform** решение менялось так:

- **2026-06-15** — **D15**, статус: *superseded*  
  `Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July`  
  Источник: `meetings/2026-06-15-weekly-sync.txt`

- **2026-08-03** — **D17**, статус: *active*  
  `Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances`  
  Источник: `meetings/2026-08-03-architecture-committee.txt`

- **2026-08-03** — **D18**, статус: *rejected*  
  `Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)`  
  Источник: `meetings/2026-08-03-architecture-committee.txt`

Если хочешь, могу ещё показать **цепочку supersedes** или **текущее решение в силе** по этой теме в одном предложении.

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

### memory-eval-both (completed, 2.9s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

The current SLO decision is:

- **“Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s”**
- **Made on:** **2026-10-05**
- **Status:** active
- **Source:** `meetings/2026-10-05-cutover-planning.txt`

It also notes that `docs/slo.md` was still outdated as of `2026-01-28`.

### memory-eval-graph (completed, 2.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

Current SLO decision: “Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s” — status **active**. Source: `meetings/2026-10-05-cutover-planning.txt`, dated **2026-10-05**.

The decision note also says `docs/slo.md` was still outdated as of **2026-01-28**.

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

### memory-eval-both (completed, 3.7s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE d.status <> 'rejec"]

По теме «SLO» изменения такие:

- 2026-01-26 — **D02**: `Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%`  
  Статус: `superseded`  
  Источник: `meetings/2026-01-26-weekly-sync.txt`

- 2026-10-05 — **D28**: `Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s`  
  Статус: `active`  
  Источник: `meetings/2026-10-05-cutover-planning.txt`

Если хочешь, могу ещё кратко показать, **какое решение сейчас в силе**.

### memory-eval-graph (completed, 3.1s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) OPTIONAL MATCH (d)-[:SUP"]

По теме **SLO** решения менялись так:

- **2026-01-26** — **D02**: «Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%»; статус **superseded**. Источник: `meetings/2026-01-26-weekly-sync.txt`.
- **2026-10-05** — **D28**: «Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s»; статус **active**. Источник: `meetings/2026-10-05-cutover-planning.txt`.

Если хочешь, могу ещё кратко показать, **какое решение сейчас в силе** по SLO.

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

### memory-eval-both (completed, 2.6s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.to IS NULL RE"]

Темой «retries» сейчас владеет Ivan Melnik, с 2026-09-07.

### memory-eval-graph (completed, 2.4s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.to IS NULL RE"]

Темой «retries» сейчас владеет **Ivan Melnik** с **2026-09-07**.  
Источник: граф памяти, ownership по теме `topic:retries` (связь OWNS), дата начала владения `2026-09-07`.

### memory-eval-vector (completed, 2.7s, 3 tool calls)
queries: ['Кто сейчас владеет темой «retries» и с какой даты?', 'Who owns retries and since when?', 'ownership retries from date owner current']

Сейчас тему **retries** владеет **Ivan Melnik** — **с 2026-09-07**. Источник: `memory/decisions.jsonl`, запись `claim ownership | retries | 2026-09-07` (статус `active`).

## t14 [en / owner_at] Who owned retries on 2026-06-15?
**expected:** Anna Sokolova (from 2026-06-01 to 2026-09-07)  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 2.5s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.from <= '2026"]

On 2026-06-15, **Anna Sokolova** owned retries.

- Source: graph ownership edge
- Effective: from **2026-06-01** to **2026-09-07**

### memory-eval-graph (completed, 2.6s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.from <= '2026"]

Anna Sokolova owned retries on 2026-06-15, from 2026-06-01 to 2026-09-07. Source: memory graph ownership edge for topic:retries; no file is attached to ownership edges in memory.

### memory-eval-vector (completed, 4.3s, 3 tool calls)
queries: ['Who owned retries on 2026-06-15?', 'retries ownership 2026-06-15', 'owner retries 2026-06-15']

On 2026-06-15, **Anna Sokolova** owned retries. The active ownership decision is from **2026-06-01** and says “Anna Sokolova owns retries from 2026-06-01 to 2026-09-07.” Source: **memory/decisions.jsonl** dated **2026-06-01**.

I also retrieved a meeting note from **2026-06-15** that says “без владельца” (“without an owner”), but it appears to be about a different item in that sync, not the retries ownership decision. Source: **meetings/2026-06-15-weekly-sync.txt** dated **2026-06-15**.



## t15 [ru / owner_now] Кто сейчас владеет темой «compute platform» и с какой даты?
**expected:** Ivan Melnik, с 2026-07-13  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt']}

### memory-eval-both (completed, 3.0s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.to IS NULL RE"]

Тему «compute platform» сейчас владеет **Ivan Melnik** — с **2026-07-13**.  
Источник: граф памяти, связь OWNS к теме `topic:compute`; дата владения — `2026-07-13`.

### memory-eval-graph (completed, 2.8s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.from <= $d AN"]

Тему «compute platform» сейчас владеет **Ivan Melnik** — с **2026-07-13**.  
Источник: граф памяти, связь **OWNS** для темы `topic:compute`, дата начала владения `2026-07-13`.

### memory-eval-vector (completed, 2.5s, 1 tool calls)
queries: ['Кто сейчас владеет темой «compute platform» и с какой даты?']

Сейчас темой **compute** владеет **Ivan Melnik** с **2026-07-13**. Источник: `memory/decisions.jsonl` (claim ownership | compute | 2026-07-13).

Нашёл также более старую, уже неактуальную запись: **Sergey Belov** владел compute с **2026-06-15** по **2026-07-13**. Источник: `memory/decisions.jsonl` (claim ownership | compute | 2026-06-15).

## t16 [en / owner_at] Who owned compute platform on 2026-06-28?
**expected:** Sergey Belov (from 2026-06-15 to 2026-07-13)  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt']}

### memory-eval-both (completed, 2.7s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.from <= '2026"]

Sergey Belov owned compute platform on 2026-06-28, from 2026-06-15 to 2026-07-13.  
Source: graph OWNS edge on topic:compute.

### memory-eval-graph (completed, 2.8s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.from <= '2026"]

On 2026-06-28, **Sergey Belov** owned **compute platform**. Source: ownership edge in memory, with ownership valid from **2026-06-15** to **2026-07-13**.

### memory-eval-vector (completed, 4.1s, 3 tool calls)
queries: ['Who owned compute platform on 2026-06-28?', 'compute platform owner 2026-06-28', 'ownership of compute platform on 2026-06-28']

On 2026-06-28, **Sergey Belov** owned compute. Source: **memory/decisions.jsonl** — claim dated **2026-06-15**: “Sergey Belov owns compute from 2026-06-15 to 2026-07-13.”

I also found a newer ownership decision for compute dated **2026-07-13** saying **Ivan Melnik** owns compute from that date onward, so the 2026-06-15 decision is the applicable one for 2026-06-28. Source: **memory/decisions.jsonl** — decision dated **2026-07-13**.

## t17 [ru / owner_now] Кто сейчас владеет темой «idempotency» и с какой даты?
**expected:** Anna Sokolova, с 2026-06-01  
**expected sources:** {'sources': []}

### memory-eval-both (completed, 2.5s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.to IS NUL"]

Темой «idempotency» сейчас владеет **Anna Sokolova** с **2026-06-01**.

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.to IS NUL"]

Тему «idempotency» сейчас владеет **Anna Sokolova** с **2026-06-01**.  
Источник: граф памяти, связь `OWNS` к теме `topic:idempotency` (данные по владельцу и дате из результата запроса; дата владения: `2026-06-01`).

### memory-eval-vector (completed, 3.0s, 3 tool calls)
queries: ['Кто сейчас владеет темой «idempotency» и с какой даты?', 'idempotency ownership current owner from date', 'владелец idempotency дата']

Сейчас темой **idempotency** владеет **Anna Sokolova** — с **2026-06-01**.  
Источник: `memory/decisions.jsonl`, запись `ownership:idempotency:2026-06-01` (дата 2026-06-01).

## t18 [en / owner_at] Who owned idempotency on 2026-05-28?
**expected:** Nikita Frolov (from 2026-05-18 to 2026-06-01)  
**expected sources:** {'sources': []}

### memory-eval-both (completed, 2.0s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(x {key:'topic:idempotency'}) WHERE o.from <= '2026-0"]

On 2026-05-28, **Nikita Frolov** owned idempotency.

- Source: graph OWNS edge
- Owned from: **2026-05-18**
- Owned to: **2026-06-01**

### memory-eval-graph (completed, 2.9s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.from <= '"]

On 2026-05-28, **Nikita Frolov** owned idempotency. Source: **memory graph** via the ownership edge for `topic:idempotency`; ownership was active from **2026-05-18** to **2026-06-01**.

### memory-eval-vector (completed, 3.0s, 3 tool calls)
queries: ['Who owned idempotency on 2026-05-28?', 'idempotency owner 2026-05-28', 'ownership of idempotency on 2026-05-28']

Nikita Frolov owned idempotency on 2026-05-28. Source: `meetings/2026-05-18-weekly-sync.txt` and `memory/decisions.jsonl`, dated 2026-05-18. The newer ownership decision says Anna Sokolova owns idempotency from 2026-06-01, so that does not apply yet. Source: `meetings/2026-06-01-weekly-sync.txt` and `memory/decisions.jsonl`, dated 2026-06-01.

## t19 [ru / objector] Кто предложил и кто возражал против решения «Migrate Relay infrastructure code from Terraform to CloudFor…»?
**expected:** proposer Pavel Grishin, objector Timur Aliev, 2026-01-12  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt']}

### memory-eval-both (completed, 3.1s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Migrate Relay infrastructure code f"]

Решение «Migrate Relay infrastructure code from Terraform to CloudFor…» предложил **Pavel Grishin**, а возражал **Timur Aliev**.

Источник: `meetings/2026-01-12-weekly-sync.txt`, дата решения: `2026-01-12`.

### memory-eval-graph (completed, 3.2s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Migrate Relay infrastructure code f"]

Решение **«Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1»**:

- **Предложил:** Павел Гришин — источник: `meetings/2026-01-12-weekly-sync.txt`, дата: `2026-01-12`
- **Возражал:** Тимур Алиев — источник: `meetings/2026-01-12-weekly-sync.txt`, дата: `2026-01-12`

Если хотите, я могу ещё показать саму запись решения целиком.

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

### memory-eval-both (completed, 1.9s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout 10 s on"]

Pavel Grishin proposed it, and Anna Sokolova objected to it.

- Source: `meetings/2026-03-16-weekly-sync.txt`
- Date: `2026-03-16`

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout 10 s on"]

Pavel Grishin proposed the decision and Anna Sokolova objected to it.

- Decision: “Gateway integration timeout 10 s on every Relay route”
- Date: 2026-03-16
- Status: superseded
- Source: `meetings/2026-03-16-weekly-sync.txt`

Source: `meetings/2026-03-16-weekly-sync.txt`, 2026-03-16

### memory-eval-vector (completed, 3.5s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'Gateway integration timeout 10 s ", 'Gateway integration timeout 10 s on every Relay route', 'relay route gateway integration timeout 10 s proposed objected']

Proposed by Pavel Grishin and objected by Anna Sokolova. Source: `meetings/2026-03-16-weekly-sync.txt` / claim D06, dated 2026-03-16.

Note: this decision is marked superseded in the same source, with later related decisions existing.

## t21 [ru / objector] Кто предложил и кто возражал против решения «Hybrid IaC: networking (VPC, peering, DNS) stays in Terrafor…»?
**expected:** proposer Sergey Belov, objector Pavel Grishin, 2026-04-20  
**expected sources:** {'sources': ['meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 2.2s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Hybrid IaC: networking (VPC, peerin"]

Решение **«Hybrid IaC: networking (VPC, peering, DNS) stays in Terrafor…»**:

- **Предложил:** Sergey Belov  
- **Возражал:** Pavel Grishin

Источник: `meetings/2026-04-20-weekly-sync.txt`, дата **2026-04-20**.

### memory-eval-graph (completed, 2.5s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Hybrid IaC: networking (VPC, peerin"]

Предложил: Сергей Белов, источник: `meetings/2026-04-20-weekly-sync.txt`, дата: `2026-04-20`.

Возражал: Павел Гришин, источник: `meetings/2026-04-20-weekly-sync.txt`, дата: `2026-04-20`.

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

### memory-eval-both (completed, 2.7s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'DynamoDB single-table design, chose"]

Proposed by Denis Orlov and objected to by Timur Aliev.

Source: `meetings/2026-05-04-poc-review.txt`, date `2026-05-04`.

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'DynamoDB single-table design, chose"]

Proposed by Denis Orlov and objected to by Timur Aliev, according to `meetings/2026-05-04-poc-review.txt` on `2026-05-04`.

### memory-eval-vector (completed, 3.2s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'DynamoDB single-table design, cho", 'DynamoDB single-table design, chosen on PoC-1 results p99 proposed objected', 'single-table design PoC-1 results p99 proposed objected DynamoDB']

Proposed by **Denis Orlov** and objected by **Timur Aliev**.  
Source: `meetings/2026-05-04-poc-review.txt` via claim D10, dated **2026-05-04**.

## t23 [en / objector] Who proposed and who objected to the decision 'Gateway integration timeout raised from 10 s to 30 s after t…'?
**expected:** proposer Anna Sokolova, objector Lena Kim, 2026-05-18  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt']}

### memory-eval-both (completed, 2.1s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout raised "]

Proposed by Anna Sokolova and objected to by Lena Kim.

Source: `meetings/2026-05-18-weekly-sync.txt`, 2026-05-18.

### memory-eval-graph (completed, 3.8s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout raised ", "MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout raised "]

Proposed by Anna Sokolova and objected to by Lena Kim for the decision **“Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14”**.

Source: `meetings/2026-05-18-weekly-sync.txt`, date `2026-05-18`.

### memory-eval-vector (completed, 2.4s, 1 tool calls)
queries: ["Who proposed and who objected to the decision 'Gateway integration timeout raise"]

Proposed by **Anna Sokolova** and objected to by **Lena Kim**. Source: **meetings/2026-05-18-weekly-sync.txt** (2026-05-18).

## t24 [ru / objector] Кто предложил и кто возражал против решения «Relay moves to Lambda with provisioned concurrency on /deliv…»?
**expected:** proposer Olga Petrova, objector Timur Aliev, 2026-08-03  
**expected sources:** {'sources': ['meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 2.8s, 2 tool calls)
queries: ['"Relay moves to Lambda with provisioned concurrency on /deliv" proposer objected', "MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio"]

Предложила **Olga Petrova**, возразил **Timur Aliev**.

Источник: `meetings/2026-08-03-architecture-committee.txt`, дата `2026-08-03`.

### memory-eval-graph (completed, 2.9s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio"]

Предложила **Ольга Петрова**; возражал **Тимур Алиев**.

Источник: `meetings/2026-08-03-architecture-committee.txt`, дата решения: **2026-08-03**.

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

### memory-eval-both (completed, 3.3s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Retries move out of the gateway int"]

Решение предложил **Ivan Melnik**, возражала **Anna Sokolova**.

Источник: `meetings/2026-08-24-weekly-sync.txt`, дата: `2026-08-24`.

### memory-eval-graph (completed, 2.9s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Retries move out of the gateway int"]

Предложил **Ivan Melnik** и возражала **Anna Sokolova** — решение от **2026-08-24**, источник: `meetings/2026-08-24-weekly-sync.txt`.

### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Retries move out of the gateway int', 'Who proposed and who objected to the decision "Retries move out of the gateway i', 'Retries move out of the gateway into SQS with a dead-letter']

Решение предложил **Ivan Melnik**, а возражала **Anna Sokolova**.  
Источник: **meetings/2026-08-24-weekly-sync.txt**; решение зафиксировано в **ADR-009: Retries through SQS with a dead-letter queue**. Дата: **2026-08-24**.

## t26 [en / objector] Who proposed and who objected to the decision 'Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after t…'?
**expected:** proposer Lena Kim, objector Marat Yusupov, 2026-10-05  
**expected sources:** {'sources': ['meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 4.1s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Delivery p95 SLO relaxed from 2 s t", '"Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after t" proposed objected']

Proposed by **Lena Kim** and objected to by **Marat Yusupov**.

Source:
- `meetings/2026-10-05-cutover-planning.txt` — `2026-10-05`

### memory-eval-graph (completed, 3.4s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Delivery p95 SLO relaxed from 2 s t", "MATCH (d:Decision) WHERE d.text STARTS WITH 'Delivery p95 SLO relaxed from 2 s t"]

Proposed by Lena Kim and objected to by Marat Yusupov, according to `meetings/2026-10-05-cutover-planning.txt` on `2026-10-05`.

### memory-eval-vector (completed, 2.4s, 1 tool calls)
queries: ["Who proposed and who objected to the decision 'Delivery p95 SLO relaxed from 2 s"]

Proposed by **Lena Kim** and objected to by **Marat Yusupov**. Source: `meetings/2026-10-05-cutover-planning.txt` (2026-10-05), claim D28.

## t27 [en / aggregate] How many decisions have been superseded, and on which topics?
**expected:** 7: D01 (infrastructure as code, 2026-01-12); D02 (SLO, 2026-01-26); D06 (gateway timeout, 2026-03-16); D07 (retries, 2026-03-30); D12 (gateway timeout, 2026-05-18); D14 (retries, 2026-06-15); D15 (compute platform, 2026-06-15)  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-01-26-weekly-sync.txt', 'meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt']}

### memory-eval-both (completed, 2.9s, 1 tool calls)
queries: ["MATCH (d:Decision {status:'superseded'})-[:ABOUT]->(t:Topic) RETURN count(d) AS "]

There are **7 superseded decisions**.

They span these topics:
- **infrastructure as code** (`topic:iac`)
- **SLO** (`topic:slo`)
- **gateway timeout** (`topic:timeouts`)
- **retries** (`topic:retries`)
- **compute platform** (`topic:compute`)

Source: graph query result over `Decision` nodes with status `superseded`.

### memory-eval-graph (completed, 3.2s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:SUPERSEDES]->(old:Decision) MATCH (old)-[:ABOUT]->(t:Topic)']

7 decisions have been superseded.

The topics are:
- topic:iac — infrastructure as code
- topic:timeouts — gateway timeout
- topic:retries — retries
- topic:compute — compute platform
- topic:slo — SLO

Source: graph memory query results, with superseded decisions counted from `Decision-[:SUPERSEDES]->Decision` and topics from the related `ABOUT` edges.

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

### memory-eval-both (completed, 3.5s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:anna-sokolova'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

У Anna Sokolova **2 действующих решения**.

1. **Retries and idempotency ownership moves from Nikita to Anna (Nikita leaves on 2026-06-01)**  
   Дата: **2026-06-01**  
   Статус: **active**  
   Источник: **meetings/2026-06-01-weekly-sync.txt**

2. **Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off**  
   Дата: **2026-08-24**  
   Статус: **active**  
   Источник: **meetings/2026-08-24-weekly-sync.txt**

Итого: **2**.

### memory-eval-graph (completed, 6.2s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:anna-sokolova'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

У Anna Sokolova **2 действующих решения**.

- **D13** — “Retries and idempotency ownership moves from Nikita to Anna (Nikita leaves on 2026-06-01)” — **2026-06-01**, `meetings/2026-06-01-weekly-sync.txt`
- **D21** — “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off” — **2026-08-24**, `meetings/2026-08-24-weekly-sync.txt`

Источник: `meetings/2026-06-01-weekly-sync.txt` и `meetings/2026-08-24-weekly-sync.txt`.

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

Pavel Grishin владеет 3 действующими решениями:

1. **One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)**  
   — дата: 2026-02-09  
   — источник: `meetings/2026-02-09-weekly-sync.txt`

2. **Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack**  
   — дата: 2026-03-02  
   — источник: `meetings/2026-03-02-weekly-sync.txt`

3. **Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation**  
   — дата: 2026-04-20  
   — источник: `meetings/2026-04-20-weekly-sync.txt`

Если хотите, я могу ещё показать их в хронологическом порядке или перечислить только тексты без дат.

### memory-eval-graph (completed, 4.0s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:pavel-grishin'})-[o:OWNS]->(d:Decision)\nWHERE o.to I"]

Pavel Grishin владеет 3 действующими решениями.

- D03 — “One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)” — 2026-02-09 — `meetings/2026-02-09-weekly-sync.txt`
- D05 — “Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack” — 2026-03-02 — `meetings/2026-03-02-weekly-sync.txt`
- D09 — “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation” — 2026-04-20 — `meetings/2026-04-20-weekly-sync.txt`

Итого: 3.

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

### memory-eval-both (completed, 5.9s, 3 tool calls)
queries: ["MATCH (:Person {key:'ivan-melnik'})-[o:OWNS]->(d:Decision) WHERE o.to IS NULL AN", "MATCH (:Person {key:'ivan-melnik'})-[o:OWNS]->(d:Decision) WHERE o.to IS NULL RE", 'Ivan Melnik owns active decisions']

По памяти у Ivan Melnik **нет действующих решений, которыми он владеет**.

Проверка графа по `OWNS` на активные решения для `ivan-melnik` вернула пусто; по текущим записям в векторной памяти у него есть владение темами, но не решениями.

**Итого: 0 действующих решений.**

Источник проверки: графовая память (`OWNS` к `Decision`), дата не указана в записи.

### memory-eval-graph (completed, 8.7s, 4 tool calls)
queries: ["MATCH (:Person {key:'ivan-melnik'})-[o:OWNS]->(d:Decision)\nWHERE o.to IS NULL AN", "MATCH (:Person {key:'ivan-melnik'})-[o:OWNS]->(d:Decision)\nWHERE o.to IS NULL\nRE", "MATCH (p:Person)\nWHERE p.key = 'ivan-melnik' OR p.name = 'Ivan Melnik' OR 'ivan'", "MATCH (:Person {key:'person:ivan-melnik'})-[o:OWNS]->(d:Decision)\nWHERE o.to IS "]

Ivan Melnik владеет 5 действующими решениями: D16, D17, D20, D22 и D25.

- D16 — “Serverless PoC ownership moves from Sergey to Ivan” — 2026-07-13 — `meetings/2026-07-13-weekly-sync.txt`
- D17 — “Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances” — 2026-08-03 — `meetings/2026-08-03-architecture-committee.txt`
- D20 — “Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom” — 2026-08-24 — `meetings/2026-08-24-weekly-sync.txt`
- D22 — “Retries ownership moves from Anna to Ivan, who owns the SQS pipeline” — 2026-09-07 — `meetings/2026-09-07-security-review.txt`
- D25 — “Serverless cutover on 2026-10-19 at 09:00 local, inside the planned-work error budget” — 2026-10-05 — `meetings/2026-10-05-cutover-planning.txt`

Итого: 5.

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

### memory-eval-both (completed, 4.0s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:lena-kim'})-[o:OWNS]->(d:Decision) WHERE o.to IS NUL"]

Lena Kim владеет 3 действующими решениями:

1. **Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call**  
   - Дата: 2026-02-23  
   - Источник: `meetings/2026-02-23-incident-review.txt`

2. **Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s**  
   - Дата: 2026-10-05  
   - Источник: `meetings/2026-10-05-cutover-planning.txt`

3. **Rollback owner for both cutovers is Lena**  
   - Дата: 2026-10-05  
   - Источник: `meetings/2026-10-05-cutover-planning.txt`

Итого: **3**.

### memory-eval-graph (completed, 4.4s, 1 tool calls)
queries: ["MATCH (p:Person {key:'person:lena-kim'})-[o:OWNS]->(d:Decision) WHERE o.to IS NU"]

Lena Kim владеет 3 действующими решениями.

1. **D04** — “Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call”  
   Дата: **2026-02-23**  
   Источник: **meetings/2026-02-23-incident-review.txt**

2. **D28** — “Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s”  
   Дата: **2026-10-05**  
   Источник: **meetings/2026-10-05-cutover-planning.txt**

3. **D27** — “Rollback owner for both cutovers is Lena”  
   Дата: **2026-10-05**  
   Источник: **meetings/2026-10-05-cutover-planning.txt**

Итого: **3**.

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

### memory-eval-both (completed, 2.5s, 1 tool calls)
queries: ["MATCH (a:ADR) WHERE a.status <> 'Accepted' RETURN a.id, a.title, a.status, a.fil"]

The ADRs that are not Accepted are:

- ADR-001 — status: Superseded — `adr/ADR-001.md`
- ADR-005 — status: Superseded — `adr/ADR-005.md`
- ADR-007 — status: Rejected — `adr/ADR-007.md`
- ADR-010 — status: Proposed — `adr/ADR-010.md`

Source: graph query result from ADR nodes.

### memory-eval-graph (completed, 3.7s, 1 tool calls)
queries: ["MATCH (a:ADR) WHERE a.status <> 'Accepted' RETURN a.id, a.title, a.status, a.fil"]

The ADRs that are not Accepted are:

- ADR-001 — **Superseded** — `adr/ADR-001.md` — dated `n/a` in the retrieved row
- ADR-005 — **Superseded** — `adr/ADR-005.md` — dated `n/a` in the retrieved row
- ADR-007 — **Rejected** — `adr/ADR-007.md` — dated `n/a` in the retrieved row
- ADR-010 — **Proposed** — `adr/ADR-010.md` — dated `n/a` in the retrieved row

Source: the ADR nodes returned by the graph query (`adr/ADR-001.md`, `adr/ADR-005.md`, `adr/ADR-007.md`, `adr/ADR-010.md`).

If you want, I can also list them in a table with their titles.

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

### memory-eval-both (completed, 5.5s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На 2026-06-15 без владельца были такие открытые вопросы:

- **O1** — *DynamoDB migration dry run on a production snapshot*  
  Ранее поднят: **2026-05-04**; raised_again: **2026-05-18, 2026-06-15, 2026-06-29, 2026-07-20**.  
  Статус: **closed**.  
  Источник: `o.raised`, `o.raised_again`, `o.status`, `o.text` по вопросу `2026-06-15`.

- **O4** — *DocumentDB decommission date*  
  Ранее поднят: **2026-05-18**; raised_again: **2026-08-10, 2026-10-05**.  
  Статус: **open**.  
  Источник: `o.raised`, `o.raised_again`, `o.status`, `o.text` по вопросу `2026-06-15`.

Если хотите, я могу ещё отфильтровать только **реально открытые** на эту дату и исключить закрытые, как O1.

### memory-eval-graph (completed, 5.0s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На 2026-06-15 без владельца были 2 открытых вопроса:

1. **O1** — “DynamoDB migration dry run on a production snapshot”  
   - поднят: **2026-05-04**
   - поднимался снова: **2026-05-18, 2026-06-15, 2026-06-29, 2026-07-20**
   - статус: **closed**  
   - источник: **не указан в результатах запроса**; дата из графа: **2026-05-04** и повторное поднятие **2026-06-15**

2. **O4** — “DocumentDB decommission date”  
   - поднят: **2026-05-18**
   - поднимался снова: **2026-08-10, 2026-10-05**
   - статус: **open**  
   - источник: **не указан в результатах запроса**; дата из графа: **2026-05-18**

Источник проверки: граф памяти, запрос по открытым вопросам без владельца на дату **2026-06-15**.

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

### memory-eval-both (completed, 4.8s, 1 tool calls)
queries: ["MATCH (o:OpenItem) WHERE o.raised <= '2026-08-17' AND NOT EXISTS { MATCH (o)<-[w"]

На 2026-08-17 без владельца были такие открытые вопросы:

- **O3** — “Load test on Lambda at 10x current volume”  
  - raised: **2026-07-27**
  - raised_again: **2026-08-17**, **2026-09-14**
  - status: **open**
  - источник: **не указан в записи вопроса**; дата из узла: **2026-07-27**

- **O4** — “DocumentDB decommission date”  
  - raised: **2026-05-18**
  - raised_again: **2026-08-10**, **2026-10-05**
  - status: **open**
  - источник: **не указан в записи вопроса**; дата из узла: **2026-05-18**

Если хотите, я могу ещё показать, в каких встречах они были подняты.

### memory-eval-graph (completed, 5.0s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На 2026-08-17 без владельца были такие открытые вопросы:

- **O3** — “Load test on Lambda at 10x current volume”; raised **2026-07-27**, raised_again **2026-08-17**, **2026-09-14**; статус **open**. Источник: `O3` (дата взята из полей open item).  
- **O4** — “DocumentDB decommission date”; raised **2026-05-18**, raised_again **2026-08-10**, **2026-10-05**; статус **open**. Источник: `O4` (дата взята из полей open item).

Проверка на 2026-08-17 выполнена по правилу: у open item не было активного владельца и не было закрывающего решения на эту дату.

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

### memory-eval-both (completed, 4.6s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $d AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

On 2026-10-05, these open items had no owner:

- **O3** — “Load test on Lambda at 10x current volume”  
  Raised: 2026-07-27; raised again: 2026-08-17, 2026-09-14  
  Status: open  
  Source: open-item graph, date 2026-10-05

- **O4** — “DocumentDB decommission date”  
  Raised: 2026-05-18; raised again: 2026-08-10, 2026-10-05  
  Status: open  
  Source: open-item graph, date 2026-10-05

- **O7** — “Rotate DocumentDB credentials before decommission”  
  Raised: 2026-09-07; raised again: 2026-09-28  
  Status: open  
  Source: open-item graph, date 2026-10-05

### memory-eval-graph (completed, 4.5s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

On 2026-10-05, the open items with no owner were:

- O3 — “Load test on Lambda at 10x current volume” — raised 2026-07-27; raised again 2026-08-17, 2026-09-14 — status open. Source: not stored on the OpenItem row; retrieved from the graph query.  
- O4 — “DocumentDB decommission date” — raised 2026-05-18; raised again 2026-08-10, 2026-10-05 — status open. Source: not stored on the OpenItem row; retrieved from the graph query.  
- O7 — “Rotate DocumentDB credentials before decommission” — raised 2026-09-07; raised again 2026-09-28 — status open. Source: not stored on the OpenItem row; retrieved from the graph query.

This follows the open-item/no-owner rule for 2026-10-05.

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

### memory-eval-both (completed, 8.5s, 1 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D AND dec']

On 2026-07-01, these documents were out of date:

- `confluence/architecture.xhtml`  
  - Updated: 2026-03-12  
  - Out of date because a later decision on 2026-05-04 changed the fact that it still “shows DocumentDB”.  
  - Source of the later decision: `meetings/2026-05-04-poc-review.txt`

- `confluence/decision-log.xhtml`  
  - Updated: 2026-06-03  
  - Out of date because a later decision on 2026-06-15 changed the fact that it “stops at 2026-06-01”.  
  - Source of the later decision: `meetings/2026-06-15-weekly-sync.txt`

- `docs/gateway.md`  
  - Updated: 2026-03-18  
  - Out of date for two reasons:
    - A decision on 2026-06-15 changed the fact that it “says retries are disabled on /deliver”.  
      - Source: `meetings/2026-06-15-weekly-sync.txt`
    - A decision on 2026-05-18 changed the fact that it “says the integration timeout is 10 s”.  
      - Source: `meetings/2026-05-18-weekly-sync.txt`

- `docs/iac-cloudformation.md`  
  - Updated: 2026-02-11  
  - Out of date because a later decision on 2026-04-20 changed the fact that it “says all infrastructure including networking moves to CloudFormation”.  
  - Source of the later decision: `meetings/2026-04-20-weekly-sync.t

### memory-eval-graph (completed, 9.8s, 1 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ']

The following documents were out of date on 2026-07-01, because later decisions changed facts in them:

- `confluence/architecture.xhtml` — outdated because a 2026-05-04 decision changed the fact it “shows DocumentDB.” Source: `meetings/2026-05-04-poc-review.txt` on 2026-05-04. The document was last updated on 2026-03-12.
- `confluence/decision-log.xhtml` — outdated because a 2026-06-15 decision changed the fact it “stops at 2026-06-01.” Source: `meetings/2026-06-15-weekly-sync.txt` on 2026-06-15. The document was last updated on 2026-06-03.
- `docs/gateway.md` — outdated because a 2026-06-15 decision changed the fact that it “says retries are disabled on /deliver.” Source: `meetings/2026-06-15-weekly-sync.txt` on 2026-06-15. The document was last updated on 2026-03-18.
- `docs/gateway.md` — also outdated because a 2026-05-18 decision changed the fact that it “says the integration timeout is 10 s.” Source: `meetings/2026-05-18-weekly-sync.txt` on 2026-05-18. The document was last updated on 2026-03-18.
- `docs/iac-cloudformation.md` — outdated because a 2026-04-20 decision changed the fact that it “says all infrastructure including networking moves to CloudFormation.” Source: `meet

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

### memory-eval-both (completed, 25.3s, 1 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ']

On **2026-10-05**, these documents were out of date, because later decisions had changed facts they contain:

- **confluence/architecture.xhtml** — updated **2026-03-12**  
  Out of date because later decisions changed:
  - **2026-05-04**: “shows DocumentDB”
  - **2026-08-03**: “shows EKS as the runtime”  
  Source: `meetings/2026-05-04-poc-review.txt`, `meetings/2026-08-03-architecture-committee.txt`

- **confluence/decision-log.xhtml** — updated **2026-06-03**  
  Out of date because **2026-06-15** changed the fact it “stops at 2026-06-01”.  
  Source: `meetings/2026-06-15-weekly-sync.txt`

- **confluence/migration-roadmap.xhtml** — updated **2026-06-20**  
  Out of date because **2026-08-03** changed the fact that it “lists compute decision as pending PoC”.  
  Source: `meetings/2026-08-03-architecture-committee.txt`

- **confluence/team-roster.xhtml** — updated **2026-07-08**  
  Out of date because **2026-09-07** changed the fact that it “lists Anna as retries owner”.  
  Source: `meetings/2026-09-07-security-review.txt`

- **docs/db-migration-plan.md** — updated **2026-05-26**  
  Out of date because later decisions changed:
  - **2026-10-05**: “has no cutover date”
  - **202

### memory-eval-graph (completed, 28.4s, 1 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ']

Documents that were out of date on 2026-10-05, and why:

- `confluence/architecture.xhtml` — outdated because later decisions changed what it shows:
  - a 2026-05-04 decision says it “shows DocumentDB”
  - a 2026-08-03 decision says it “shows EKS as the runtime”
  - source files: `meetings/2026-05-04-poc-review.txt`, `meetings/2026-08-03-architecture-committee.txt`
  - document updated: 2026-03-12

- `confluence/decision-log.xhtml` — outdated because a later decision changed the timeframe it reflects:
  - a 2026-06-15 decision says it “stops at 2026-06-01”
  - source file: `meetings/2026-06-15-weekly-sync.txt`
  - document updated: 2026-06-03

- `confluence/migration-roadmap.xhtml` — outdated because a later decision changed the compute status it describes:
  - a 2026-08-03 decision says it “lists compute decision as pending PoC”
  - source file: `meetings/2026-08-03-architecture-committee.txt`
  - document updated: 2026-06-20

- `confluence/team-roster.xhtml` — outdated because a later decision changed the retries ownership it lists:
  - a 2026-09-07 decision says it “lists Anna as retries owner”
  - source file: `meetings/2026-09-07-security-review.txt`
  - document updated: 2026

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

### memory-eval-both (completed, 4.4s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'DynamoDB singl", '"DynamoDB single-table design, chosen on PoC-1 results (p99 r" PoC цифры p99 rea']

Решение основано на **PoC-1: DynamoDB single-table vs multi-table**.

Цифры, на которых оно основано:
- **p99 read**: **4 ms** для single-table против **11 ms** для multi-table
- **cost at projected volume**: **38% ниже** (`single_table_cost_delta_pct: -38`)
- в отчёте PoC также указано, что baseline DocumentDB был **9 ms** p99 read

Ссылки на источники:
- **meetings/2026-05-04-poc-review.txt**, **2026-05-04** — решение: «DynamoDB single-table design, chosen on PoC-1 results (p99 read 4 ms vs 11 ms; 38% lower cost at projected volume).»
- **docs/poc-dynamodb-report.md**, **2026-05-01** — таблица результатов PoC-1 с цифрами:
  - DocumentDB: **9 ms**
  - DynamoDB multi-table: **11 ms**
  - DynamoDB single-table: **4 ms**
  - single-table cost: **$3,200 (-38%)**

### memory-eval-graph (completed, 4.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'DynamoDB singl"]

Решение основано на PoC-1: **“DynamoDB single-table vs multi-table”**; отчёт — **`docs/poc-dynamodb-report.md`**; дата решения — **2026-05-04**; источник решения — **`meetings/2026-05-04-poc-review.txt`**.

Цифры из результатов PoC:
- **single_table_p99_read_ms = 4**
- **multi_table_p99_read_ms = 11**
- **single_table_cost_delta_pct = -38**
- **documentdb_p99_read_ms = 9**

Источник цифр: **`docs/poc-dynamodb-report.md`** через связь PoC, а само решение зафиксировано в **`meetings/2026-05-04-poc-review.txt`** на **2026-05-04**.

Если хотите, я могу ещё найти точную формулировку решения целиком и кто его предложил/оспаривал.

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

### memory-eval-both (completed, 4.9s, 2 tool calls)
queries: ['"Relay moves to Lambda with provisioned concurrency on /deliv" PoC numbers resul', "MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'Relay moves to"]

Решение **«Relay moves to Lambda with provisioned concurrency on /deliver»** основано на **PoC-3: Relay on Lambda**.

Цифры, на которых оно основано:
- **p95 latency с provisioned concurrency:** **1.9 s**
- **p95 latency без provisioned concurrency:** **3.4 s**
- **cold start:** **1.2 s**
- **monthly cost:** **$3,600**
- **стоимость ниже EKS:** **-41%**
- В отчёте PoC также указано, что при provisioned concurrency на `/deliver` p95 был **1.9 s**.

Источники:
- **meetings/2026-08-03-architecture-committee.txt** — decision, дата **2026-08-03**
- **docs/poc-lambda-report.md** — report, updated **2026-07-24**
- **ADR-006** — updated **2026-08-05**

Если хочешь, я могу ещё показать, какие именно формулировки в ADR-006 ссылаются на эти цифры.

### memory-eval-graph (completed, 4.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(c:PoC)\nWHERE d.text STARTS WITH 'Relay moves to"]

Решение **«Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances»** основано на **PoC-3: Relay on Lambda**. Источник: `meetings/2026-08-03-architecture-committee.txt`, дата решения: **2026-08-03**.

Цифры из PoC:
- **p95 warm**: **1.9 s**
- **p95 cold**: **3.4 s**
- **cold start**: **1.2 s**
- **monthly cost**: **3600 USD**
- **cost delta vs EKS**: **-41%**

Источник PoC: `docs/poc-lambda-report.md`.

Если хотите, я могу еще показать формулировку решения дословно и связанное обоснование по этим цифрам.

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

### memory-eval-both (completed, 3.8s, 2 tool calls)
queries: ['"Keep Relay on EKS with autoscaling" PoC цифры p95 0.4 s rejected', "MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'Keep Relay on "]

Решение основано на **PoC-2: Relay on EKS with autoscaling**.  
Источник решения: **meetings/2026-08-03-architecture-committee.txt**, дата **2026-08-03**.

Цифры из PoC:
- **p95 delivery latency = 0.4 s**
- **monthly cost = $6,100**
- **ops effort**: «a second platform team» / в ADR сформулировано как «a second platform to run»

Источник PoC: **docs/poc-eks-report.md**, дата обновления **2026-07-24**.

### memory-eval-graph (completed, 6.2s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Keep Relay on EKS with autoscaling ", "MATCH (d:Decision) WHERE d.text STARTS WITH 'Keep Relay on EKS with autoscaling "]

Решение **«Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)»** основано на:

- **PoC:** **PoC-2: Relay on EKS with autoscaling**  
  **Источник:** `docs/poc-eks-report.md`  
  **Дата:** `2026-08-03`

- **Цифры из PoC:**  
  - **p95 = 0.4 s**  
  - **monthly_cost_usd = 6100**  
  - **ops_effort = "a second platform team"**  
  **Источник:** `docs/poc-eks-report.md`  
  **Дата:** `2026-08-03`

Само решение зафиксировано как:
- **D18** — `Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)`  
  **Источник:** `meetings/2026-08-03-architecture-committee.txt`  
  **Дата:** `2026-08-03`

Если хотите, я могу ещё показать, **какая именно формулировка в решении соответствует этим цифрам**.

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

### memory-eval-both (completed, 2.8s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-001'}) RETURN a.id, a.title, a.status, a.file"]

ADR-001 is **Superseded**.

- **ADR-001** — *“Migrate infrastructure code from Terraform to CloudFormation”*
- **Status:** Superseded
- **File:** `adr/ADR-001.md`

If you want, I can also look up what superseded it.

### memory-eval-graph (completed, 2.5s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-001'}) RETURN a.id, a.title, a.status, a.file"]

ADR-001 is **Superseded**. Source: `adr/ADR-001.md`, dated by the ADR record itself in the graph as `ADR-001` with status `Superseded` (no separate date field was returned in the retrieved ADR row).

### memory-eval-vector (completed, 4.8s, 3 tool calls)
queries: ["What is the status of ADR-001 ('Migrate infrastructure code from Terraform to Cl", 'ADR-001 Migrate infrastructure code from Terraform to CloudFormation status', 'status ADR-001 Terraform CloudFormation']

ADR-001 is **Superseded (superseded by ADR-004)**. Source: `adr/ADR-001.md` (updated **2026-01-14**). The ADR header explicitly says “Status: Superseded (superseded by ADR-004)”.

I also found ADR-004, which is **Accepted, supersedes ADR-001** in `adr/ADR-004.md` (updated **2026-04-22**). Since it is newer, ADR-004 is the current decision on this topic.

## t42 [en / adr_status] What is the status of ADR-005 ('Evaluate EKS and Lambda with two proofs of concept')?
**expected:** Superseded, superseded by ADR-006  
**expected sources:** {'sources': ['adr/ADR-005.md']}

### memory-eval-both (completed, 2.7s, 2 tool calls)
queries: ['ADR-005 Evaluate EKS and Lambda with two proofs of concept status', "MATCH (a:ADR {key:'adr-005'}) RETURN a.id, a.title, a.status, a.date, a.file"]

ADR-005 is **superseded** by ADR-006.

- **Source:** `adr/ADR-005.md`
- **Date:** `2026-06-17`

The vector memory also says:
- `status Superseded (superseded by ADR-006)`.

So the current status is **Superseded**.

### memory-eval-graph (completed, 2.8s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-005'}) RETURN a.id, a.title, a.status, a.file"]

ADR-005 is **Superseded** — source file: `adr/ADR-005.md`, date: **not in memory** for this ADR record.

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

### memory-eval-both (completed, 3.7s, 3 tool calls)
queries: ["MATCH (a:ADR {key:'adr-007'}) RETURN a.id, a.title, a.status, a.file, a.date", 'ADR-007 Keep Relay on EKS with autoscaling status', "MATCH (a:ADR) WHERE a.id = 'ADR-007' OR a.key = 'adr-007' RETURN a.id, a.title, "]

ADR-007 is **Rejected**.

- **Source:** `adr/ADR-007.md`
- **Date:** `2026-08-05`

The ADR record and the document both show status **Rejected**.

### memory-eval-graph (completed, 2.4s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.date, a.file"]

ADR-007 is **Rejected**. Source: `adr/ADR-007.md`, dated **2026-08-05**.

### memory-eval-vector (completed, 3.9s, 3 tool calls)
queries: ["What is the status of ADR-007 ('Keep Relay on EKS with autoscaling')?", 'ADR-007 Keep Relay on EKS with autoscaling status', 'status ADR-007 Keep Relay on EKS autoscaling']

ADR-007 is **Rejected**. The ADR record shows **Status: Rejected** and **Date: 2026-08-05**. Source: `adr/ADR-007.md` (updated 2026-08-05).

I also found a supporting decision chunk stating “Keep Relay on EKS with autoscaling (rejected…)” in `adr/ADR-007.md` (updated 2026-08-05).

## t44 [en / adr_status] What is the status of ADR-010 ('Gateway timeout policy for Lambda integrations')?
**expected:** Proposed; Never accepted; D20 (25 s) is the live decision and the ADR still proposes 20 s  
**expected sources:** {'sources': ['adr/ADR-010.md']}

### memory-eval-both (completed, 1.9s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.date, a.file"]

ADR-010 (“Gateway timeout policy for Lambda integrations”) is **Proposed**.

Source: `adr/ADR-010.md`, dated `2026-09-23`.

### memory-eval-graph (completed, 2.6s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.date, a.file"]

ADR-010 is **Proposed**.  
Source: `adr/ADR-010.md`, dated `2026-09-23`.

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

### memory-eval-both (completed, 3.1s, 1 tool calls)
queries: ['MATCH (d:Decision) WHERE d.text STARTS WITH $prefix OPTIONAL MATCH (d)-[:DEPENDS']

It depended on:

- **One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)** — **2026-02-09**, status **active**, source **meetings/2026-02-09-weekly-sync.txt**.

If you want, I can also check whether that dependency was later superseded.

### memory-eval-graph (completed, 3.3s, 1 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Front Relay with the API gateway; t"]

The decision **“Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack”** depended on:

- **“One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)”** — dated **2026-02-09**, source **`meetings/2026-02-09-weekly-sync.txt`**.  

That is the only dependency found in memory for this decision.

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
