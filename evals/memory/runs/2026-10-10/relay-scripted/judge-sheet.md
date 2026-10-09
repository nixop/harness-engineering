
## m01 [en / fact] What is the delivery latency SLO and what exactly does it measure?
**expected:** p95 2 s over 5 minutes, from POST /deliver accepted to the first delivery attempt sent, not to the customer's answer; success rate 99.5% monthly  
**expected sources:** {'sources': ['docs/slo.md', 'meetings/2026-01-26-weekly-sync.txt']}

### memory-eval-both (completed, 5.6s, 2 tool calls)
queries: ['delivery latency SLO what exactly does it measure', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:slo'}) WHERE d.status <> 'reje"]

The current delivery latency SLO is:

- **p95 = 3 s for 30 days after the serverless cutover, then back to 2 s**  
  Source: **meetings/2026-10-05-cutover-planning.txt**  
  Date: **2026-10-05**

What it measures:

- It measures **delivery latency from `POST /deliver` being accepted to the first delivery attempt being sent**.
- It **measures Relay, not the customer**: it ends when the first attempt is sent, **not when the customer responds**.  
  Source: **docs/slo.md**  
  Date: **2026-01-28**

I also found an older SLO doc/decision that said **2 s over 5 minutes**, but that decision is **superseded** by the newer 2026-10-05 decision, so it is not current.

### memory-eval-graph (completed, 6.0s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:$topic}) WHERE NOT (d)<-[:SUPERSEDES]', 'MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:$topic}) RETURN d.key AS key, d.text ']

The current delivery latency SLO is:

- **p95 delivery latency = 3 seconds for 30 days after the serverless cutover, then back to 2 seconds**  
  Source: `meetings/2026-10-05-cutover-planning.txt`, decision dated **2026-10-05**.

What it measures:

- The earlier SLO text spells it out as **“p95 end-to-end delivery latency”**.  
  Source: `meetings/2026-01-26-weekly-sync.txt`, decision dated **2026-01-26**.
- That earlier decision is **superseded** by the 2026-10-05 decision above.

Also, the note on the current decision says `docs/slo.md` is **stale**: it still says **p95 2 s with no stabilisation window**, but the newer decision on **2026-10-05** changed that.  
Source: `meetings/2026-10-05-cutover-planning.txt`, decision dated **2026-10-05**.

If you want, I can also give you the full SLO, including the delivery success-rate part from the older decision.

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

### memory-eval-both (completed, 2.3s, 1 tool calls)
queries: ['delivery queue dead-letter retry attempts delays retries backoff dead letter']

Очередь делает **5 попыток** до dead-letter queue. Задержки между попытками: **30 s, 2 min, 10 min, 30 min, 2 h**.

Источник:
- `docs/retries-dlq.md`, раздел **Mechanism**, updated **2026-08-27**
- `adr/ADR-009.md`, раздел **Decision**, updated **2026-08-26**

### memory-eval-graph (completed, 5.9s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nWHERE d.status <> 'r"]

Очередь делает **5 попыток** до dead-letter, затем сообщение уходит в DLQ. Источник: решение `decision:retries:2026-08-24` в `meetings/2026-08-24-weekly-sync.txt`, зафиксировано также в `adr/ADR-009.md`, дата **2026-08-24**.

По **задержкам** в найденном решении ничего не сказано — в памяти есть только число попыток и факт перехода в DLQ, но **задержки не в памяти**. Источники: `meetings/2026-08-24-weekly-sync.txt` и `adr/ADR-009.md`, дата **2026-08-24**.

Я также нашёл более старые, уже **superseded** решения по retries:
- `meetings/2026-06-15-weekly-sync.txt`, дата **2026-06-15** — max 3 attempts;
- `meetings/2026-03-30-weekly-sync.txt`, дата **2026-03-30** — retries disabled on POST /deliver.



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
queries: ['hybrid IaC layout keep networking in Terraform why networking in Terraform ratio', 'why networking stays in Terraform decision rationale ADR-004 networking stays in']

Because ADR-004 says the networking module was the last and hardest part to move: cross-account peering and DNS delegation would need CloudFormation custom resources, while the same networking is already expressed natively in the Terraform the network team maintains. So the chosen boundary was to keep VPC, peering, and DNS in Terraform and move application stacks to CloudFormation. Source: `adr/ADR-004.md`, updated `2026-04-22`.

Also, the hybrid layout doc says this decision supersedes ADR-001, so this is the current state. Source: `docs/iac-hybrid.md`, updated `2026-04-24`.

### memory-eval-graph (completed, 6.0s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERSE", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'})-[:OWNS]-(p:Person) RETUR"]

The hybrid IaC layout keeps networking in Terraform because the current decision says to do so: “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation.” Source: `meetings/2026-04-20-weekly-sync.txt`, decision date `2026-04-20`.

This is also the current decision on the IaC topic; it supersedes the earlier CloudFormation-only direction from:
- `meetings/2026-02-09-weekly-sync.txt` (`2026-02-09`): “One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)”
- `meetings/2026-01-12-weekly-sync.txt` (`2026-01-12`): “Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1”

I don’t see a rationale beyond the layout itself in memory. The only related note I found is that the 2026-04-20 decision says the older doc is stale: `docs/iac-cloudformation.md` updated `2026-02-11` still said all infrastructure, including networking, moves to CloudFormation, but that was superseded by the `2026-04-20` decision.

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['Why does the hybrid IaC layout keep networking in Terraform?', 'hybrid IaC layout keep networking in Terraform', 'networking in Terraform hybrid IaC layout']

The memory says **networking stays in Terraform because ADR-004 fixed the hybrid boundary**: VPC, peering, and DNS are kept in Terraform, while data/compute/gateway application stacks move to CloudFormation. The recorded consequence is that **both sides run drift detection**, and Terraform state was cleaned of resources already imported into stacks. Source: **adr/ADR-004.md** and **meetings/2026-04-20-weekly-sync.txt** (2026-04-22, 2026-04-20).

There is also a hand-off reason in the docs: Terraform exports network outputs to SSM Parameter Store, and CloudFormation reads them with dynamic references; changing a network output requires a Terraform apply and then a CloudFormation deploy, with no automatic trigger. Source: **docs/iac-hybrid.md** (2026-04-24).

If you want, I can also summarize the **full hybrid layout boundary** from memory.

## m04 [ru / contradiction] В gateway.md написано, что таймаут интеграции 10 секунд. Это актуально?
**expected:** нет; документ от 2026-03-18, таймаут менялся на 30 с (2026-05-18) и на 25 с (2026-08-24); текущее значение 25 с  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 5.4s, 2 tool calls)
queries: ['gateway.md integration timeout 10 seconds current decision timeout gateway', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:timeouts'})\nWHERE d.status <> "]

Нет, это не актуально.

В памяти есть более новая текущая decision по `topic:timeouts`:  
- `decision:timeouts:2026-08-24` — дата `2026-08-24`, статус `active`, источник `meetings/2026-08-24-weekly-sync.txt`. В ней сказано: **gateway integration timeout lowered from 30 s to 25 s**.

Значит `docs/gateway.md`, где указано **10 seconds** и обновление `2026-03-18`, устарел относительно этой decision.

Что я нашёл:
- `docs/gateway.md` — утверждает 10 s, updated `2026-03-18`
- текущая decision по таймаутам — `2026-08-24`, source `meetings/2026-08-24-weekly-sync.txt`, timeout = 25 s



### memory-eval-graph (completed, 6.0s, 2 tool calls)
queries: ["MATCH (t:Topic {key:$topic})<-[:ABOUT]-(d:Decision)\nWHERE d.status <> 'rejected'", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'})\nRETURN d.key AS dke"]

Нет, **не актуально**.

По памяти:
- **2026-03-16** — в `meetings/2026-03-16-weekly-sync.txt` было решение: “Gateway integration timeout 10 s on every Relay route”. Сейчас оно **superseded**.
- **2026-05-18** — в `meetings/2026-05-18-weekly-sync.txt` таймаут подняли с 10 s до 30 s. Это решение **superseded**.
- **2026-08-24** — в `meetings/2026-08-24-weekly-sync.txt` текущий активный таймаут снижен с 30 s до **25 s**.

Дополнительно: `docs/gateway.md` был уже **устаревшим** на 2026-05-18; в памяти есть примечание, что он всё ещё говорил про 10 s, но это было stale по решению от 2026-05-18.

Если хотите, могу ещё отдельно показать, **какое именно решение делает `gateway.md` устаревшим**.

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
queries: ['Anna owns retries roster page current owner retries Anna', "MATCH (t:Topic {key:'topic:retries'})<- [o:OWNS]-(p:Person)\nRETURN p.name AS own"]

No — Anna is not the current owner of retries today.

Current owner in memory:
- Ivan Melnik owns retries from 2026-09-07 onward.

Anna’s ownership was earlier:
- Anna Sokolova owned retries from 2026-06-01 to 2026-09-07.

Sources:
- `memory/decisions.jsonl` claim `ownership:retries:2026-09-07` dated 2026-09-07.
- Graph `OWNS` relationship for `topic:retries` with `from=2026-09-07, to=null`.

So if the roster page still says Anna, it is stale.

### memory-eval-graph (completed, 6.1s, 2 tool calls)
queries: ["MATCH (p:Person {key:'person:anna-sokolova'})-[o:OWNS]->(t:Topic {key:'topic:ret", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (d)<-[:SUP"]

No — not today.

- The current owner of `topic:retries` is still Anna Sokolova, but only **from 2026-06-01 to 2026-09-07**; there is **no current OWNS row with `to = null`** for Anna on retries, so the roster page is stale on ownership as of today. Source: graph ownership record, dated **2026-06-01** to **2026-09-07**.
- The current decision on retries is from **2026-08-24** (`meetings/2026-08-24-weekly-sync.txt`): “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off.” This does not say ownership changed, but it is the latest retries decision in memory. Source: decision `decision:retries:2026-08-24`, dated **2026-08-24**.

What I retrieved:
- Ownership edge for Anna on retries.
- Current active decision on retries.

If you want, I can also check whether anyone else currently owns retries.

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['The team roster page says Anna owns retries. Is that right today?', 'Anna owns retries', 'retries owner Anna']

No — Anna does **not** own retries today. The current decision says **Ivan Melnik** owns retries from **2026-09-07**. Source: **meetings/2026-09-07-security-review.txt** (2026-09-07).

The team roster page is stale on this point: it still lists **Anna Sokolova** as retries owner, but it was updated on **2026-07-08**, and the newer ownership decision supersedes it. Source: **confluence/team-roster.xhtml** (2026-07-08) and **meetings/2026-09-07-security-review.txt** (2026-09-07).

## m06 [ru / contradiction] Decision log в Confluence актуален?
**expected:** нет; последняя версия 2026-06-03, в нём нет решений после 1 июня: ретраи на gateway (06-15), два PoC (06-15), передача PoC Ване (07-13), выбор Lambda (08-03), таймаут 25 с и ретраи через SQS (08-24), SSM (09-07), бюджет (09-21), даты катовера (10-05)  
**expected sources:** {'sources': ['confluence/decision-log.xhtml', 'memory/decisions.jsonl']}

### memory-eval-both (completed, 4.2s, 2 tool calls)
queries: ['Decision log Confluence актуален current status updated stale decision log Confl', "MATCH (d:Document {title:'Decision log'}) RETURN d.file AS file, d.updated AS up"]

Да — в памяти это **актуальный** документ.

- **Decision log**: `confluence/decision-log.xhtml`, updated **2026-06-03**.
- В самой записи он помечен как updated 2026-06-03 и содержит текущий список решений.  
  Источник: `confluence/decision-log.xhtml`, дата **2026-06-03**.

Дополнительно: в памяти нет более нового решения, которое делало бы сам **Decision log** устаревшим.

### memory-eval-graph (completed, 5.3s, 2 tool calls)
queries: ["MATCH (d:Document) WHERE toLower(d.title) CONTAINS 'decision log' OR toLower(d.f", 'MATCH (dec:Decision)-[:MAKES_STALE]->(doc:Document) WHERE toLower(doc.title) CON']

Нет, `Decision log` в Confluence не актуален: по памяти есть более новая decision, которая делает его устаревшим.

- Документ `confluence/decision-log.xhtml` — **Decision log**, updated `2026-06-03`.  
- Decision `decision:retries:2026-06-15` от `2026-06-15` помечает этот документ как stale (`MAKES_STALE`) и имеет статус `superseded`.  

Источник:  
- `confluence/decision-log.xhtml` — updated `2026-06-03`  
- decision `decision:retries:2026-06-15` — `2026-06-15`

Что я проверил:
- нашёл документ `Decision log`;
- нашёл decision, которая делает его устаревшим.

Если хотите, могу ещё сказать, **с какой даты** он стал неактуален и **какой именно факт** в нём устарел.

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

### memory-eval-both (completed, 5.2s, 2 tool calls)
queries: ['ADR-010 gateway timeout Lambda 20 s policy current decision timeout topic gatewa', "MATCH (d:Decision)-[:RECORDED_IN]->(a:ADR {id:'ADR-010'})\nOPTIONAL MATCH (d)-[:S"]

Not in memory as a current policy.

What I retrieved:
- ADR-010 is **Proposed** and says in the document body: “20 s on every route, with per-route overrides.” Source: `adr/ADR-010.md`, updated `2026-09-23`.
- The ADR text also says it is **proposed, not accepted** and that the live value was set by the team on `2026-08-24` at **25 s**. Source: `adr/ADR-010.md`, updated `2026-09-23`.

So the memory indicates the ADR is **not** the policy; it is a proposal, and the live decision is **25 s**, not 20 s.

### memory-eval-graph (completed, 5.7s, 3 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-010'}) RETURN a.key AS key, a.id AS id, a.title AS title, ", "MATCH (d:Decision)-[:RECORDED_IN]->(a:ADR {id:'ADR-010'}) RETURN d.key AS dkey, ", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) RETURN d.key AS dke"]

No — in memory, the current policy is **25 s**, not 20 s.

Sources:
- **Decision D20** in `meetings/2026-08-24-weekly-sync.txt` dated **2026-08-24**: “Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom”
- **ADR-010** in `adr/ADR-010.md` dated **2026-09-23** is **Proposed**, so it is not the current policy.

Also, the earlier timeout decisions are superseded:
- **D12** dated **2026-05-18** — superseded
- **D06** dated **2026-03-16** — superseded

So ADR-010’s “20 s” does **not** match the current policy in memory.

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

### memory-eval-both (completed, 6.3s, 2 tool calls)
queries: ['runbook катовер откат TBD владелец кто на самом деле owner rollback runbook cuto', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:cutover'})\nOPTIONAL MATCH (d)<"]

На самом деле владелец отката — **Lena Kim**.

Что нашёл:
- В решении по катоверу от **2026-10-05** сказано: **“Rollback owner for both cutovers is Lena. Owner: Lena Kim.”**
  - источник: `meetings/2026-10-05-cutover-planning.txt`
  - дата: `2026-10-05`
- Этот же источник помечает старую формулировку в runbook как устаревшую: **“docs/runbook-cutover-serverless.md (updated 2026-09-29) still says rollback owner TBD”**
  - источник: `meetings/2026-10-05-cutover-planning.txt`
  - дата: `2026-10-05`

То есть runbook с `TBD` — устарел по сравнению с решением от 2026-10-05.

### memory-eval-graph (completed, 3.8s, 2 tool calls)
queries: ["MATCH (d:Document) WHERE toLower(d.file) CONTAINS 'runbook' AND toLower(d.file) ", "MATCH (t:Topic {key:'topic:cutover'})<-[:ABOUT]-(dec:Decision) RETURN dec.key AS"]

На самом деле владелец отката — **Лена**.

- Источник: `meetings/2026-10-05-cutover-planning.txt`
- Решение от **2026-10-05**: “Rollback owner for both cutovers is Lena”
- Это **новее**, чем runbook `docs/runbook-cutover-serverless.md` (обновлён **2026-09-29**), поэтому runbook устарел.

Если нужно, могу ещё проверить, есть ли в графе явная запись об ownership у Лены по topic:cutover.

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['В runbook катовера написано, что владелец отката TBD. Кто на самом деле?', 'runbook катовера владелец отката TBD кто владелец', 'rollback owner cutover runbook TBD who owns rollback']

На самом деле владелец отката — **Lena Kim**. Это зафиксировано в решении от **2026-10-05**: “Rollback owner for both cutovers is Lena. Owner: Lena Kim.”  
Источник: `meetings/2026-10-05-cutover-planning.txt` — **2026-10-05**.

Замечание: runbook с `TBD` уже устарел по сравнению с этим решением. В найденных материалах runbook `docs/runbook-cutover-serverless.md` упомянут как обновлённый **2026-09-29**, но решение новее.

## m09 [ru / crosslingual] Что на митингах называли «провижнд конкаренси» и почему без этого не проходит SLO?
**expected:** provisioned concurrency: прогретые инстансы Lambda на /deliver; без них p95 3.4 с при SLO 2 с, с ними 1.9 с (PoC-3)  
**expected sources:** {'sources': ['docs/poc-lambda-report.md', 'meetings/2026-07-27-poc-review.txt', 'adr/ADR-006.md']}

### memory-eval-both (completed, 12.0s, 2 tool calls)
queries: ['"провижнд конкаренси" SLO why not pass meetings relay webhook delivery', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:compute'}) WHERE toLower(d.tex"]

На митингах под «провижнд конкаренси» имели в виду **Lambda с provisioned concurrency на `/deliver`**.

Что есть в памяти:
- Решение от **2026-08-03**:  
  **“Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances”**  
  Источник: `meetings/2026-08-03-architecture-committee.txt`  
  Статус: `active`
- В обсуждении PoC от **2026-07-27** сказали:  
  **“провижнд конкаренси на deliver обязательно без него не проходим”**  
  и рядом:  
  **“SLO две секунды это про первую попытку доставки … одна и девять проходит”**  
  Источник: `meetings/2026-07-27-poc-review.txt`
- В SLO-документе от **2026-01-28** записано, что SLO по latency — это **2 s** от `POST /deliver` accepted до **первой попытки доставки**, а не до ответа клиента.  
  Источник: `docs/slo.md`  
  Но этот документ **устарел**, потому что более позднее решение от **2026-08-03** уже явно фиксирует `p95 1.9 s with warm instances` и делает provisioned concurrency частью решения.  

Почему без этого “не проходит SLO”:
- По памяти митинга, без provisioned concurrency время было на грани SLO: **1.9 s проходит, но без запаса**, а SLO для latency — **2 s** д

### memory-eval-graph (completed, 11.0s, 6 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE toLower(d.text", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE toLower(d.text) CO", "MATCH (m:Meeting)<-[:DECIDED_IN]-(d:Decision)-[:ABOUT]->(:Topic {key:'topic:comp", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) RETURN d.date AS date, d", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) RETURN d.date AS da", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) RETURN d.date AS dat"]

На митингах под «provisioned concurrency» имели в виду запуск Relay на Lambda с **pre-warmed instances** для `/deliver`, чтобы держать p95 в пределах SLO.

Что нашёл в памяти:
- **Решение по compute**: `Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances`
  - дата: **2026-08-03**
  - источник: **meetings/2026-08-03-architecture-committee.txt**
- **SLO по доставке**:
  - актуальное решение: `Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s`
  - дата: **2026-10-05**
  - источник: **meetings/2026-10-05-cutover-planning.txt**
- **Почему без этого не проходит SLO**: в том же решении по compute сказано, что PoC-3 дал **p95 1.9 s with warm instances**, то есть provisioned concurrency нужен, чтобы сохранять warm instances и укладываться в p95. Без него в памяти нет отдельного решения с формулировкой причины, но связь именно такая следует из решения от **2026-08-03**.

Если нужен совсем короткий ответ:  
**Это прогрев Lambda-инстансов для `/deliver`; без warm instances p95 не укладывается в SLO.**  
Источник: `meetings/2026-08-03-architecture-committee.txt` от

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

### memory-eval-both (completed, 6.4s, 2 tool calls)
queries: ['дрифт rule came out of it team meant by дрифт', 'дрифт detection rule manual changes console change freeze template wins incident']

By **“дрифт”** the team meant **infrastructure drift**: the stack had diverged from what was in the template because someone made a **manual console change**.

What rule came out of it:
- **No manual changes in the AWS console for production resources that belong to a Relay stack.**
- **Every Relay stack runs `DetectStackDrift` nightly at 01:00.**
- **A stack in `DRIFTED` state blocks the pipeline until it is reconciled.**

Sources:
- **meetings/2026-02-23-incident-review.txt** — 2026-02-23: the review says someone changed the load balancer timeout by hand, the stack drifted, and Lena proposed banning manual console changes and enabling nightly drift detection with alerts.
- **meetings/2026-02-23-incident-review.txt** / claim **D04** — 2026-02-23: “Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call.”
- **docs/drift-detection.md** — updated 2026-02-25: records the rules above.

If you want, I can also quote the exact Russian lines from the incident review.

### memory-eval-graph (completed, 6.0s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:iac'}) WHERE d.text CONTAINS '", "MATCH (o:OpenItem)-[:ABOUT]->(t:Topic {key:'topic:iac'}) WHERE o.text CONTAINS '", "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:iac'}) WHERE d.text CONTAINS '"]

By **“дрифт”** the team meant **infrastructure drift**: manual console changes that make deployed infrastructure diverge from the declared IaC state.

The rule that came out of it was:

- **Manual console changes are frozen**
- **Nightly drift detection runs on every stack**
- **Drift alerts go to on-call**

**Source:** `meetings/2026-02-23-incident-review.txt`, decision `decision:iac:2026-02-23`, dated **2026-02-23**.

I also found the related open item:

- `openitem:iac:2026-02-23` — “Route drift-detection alerts to on-call”, raised **2026-02-23**, status **closed**.

If you want, I can also look for whether this rule later got superseded or tied to a specific ADR.

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

### memory-eval-both (completed, 11.6s, 4 tool calls)
queries: ['gateway retries /deliver turned off in August turned on in June why, decision, r', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:gateway'}) WHERE d.text CONTAI", "MATCH (adr:ADR)-[:RECORDED_IN]->(d:Decision)-[:ABOUT]->(t:Topic {key:'topic:gate", "MATCH (dec:Decision)-[:ABOUT]->(t:Topic {key:'topic:gateway'}) RETURN dec.key AS"]

Not in memory.

What I retrieved:
- Vector store hits on gateway retries /deliver:
  - `docs/idempotency.md` updated `2026-05-20`: says gateway retries on `/deliver` were disabled because a retried delivery could reach a customer twice; retries can be enabled once callers send idempotency keys.
  - `docs/gateway.md` updated `2026-03-18`: says retries on `POST /deliver` are disabled because delivery is not idempotent yet and a retried request can reach the customer twice.
  - `docs/retries-dlq.md` updated `2026-08-27`: says decided `2026-08-24` in `ADR-009`; retries are no longer a gateway policy.
  - `adr/ADR-002.md` updated `2026-03-04`: retries disabled on `POST /deliver` until idempotency keys exist because a retried delivery can reach a customer twice.
  - `adr/ADR-009.md` updated `2026-08-26`: options considered include “Keep gateway retries and deduplicate in the handler” vs “Retries in SQS with a dead-letter queue ...; gateway retries off on /deliver (chosen)”.

- Graph lookup:
  - I found only one gateway decision node in the graph: `decision:gateway:2026-03-02` about the gateway stack, not about retries.

So the memory has an explanation for why retries were turned off gen

### memory-eval-graph (completed, 10.1s, 7 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'})\nWHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'})\nWHERE (d.text CONTAI", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'})\nRETURN d.key AS key,", "MATCH (o:OpenItem)-[:ABOUT]->(:Topic {key:'topic:gateway'})\nRETURN o.key AS key,", "MATCH (d:Decision)\nWHERE d.text CONTAINS 'retry' OR d.note CONTAINS 'retry' OR d", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'})\nRETURN d.key AS key", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nRETURN d.key AS key,"]

Gateway retries on `/deliver` were turned off in August because the team decided to move retries out of the gateway and into SQS with a dead-letter queue after 5 attempts.

Sources:
- `meetings/2026-08-24-weekly-sync.txt` — decision `decision:retries:2026-08-24` — date `2026-08-24`
- The current decision on retries is this August decision; the earlier June enablement was superseded:
  - `meetings/2026-06-15-weekly-sync.txt` — decision `decision:retries:2026-06-15` — date `2026-06-15` — superseded
  - `meetings/2026-03-30-weekly-sync.txt` — decision `decision:retries:2026-03-30` — date `2026-03-30` — superseded

The graph does not contain a more detailed rationale beyond that move to SQS/DLQ.

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

### memory-eval-both (completed, 8.0s, 2 tool calls)
queries: ['Terraform network remained chain of events why network stayed in Terraform what ', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:iac'})\nOPTIONAL MATCH (d)-[:DE"]

Цепочка по памяти такая:

1. **2026-01-12** — было первоначальное решение по IaC, которое затем стало **superseded**.  
   Источник: `meeting:2026-01-12`  
   Это решение позже было заменено.  

2. **2026-02-09** — следующее решение по IaC.  
   Источник: `meeting:2026-02-09`  
   По графу оно остаётся **active**.  

3. **2026-02-23** — решение, принятое после incident review.  
   Источник: `meeting:2026-02-23:incident-review`  
   Оно тоже остаётся **active**.  

4. **2026-04-20** — итоговое решение:  
   **networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation**.  
   Источник: `meeting:2026-04-20`  
   Статус: **active**  
   Это решение **supersedes** `decision:iac:2026-01-12`.

Вывод: сеть осталась в Terraform из-за более позднего решения **2026-04-20**, которое закрепило гибридную схему и заменило ранний курс на полный перенос.

Если хотите, я могу ещё разложить это как **полную хронологию причинно‑следственных шагов** по каждому из решений IaC.

### memory-eval-graph (completed, 9.3s, 3 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nOPTIONAL MATCH (d)-[:SUPERSED', 'MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nOPTIONAL MATCH (p:Person)-[:P', 'MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})-[:OWNS]->(x)\nRETURN labels(x)']

Цепочка в памяти выглядит так:

1. **2026-01-12 — D01**: предложили перейти с Terraform на CloudFormation по частям, «module by module», и завершить к концу Q1.  
   **Источник:** Decision `D01`, дата `2026-01-12`.

2. **2026-02-09 — D03**: закрепили целевую структуру CloudFormation — один root stack на окружение и nested stacks по компонентам, включая **network**.  
   **Источник:** Decision `D03`, дата `2026-02-09`.

3. **2026-04-20 — D09**: это решение **supersedes D01** и меняет курс на гибридный IaC: **networking (VPC, peering, DNS) остаётся в Terraform**, а application stacks — в CloudFormation.  
   **Источник:** Decision `D09`, дата `2026-04-20`.

Итог: сеть осталась в Terraform не как отдельное «исключение» в ранних записях, а потому что более позднее решение **D09** явно зафиксировало гибридную схему и **переопределило** ранний план полного перехода на CloudFormation.  
**Источник:** Decision `D09`, дата `2026-04-20`.

Что я дополнительно проверил:
- Нашёл все решения по `topic:iac` в памяти.
- Среди них только `D09` явно говорит, что networking остаётся в Terraform.
- Других связанных решений/цепочек в памяти не оказалось.

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

### memory-eval-both (completed, 5.4s, 1 tool calls)
queries: ['MATCH (oi:OpenItem)<-[:CLOSES]-(d:Decision)\nWITH oi, d, date(oi.raised) AS raise']

The longest-standing open item that was closed by a decision is:

- Open item: `openitem:database:2026-05-04` (raised on `2026-05-04`)
- Decision: `decision:database:2026-08-10`
- Decision text: “DynamoDB migration dry run on a production snapshot is owned by Sergey, due 2026-09-04”
- Decision source file: `meetings/2026-08-10-weekly-sync.txt`
- Decision date: `2026-08-10`

Who took it:
- Sergey

How many times it had been raised before:
- 4 times in `raised_again`
- So, it had been raised 5 times total including the original raise

Source:
- Graph record for `openitem:database:2026-05-04` and `decision:database:2026-08-10`, dated `2026-08-10` and `2026-05-04` respectively.

### memory-eval-graph (completed, 5.1s, 2 tool calls)
queries: ['MATCH (oi:OpenItem)\nRETURN oi.key AS key, oi.text AS text, oi.raised AS raised, ', 'MATCH (d:Decision)-[:CLOSES]->(oi:OpenItem)\nRETURN d.key AS decision_key, d.text']

The longest-standing open item that was closed in the graph is:

- **Decision:** `decision:database:2026-08-10` — “DynamoDB migration dry run on a production snapshot is owned by Sergey, due 2026-09-04”
- **Who took it:** **Sergey** (`person:sergey-belov`), per the decision text
- **Open item it closed:** `openitem:database:2026-05-04` — “DynamoDB migration dry run on a production snapshot”
- **How many times it had been raised before:** **4** times (`raised_again_count = 4`)

Sources:
- Decision file: `meetings/2026-08-10-weekly-sync.txt`, date **2026-08-10**
- Open item raised: **2026-05-04**

I retrieved the set of closed open items and compared their raised dates; this one is the earliest raised among the closed items returned.

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

### memory-eval-both (completed, 6.2s, 3 tool calls)
queries: ['January objection to moving to CloudFormation and April hybrid discussion who ob', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:iac'}) RETURN d.key AS key, d.", "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:iac'})<-[:DECIDED_IN]-(m:Meeti"]

Возражал **Тимур Алиев**. В январе он сказал: **«я против, но не блокирую; запишите мое возражение»**. Источник: `meetings/2026-01-12-weekly-sync.txt`, дата **2026-01-12**.

В апреле, когда обсуждали гибридный вариант, его позиция в памяти не отражена напрямую в графе по decision:iac:2026-04-20, но из найденной записи видно, что текущая гибридная схема была **принята**, а возражение было зафиксировано за **Pavel Grishin** в ADR-004. Источник: `adr/ADR-004.md`, дата **2026-04-22**.

Если хотите, я могу ещё точно проверить по графу, был ли именно Тимур участником апрельского обсуждения гибрида.

### memory-eval-graph (completed, 5.1s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'})\nWHERE d.date STARTS WITH", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'})\nWHERE d.date STARTS WITH"]

В январе против переезда на CloudFormation возражал **Тимур Алиев** (`person:timur-aliev`) — по решению от **2026-01-12**: “Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1”.

В апреле, когда обсуждали гибрид, позицию занял **Павел Гришин** (`person:pavel-grishin`) — по решению от **2026-04-20**: “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation”.

Источники:  
- Decision `decision:iac:2026-01-12` — **2026-01-12**  
- Decision `decision:iac:2026-04-20` — **2026-04-20**

### memory-eval-vector (completed, 5.7s, 3 tool calls)
queries: ['Кто возражал против переезда на CloudFormation в январе и какую позицию он занял', 'возражал против переезда на CloudFormation в январе hybrid апрель позиция', 'January CloudFormation opposed April hybrid position']

В январе против переезда на CloudFormation возражал **Тимур Алиев**: в weekly sync от **2026-01-12** он сказал «я против, но не блокирую», и его возражение записали. Источник: `meetings/2026-01-12-weekly-sync.txt` (2026-01-12).

В апреле, когда обсуждали гибрид, в ADR-004 зафиксирована позиция **объединённая**: **сеть остаётся в Terraform, а application stacks — в CloudFormation**. Там же записано, что возражение было от **Pavel Grishin**. Источник: `adr/ADR-004.md` (2026-04-22).

Если вы имели в виду одного и того же человека, то в памяти есть несостыковка: январское возражение относится к Тимуру, а апрельское — к Павлу.

## m15 [en / point_in_time] On 2026-07-01, who owned retries, who owned the serverless PoC, and was the dry run owned?
**expected:** retries: Anna (since 06-01); serverless PoC: Sergey (until 07-13); dry run: no owner  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-06-29-weekly-sync.txt']}

### memory-eval-both (completed, 7.8s, 4 tool calls)
queries: ["MATCH (t:Topic) WHERE t.key IN ['topic:retries'] OPTIONAL MATCH (p:Person)-[o:OW", "MATCH (p:PoC {name:'serverless'}) OPTIONAL MATCH (owner:Person)-[o:OWNS]->(p) WH", "MATCH (o:OpenItem) WHERE toLower(o.text) CONTAINS 'dry run' OPTIONAL MATCH (p:Pe", 'serverless PoC ownership PoC serverless owned by who']

On 2026-07-01:

- retries: no owner found in memory for that date.
- serverless PoC: not in memory as a graph object/ownership edge I could verify for 2026-07-01. The closest memory claim says serverless PoC ownership moved from Sergey to Ivan on 2026-07-13, so that July 13 claim is later than your date and does not answer ownership on July 1.
- dry run: no owner found in memory for that date. The open item “DynamoDB migration dry run on a production snapshot” was raised on 2026-05-04, with no owner.

What I retrieved:
- Graph lookup for retries ownership on 2026-07-01: no owner.
- Graph lookup for a serverless PoC node: no matching PoC ownership edge found.
- Vector memory claim for serverless PoC ownership: 2026-07-13, owner Ivan Melnik, from `meetings/2026-07-13-weekly-sync.txt`.
- Graph lookup for the dry run open item: open item `openitem:database:2026-05-04`, raised 2026-05-04, no owner.

### memory-eval-graph (completed, 8.2s, 3 tool calls)
queries: ["MATCH (t:Topic) WHERE t.key IN ['topic:retries','topic:compute','topic:database'", "MATCH (p:PoC) WHERE p.name CONTAINS 'serverless' OPTIONAL MATCH (owner:Person)-[", "MATCH (t:Topic {key:'topic:database'}) OPTIONAL MATCH (p:Person)-[o:OWNS]->(t) W"]

On 2026-07-01:

- **Retries** was owned by **person:anna-sokolova** — ownership from **2026-06-01** to **2026-09-07**.  
  Source: graph memory, `OWNS` on `topic:retries` / `topic:compute` query result, date range covering 2026-07-01.

- **Serverless PoC**: **not in memory** as an owned item with that name. I searched PoCs whose name contains **“serverless”** and got no matches.  
  Source: graph memory query on `PoC.name`, date 2026-07-01.

- **Dry run**: I could not confirm ownership from the retrieved data. The only directly checked topic ownership result was for `topic:database`, which had **person:denis-orlov** as owner on 2026-07-01, but that does **not** establish that “dry run” was owned.  
  Source: graph memory query on `topic:database`, date 2026-07-01.

What I retrieved:
- `topic:retries` owner on 2026-07-01: **person:anna-sokolova**
- No `PoC` with name containing “serverless”
- `topic:database` had one owner on 2026-07-01: **person:denis-orlov**

If you want, I can do one more pass to check whether “dry run” corresponds to a specific topic or open item key in memory.

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

### memory-eval-both (completed, 5.8s, 2 tool calls)
queries: ["MATCH (t:Topic {key:'topic:timeouts'})<-[:ABOUT]-(d:Decision)\nWHERE d.date <= da", "MATCH (t:Topic {key:'topic:timeouts'})<-[:ABOUT]-(d:Decision)\nWHERE d.date <= '2"]

На 1 июля 2026 для gateway действовал таймаут **30 s**.

Владелец: **Pavel Grishin** (`person:pavel-grishin`).

Источник:
- **decision:timeouts:2026-05-18** — от **2026-05-18**: “Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14”.

Если хотите, могу ещё проверить, не было ли более позднего решения, которое это изменило к той дате.

### memory-eval-graph (completed, 8.6s, 2 tool calls)
queries: ["MATCH (t:Topic {key:'topic:timeouts'})<-[:ABOUT]-(d:Decision)\nWHERE d.date <= '2", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'})\nWHERE d.date <= '20"]

На 2026-07-01 в памяти есть только две найденные решения по `topic:timeouts`, и обе к этой дате уже **superseded**, поэтому актуального решения на 1 июля 2026 в памяти нет.

Что найдено:
- `meetings/2026-03-16-weekly-sync.txt` — решение от `2026-03-16`: **gateway integration timeout 10 s on every Relay route**; статус `superseded`.
- `meetings/2026-05-18-weekly-sync.txt` — решение от `2026-05-18`: **gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14**; статус `superseded`.

Владелец:
- На обеих найденных записях владельцем указан `person:pavel-grishin` (`паша`), но это относится к этим решениям, а не к найденному актуальному решению на 2026-07-01.

Итог: **в памяти нет подтверждённого действовавшего таймаута gateway на 2026-07-01**; найденные записи только показывают историю и владельца решений:
- `meetings/2026-03-16-weekly-sync.txt`, `2026-03-16`
- `meetings/2026-05-18-weekly-sync.txt`, `2026-05-18`



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

### memory-eval-both (completed, 8.1s, 2 tool calls)
queries: ['architecture committee 2026-08-03 decisions open item raised meeting', 'MATCH (m:Meeting {date:$date})<-[:DECIDED_IN]-(d:Decision)\nOPTIONAL MATCH (oi:Op']

At the architecture committee on **2026-08-03**, the following decisions were made:

1. **Relay moves to Lambda with provisioned concurrency on /deliver**  
   - Decision key: `decision:compute:2026-08-03:d17`  
   - Status: **active**  
   - Note: `confluence/architecture.xhtml (updated 2026-03-12) still shows EKS as the runtime; confluence/migration-roadmap.xhtml (updated 2026-06-20) still lists compute decision as pending PoC`  
   - Source file: `meetings/2026-08-03-architecture-committee.txt`  
   - Date: `2026-08-03`

2. **Keep Relay on EKS with autoscaling**  
   - Decision key: `decision:compute:2026-08-03:d18`  
   - Status: **rejected**  
   - Source file: `meetings/2026-08-03-architecture-committee.txt`  
   - Date: `2026-08-03`

The open item raised there was:

- **Provisioned concurrency sizing for /deliver**  
  - Open item key: `openitem:compute:2026-08-03`  
  - Status: **closed**  
  - Raised: `2026-08-03`  
  - Source file: `meetings/2026-08-03-architecture-committee.txt`

If you want, I can also list the speakers or explain how the decision and open item relate.

### memory-eval-graph (completed, 7.3s, 2 tool calls)
queries: ['MATCH (m:Meeting {date:$date})<-[:DECIDED_IN]-(d:Decision)-[:ABOUT]->(t:Topic)\nO', 'MATCH (oi:OpenItem)-[:RAISED_IN]->(m:Meeting {date:$date})\nRETURN oi.id AS openi']

At the architecture committee on **2026-08-03** (`meetings/2026-08-03-architecture-committee.txt`), the decisions were:

1. **D17** — “Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances”  
   - Topic: `topic:compute`  
   - Status: active  
   - Date: 2026-08-03  
   - Source: `meetings/2026-08-03-architecture-committee.txt`

2. **D18** — “Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)”  
   - Topic: `topic:compute`  
   - Status: rejected  
   - Date: 2026-08-03  
   - Source: `meetings/2026-08-03-architecture-committee.txt`

The open item raised there was:

- **O6** — “Provisioned concurrency sizing for /deliver”  
  - Status: closed  
  - Raised: 2026-08-03  
  - Source: `meetings/2026-08-03-architecture-committee.txt`

If you want, I can also list which decision superseded the rejected one, if any.

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

### memory-eval-both (completed, 10.3s, 2 tool calls)
queries: ['ретраи политика retrys retries policy changes ownership topic', "MATCH (t:Topic {key:'topic:retries'}) OPTIONAL MATCH (d:Decision)-[:ABOUT]->(t) "]

Политика ретраев менялась **3 раза**: есть **3 решения** по теме `topic:retries` (одно текущее и два исторических).

Шаги и владельцы:

1. **2026-03-30** — `decision:retries:2026-03-30`  
   Политика: ретраи на `POST /deliver` в gateway отключены до появления idempotency keys; read routes могут ретраить дважды.  
   Владелец: **Nikita Frolov** (`from 2026-03-30` до `2026-06-01`).  
   Источник: `meetings/2026-03-30-weekly-sync.txt`

2. **2026-06-15** — `decision:retries:2026-06-15`  
   Политика: ретраи на `POST /deliver` в gateway включены, максимум 3 попытки, retry budget 15%.  
   Владелец: **Anna Sokolova** (`from 2026-06-01` до `2026-09-07`).  
   Источник: `meetings/2026-06-15-weekly-sync.txt`

3. **2026-08-24** — `decision:retries:2026-08-24`  
   Политика: ретраи вынесены из gateway в SQS с DLQ после 5 попыток; gateway retries на `/deliver` выключены.  
   Владелец: **Ivan Melnik** (`from 2026-09-07`, текущий).  
   Источник: `meetings/2026-08-24-weekly-sync.txt`

Итого: **2 изменения от предыдущей политики**, если считать именно переходы между состояниями, или **3 версии политики** всего.

Если хотите, могу ещё показать это в виде таймлайна или таблицы.

### memory-eval-graph (completed, 10.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nOPTIONAL MATCH (p:Pe"]

Политика ретраев менялась **3 раза** по записям в памяти.

### Шаги и владельцы
1. **2026-03-30** — `decision:retries:2026-03-30`  
   Текст: “Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice”  
   Владелец: **person:nikita-frolov** с **2026-03-30**  
   Источник: решение в памяти, дата **2026-03-30**

2. **2026-06-15** — `decision:retries:2026-06-15`  
   Текст: “Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%”  
   Владелец: **person:anna-sokolova** с **2026-06-15**  
   Источник: решение в памяти, дата **2026-06-15**

3. **2026-08-24** — `decision:retries:2026-08-24`  
   Текст: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”  
   Владелец: **person:anna-sokolova** с **2026-08-24**  
   Источник: решение в памяти, дата **2026-08-24**

### Итог
- **Всего изменений политики ретраев: 3**
- **Текущий владелец темы/политики ретраев:** **person:anna-sokolova**  
  Источник: владение без `to` по теме/решениям, актуально на основании записи от **2026-08-24**

Если хотите, я могу ещё кратко показать **цепочку “что был

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

### memory-eval-both (completed, 7.5s, 2 tool calls)
queries: ["MATCH (o:OpenItem)\nWHERE NOT EXISTS { MATCH (o)<-[:OWNS]-(:Person {key: 'person'", 'MATCH (o:OpenItem)\nWHERE NOT EXISTS { MATCH (o)<-[:OWNS]-(:Person) }\nRETURN o.ke']

As of **2026-10-05**, the open items that are still **unowned** in memory are:

1. **openitem:database:2026-05-04** — “DynamoDB migration dry run on a production snapshot”  
   - Raised **0** times in the graph
   - Source: graph `OpenItem` node, raised date **2026-05-04**

2. **openitem:database:2026-05-18** — “DocumentDB decommission date”  
   - Raised **0** times in the graph
   - Source: graph `OpenItem` node, raised date **2026-05-18**

3. **openitem:compute:2026-07-27** — “Load test on Lambda at 10x current volume”  
   - Raised **0** times in the graph
   - Source: graph `OpenItem` node, raised date **2026-07-27**

4. **openitem:security:2026-09-07** — “Rotate DocumentDB credentials before decommission”  
   - Raised **0** times in the graph
   - Source: graph `OpenItem` node, raised date **2026-09-07**

I checked for OpenItem nodes with no incoming `OWNS` relationship and counted `RAISED_IN` links.

### memory-eval-graph (completed, 6.4s, 1 tool calls)
queries: ['MATCH (o:OpenItem)\nWHERE o.raised <= $d\nAND NOT EXISTS {\n  MATCH (:Person)-[ow:O']

As of **2026-10-05**, these items are still **unowned**:

1. **openitem:database:2026-05-18** — “DocumentDB decommission date”  
   - Raised **3 times**  
   - Source: **OpenItem** key `openitem:database:2026-05-18`, raised `2026-05-18`

2. **openitem:compute:2026-07-27** — “Load test on Lambda at 10x current volume”  
   - Raised **3 times**  
   - Source: **OpenItem** key `openitem:compute:2026-07-27`, raised `2026-07-27`

3. **openitem:security:2026-09-07** — “Rotate DocumentDB credentials before decommission”  
   - Raised **2 times**  
   - Source: **OpenItem** key `openitem:security:2026-09-07`, raised `2026-09-07`

Retrieved from memory:
- Open items raised by or before `2026-10-05`
- No current owner on those items as of `2026-10-05`
- No decision closing them on or before `2026-10-05`

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

### memory-eval-both (completed, 4.0s, 1 tool calls)
queries: ['serverless cutover 19 October what should happen before it and in what order']

По памяти есть такой порядок перед серверлес-катовером 19 октября:

1. За 24 часа заморозить изменения endpoint’ов.  
2. Переключить gateway-интеграции для `POST /relay/deliver` и `GET /relay/*` с VPC link на Lambda-интеграции.  
3. Опустить EKS deployments до 0 replicas, но оставить кластер на 7 дней.  
4. Затем 30 минут наблюдать за `delivery p95`, глубиной DLQ и `intake 5xx`.

Дополнительно из того же runbook’а есть предпосылки:
- staging на Lambda должен быть без инцидентов неделю;
- provisioned concurrency для `relay-deliver` — 4;
- 10x load test ещё не сделан;
- cutover с DynamoDB должен идти первым, и эти два cutover’а должны быть разнесены на неделю.

Источники:
- `docs/runbook-cutover-serverless.md`, updated `2026-09-29`
- `meetings/2026-10-05-cutover-planning.txt`, decision dated `2026-10-05` (cutover on `2026-10-19 09:00 local`)

### memory-eval-graph (completed, 13.1s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'})-[:OWNS]-(p:Person)\nW", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'})\nWHERE d.date <= '202", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'})\nWHERE d.date <= '202", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'})\nWHERE d.date <= '202"]

До серверлес-катовера 2026-10-19 зафиксированы только два актуальных решения по теме cutover, и оба относятся к самому катоверу, а не к предварительным шагам:

1. **Serverless cutover on 2026-10-19 at 09:00 local, inside the planned-work error budget** — решение от **2026-10-05**, источник: **`meetings/2026-10-05-cutover-planning.txt`**.  
   Это текущая дата/время катовера.  
   Источник: решение `decision:cutover:2026-10-05:d25`, дата `2026-10-05`.

2. **Rollback owner for both cutovers is Lena** — решение от **2026-10-05**, источник: **`meetings/2026-10-05-cutover-planning.txt`**.  
   Это назначение владельца отката.  
   Источник: решение `decision:cutover:2026-10-05:d27`, дата `2026-10-05`.

**Порядок:**  
Сначала в памяти идет фиксация **времени катовера**, затем — **владельца rollback**. Оба решения одного дня, и между ними нет зависимостей `DEPENDS_ON` в графе.

Что я проверил:
- текущие решения по `topic:cutover`;
- зависимости между решениями;
- есть ли более ранние/актуальные шаги до `2026-10-19`.

Если вам нужен именно **список подготовительных действий до катовера**, то в памяти **это не зафиксировано** — есть только упомянутые выше решения.

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

### memory-eval-both (completed, 5.7s, 3 tool calls)
queries: ['SLO changed current SLO decision status supersedes Relay webhook delivery', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:slo'})\nOPTIONAL MATCH (d2:Deci", "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:slo'})\nWHERE NOT EXISTS { MATC"]

Yes — the SLO has changed.

Current SLO:
- Delivery p95 SLO is **3 s for 30 days after the serverless cutover, then back to 2 s**.
- Source: decision `decision:slo:2026-10-05`, dated **2026-10-05**.

History:
- On **2026-01-26**, the SLO was **p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%**.
- That decision is marked **superseded**.
- Source: decision `decision:slo:2026-01-26`, dated **2026-01-26**.

The docs I found (`docs/slo.md`, updated **2026-01-28**) are stale relative to the newer **2026-10-05** decision, because they still reflect the earlier 2 s / 99.5% SLO.

### memory-eval-graph (completed, 5.3s, 1 tool calls)
queries: ["MATCH (t:Topic {key:'topic:slo'})<-[:ABOUT]-(d:Decision)\nRETURN d.date AS date, "]

Yes — the SLO has changed.

Current SLO:
- Delivery p95 end-to-end latency is 3 s for 30 days after the serverless cutover, then it returns to 2 s.
- Source: `meetings/2026-10-05-cutover-planning.txt`, dated 2026-10-05.
- Decision: `decision:slo:2026-10-05` (active)

Earlier SLO:
- Delivery SLO was p95 end-to-end delivery latency 2 s over 5 minutes, with monthly delivery success rate 99.5%.
- Source: `meetings/2026-01-26-weekly-sync.txt`, dated 2026-01-26.
- Decision: `decision:slo:2026-01-26` (superseded)

So the current state is the temporary 3 s p95 SLO after cutover, with a planned return to 2 s after 30 days.

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

### memory-eval-both (completed, 5.0s, 2 tool calls)
queries: ['ADR-007 rejected why what numbers were EKS', "MATCH (d:Decision {id:'ADR-007'}) OPTIONAL MATCH (d)-[:ABOUT]->(t:Topic) OPTIONA"]

Не в памяти: я нашёл только сам ADR-007 в vector store, но не нашёл его узел в графе по `id:'ADR-007'`.

Что удалось извлечь:
- `adr/ADR-007.md`, обновлён 2026-08-05, статус `Rejected`.
- Текст причины из решения: “rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run.”
- В разделе `Consequences` сказано: “p95 is five times better than Lambda but monthly cost is 1.7x and the platform team would have to become a Kubernetes team.”
- В метаданных документа указано, что решение было на `Relay weekly sync, 2026-08-03`.

По цифрам EKS:
- p95: `0.4 s`
- ежемесячная стоимость: `1.7x`

Если хотите, я могу ещё поискать, с чем именно сравнивали эти цифры — например, в пользу какого решения ADR-007 отклонили.

### memory-eval-graph (completed, 6.0s, 3 tool calls)
queries: ["MATCH (d:ADR {id:'ADR-007'}) RETURN d.key AS key, d.title AS title, d.date AS da", "MATCH (d:Decision)-[:RECORDED_IN]->(a:ADR {id:'ADR-007'}) RETURN d.key AS decisi", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) OPTIONAL MATCH (d)-["]

ADR-007 отклонили, потому что по записанной в памяти причине вариант EKS с autoscaling дал **p95 0.4 s**, но при этом был **в 1.7 раза дороже по месячной стоимости** и требовал **отдельной platform team / второй платформы**.  
Источник: **decision:compute:2026-08-03:d18**; ADR: **ADR-007** (`adr/ADR-007.md`, дата 2026-08-05; решение от 2026-08-03).

По цифрам для EKS в памяти есть:
- **p95 = 0.4 s**
- **monthly_cost_usd = 6100**
- формулировка в решении: **1.7x monthly cost**

Источник: **PoC-2: Relay on EKS with autoscaling** / решение **decision:compute:2026-08-03:d18** от 2026-08-03.

Если хотите, могу ещё кратко сравнить это с цифрами Lambda из того же решения.

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

### memory-eval-both (completed, 5.8s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:iac'})\nWHERE d.status <> 'reje", "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:iac'})\nWHERE d.status <> 'reje"]

The current decision on infrastructure as code is:

- Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation.

It was made on **2026-04-20**. Source: **meetings/2026-04-20-weekly-sync.txt**.



### memory-eval-graph (completed, 3.5s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERS"]

The current decision on infrastructure as code is:

- **Hybrid IaC:** networking (VPC, peering, DNS) stays in **Terraform**; application stacks are **CloudFormation**  
  Source: **meetings/2026-04-20-weekly-sync.txt**  
  Date: **2026-04-20**

This is the current decision because it is the latest active decision on `topic:iac` and nothing supersedes it.

### memory-eval-vector (completed, 4.4s, 3 tool calls)
queries: ['What is the current decision on infrastructure as code, and when was it made?', 'current decision infrastructure as code made date', 'infrastructure as code decision']

The current decision on infrastructure as code is **hybrid IaC**: **networking stays in Terraform, and application stacks use CloudFormation**. This decision was made in **ADR-004 on 2026-04-20** and is recorded as superseding ADR-001. Source: **confluence/decision-log.xhtml** (updated **2026-06-03**) and **adr/ADR-004.md** (updated **2026-04-22**).

The earlier decision to migrate everything from Terraform to CloudFormation exists in **ADR-001** but it is **superseded**, so it is not the current decision. Source: **adr/ADR-001.md** (updated **2026-01-14**).



## t02 [ru / history] Как менялось решение по теме «infrastructure as code»? Перечисли по датам.
**expected:** 2026-01-12: Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1 → 2026-02-09: One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway) → 2026-02-23: Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call → 2026-04-20: Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-02-09-weekly-sync.txt', 'meetings/2026-02-23-incident-review.txt', 'meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 5.1s, 2 tool calls)
queries: ['infrastructure as code решение по теме даты decision ADR topic iac', 'topic infrastructure as code decisions ADR-001 ADR-004 dated status superseded a']

По теме **infrastructure as code** в памяти есть две смены решения:

- **2026-01-14** — решение: **мигрировать инфраструктурный код с Terraform на CloudFormation**, по модулю, с импортом ресурсов без пересоздания.  
  Источник: `adr/ADR-001.md`, дата документа/решения: **2026-01-14**.  
  Это решение позже стало **superseded**.

- **2026-04-22** — новое решение: **гибридный IaC** — сеть (`VPC`, peering, `DNS`) остаётся в Terraform, а application stacks — в CloudFormation.  
  Источник: `adr/ADR-004.md`, дата документа/решения: **2026-04-22**.  
  Это решение **supersedes ADR-001**, то есть заменяет предыдущее.

Если хочешь, я могу ещё коротко показать это как цепочку **“было → стало”**.

### memory-eval-graph (completed, 7.1s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:$topic})\nOPTIONAL MATCH (d)-[:DECIDED']

По теме **infrastructure as code** решение менялось так, по датам:

- **2026-01-12** — **superseded**: мигрировать инфраструктурный код Relay **с Terraform на CloudFormation**, по модулю, до конца Q1.  
  **Источник:** `meetings/2026-01-12-weekly-sync.txt`

- **2026-02-09** — **active**: использовать **один root stack CloudFormation на окружение** с nested stacks по компонентам: network, data, compute, gateway.  
  **Источник:** `meetings/2026-02-09-weekly-sync.txt`

- **2026-02-23** — **active**: **ручные изменения в консоли заморожены**; включён **ночной drift detection** для каждого stack с алертами on-call.  
  **Источник:** `meetings/2026-02-23-incident-review.txt`

- **2026-04-20** — **active**: **гибридный IaC-подход** — networking (VPC, peering, DNS) остаётся в **Terraform**, а application stacks — в **CloudFormation**.  
  **Источник:** `meetings/2026-04-20-weekly-sync.txt`

Если хочешь, я могу ещё показать это как цепочку **«что supersedes что»**.

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

### memory-eval-both (completed, 3.9s, 2 tool calls)
queries: ['current decision on gateway timeout made when topic gateway timeouts decision', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:timeouts'})\nWHERE NOT (d)<-[:S"]

The current decision on gateway timeout is:

- **Gateway integration timeout lowered from 30 s to 25 s**
- **Made on:** **2026-08-24**
- **Source file:** `meetings/2026-08-24-weekly-sync.txt`

This is the current decision because it has no incoming `SUPERSEDES` and its status is `active`.

### memory-eval-graph (completed, 3.8s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nWHERE NOT (d)<-[:SUPERSEDES]-']

Current gateway decision: **Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack**.  
It was made on **2026-03-02** in **meetings/2026-03-02-weekly-sync.txt**.

I did not find a separate current decision specifically labeled “gateway timeout” in memory; the current gateway-related decision I retrieved is the one above.

### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['What is the current decision on gateway timeout, and when was it made?', 'current decision gateway timeout made date', 'gateway timeout decision']

The current decision is: **gateway integration timeout is 25 s**. It was made on **2026-08-24**. Source: **meetings/2026-08-24-weekly-sync.txt** (`D20`, status active).

I also found a newer document, **ADR-010: Gateway timeout policy for Lambda integrations** updated **2026-09-23**, but it says **“No decision recorded”** in the Decision section and is therefore stale on this point relative to the meeting decision. Source: **adr/ADR-010.md** (`Decision`, updated 2026-09-23).

## t04 [ru / history] Как менялось решение по теме «gateway timeout»? Перечисли по датам.
**expected:** 2026-03-16: Gateway integration timeout 10 s on every Relay route → 2026-05-18: Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14 → 2026-08-24: Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom  
**expected sources:** {'sources': ['meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 6.6s, 2 tool calls)
queries: ['topic gateway timeout decision history changed by date gateway timeout', 'gateway timeout decision superseded by date D06 D12 D20']

По памяти, решение по теме **gateway timeout** менялось так:

1. **2026-03-16** — timeout был **10 s на каждом маршруте Relay**.  
   Источник: `meetings/2026-03-16-weekly-sync.txt` / claim `D06`  
   Статус: **superseded**.  
   Это решение позже было заменено.  

2. **2026-05-18** — timeout **увеличили с 10 s до 30 s** после инцидента с медленным target.  
   Источник: `meetings/2026-05-18-weekly-sync.txt` / claim `D12`  
   Статус: **superseded**.  
   Это решение **supersedes D06** и само **superseded by D20**.  

3. **2026-08-24** — timeout **снизили с 30 s до 25 s**, потому что hard limit gateway — 29 s и Lambda нужен запас.  
   Источник: `meetings/2026-08-24-weekly-sync.txt` / claim `D20`  
   Статус: **active**.  
   Это текущее решение на эту тему.

Если хочешь, я могу ещё свести это в короткую таблицу «дата → значение timeout → статус».

### memory-eval-graph (completed, 7.0s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nOPTIONAL MATCH (d)-[:SUPERSED']

По теме **gateway timeout** в памяти есть 3 решения, по датам:

- **2026-03-16** — `Gateway integration timeout 10 s on every Relay route`  
  Источник: `meetings/2026-03-16-weekly-sync.txt`  
  Статус: **superseded**

- **2026-05-18** — `Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14`  
  Источник: `meetings/2026-05-18-weekly-sync.txt`  
  Статус: **superseded**  
  Это решение **supersedes** решение от 2026-03-16.

- **2026-08-24** — `Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom`  
  Источник: `meetings/2026-08-24-weekly-sync.txt`  
  Статус: **active**  
  Это текущее решение; оно **supersedes** решение от 2026-05-18.

Если хочешь, могу ещё кратко показать это как цепочку изменений: **10 s → 30 s → 25 s**.

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

### memory-eval-both (completed, 4.0s, 2 tool calls)
queries: ['current decision gateway timeout replaced an earlier one earlier decision what d', 'gateway timeout decision supersedes D06 what did D06 supersede when gateway time']

The earlier gateway-timeout decision was **D06**, and it was made on **2026-03-16**. It set the gateway integration timeout to **10 s on every Relay route** and was later superseded by D12. Source: `meetings/2026-03-16-weekly-sync.txt` / claim `D06` (`2026-03-16`).

So the chain is:

- **D12** (2026-05-18) superseded **D06**
- **D06** (2026-03-16) was the decision that the current one replaced



### memory-eval-graph (completed, 4.9s, 1 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'})\nWHERE NOT (cur)<-"]

The earlier gateway-timeout decision was **the one from 2026-05-18**, and it **replaced the decision from 2026-03-16**.

- **Earlier decision:** `decision:timeouts:2026-05-18` — date **2026-05-18**  
- **What it replaced:** `decision:timeouts:2026-03-16` — date **2026-03-16**

Source: graph memory, `Decision` chain on `topic:timeouts` via `SUPERSEDES` (current decision dated 2026-08-24; previous dated 2026-05-18; older dated 2026-03-16).

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

### memory-eval-both (completed, 3.0s, 2 tool calls)
queries: ['current decision retries made date topic retries decision current status superse', 'current retries decision latest supersedes D14 D21 topic retries current decisio']

The current decision on retries is: retries move out of the gateway into SQS with a dead-letter queue after 5 attempts, and gateway retries on `/deliver` are turned off.

It was made on **2026-08-24**.  
Source: **meetings/2026-08-24-weekly-sync.txt**.  
Status: **active**.

### memory-eval-graph (completed, 4.0s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nWHERE NOT (d)<-[:SUPERSEDES]-']

Current decision on retries: retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on `/deliver` are turned off. Source: `meetings/2026-08-24-weekly-sync.txt`, dated `2026-08-24`.

I also retrieved that the decision note says `docs/gateway.md` (updated `2026-03-18`) is stale, and `ADR-002`’s Retries section is stale since `2026-08-24`.

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

### memory-eval-both (completed, 7.0s, 1 tool calls)
queries: ['topic retries decisions chronology changed by date current and superseded']

По теме **retries** в памяти есть такая хронология решений:

- **2026-03-30** — **Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice.**  
  Статус: **superseded**. Суперседирован решением от 2026-06-15.  
  Источник: `meetings/2026-03-30-weekly-sync.txt`  
  Дата: `2026-03-30`

- **2026-06-15** — **Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%.**  
  Статус: **superseded**. Суперседирует решение от 2026-03-30 и само суперседировано решением от 2026-08-24.  
  Источник: `meetings/2026-06-15-weekly-sync.txt`  
  Дата: `2026-06-15`

- **2026-08-24** — **Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off.**  
  Статус: **active**. Это текущее решение по теме, потому что его ничего не суперседирует.  
  Источник: `meetings/2026-08-24-weekly-sync.txt` и ADR `ADR-009`  
  Дата: `2026-08-24`

Если хочешь, могу ещё кратко показать это как цепочку **«было → стало → сейчас»**.

### memory-eval-graph (completed, 6.0s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nOPTIONAL MATCH (d)-[:SUPERSED']

По теме «retries» в памяти есть 3 решения, по датам:

1. **2026-03-30** — `meetings/2026-03-30-weekly-sync.txt`  
   Решение: *Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice*.

2. **2026-06-15** — `meetings/2026-06-15-weekly-sync.txt`  
   Решение: *Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%*.  
   Это решение **supersedes** решение от 2026-03-30.

3. **2026-08-24** — `meetings/2026-08-24-weekly-sync.txt`  
   Решение: *Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off*.  
   Это текущее решение; оно **supersedes** решение от 2026-06-15.

Если хочешь, могу ещё показать это как цепочку «что было → что стало».

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

### memory-eval-both (completed, 4.3s, 2 tool calls)
queries: ['current decision retries replaced an earlier one supersedes previous decision wh', "MATCH (d:Decision {key:'decision:retries:2026-06-15'})-[:SUPERSEDES]->(prev:Deci"]

The earlier decision was **decision:retries:2026-03-30** on **2026-03-30**. It replaced **nothing else** in memory: I found no incoming `SUPERSEDES` edge for it, so it appears to be the earliest decision in that retries chain.

Sources:
- `meetings/2026-06-15-weekly-sync.txt` — 2026-06-15
- `meetings/2026-03-30-weekly-sync.txt` — 2026-03-30

### memory-eval-graph (completed, 14.8s, 4 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nWHERE NOT (cur)<-[", "MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nWHERE NOT (cur)<-[", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nRETURN d.key AS key,", "MATCH (e:Decision {key:'decision:retries:2026-06-15'})-[:SUPERSEDES]->(prev:Deci"]

The earlier decision was **decision:retries:2026-06-15** on **2026-06-15**. It replaced **decision:retries:2026-03-30**.

Sources:
- **decision:retries:2026-06-15** — `Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%`
- **decision:retries:2026-03-30** — `Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice`

I found these decisions in memory, but there is **no file field recorded** for either one.

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

### memory-eval-both (completed, 5.1s, 2 tool calls)
queries: ['current decision compute platform made when compute platform topic compute decis', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:compute'})\nWHERE NOT EXISTS { "]

The current decision on compute platform is:

- **Relay moves to Lambda with provisioned concurrency on /deliver**.  
- It was made on **2026-08-03**.  
- Source: **meetings/2026-08-03-architecture-committee.txt**.  

This is the current decision because there are no newer decisions superseding it in memory.

### memory-eval-graph (completed, 7.1s, 3 tool calls)
queries: ["MATCH (t:Topic {key:'topic:compute'})<-[:ABOUT]-(d:Decision)\nWHERE NOT (d)<-[:SU", "MATCH (t:Topic)\nWHERE t.key = 'topic:compute' OR 'compute' IN t.aliases OR t.nam", "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE t.key IN ['topic:compute','topic:ga"]

The current decision on compute platform is: Relay moves to Lambda with provisioned concurrency on `/deliver`. It was made on 2026-08-03 in `meetings/2026-08-03-architecture-committee.txt`. The decision is active.

### memory-eval-vector (completed, 3.4s, 3 tool calls)
queries: ['What is the current decision on compute platform, and when was it made?', 'current decision compute platform made date', 'compute platform decision']

The current decision on compute is: **Relay moves to Lambda with provisioned concurrency on `/deliver`**. It was made on **2026-08-03**. Source: `meetings/2026-08-03-architecture-committee.txt` / claim `D17` (recorded in ADR-006), dated **2026-08-03**.

I also found an older document saying to **keep Relay on EKS with autoscaling**, but it is **rejected/superseded** by the 2026-08-03 decision. Sources: `adr/ADR-007.md` dated **2026-08-05** and `meetings/2026-08-03-architecture-committee.txt` dated **2026-08-03**.

## t10 [ru / history] Как менялось решение по теме «compute platform»? Перечисли по датам.
**expected:** 2026-06-15: Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July → 2026-08-03: Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances  
**expected sources:** {'sources': ['meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 6.1s, 2 tool calls)
queries: ['compute platform decision history dates topic compute platform', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:compute'})\nOPTIONAL MATCH (d)-"]

По теме **compute** в памяти есть такие решения по датам:

- **2026-06-15** — `decision:compute:2026-06-15` — статус **superseded**; источник: `meetings/2026-06-15-weekly-sync.txt`.
- **2026-08-03** — `decision:compute:2026-08-03:d18` — статус **rejected**; источник: `meetings/2026-08-03-architecture-committee.txt`.
- **2026-08-03** — `decision:compute:2026-08-03:d17` — статус **active**; этот decision **supersedes** `decision:compute:2026-06-15`; источник: `meetings/2026-08-03-architecture-committee.txt`.

Итог по текущему решению: на дату **2026-08-03** актуально **decision:compute:2026-08-03:d17**, потому что у него нет входящих `SUPERSEDES`, и его статус — `active`.

### memory-eval-graph (completed, 9.9s, 2 tool calls)
queries: ["MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'compute' OR any(a IN coalesce(t.", "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:compute'})\nOPTIONAL MATCH (d)<"]

По теме **compute platform** в памяти есть такие решения, по датам:

- **2026-06-15** — *«Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July»*  
  **Статус:** `superseded`  
  **Источник:** `meetings/2026-06-15-weekly-sync.txt`

- **2026-08-03** — *«Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)»*  
  **Статус:** `rejected`  
  **Источник:** `meetings/2026-08-03-architecture-committee.txt`

- **2026-08-03** — *«Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances»*  
  **Статус:** `active`  
  **Источник:** `meetings/2026-08-03-architecture-committee.txt`

Если нужно, могу ещё кратко показать **цепочку смены решения**: от PoC-запуска к финальному выбору.

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

### memory-eval-both (completed, 4.0s, 2 tool calls)
queries: ['current decision on SLO made when decision status current topic:slo', "MATCH (t:Topic {key:'topic:slo'})<-[:ABOUT]-(d:Decision) WHERE d.status <> 'reje"]

The current decision on SLO is:

- **Delivery SLO:** **p95 end-to-end delivery latency 2 s over 5 minutes**; **monthly delivery success rate 99.5%**.
- It was made on **2026-10-05**.
- Source: **meetings/2026-10-05-cutover-planning.txt**.

Note: I also found an older SLO decision from **2026-01-26** in the decision log, but it is marked **superseded**, so it is not the current decision.

### memory-eval-graph (completed, 4.3s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nWHERE NOT (d)<-[:SUPERSEDES]-']

Current SLO decision: the delivery p95 SLO was relaxed from 2 s to 3 s for 30 days after the serverless cutover, then returns to 2 s. Source: meeting file `meetings/2026-10-05-cutover-planning.txt`, dated 2026-10-05.

Made on: 2026-10-05. Source: `meetings/2026-10-05-cutover-planning.txt`.

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

### memory-eval-both (completed, 4.5s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:slo'})\nRETURN d.date AS date, "]

По теме «SLO» в памяти есть два решения, по датам:

- **2026-01-26** — *Delivery SLO*: p95 end-to-end delivery latency **2 s over 5 minutes**; monthly delivery success rate **99.5%**.  
  Источник: `meetings/2026-01-26-weekly-sync.txt`  
  Статус: **superseded**

- **2026-10-05** — *Delivery p95 SLO* **смягчён с 2 s до 3 s на 30 дней после serverless cutover, затем обратно до 2 s**.  
  Источник: `meetings/2026-10-05-cutover-planning.txt`  
  Статус: **active**

Если смотреть текущую версию решения, то актуальным является **решение от 2026-10-05**; оно делает старое решение от 2026-01-26 историческим.

### memory-eval-graph (completed, 4.5s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nRETURN d.date AS date, d.text']

По теме **SLO** в памяти есть 2 решения, по датам:

1. **2026-01-26** — **superseded**  
   **Источник:** `meetings/2026-01-26-weekly-sync.txt`  
   **Суть решения:** `Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5%`

2. **2026-10-05** — **active**  
   **Источник:** `meetings/2026-10-05-cutover-planning.txt`  
   **Суть решения:** `Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s`

Дополнительно: решение от **2026-01-26** помечено как **superseded**, то есть это уже история, а текущим является решение от **2026-10-05**.

Если хочешь, могу ещё показать это как цепочку «что было заменено чем».

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

### memory-eval-both (completed, 5.1s, 2 tool calls)
queries: ["MATCH (t:Topic {key:'topic:retries'})<-[:OWNS]-(p:Person) WHERE p.left IS NULL O", "MATCH (t:Topic {key:'topic:retries'})<- [o:OWNS]-(p:Person) WHERE o.to IS NULL R"]

Сейчас тему «retries» владеет **Ivan Melnik** с даты **2026-09-07**.

Источник: граф знаний, связь **OWNS** для `topic:retries`, дата из свойства `from` на ребре OWNS.

### memory-eval-graph (completed, 3.1s, 1 tool calls)
queries: ['MATCH (p:Person)-[o:OWNS]->(t:Topic {key:$topic})\nWHERE o.to IS NULL\nRETURN p.ke']

Темой «retries» сейчас владеет **Иван Мельник** — с **2026-09-07**.  
Источник: граф памяти, связь `OWNS` к теме `topic:retries`, дата начала владения `2026-09-07`.

### memory-eval-vector (completed, 2.7s, 3 tool calls)
queries: ['Кто сейчас владеет темой «retries» и с какой даты?', 'Who owns retries and since when?', 'ownership retries from date owner current']

Сейчас тему **retries** владеет **Ivan Melnik** — **с 2026-09-07**. Источник: `memory/decisions.jsonl`, запись `claim ownership | retries | 2026-09-07` (статус `active`).

## t14 [en / owner_at] Who owned retries on 2026-06-15?
**expected:** Anna Sokolova (from 2026-06-01 to 2026-09-07)  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 5.0s, 2 tool calls)
queries: ["MATCH (t:Topic {key:'topic:retries'})<- [o:OWNS]-(p:Person)\nWHERE o.from <= date", "MATCH (t:Topic {key:'topic:retries'})<- [o:OWNS]-(p:Person)\nRETURN p.key AS pers"]

On 2026-06-15, **Anna Sokolova** owned retries.

Source: graph `OWNS` relationship on `topic:retries`, with ownership from **2026-06-01** to **2026-09-07** (`person:anna-sokolova`, name: Anna Sokolova).

### memory-eval-graph (completed, 3.9s, 1 tool calls)
queries: ['MATCH (p:Person)-[o:OWNS]->(:Topic {key:$topic})\nWHERE o.from <= $date AND (o.to']

On 2026-06-15, **Anna Sokolova** owned **retries**.

- Source: ownership edge on **topic:retries**
- Date range: **from 2026-06-01 to 2026-09-07**
- Therefore 2026-06-15 falls within that ownership period.

Source: graph memory query result; no document file was returned for this ownership record.

### memory-eval-vector (completed, 4.3s, 3 tool calls)
queries: ['Who owned retries on 2026-06-15?', 'retries ownership 2026-06-15', 'owner retries 2026-06-15']

On 2026-06-15, **Anna Sokolova** owned retries. The active ownership decision is from **2026-06-01** and says “Anna Sokolova owns retries from 2026-06-01 to 2026-09-07.” Source: **memory/decisions.jsonl** dated **2026-06-01**.

I also retrieved a meeting note from **2026-06-15** that says “без владельца” (“without an owner”), but it appears to be about a different item in that sync, not the retries ownership decision. Source: **meetings/2026-06-15-weekly-sync.txt** dated **2026-06-15**.



## t15 [ru / owner_now] Кто сейчас владеет темой «compute platform» и с какой даты?
**expected:** Ivan Melnik, с 2026-07-13  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt']}

### memory-eval-both (completed, 4.0s, 2 tool calls)
queries: ["MATCH (t:Topic {key:'topic:compute'})<-[:OWNS]-(p:Person)\nWHERE (p)-[o:OWNS]->(t", "MATCH (t:Topic {key:'topic:compute'})<- [o:OWNS]-(p:Person)\nWHERE o.to IS NULL\nR"]

Темой «compute platform» сейчас владеет **Ivan Melnik** с **2026-07-13**.

Источник: граф памяти, связь `OWNS` для `topic:compute`, дата начала владения `2026-07-13`.

### memory-eval-graph (completed, 3.3s, 1 tool calls)
queries: ["MATCH (t:Topic {name:'compute platform'}) OPTIONAL MATCH (p:Person)-[o:OWNS]->(t"]

Сейчас темой «compute platform» владеет **Ivan Melnik** — **с 2026-07-13**.  
Источник: граф памяти, тема `topic:compute`, связь `OWNS` от `person:ivan-melnik`, дата начала `2026-07-13`.

### memory-eval-vector (completed, 2.5s, 1 tool calls)
queries: ['Кто сейчас владеет темой «compute platform» и с какой даты?']

Сейчас темой **compute** владеет **Ivan Melnik** с **2026-07-13**. Источник: `memory/decisions.jsonl` (claim ownership | compute | 2026-07-13).

Нашёл также более старую, уже неактуальную запись: **Sergey Belov** владел compute с **2026-06-15** по **2026-07-13**. Источник: `memory/decisions.jsonl` (claim ownership | compute | 2026-06-15).

## t16 [en / owner_at] Who owned compute platform on 2026-06-28?
**expected:** Sergey Belov (from 2026-06-15 to 2026-07-13)  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt']}

### memory-eval-both (completed, 4.3s, 2 tool calls)
queries: ['compute platform ownership owner on 2026-06-28 compute platform topic ownership', "MATCH (t:Topic {key:'topic:compute'})<- [o:OWNS]-(p:Person)\nWHERE o.from <= date"]

Not in memory.

What I retrieved:
- Vector search found a claim that **Ivan Melnik owns compute from 2026-07-13 (current)**, source file `memory/decisions.jsonl`, date `2026-07-13`.
- Vector search also found a superseded claim that **Sergey Belov owned compute from 2026-06-15 to 2026-07-13**, source file `memory/decisions.jsonl`, date `2026-06-15`.
- Cypher lookup for `topic:compute` ownership on `2026-06-28` returned no matching graph records.

### memory-eval-graph (completed, 4.1s, 2 tool calls)
queries: ["MATCH (t:Topic {key:'topic:compute'}) RETURN t.key AS topic, t.name AS name", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.from <= '2026"]

On **2026-06-28**, **Sergey Belov** owned **compute platform**.  
**Source:** graph ownership edge for topic `topic:compute`; ownership period **from 2026-06-15 to 2026-07-13**.

### memory-eval-vector (completed, 4.1s, 3 tool calls)
queries: ['Who owned compute platform on 2026-06-28?', 'compute platform owner 2026-06-28', 'ownership of compute platform on 2026-06-28']

On 2026-06-28, **Sergey Belov** owned compute. Source: **memory/decisions.jsonl** — claim dated **2026-06-15**: “Sergey Belov owns compute from 2026-06-15 to 2026-07-13.”

I also found a newer ownership decision for compute dated **2026-07-13** saying **Ivan Melnik** owns compute from that date onward, so the 2026-06-15 decision is the applicable one for 2026-06-28. Source: **memory/decisions.jsonl** — decision dated **2026-07-13**.

## t17 [ru / owner_now] Кто сейчас владеет темой «idempotency» и с какой даты?
**expected:** Anna Sokolova, с 2026-06-01  
**expected sources:** {'sources': []}

### memory-eval-both (completed, 4.2s, 2 tool calls)
queries: ["MATCH (t:Topic {key:'topic:idempotency'})<-[:OWNS]-(p:Person)\nWHERE p.key STARTS", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'})\nWHERE o.to IS NUL"]

Сейчас тему «idempotency» владеет **Анна Соколова** — с **2026-06-01**.

Источник: граф знаний, связь `OWNS` для `topic:idempotency` от `person:anna-sokolova`; дата начала владения `2026-06-01`.

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ['MATCH (p:Person)-[o:OWNS]->(t:Topic {key:$topic})\nWHERE o.to IS NULL\nRETURN p.ke']

Тему «idempotency» сейчас владеет **Анна Соколова** — **с 2026-06-01**.  
Источник: граф памяти, связь `OWNS` к теме `topic:idempotency`, дата начала владения `from=2026-06-01`.

### memory-eval-vector (completed, 3.0s, 3 tool calls)
queries: ['Кто сейчас владеет темой «idempotency» и с какой даты?', 'idempotency ownership current owner from date', 'владелец idempotency дата']

Сейчас темой **idempotency** владеет **Anna Sokolova** — с **2026-06-01**.  
Источник: `memory/decisions.jsonl`, запись `ownership:idempotency:2026-06-01` (дата 2026-06-01).

## t18 [en / owner_at] Who owned idempotency on 2026-05-28?
**expected:** Nikita Frolov (from 2026-05-18 to 2026-06-01)  
**expected sources:** {'sources': []}

### memory-eval-both (completed, 4.9s, 2 tool calls)
queries: ["MATCH (t:Topic {key:'topic:idempotency'})<- [o:OWNS]-(p:Person)\nWHERE o.from <= ", "MATCH (t:Topic {key:'topic:idempotency'})<- [o:OWNS]-(p:Person)\nRETURN p.key AS "]

On 2026-05-28, **Nikita Frolov** owned **idempotency**.

Source: graph `Topic`/`OWNS` relation for `topic:idempotency`, ownership from **2026-05-18** to **2026-06-01**.

### memory-eval-graph (completed, 3.4s, 1 tool calls)
queries: ['MATCH (p:Person)-[o:OWNS]->(:Topic {key:$topic})\nWHERE o.from <= $date AND (o.to']

On 2026-05-28, idempotency was owned by **Nikita Frolov**.

- Source: ownership edge on **topic:idempotency**.
- Ownership period: **from 2026-05-18 to 2026-06-01**.
- Date checked: **2026-05-28**.



### memory-eval-vector (completed, 3.0s, 3 tool calls)
queries: ['Who owned idempotency on 2026-05-28?', 'idempotency owner 2026-05-28', 'ownership of idempotency on 2026-05-28']

Nikita Frolov owned idempotency on 2026-05-28. Source: `meetings/2026-05-18-weekly-sync.txt` and `memory/decisions.jsonl`, dated 2026-05-18. The newer ownership decision says Anna Sokolova owns idempotency from 2026-06-01, so that does not apply yet. Source: `meetings/2026-06-01-weekly-sync.txt` and `memory/decisions.jsonl`, dated 2026-06-01.

## t19 [ru / objector] Кто предложил и кто возражал против решения «Migrate Relay infrastructure code from Terraform to CloudFor…»?
**expected:** proposer Pavel Grishin, objector Timur Aliev, 2026-01-12  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt']}

### memory-eval-both (completed, 4.4s, 2 tool calls)
queries: ['решение "Migrate Relay infrastructure code from Terraform to CloudFor" proposed ', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:iac'}) OPTIONAL MATCH (d)<-[:P"]

Решение **«Migrate Relay infrastructure code from Terraform to CloudFormation»** было:

- **предложено**: **Павелом Гришиным** — источник: `meetings/2026-01-12-weekly-sync.txt`, дата `2026-01-12`
- **возражение**: **Тимуром Алиевым** — источник: `adr/ADR-001.md`, дата `2026-01-14`

Это относится к решению `decision:iac:2026-01-12`; оно сейчас **superseded** более новым решением по той же теме.

### memory-eval-graph (completed, 5.1s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:$topic})\nWHERE d.text CONTAINS $needl']

Решение **«Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1»** было:

- **предложено**: **Павелом Гришиным** — источник: `meetings/2026-01-12-weekly-sync.txt`, дата: **2026-01-12**
- **возражал**: **Тимуром Алиевым** — источник: `meetings/2026-01-12-weekly-sync.txt`, дата: **2026-01-12**

Если хотите, могу ещё назвать сам `Decision` ID и кратко пересказать формулировку решения.

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

### memory-eval-both (completed, 2.3s, 1 tool calls)
queries: ['decision Gateway integration timeout 10 s on every Relay route proposed objected']

Proposed by **Pavel Grishin**; objected to by **Anna Sokolova**.

Source: `meetings/2026-03-16-weekly-sync.txt`  
Date: `2026-03-16`

### memory-eval-graph (completed, 4.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:timeouts'})\nWHERE d.text CONTA"]

The decision was proposed by **Pavel Grishin** and objected to by **Anna Sokolova**.

- **Source:** `meetings/2026-03-16-weekly-sync.txt`
- **Decision date:** `2026-03-16`

### memory-eval-vector (completed, 3.5s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'Gateway integration timeout 10 s ", 'Gateway integration timeout 10 s on every Relay route', 'relay route gateway integration timeout 10 s proposed objected']

Proposed by Pavel Grishin and objected by Anna Sokolova. Source: `meetings/2026-03-16-weekly-sync.txt` / claim D06, dated 2026-03-16.

Note: this decision is marked superseded in the same source, with later related decisions existing.

## t21 [ru / objector] Кто предложил и кто возражал против решения «Hybrid IaC: networking (VPC, peering, DNS) stays in Terrafor…»?
**expected:** proposer Sergey Belov, objector Pavel Grishin, 2026-04-20  
**expected sources:** {'sources': ['meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 2.3s, 1 tool calls)
queries: ['"Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform" proposed objecte']

Предложил: **Sergey Belov**.  
Возражал: **Pavel Grishin**.

Источник: `meetings/2026-04-20-weekly-sync.txt` / `ADR-004` / дата **2026-04-20**.

### memory-eval-graph (completed, 5.3s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:$topic})\nOPTIONAL MATCH (p:Person)-[:', "MATCH (d:Decision {key:'decision:iac:2026-04-20'})<-[:PROPOSED]-(p:Person)\nOPTIO"]

Решение **«Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation»** было:

- **предложено**: **Сергеем Беловым** — источник: `meetings/2026-04-20-weekly-sync.txt`, дата **2026-04-20**
- **возражал**: **Павел Гришин** — источник: `meetings/2026-04-20-weekly-sync.txt`, дата **2026-04-20**

Если нужно, могу также показать, есть ли более ранние или более поздние решения по теме **IaC**.

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

### memory-eval-both (completed, 4.2s, 3 tool calls)
queries: ['decision DynamoDB single-table design chosen on PoC-1 results p99 proposed objec', "MATCH (d:Decision {key:'decision:database:2026-05-04'})<-[:PROPOSED]-(p:Person) ", "MATCH (d:Decision {key:'decision:database:2026-05-04'})<-[:OBJECTED_TO]-(p:Perso"]

Proposed by Denis Orlov; objected to by Timur Aliev.

Source: `meetings/2026-05-04-poc-review.txt` / `ADR-003`  
Date: 2026-05-04

### memory-eval-graph (completed, 5.3s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:database'})\nWHERE d.text STARTS", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:database'})\nWHERE d.text STARTS"]

Proposed by Denis Orlov and objected to by Timur Aliev.

Source: `meetings/2026-05-04-poc-review.txt`, decision date `2026-05-04` (`decision:database:2026-05-04`).

### memory-eval-vector (completed, 3.2s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'DynamoDB single-table design, cho", 'DynamoDB single-table design, chosen on PoC-1 results p99 proposed objected', 'single-table design PoC-1 results p99 proposed objected DynamoDB']

Proposed by **Denis Orlov** and objected by **Timur Aliev**.  
Source: `meetings/2026-05-04-poc-review.txt` via claim D10, dated **2026-05-04**.

## t23 [en / objector] Who proposed and who objected to the decision 'Gateway integration timeout raised from 10 s to 30 s after t…'?
**expected:** proposer Anna Sokolova, objector Lena Kim, 2026-05-18  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt']}

### memory-eval-both (completed, 1.9s, 1 tool calls)
queries: ['decision Gateway integration timeout raised from 10 s to 30 s after t proposed o']

Proposed by **Anna Sokolova** and objected to by **Lena Kim**.

Source: `meetings/2026-05-18-weekly-sync.txt`, dated **2026-05-18**.

### memory-eval-graph (completed, 3.9s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'})\nWHERE d.text CONTAI"]

The decision was **proposed by Anna Sokolova** and **objected to by Lena Kim**.

- **Proposed by:** `person:anna-sokolova`  
- **Objected to by:** `person:lena-kim`  
- **Source:** `meetings/2026-05-18-weekly-sync.txt`  
- **Date:** `2026-05-18`

### memory-eval-vector (completed, 2.4s, 1 tool calls)
queries: ["Who proposed and who objected to the decision 'Gateway integration timeout raise"]

Proposed by **Anna Sokolova** and objected to by **Lena Kim**. Source: **meetings/2026-05-18-weekly-sync.txt** (2026-05-18).

## t24 [ru / objector] Кто предложил и кто возражал против решения «Relay moves to Lambda with provisioned concurrency on /deliv…»?
**expected:** proposer Olga Petrova, objector Timur Aliev, 2026-08-03  
**expected sources:** {'sources': ['meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 3.3s, 1 tool calls)
queries: ['Relay moves to Lambda with provisioned concurrency on /deliv proposed objected t']

Предложила Оля Петрова, возражал Тимур Алиев.

Источник:
- `meetings/2026-08-03-architecture-committee.txt` — 2026-08-03: «proposed by Olga Petrova; objection from Timur Aliev»
- `meetings/2026-08-03-architecture-committee.txt` — 2026-08-03: «relay moves to Lambda with provisioned concurrency on /deliver…»



### memory-eval-graph (completed, 4.8s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic}) WHERE d.text CONTAINS $needle', 'MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic}) WHERE d.text CONTAINS $needle']

Решение **«Relay moves to Lambda with provisioned concurrency on /deliver»** предложила **Ольга Петрова** и возразил **Тимур Алиев**.

Источник: `meetings/2026-08-03-architecture-committee.txt`, дата **2026-08-03**.

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

### memory-eval-both (completed, 7.9s, 4 tool calls)
queries: ['Retries move out of the gateway into SQS with a dead-letter proposed objected de', 'MATCH (d:Decision {id:$id})<-[:PROPOSED]-(p:Person)\nOPTIONAL MATCH (p)-[:OBJECTE', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nRETURN d.id AS id, d", "MATCH (d:Decision {id:'D21'})<-[:PROPOSED]-(p:Person)\nOPTIONAL MATCH (o:Person)-"]

Предложил **Ivan Melnik**, возражала **Anna Sokolova**.

Источник:
- decision **D21** / тема retries, дата **2026-08-24**: «Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off».
- В памяти это же зафиксировано как: **Proposed by Ivan Melnik; objection from Anna Sokolova**.

### memory-eval-graph (completed, 4.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nWHERE d.text CONTAIN"]

Решение **«Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off»** было:

- **Предложено**: **Иваном Мельником** — `person:ivan-melnik`  
- **Возражение**: **Анной Соколовой** — `person:anna-sokolova`

Источник: `meetings/2026-08-24-weekly-sync.txt`, дата **2026-08-24**.

### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Retries move out of the gateway int', 'Who proposed and who objected to the decision "Retries move out of the gateway i', 'Retries move out of the gateway into SQS with a dead-letter']

Решение предложил **Ivan Melnik**, а возражала **Anna Sokolova**.  
Источник: **meetings/2026-08-24-weekly-sync.txt**; решение зафиксировано в **ADR-009: Retries through SQS with a dead-letter queue**. Дата: **2026-08-24**.

## t26 [en / objector] Who proposed and who objected to the decision 'Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after t…'?
**expected:** proposer Lena Kim, objector Marat Yusupov, 2026-10-05  
**expected sources:** {'sources': ['meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 2.4s, 1 tool calls)
queries: ['decision "Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after t…" propose']

Proposed by **Lena Kim** and objected to by **Marat Yusupov**.

Source: `meetings/2026-10-05-cutover-planning.txt` — `2026-10-05`  
The decision record also states: “Proposed by Lena Kim; objection from Marat Yusupov.”

### memory-eval-graph (completed, 3.6s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nWHERE d.text STARTS WITH $pre']

Proposed by Lena Kim and objected to by Marat Yusupov.  
Source: `meetings/2026-10-05-cutover-planning.txt`, decision dated `2026-10-05`.

### memory-eval-vector (completed, 2.4s, 1 tool calls)
queries: ["Who proposed and who objected to the decision 'Delivery p95 SLO relaxed from 2 s"]

Proposed by **Lena Kim** and objected to by **Marat Yusupov**. Source: `meetings/2026-10-05-cutover-planning.txt` (2026-10-05), claim D28.

## t27 [en / aggregate] How many decisions have been superseded, and on which topics?
**expected:** 7: D01 (infrastructure as code, 2026-01-12); D02 (SLO, 2026-01-26); D06 (gateway timeout, 2026-03-16); D07 (retries, 2026-03-30); D12 (gateway timeout, 2026-05-18); D14 (retries, 2026-06-15); D15 (compute platform, 2026-06-15)  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-01-26-weekly-sync.txt', 'meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt']}

### memory-eval-both (completed, 4.3s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:SUPERSEDES]->(old:Decision)\nOPTIONAL MATCH (old)-[:ABOUT]->']

There are **7 superseded decisions** in memory.

Topics involved:
- **topic:iac** — `decision:iac:2026-01-12`
- **topic:timeouts** — `decision:timeouts:2026-03-16`
- **topic:retries** — `decision:retries:2026-03-30`
- **topic:compute** — `decision:compute:2026-06-15`
- **topic:timeouts** — `decision:timeouts:2026-05-18`
- **topic:retries** — `decision:retries:2026-06-15`
- **topic:slo** — `decision:slo:2026-01-26`

Source: graph query over `Decision` nodes with `SUPERSEDES` relationships.

### memory-eval-graph (completed, 4.2s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:SUPERSEDES]->(old:Decision)\nWITH count(DISTINCT old) AS sup', 'MATCH (d:Decision)-[:SUPERSEDES]->(old:Decision)-[:ABOUT]->(t:Topic)\nRETURN DIST']

There are **7 superseded decisions** in memory. The topics involved are:

- **topic:compute** — compute platform
- **topic:iac** — infrastructure as code
- **topic:retries** — retries
- **topic:slo** — SLO
- **topic:timeouts** — gateway timeout

Sources:
- Query result from the memory graph, retrieved **2026-10-09**.
- The topic list came from decisions linked by `SUPERSEDES` to prior decisions.

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

### memory-eval-both (completed, 4.9s, 1 tool calls)
queries: ["MATCH (p:Person {key:'person:anna-sokolova'})-[o:OWNS]->(d:Decision)\nWHERE o.to "]

У Anna Sokolova есть **2 действующих решения**.

Это:
1. **decision:ownership:2026-06-01** — `active` — источник: `meetings/2026-06-01-weekly-sync.txt` — дата: **2026-06-01**
2. **decision:retries:2026-08-24** — `active` — источник: `meetings/2026-08-24-weekly-sync.txt` — дата: **2026-08-24**

Решение **decision:retries:2026-06-15** не считаю действующим, потому что у него статус **superseded** — это история, а не текущее состояние.

Если хотите, я могу ещё перечислить, **какие именно темы** это решения покрывают.

### memory-eval-graph (completed, 5.1s, 1 tool calls)
queries: ['MATCH (p:Person {key:$person})-[o:OWNS]->(d:Decision)\nWHERE o.to IS NULL AND d.s']

Anna Sokolova владеет **2 действующими решениями**.

1. **D13** — “Retries and idempotency ownership moves from Nikita to Anna (Nikita leaves on 2026-06-01)”  
   Источник: `meetings/2026-06-01-weekly-sync.txt`  
   Дата: `2026-06-01`

2. **D21** — “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off”  
   Источник: `meetings/2026-08-24-weekly-sync.txt`  
   Дата: `2026-08-24`

Источник вывода: граф памяти, запрос по текущим владениям (`OWNS` с `to = NULL`) для `person:anna-sokolova`.

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

### memory-eval-both (completed, 7.1s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(d:Decision)\nWHERE p.key = 'person:pavel-grishin' AND"]

У Pavel Grishin в памяти есть 4 решения, где он указан как владелец.

Действующие:
1. `decision:iac:2026-02-09` — 2026-02-09 — source: `meetings/2026-02-09-weekly-sync.txt` — status: `active`
2. `decision:gateway:2026-03-02` — 2026-03-02 — source: `meetings/2026-03-02-weekly-sync.txt` — status: `active`

Не действующие:
- `decision:iac:2026-01-12` — 2026-01-12 — source: `meetings/2026-01-12-weekly-sync.txt` — status: `superseded`
- `decision:timeouts:2026-03-16` — 2026-03-16 — source: `meetings/2026-03-16-weekly-sync.txt` — status: `superseded`

Если хотите, я могу еще отдельно вывести только действующие решения в виде списка ключей и дат.

### memory-eval-graph (completed, 10.8s, 2 tool calls)
queries: ["MATCH (p:Person {key:'person:pavel-grishin'})-[o:OWNS]->(d:Decision)\nWHERE o.to ", "MATCH (p:Person {key:'person:pavel-grishin'})-[o:OWNS]->(d:Decision)\nWHERE o.to "]

У Павла Гришина **3 действующих решения**. Источник: граф памяти, связь **OWNS** от `person:pavel-grishin` к решениям; актуальность определена по критерию: у решения нет входящей `SUPERSEDES`, и `status <> 'rejected'`. Дата запроса: граф не хранит отдельную дату для этого факта; я использовал текущие данные из памяти.

Действующие решения:
1. `decision:iac:2026-02-09` — **2026-02-09** — “One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)” — источник: `meetings/2026-02-09-weekly-sync.txt` — статус: `active`.
2. `decision:gateway:2026-03-02` — **2026-03-02** — “Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack” — источник: `meetings/2026-03-02-weekly-sync.txt` — статус: `active`.
3. `decision:iac:2026-04-20` — **2026-04-20** — “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation” — источник: `meetings/2026-04-20-weekly-sync.txt` — статус: `active`.

Для полноты: ещё 3 решения у него в собственности есть, но они **superseded** и поэтому не считаются действующими:
- `decision:iac:2026-01-12` — 2026-01-12 — источник `meetings/2

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

### memory-eval-both (completed, 10.7s, 1 tool calls)
queries: ["MATCH (p:Person {key:'person:ivan-melnik'})-[o:OWNS]->(d:Decision)\nWHERE o.to IS"]

Ivan Melnik владеет 5 действующими решениями:

1. **decision:ownership:2026-07-13** — *Serverless PoC ownership moves from Sergey to Ivan*  
   Источник: `meetings/2026-07-13-weekly-sync.txt`  
   Дата решения: **2026-07-13**

2. **decision:compute:2026-08-03:d17** — *Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances*  
   Источник: `meetings/2026-08-03-architecture-committee.txt`  
   Дата решения: **2026-08-03**

3. **decision:timeouts:2026-08-24** — *Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom*  
   Источник: `meetings/2026-08-24-weekly-sync.txt`  
   Дата решения: **2026-08-24**

4. **decision:ownership:2026-09-07** — *Retries ownership moves from Anna to Ivan, who owns the SQS pipeline*  
   Источник: `meetings/2026-09-07-security-review.txt`  
   Дата решения: **2026-09-07**

5. **decision:cutover:2026-10-05:d25** — *Serverless cutover on 2026-10-19 at 09:00 local, inside the planned-work error budget*  
   Источник: `meetings/2026-10-05-cutover-planning.txt`  
   Дата решения: **2026-10-05**

Если хотите, я могу также переч

### memory-eval-graph (completed, 7.8s, 1 tool calls)
queries: ["MATCH (p:Person {key:'person:ivan-melnik'})-[o:OWNS]->(d:Decision)\nWHERE o.to IS"]

У Ivan Melnik сейчас **5 действующих решений**.

Список:
1. **decision:ownership:2026-07-13** — “Serverless PoC ownership moves from Sergey to Ivan”  
   Источник: `meetings/2026-07-13-weekly-sync.txt`  
   Дата: **2026-07-13**

2. **decision:compute:2026-08-03:d17** — “Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances”  
   Источник: `meetings/2026-08-03-architecture-committee.txt`  
   Дата: **2026-08-03**

3. **decision:timeouts:2026-08-24** — “Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom”  
   Источник: `meetings/2026-08-24-weekly-sync.txt`  
   Дата: **2026-08-24**

4. **decision:ownership:2026-09-07** — “Retries ownership moves from Anna to Ivan, who owns the SQS pipeline”  
   Источник: `meetings/2026-09-07-security-review.txt`  
   Дата: **2026-09-07**

5. **decision:cutover:2026-10-05:d25** — “Serverless cutover on 2026-10-19 at 09:00 local, inside the planned-work error budget”  
   Источник: `meetings/2026-10-05-cutover-planning.txt`  
   Дата: **2026-10-05**

Если хотите, я могу ещё сгруппировать их по темам.

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

### memory-eval-both (completed, 6.7s, 1 tool calls)
queries: ["MATCH (p:Person {key:$key})-[:OWNS]->(d:Decision)\nWHERE d.status <> 'rejected' A"]

У Lena Kim 3 действующих решения.

1. **decision:iac:2026-02-23** — `D04`  
   Дата: 2026-02-23  
   Источник: `meetings/2026-02-23-incident-review.txt`  
   Текст: “Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call”

2. **decision:slo:2026-10-05** — `D28`  
   Дата: 2026-10-05  
   Источник: `meetings/2026-10-05-cutover-planning.txt`  
   Текст: “Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s”

3. **decision:cutover:2026-10-05:d27** — `D27`  
   Дата: 2026-10-05  
   Источник: `meetings/2026-10-05-cutover-planning.txt`  
   Текст: “Rollback owner for both cutovers is Lena”

Итого: **3**.

### memory-eval-graph (completed, 5.4s, 1 tool calls)
queries: ['MATCH (p:Person {key:$key})-[o:OWNS]->(d:Decision)\nWHERE o.to IS NULL AND d.stat']

У Lena Kim сейчас 3 действующих решения в её владении.

- `decision:iac:2026-02-23` — «Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call» — источник: `meetings/2026-02-23-incident-review.txt`, дата: `2026-02-23`.
- `decision:slo:2026-10-05` — «Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s» — источник: `meetings/2026-10-05-cutover-planning.txt`, дата: `2026-10-05`.
- `decision:cutover:2026-10-05:d27` — «Rollback owner for both cutovers is Lena» — источник: `meetings/2026-10-05-cutover-planning.txt`, дата: `2026-10-05`.

Замечание: решение `decision:slo:2026-01-26` есть в её владении, но его статус `superseded`, поэтому я не считаю его действующим. Источник: `meetings/2026-01-26-weekly-sync.txt`, дата: `2026-01-26`.

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

### memory-eval-both (completed, 5.7s, 1 tool calls)
queries: ["MATCH (a:ADR)\nWHERE coalesce(a.status,'') <> 'Accepted'\nRETURN a.key AS key, a.i"]

The ADRs that are not `Accepted` are:

- **ADR-001** — status: **Superseded**  
  Source: `adr/ADR-001.md` (dated **2026-01-14**)

- **ADR-005** — status: **Superseded**  
  Source: `adr/ADR-005.md` (dated **2026-06-17**)

- **ADR-007** — status: **Rejected**  
  Source: `adr/ADR-007.md` (dated **2026-08-05**)

- **ADR-010** — status: **Proposed**  
  Source: `adr/ADR-010.md` (dated **2026-09-23**)

### memory-eval-graph (completed, 3.7s, 1 tool calls)
queries: ["MATCH (a:ADR) WHERE a.status <> 'Accepted' RETURN a.title AS title, a.file AS fi"]

These ADRs are not Accepted:

- **adr/ADR-001.md** — *Migrate infrastructure code from Terraform to CloudFormation* — **Superseded** — date **2026-01-14**
- **adr/ADR-005.md** — *Evaluate EKS and Lambda with two proofs of concept* — **Superseded** — date **2026-06-17**
- **adr/ADR-007.md** — *Keep Relay on EKS with autoscaling* — **Rejected** — date **2026-08-05**
- **adr/ADR-010.md** — *Gateway timeout policy for Lambda integrations* — **Proposed** — date **2026-09-23**

Source: ADR records in memory.

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

### memory-eval-both (completed, 7.3s, 2 tool calls)
queries: ['MATCH (o:OpenItem)\nWHERE o.raised <= $d\nOPTIONAL MATCH (o)<-[ow:OWNS]-(:Person)\n', "MATCH (o:OpenItem)\nWHERE o.raised <= $d AND o.status = 'open'\nOPTIONAL MATCH (o)"]

На 2026-06-15 открытых вопросов **без владельца** в памяти **нет**.

Что я проверил:
- нашёл открытые вопросы, поднятые до 2026-06-15;
- отдельно отфильтровал только статус `open`;
- проверил наличие текущего владельца по правилу `OWNS` с `to = NULL`.

Результат:
- **not in memory** для открытых вопросов без владельца на эту дату.

Что нашлось в памяти дополнительно:
- `openitem:database:2026-05-04` — `O1`, но статус `closed`
- `openitem:database:2026-05-18` — `O4`, статус `open`, но он не оказался без владельца по графу

Источники:
- граф памяти, срез на дату `2026-06-15`

### memory-eval-graph (completed, 4.4s, 1 tool calls)
queries: ['MATCH (o:OpenItem)\nWHERE o.raised <= $d\nAND NOT EXISTS {\n  MATCH (p:Person)-[own']

На 2026-06-15 без владельца был один открытый вопрос:

- `openitem:database:2026-05-18` — “DocumentDB decommission date” — поднят 2026-05-18, статус `open`, файл-источник: `meetings/2026-05-18-weekly-sync.txt` (meeting date 2026-05-18).

Я также проверил, что другой найденный вопрос на ту же дату (`openitem:database:2026-05-04`) был `closed`, поэтому в ответ не входит.

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

### memory-eval-both (completed, 4.6s, 1 tool calls)
queries: ["MATCH (o:OpenItem)\nWHERE o.raised <= date('2026-08-17')\nOPTIONAL MATCH (o)<-[own"]

На дату 2026-08-17 в памяти **нет** открытых вопросов без владельца.

Что я проверил:
- схему графа;
- все `OpenItem`, поднятые не позже 2026-08-17, и их связи `OWNS`.

Результат запроса:
- записей не найдено.

Если хотите, я могу ещё проверить, есть ли **открытые вопросы с владельцем, но с истёкшим сроком владения** на эту дату.

### memory-eval-graph (completed, 5.3s, 1 tool calls)
queries: ['MATCH (o:OpenItem)\nWHERE o.raised <= $d\n  AND NOT EXISTS {\n    MATCH (p:Person)-']

На **2026-08-17** без владельца были такие открытые вопросы:

1. **DocumentDB decommission date**  
   - raised: **2026-05-18**  
   - status: **open**  
   - key: **openitem:database:2026-05-18**  
   - source: **OpenItem** с датой raised **2026-05-18**

2. **Load test on Lambda at 10x current volume**  
   - raised: **2026-07-27**  
   - status: **open**  
   - key: **openitem:compute:2026-07-27**  
   - source: **OpenItem** с датой raised **2026-07-27**

Я искал открытые `OpenItem`, поднятые не позже **2026-08-17**, у которых на эту дату нет действующего владельца и которые не закрыты решением к этой дате.

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

### memory-eval-both (completed, 7.3s, 2 tool calls)
queries: ['MATCH (o:OpenItem)-[:RAISED_IN]->(m:Meeting)\nOPTIONAL MATCH (o)<-[ow:OWNS]-(p:Pe', 'MATCH (o:OpenItem)-[:RAISED_IN]->(m:Meeting)\nOPTIONAL MATCH (o)<-[ow:OWNS]-(p:Pe']

On 2026-10-05, the open items with no owner in memory were:

- `openitem:database:2026-05-18` — “DocumentDB decommission date”  
  Raised in `meeting:2026-05-18` on 2026-05-18. Status: open.
- `openitem:compute:2026-07-27` — “Load test on Lambda at 10x current volume”  
  Raised in `meeting:2026-07-27:poc-review` on 2026-07-27. Status: open.
- `openitem:security:2026-09-07` — “Rotate DocumentDB credentials before decommission”  
  Raised in `meeting:2026-09-07:security-review` on 2026-09-07. Status: open.

Source: Neo4j graph, queried for `OpenItem` nodes with no active `OWNS` relationship on 2026-10-05.

### memory-eval-graph (completed, 4.6s, 1 tool calls)
queries: ['MATCH (o:OpenItem)\nWHERE o.raised <= $d\n  AND NOT EXISTS {\n    MATCH (:Person)-[']

On 2026-10-05, these open items had no owner:

- `openitem:database:2026-05-04` — “DynamoDB migration dry run on a production snapshot” — raised 2026-05-04, status `closed`
- `openitem:database:2026-05-18` — “DocumentDB decommission date” — raised 2026-05-18, status `open`
- `openitem:compute:2026-07-27` — “Load test on Lambda at 10x current volume” — raised 2026-07-27, status `open`
- `openitem:security:2026-09-07` — “Rotate DocumentDB credentials before decommission” — raised 2026-09-07, status `open`

Source: graph memory query on open items and OWNS edges, evaluated as of 2026-10-05.

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

### memory-eval-both (completed, 19.5s, 2 tool calls)
queries: ["MATCH (d:Document)<-[m:MAKES_STALE]-(dec:Decision)\nWHERE m.since <= date('2026-0", 'MATCH (d:Document)<-[m:MAKES_STALE]-(dec:Decision)\nRETURN d.key AS doc_key, d.fi']

On 2026-07-01, the documents that were out of date in memory were:

- `docs/iac-cloudformation.md` — **CloudFormation migration guide**  
  - Why stale: a decision on `2026-04-20` says “all infrastructure including networking moves to CloudFormation.”  
  - Source: `meetings/2026-04-20-weekly-sync.txt`  
  - The document was last updated `2026-02-11`, so it was already stale by 2026-07-01.

- `confluence/architecture.xhtml` — **Relay architecture**  
  - Why stale: a decision on `2026-05-04` says it “shows DocumentDB.”  
  - Source: `meetings/2026-05-04-poc-review.txt`  
  - Updated `2026-03-12`, so stale by 2026-07-01.

- `docs/gateway.md` — **API gateway integration**  
  - Why stale: a decision on `2026-05-18` says it “says the integration timeout is 10 s.”  
  - Source: `meetings/2026-05-18-weekly-sync.txt`  
  - Updated `2026-03-18`, so stale by 2026-07-01.  
  - There is also a later superseded note from `2026-06-15` that it “says retries are disabled on /deliver.”

- `docs/onboarding.md` — **Team onboarding**  
  - Why stale: a decision on `2026-06-01` says it “lists Nikita as retries owner and does not list Sergey or Ivan.”  
  - Source: `meetings/2026-06-01-weekly-sync.txt

### memory-eval-graph (completed, 17.4s, 1 tool calls)
queries: ['MATCH (d:Decision)-[s:MAKES_STALE]->(doc:Document)\nWHERE s.since <= $date\nRETURN']

На 2026-07-01 в памяти есть 5 документов, которые были устаревшими, и причина для каждого зафиксирована как decision → MAKES_STALE.

- `confluence/architecture.xhtml` — **Relay architecture**  
  Устарел с `2026-05-04`, потому что решение от `2026-05-04` изменило факт: документ **показывает DocumentDB**, а текущая decision говорит **“DynamoDB single-table design”**.  
  Источник решения: `meetings/2026-05-04-poc-review.txt` от `2026-05-04`.

- `confluence/decision-log.xhtml` — **Decision log**  
  Устарел с `2026-06-15`, потому что решение от `2026-06-15` изменило факт: документ **останавливается на 2026-06-01**, но decision от `2026-06-15` уже зафиксировала, что **retries включены на POST /deliver**.  
  Источник решения: `meetings/2026-06-15-weekly-sync.txt` от `2026-06-15`.

- `docs/gateway.md` — **API gateway integration**  
  Устарел с `2026-05-18`, потому что решение от `2026-05-18` изменило факт: документ **говорит, что integration timeout = 10 s**, а decision установила **30 s**.  
  Источник решения: `meetings/2026-05-18-weekly-sync.txt` от `2026-05-18`.

- `docs/gateway.md` — **API gateway integration**  
  Устарел с `2026-06-15`, потому что решение от `2026-06-15` измени

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

### memory-eval-both (completed, 31.4s, 1 tool calls)
queries: ['MATCH (d:Document)<-[m:MAKES_STALE]-(dec:Decision)\nWHERE date(m.since) <= date($']

On 2026-10-05, these documents were out of date in memory:

- `confluence/architecture.xhtml` — **Relay architecture**
  - Last updated: 2026-03-12
  - Out of date because newer decisions say:
    - it **shows DocumentDB** since 2026-05-04
    - it **shows EKS as the runtime** since 2026-08-03
  - Sources: `meetings/2026-05-04-poc-review.txt` and `meetings/2026-08-03-architecture-committee.txt`

- `confluence/decision-log.xhtml` — **Decision log**
  - Last updated: 2026-06-03
  - Out of date because a newer decision says it **stops at 2026-06-01**
  - Source: `meetings/2026-06-15-weekly-sync.txt`

- `confluence/migration-roadmap.xhtml` — **2026 migration roadmap**
  - Last updated: 2026-06-20
  - Out of date because a newer decision says it **lists compute decision as pending PoC**
  - Source: `meetings/2026-08-03-architecture-committee.txt`

- `confluence/team-roster.xhtml` — **Team roster and ownership**
  - Last updated: 2026-07-08
  - Out of date because a newer decision says it **lists Anna as retries owner**
  - Source: `meetings/2026-09-07-security-review.txt`

- `docs/db-migration-plan.md` — **DocumentDB to DynamoDB migration plan**
  - Last updated: 2026-05-26
  - Out of d

### memory-eval-graph (completed, 95.3s, 1 tool calls)
queries: ['MATCH (d:Decision)-[s:MAKES_STALE]->(doc:Document)\nWHERE s.since <= $asOf\nRETURN']

On **2026-10-05**, the following documents were out of date, because later decisions made specific facts in them stale.

1. **`confluence/architecture.xhtml`** — *Relay architecture*  
   - **Why stale:** the document still showed **DocumentDB** (`fact: "shows DocumentDB"`) and **EKS as the runtime** (`fact: "shows EKS as the runtime"`).  
   - **What made it stale:**  
     - Decision dated **2026-05-04** from `meetings/2026-05-04-poc-review.txt` changed the architecture to **DynamoDB single-table**.  
     - Decision dated **2026-08-03** from `meetings/2026-08-03-architecture-committee.txt` changed compute to **Lambda with provisioned concurrency**.  
   - **Source:** `confluence/architecture.xhtml` updated **2026-03-12**; stale from decisions on **2026-05-04** and **2026-08-03**.

2. **`confluence/decision-log.xhtml`** — *Decision log*  
   - **Why stale:** it still said retries stopped at **2026-06-01** (`fact: "stops at 2026-06-01"`).  
   - **What made it stale:** decision dated **2026-06-15** from `meetings/2026-06-15-weekly-sync.txt` enabled retries on `POST /deliver` with max 3 attempts and a 15% retry budget.  
   - **Source:** `confluence/decision-log.xhtml` updated **20

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

### memory-eval-both (completed, 5.8s, 2 tool calls)
queries: ['"DynamoDB single-table design" PoC-1 results p99 rationale numbers decision', "MATCH (d:Decision {key:'decision:database:2026-05-04'})-[:BASED_ON]->(p:PoC) OPT"]

Решение основано на **PoC-1: DynamoDB single-table vs multi-table** (`poc:poc-1`).  
Источник: граф, связь `BASED_ON` от решения `decision:database:2026-05-04` к этому PoC.

По цифрам решение опирается на такие результаты PoC-1:

- **Read p99**: **4 ms** у single-table против **11 ms** у multi-table
- **Write p99**: **8 ms** у single-table против **9 ms** у multi-table
- **Стоимость при projected volume**: **$3,200** у single-table против **$5,100** у multi-table, то есть **на 38% ниже** baseline

Источник: `docs/poc-dynamodb-report.md`, раздел **Results**, updated **2026-05-01**.  
Дополнительно это же зафиксировано в решении `decision:database:2026-05-04` / `ADR-003`, updated **2026-05-06**.

Если хотите, я могу еще показать точную формулировку из ADR-003 и отметить, какие именно метрики были сравнены.

### memory-eval-graph (completed, 4.5s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:database'})\nWHERE d.text CONTAI"]

Решение основано на **PoC-1: DynamoDB single-table vs multi-table**.

Цифры в решении:
- **p99 read: 4 ms** для single-table
- **p99 read: 11 ms** для multi-table
- **на 38% ниже стоимость** при прогнозируемом объёме

Источник решения:
- `meetings/2026-05-04-poc-review.txt`, **2026-05-04**

Источник PoC:
- `docs/poc-dynamodb-report.md`
- `poc:poc-1` — результаты: `{"single_table_p99_read_ms": 4, "multi_table_p99_read_ms": 11, "single_table_cost_delta_pct": -38, "documentdb_p99_read_ms": 9}`

Если нужно, могу также показать, является ли это решение текущим или оно уже было чем-то superseded.

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

### memory-eval-both (completed, 6.0s, 2 tool calls)
queries: ['"Relay moves to Lambda with provisioned concurrency" PoC цифры решение', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:compute'})\nOPTIONAL MATCH (d)-"]

Решение основано на **PoC-3**.

Цифры, на которых оно основано:
- **p95 latency = 1.9 s** с provisioned concurrency на `/deliver`
- **monthly cost = $3,600**, то есть **на 41% ниже, чем EKS**
- в самом PoC также зафиксировано:
  - без provisioned concurrency p95 = **3.4 s**
  - cold start = **1.2 s**
  - scale-out до 3x volume — **immediate**

Источники:
- `docs/poc-lambda-report.md`, updated **2026-07-24**
- `adr/ADR-006.md`, updated **2026-08-05**
- decision `decision:compute:2026-08-03:d17`, date **2026-08-03**

Если нужно, могу отдельно показать, как именно формулируется связь “decision based on PoC-3” в графе.

### memory-eval-graph (completed, 7.4s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'})\nWHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'})-[:OWNS]-(p:Person)\nW"]

Решение **«Relay moves to Lambda with provisioned concurrency on /deliver»** основано на **PoC-3: Relay on Lambda**.

Что в PoC:
- **PoC key:** `poc:poc-3`
- **Название:** `PoC-3: Relay on Lambda`
- **Период:** `2026-06-22` — `2026-07-24`
- **Источник решения:** `meetings/2026-08-03-architecture-committee.txt`
- **Дата решения:** `2026-08-03`

Какие цифры указаны в PoC и в самом решении:
- **41% lower monthly cost** / `cost_delta_vs_eks_pct = -41`
- **p95 warm = 1.9 s**
- **p95 cold = 3.4 s**
- **cold start = 1.2 s**
- **monthly cost = 3600 USD**

Источник:
- `decision:compute:2026-08-03:d17` — `meetings/2026-08-03-architecture-committee.txt`, `2026-08-03`
- `poc:poc-3` — `PoC-3: Relay on Lambda`, `2026-06-22` to `2026-07-24`

Если хотите, я могу ещё отдельно выписать, какие именно цифры были аргументом за **provisioned concurrency**.

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

### memory-eval-both (completed, 9.5s, 5 tool calls)
queries: ['"Keep Relay on EKS with autoscaling" rejected p95 0.4 s PoC цифры основано решен', "MATCH (d:Decision {key:'decision:compute:2026-08-03'})-[:BASED_ON]->(p) RETURN d", "MATCH (d:Decision {key:'decision:compute:2026-08-03'})-[:RECORDED_IN]->(doc:Docu", "MATCH (d:Decision {key:'decision:compute:2026-08-03'})-[:BASED_ON]->(p:PoC) RETU", "MATCH (p:PoC)<-[:BASED_ON]-(d:Decision) WHERE d.text CONTAINS 'Keep Relay on EKS"]

Решение основано на **PoC-2: Relay on EKS with autoscaling**.

Цифры, на которых оно основано:
- **p95 = 0.4 s**
- **monthly_cost_usd = 6100**
- **ops_effort = "a second platform team"**

Источник:
- **`docs/poc-eks-report.md`**, через связь `BASED_ON` у решения `decision:compute:2026-08-03:d18`
- Дата решения: **2026-08-03**

Подтверждающая запись в памяти:
- `decision:compute:2026-08-03:d18` — статус `rejected`
- PoC: `poc:poc-2` — `PoC-2: Relay on EKS with autoscaling`
- результаты PoC: `{"p95_s": 0.4, "monthly_cost_usd": 6100, "ops_effort": "a second platform team"}`

Если хотите, я могу ещё достать, **почему именно это решение было отклонено** в формулировке ADR/meeting note.

### memory-eval-graph (completed, 7.2s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})-[:ABOUT]-(x) RETURN d.key AS ', 'MATCH (d:Decision {key:$dkey})-[:BASED_ON]->(p:PoC) OPTIONAL MATCH (p)<-[:REVIEW']

Решение основано на **PoC-2: Relay on EKS with autoscaling**.

Цифры из memory:
- **p95 = 0.4 s**
- **monthly_cost_usd = 6100**
- **ops_effort = "a second platform team"**

Источник:
- **decision:compute:2026-08-03:d18** — `meetings/2026-08-03-architecture-committee.txt` от **2026-08-03**
- **poc:poc-2** — `PoC-2: Relay on EKS with autoscaling`, период **2026-06-22 .. 2026-07-24**

В самом решении сказано:
- `Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run)`

То есть решение опирается на PoC-2 и на сравнение:
- **latency:** p95 0.4 s
- **cost:** 1.7x monthly cost
- **operations:** ещё одна platform team / вторая платформа для поддержки

Если хотите, я могу ещё достать, **относительно чего именно считались “1.7x”**, если это есть в памяти.

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

### memory-eval-both (completed, 3.2s, 1 tool calls)
queries: ['ADR-001 Migrate infrastructure code from Terraform to CloudFormation status supe']

ADR-001 is **superseded** as of **2026-01-14**. The current status in memory is:

- **Status:** Superseded
- **Superseded by:** **ADR-004**

Source: **adr/ADR-001.md** (`updated 2026-01-14`) and the linked decision claim in **meetings/2026-01-12-weekly-sync.txt** (`2026-01-12`).

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.key AS key, a.id AS id, a.title AS title, a.date']

ADR-001 is **Superseded**.  
Source: **adr/ADR-001.md**, dated **2026-01-14**.

I retrieved:
- ADR id: ADR-001
- Title: *Migrate infrastructure code from Terraform to CloudFormation*
- Status: **Superseded**

### memory-eval-vector (completed, 4.8s, 3 tool calls)
queries: ["What is the status of ADR-001 ('Migrate infrastructure code from Terraform to Cl", 'ADR-001 Migrate infrastructure code from Terraform to CloudFormation status', 'status ADR-001 Terraform CloudFormation']

ADR-001 is **Superseded (superseded by ADR-004)**. Source: `adr/ADR-001.md` (updated **2026-01-14**). The ADR header explicitly says “Status: Superseded (superseded by ADR-004)”.

I also found ADR-004, which is **Accepted, supersedes ADR-001** in `adr/ADR-004.md` (updated **2026-04-22**). Since it is newer, ADR-004 is the current decision on this topic.

## t42 [en / adr_status] What is the status of ADR-005 ('Evaluate EKS and Lambda with two proofs of concept')?
**expected:** Superseded, superseded by ADR-006  
**expected sources:** {'sources': ['adr/ADR-005.md']}

### memory-eval-both (completed, 2.1s, 1 tool calls)
queries: ['ADR-005 Evaluate EKS and Lambda with two proofs of concept status supersedes cur']

ADR-005 is **superseded**.

Source:
- **adr/ADR-005.md** — updated **2026-06-17**
- The doc status says: **“Superseded (superseded by ADR-006)”**

So the current status in memory is **Superseded**, with **ADR-006** as the superseding decision.

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-005'}) RETURN a.key AS key, a.id AS id, a.title AS title, "]

ADR-005 is **Superseded**.  
Source: `adr/ADR-005.md`, dated **2026-06-17**.

I retrieved:
- ADR id: `ADR-005`
- Title: “Evaluate EKS and Lambda with two proofs of concept”
- Status: `Superseded`
- Date: `2026-06-17`



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

### memory-eval-both (completed, 2.0s, 1 tool calls)
queries: ['ADR-007 Keep Relay on EKS with autoscaling status supersedes current decision']

ADR-007 is **Rejected**.

Source:
- `adr/ADR-007.md` — updated **2026-08-05**
- The ADR record and decision chunk both show status **Rejected** on **2026-08-05**.

### memory-eval-graph (completed, 3.1s, 1 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.key AS key, a.id AS id, a.title AS title, a.date']

ADR-007 is **Rejected**.  
Source: `adr/ADR-007.md`, dated `2026-08-05`.

I retrieved:
- ADR id: `ADR-007`
- Title: `Keep Relay on EKS with autoscaling`
- Status: `Rejected`
- File: `adr/ADR-007.md`
- Date: `2026-08-05`

### memory-eval-vector (completed, 3.9s, 3 tool calls)
queries: ["What is the status of ADR-007 ('Keep Relay on EKS with autoscaling')?", 'ADR-007 Keep Relay on EKS with autoscaling status', 'status ADR-007 Keep Relay on EKS autoscaling']

ADR-007 is **Rejected**. The ADR record shows **Status: Rejected** and **Date: 2026-08-05**. Source: `adr/ADR-007.md` (updated 2026-08-05).

I also found a supporting decision chunk stating “Keep Relay on EKS with autoscaling (rejected…)” in `adr/ADR-007.md` (updated 2026-08-05).

## t44 [en / adr_status] What is the status of ADR-010 ('Gateway timeout policy for Lambda integrations')?
**expected:** Proposed; Never accepted; D20 (25 s) is the live decision and the ADR still proposes 20 s  
**expected sources:** {'sources': ['adr/ADR-010.md']}

### memory-eval-both (completed, 2.4s, 1 tool calls)
queries: ['ADR-010 Gateway timeout policy for Lambda integrations status supersedes current']

ADR-010 is **Proposed**.

Source:
- `adr/ADR-010.md`, updated **2026-09-23** — the ADR header says **Status: Proposed**.
- The same ADR’s Consequences section also says it is **“Proposed, not accepted”** and notes that the live value was set separately on **2026-08-24**.

If you want, I can also check whether ADR-010 was later superseded or whether there is a current decision on the underlying timeout policy.

### memory-eval-graph (completed, 2.7s, 1 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-010'}) RETURN a.id AS id, a.title AS title, a.date AS date"]

ADR-010 is **Proposed**.  
Source: **adr/ADR-010.md**, dated **2026-09-23**.

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

### memory-eval-both (completed, 5.8s, 2 tool calls)
queries: ['decision "Front Relay with the API gateway; the gateway and its routes" depend o', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:gateway'}) WHERE d.status <> '"]

The decision **“Front Relay with the API gateway; the gateway and its routes…”** depended on **`decision:iac:2026-02-09`**.

- Source: graph decision `decision:gateway:2026-03-02`
- Date: **2026-03-02**
- Relation: `DEPENDS_ON -> decision:iac:2026-02-09`

I also found the matching ADR text:
- File: `adr/ADR-002.md`
- Updated: **2026-03-04**
- It describes the same gateway decision, but the graph shows the dependency explicitly.

### memory-eval-graph (completed, 5.4s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'})\nWHERE d.text STARTS ", "MATCH (d:Decision {key:'decision:gateway:2026-03-02'})-[:DEPENDS_ON]->(dep:Decis"]

The decision **“Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack”** depended on:

- **Decision `decision:iac:2026-02-09`** — *“One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway)”*  
  **Source:** `meetings/2026-02-09-weekly-sync.txt`  
  **Date:** `2026-02-09`

I retrieved:
- the gateway decision itself: `decision:gateway:2026-03-02`  
  **Source:** `meetings/2026-03-02-weekly-sync.txt`  
  **Date:** `2026-03-02`
- its dependency: `decision:iac:2026-02-09`  
  **Source:** `meetings/2026-02-09-weekly-sync.txt`  
  **Date:** `2026-02-09`



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
