
## m01 [en / fact] What is the delivery latency SLO and what exactly does it measure?
**expected:** p95 2 s over 5 minutes, from POST /deliver accepted to the first delivery attempt sent, not to the customer's answer; success rate 99.5% monthly  
**expected sources:** {'sources': ['docs/slo.md', 'meetings/2026-01-26-weekly-sync.txt']}

### memory-eval-both (completed, 3.9s, 3 tool calls)
queries: ['delivery latency SLO what exactly does it measure Relay', 'delivery latency SLO measure latency delivery Relay SLO', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'slo'}) WHERE NOT (d)<-[:SUPERSEDES]-("]

The delivery latency SLO is **p95 of 2 seconds over a 5-minute window**.

What it measures: **from `POST /deliver` being accepted to the first delivery attempt being sent**. It measures **Relay’s latency, not the customer’s** — it ends when the first attempt is sent, **not** when the customer answers.

Source: `docs/slo.md`, updated **2026-01-28**.

### memory-eval-graph (completed, 5.6s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE d.text CONTAINS 'd", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) RETURN d.text, d.date, d", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'}) WHERE d.text CONTAIN"]

The delivery latency SLO is **p95 end-to-end latency of 2 s over a 5-minute window**. It is paired with a **monthly delivery success rate of 99.5%**. Source: `meetings/2026-01-26-weekly-sync.txt`, dated `2026-01-26`.

What it measures: the decision text says it measures **end-to-end latency** at **p95** over a **5-minute window**; I don’t have a more detailed definition of the exact start/end timestamps in memory. Source: `meetings/2026-01-26-weekly-sync.txt`, dated `2026-01-26`.

Assumption: you meant the current delivery latency SLO on the SLO topic.

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['What is the delivery latency SLO and what exactly does it measure?', 'delivery latency SLO measures relay webhook delivery latency exact definition', 'delivery latency SLO definition measure latency webhook delivery']

The delivery latency SLO is **p95 of 2 seconds over a 5-minute window**. It measures the time **from `POST /deliver` being accepted to the first delivery attempt being sent**.

It specifically measures **Relay’s internal delivery work**, not the customer response: it **ends when the first attempt is sent, not when the customer answers**.

Sources:
- `docs/slo.md` — updated **2026-01-28**
- `meetings/2026-01-26-weekly-sync.txt` — decision dated **2026-01-26**

## m02 [ru / fact] Сколько попыток доставки делает очередь до dead-letter и с какими задержками?
**expected:** 5 попыток, экспоненциально: 30 с, 2 мин, 10 мин, 30 мин, 2 ч; потом DLQ и алерт  
**expected sources:** {'sources': ['docs/retries-dlq.md', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.7s, 2 tool calls)
queries: ['очередь delivery attempts dead-letter retries delays backoff SQS DLQ сколько поп', 'dead-letter queue attempts delays retry budget backoff queue delivery']

Очередь делает **5 попыток**, после чего сообщение уходит в dead-letter queue.

Задержки между ретраями по памяти проекта такие:
- **30 s**
- **2 min**
- **10 min**
- **30 min**
- **2 h**

Источник: `docs/retries-dlq.md` — обновлено **2026-08-27**; также это зафиксировано в `adr/ADR-009.md` — **2026-08-26**.

Если хотите, могу ещё сказать, **какой именно механизм redrive используется** и **что происходит после попадания в DLQ**.

### memory-eval-graph (completed, 3.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (d)<-[:SUP"]

В памяти есть только решение про retries, а не отдельная параметризованная схема очереди:  
- `meetings/2026-08-24-weekly-sync.txt` — 2026-08-24: «Retries move to SQS with a dead letter queue after 5 attempts, and gateway retries on deliver are turned off.»  

То есть до dead-letter очередь делает **5 попыток**.  
**Задержки между попытками в памяти не указаны** — это там не зафиксировано.

### memory-eval-vector (completed, 4.8s, 3 tool calls)
queries: ['Сколько попыток доставки делает очередь до dead-letter и с какими задержками?', 'сколько попыток доставки до dead-letter задержки очередь relay webhook delivery', 'attempts delivery dead-letter delays queue relay webhook']

Очередь делает **5 попыток** доставки до dead-letter queue.

Задержки между redrive-попытками: **30 s, 2 min, 10 min, 30 min, 2 h**.

Источник:
- `docs/retries-dlq.md` — updated **2026-08-27**: “SQS redrives with exponential backoff: 30 s, 2 min, 10 min, 30 min, 2 h. After 5 attempts the message goes to `relay-deliveries-dlq`.”
- `adr/ADR-009.md` — updated **2026-08-26**: “Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts.”

Если хотите, могу ещё пояснить, что именно считается “попыткой” в этой схеме.

## m03 [en / fact] Why does the hybrid IaC layout keep networking in Terraform?
**expected:** cross-account peering and DNS delegation need custom resources in CloudFormation but are native in the Terraform the network team already maintains; moving network was 30% of the effort  
**expected sources:** {'sources': ['adr/ADR-004.md', 'meetings/2026-04-20-weekly-sync.txt', 'docs/iac-hybrid.md']}

### memory-eval-both (completed, 4.4s, 2 tool calls)
queries: ['hybrid IaC layout keeps networking in Terraform why networking Terraform rationa', 'гибридный IaC networking Terraform почему сеть в Terraform причина']

Assumption: you mean the architecture decision behind the split, not just the current boundary.

It stays in Terraform because ADR-004 says the networking module was “the last to move and the hardest”: cross-account peering and DNS delegation “need custom resources in CloudFormation,” while the same networking is already “expressed natively in the Terraform the network team maintains for the whole company.”  
Source: `adr/ADR-004.md`, 2026-04-22.

The decision itself is also explicit: “networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation.”  
Source: `adr/ADR-004.md`, 2026-04-22.

There’s also an operational boundary in the hybrid layout doc: Terraform exports network outputs to SSM Parameter Store, and CloudFormation consumes them; changing a network output requires a Terraform apply followed by a CloudFormation deploy.  
Source: `docs/iac-hybrid.md`, 2026-04-24.

### memory-eval-graph (completed, 5.2s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'})\nWHERE NOT (d)<-[:SUPERSE", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'})\nOPTIONAL MATCH (d)-[:SUP"]

The live reason in memory is that the team chose a hybrid boundary: **networking remains in Terraform while application stacks move to CloudFormation**. The latest decision on this topic says exactly that the boundary is documented in an ADR. Source: `meetings/2026-04-20-weekly-sync.txt`, dated `2026-04-20` (`A21`).

There is also a later note confirming the arrangement is still in place: **“The network remains in Terraform, application stacks remain in CloudFormation, and drift detection works on both sides in production.”** Source: `meetings/2026-06-01-weekly-sync.txt`, dated `2026-06-01` (`A31`).

What I could retrieve does **not** include a more detailed rationale like cost, risk, or technical constraint for why networking stayed in Terraform; that specific explanation is **not in memory**.

### memory-eval-vector (completed, 5.6s, 3 tool calls)
queries: ['Why does the hybrid IaC layout keep networking in Terraform?', 'Why is networking kept in Terraform in the hybrid IaC layout?', 'hybrid IaC networking Terraform reason ADR-004']

The memory says networking stays in Terraform because it was the last and hardest part to move: cross-account peering and DNS delegation would require custom resources in CloudFormation, while that networking already exists natively in the Terraform the network team maintains. Source: `adr/ADR-004.md` (2026-04-22), section “Context”.

The current decision is also explicitly stated as: VPC, peering, and DNS stay in Terraform; application stacks are CloudFormation. Source: `adr/ADR-004.md` (2026-04-22), section “Decision”.

I also found the newer boundary doc, which says the same layout and notes that it is based on ADR-004, so the docs page is not newer than the decision here. Source: `docs/iac-hybrid.md` (2026-04-24), section “Hybrid IaC layout”.

## m04 [ru / contradiction] В gateway.md написано, что таймаут интеграции 10 секунд. Это актуально?
**expected:** нет; документ от 2026-03-18, таймаут менялся на 30 с (2026-05-18) и на 25 с (2026-08-24); текущее значение 25 с  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 6.0s, 3 tool calls)
queries: ["MATCH (doc:Document) WHERE doc.file ENDS WITH 'gateway.md' OPTIONAL MATCH (dec:D", 'gateway.md integration timeout 10 seconds актуально timeout integration 10 secon', 'gateway.md таймаут интеграции 10 секунд актуально']

Да — по текущей памяти это актуально.

- В `docs/gateway.md` сказано: **“The integration timeout on every Relay route is 10 seconds”**; файл обновлён **2026-03-18**.
- Это совпадает с решением из `adr/ADR-002.md` (**Accepted**, **2026-03-04**), где тоже зафиксировано **10 seconds**.

Источник:
- `docs/gateway.md`, updated **2026-03-18**
- `adr/ADR-002.md`, date **2026-03-04**, status **Accepted**

Если хочешь, могу ещё проверить, не было ли позже решения, которое это изменило.

### memory-eval-graph (completed, 5.0s, 2 tool calls)
queries: ["MATCH (doc:Document) WHERE doc.file ENDS WITH 'gateway.md' RETURN doc.file, doc.", "MATCH (doc:Document {file:'docs/gateway.md'}) OPTIONAL MATCH (dec:Decision) WHER"]

Нет, уже не актуально.

`docs/gateway.md` обновлён **2026-03-18**; позже в памяти есть решение, которое изменило лимит:
- **A30**: “The integration timeout is increased from 10 s to 30 s while synchronous mode remains enabled.”  
  источник: `meetings/2026-05-18-weekly-sync.txt`, дата **2026-05-18**

Значит, значение **10 секунд** в `docs/gateway.md` устарело, а актуальное на сегодня — **30 секунд**.

### memory-eval-vector (completed, 4.6s, 3 tool calls)
queries: ['В gateway.md написано, что таймаут интеграции 10 секунд. Это актуально?', 'gateway.md integration timeout 10 seconds актуально', 'таймаут интеграции 10 секунд gateway.md']

Да, актуально: в `docs/gateway.md` указано, что интеграционный таймаут для всех Relay route — **10 секунд**, и документ обновлён **2026-03-18**. Источник: `docs/gateway.md` / раздел `Timeouts` / дата `2026-03-18`.

Дополнительно есть более раннее подтверждение в `adr/ADR-002.md` от **2026-03-04** со статусом `Accepted`, где сказано то же самое. Источник: `adr/ADR-002.md` / раздел `Timeouts` / дата `2026-03-04`.

Старее ли `gateway.md` по сравнению с решением? Нет, наоборот: `gateway.md` новее, но не противоречит ADR.

## m05 [en / contradiction] The team roster page says Anna owns retries. Is that right today?
**expected:** no; roster updated 2026-07-08, retries moved from Anna to Ivan on 2026-09-07  
**expected sources:** {'sources': ['confluence/team-roster.xhtml', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 4.2s, 2 tool calls)
queries: ["MATCH (p:Person {key:'person:anna-sokolova'})-[o:OWNS]->(t:Topic {key:'topic:ret", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) RETURN p.name, o.from"]

No — Anna no longer owns retries today.

Current owner:
- Ivan Melnik, from 2026-09-07 onward.

Anna owned retries only from 2026-06-01 to 2026-09-07.

Source: graph OWNS edges on `topic:retries` (no document file; ownership edges only).

### memory-eval-graph (completed, 4.4s, 2 tool calls)
queries: ["MATCH (p:Person {key:'person:anna-sokolova'})-[o:OWNS]->(t:Topic {key:'topic:ret", "MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.to IS NULL RE"]

No. Today Anna does not own retries.

- Anna Sokolova owned `topic:retries` from **2026-06-01** to **2026-09-07**. Source: graph ownership edge for retries, date range from the `OWNS` relation.
- The current owner is **Ivan Melnik**, whose ownership of `topic:retries` has **no end date** (`to = null`). Source: graph ownership edge for retries.

So the roster page is out of date.

### memory-eval-vector (completed, 5.1s, 3 tool calls)
queries: ['The team roster page says Anna owns retries. Is that right today?', 'Who owns retries today?', 'retries ownership current decision Anna']

No — the current owner of retries is Ivan Melnik, not Anna.

What I found:
- `meetings/2026-06-01-weekly-sync.txt` (2026-06-01): Anna Sokolova was assigned retries starting that day. This is an active decision at the time.  
- `meetings/2026-09-07-security-review.txt` (2026-09-07): retry ownership was transferred from Anna to Vanya/Ivan; the claim shows owner as Ivan Melnik and is active.
- `memory/decisions.jsonl` (2026-09-07): “Ivan Melnik owns retries from 2026-09-07 (current).”

So the roster page is stale if it still says Anna.

## m06 [ru / contradiction] Decision log в Confluence актуален?
**expected:** нет; последняя версия 2026-06-03, в нём нет решений после 1 июня: ретраи на gateway (06-15), два PoC (06-15), передача PoC Ване (07-13), выбор Lambda (08-03), таймаут 25 с и ретраи через SQS (08-24), SSM (09-07), бюджет (09-21), даты катовера (10-05)  
**expected sources:** {'sources': ['confluence/decision-log.xhtml', 'memory/decisions.jsonl']}

### memory-eval-both (completed, 3.8s, 1 tool calls)
queries: ["MATCH (doc:Document) WHERE doc.file CONTAINS 'decision-log' OR doc.title CONTAIN"]

Нет, не актуален.

`confluence/decision-log.xhtml` обновлён **2026-06-03**, но в памяти есть более поздние решения, которые меняют его содержимое, например:
- **A36** — 2026-06-15: запуск PoC-2 на EKS и PoC-3 на Lambda;
- **A48** — 2026-08-03: “Relay moves to Lambda with provisioned concurrency on deliver”;
- **A57** — 2026-10-05: график переключения БД и compute.

Значит, документ **устарел**.

### memory-eval-graph (completed, 5.5s, 2 tool calls)
queries: ["MATCH (doc:Document)\nWHERE doc.file CONTAINS 'decision-log' OR toLower(doc.title", "MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document {file:'confluence/decision-l"]

Да, **decision log в Confluence актуален**: `confluence/decision-log.xhtml` обновлён **2026-06-03**, и в памяти **нет** решений, которые помечают этот документ как устаревший.  
Источник: `confluence/decision-log.xhtml`, дата обновления `2026-06-03`; проверка stale-решений по документу не вернула записей.

### memory-eval-vector (completed, 4.5s, 3 tool calls)
queries: ['Decision log в Confluence актуален?', 'Decision log Confluence up to date?', 'актуален ли Decision log в Confluence']

Да, по памяти Confluence decision log актуален: страница `confluence/decision-log.xhtml` обновлена **2026-06-03** и помечена как источник решений из weekly sync; если она расходится с записью встречи, приоритет у записи встречи. Источник: `confluence/decision-log.xhtml` / `Decision log` / **2026-06-03**.

Что я нашёл:
- `confluence/decision-log.xhtml` — updated **2026-06-03**, содержит список решений и open items.
- `docs/onboarding.md` — updated **2026-03-10**, говорит, что решения фиксируются в Confluence decision log и для архитектуры ещё в ADR.

Если хотите, могу ещё проверить, есть ли более новое решение, которое делает сам decision log устаревшим по какому-то конкретному пункту.

## m07 [en / contradiction] ADR-010 says the gateway timeout for Lambda should be 20 s. Is that the policy?
**expected:** no; ADR-010 is Proposed and was never accepted; the live decision of 2026-08-24 is 25 s  
**expected sources:** {'sources': ['adr/ADR-010.md', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 7.8s, 5 tool calls)
queries: ['ADR-010 Context gateway timeout Lambda 20 s policy', 'ADR-010 timeout Lambda gateway 20 seconds policy', "MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.date, a.file; MAT", "MATCH (a:ADR {id:'ADR-010'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:'ADR-010'}) RETURN n.id, n.title"]

No — ADR-010 is **Proposed**, not the policy in force.

What I found:
- **ADR-010**: “Gateway timeout policy for Lambda integrations”
  - status: **Proposed**
  - date: **2026-09-23**
  - file: **adr/ADR-010.md**
- The ADR text says:
  - “**Proposed, not accepted. The live value was set by the team on 2026-08-24 at 25 s; this document still says 20 s.**”
  - It also says: “**D20 (25 s) is the live decision and the ADR still proposes 20 s**”

So the **20 s** value is only what ADR-010 proposes; it is **not** the policy currently in force.

Source:
- **adr/ADR-010.md**, **2026-09-23**
- Decision/ADR status from graph: **ADR-010 = Proposed**

### memory-eval-graph (completed, 7.0s, 4 tool calls)
queries: ["MATCH (a:ADR {id:'adr-010'}) RETURN a.id, a.title, a.status, a.date, a.file; MAT", "MATCH (a:ADR {id:'adr-010'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (a:ADR) WHERE a.id = 'ADR-010' OR a.id = 'adr-010' RETURN a.id, a.title, a", "MATCH (n:ADR)-[:SUPERSEDES]->(a:ADR) WHERE a.id = 'ADR-010' OR a.id = 'adr-010' "]

ADR-010 is **Proposed**, not an adopted policy. The live state on this topic is that there is **no superseding ADR shown for ADR-010** in memory, so I can only confirm the ADR itself, not a policy change.

- **ADR-010**: “Gateway timeout policy for Lambda integrations” — **Proposed**, dated **2026-09-23**, file **adr/ADR-010.md**.
- No newer ADR was found that supersedes it.

So, based on memory: **no, ADR-010 itself is not the policy**. It is a proposed ADR as of **2026-09-23** in **adr/ADR-010.md**.

### memory-eval-vector (completed, 6.5s, 3 tool calls)
queries: ['ADR-010 says the gateway timeout for Lambda should be 20 s. Is that the policy?', 'gateway timeout Lambda 20 s policy ADR-010', 'Lambda gateway timeout 20 seconds decision policy']

Not as current policy. ADR-010 is **Proposed** and explicitly says **“No decision recorded”** in the Decision section, so the document is stale for policy status. Source: `adr/ADR-010.md` (updated **2026-09-23**).

What I found:
- ADR-010 Context: it proposes a policy for Lambda integrations and notes the gateway hard limit is 29 s. Source: `adr/ADR-010.md` (**2026-09-23**)
- ADR-010 Options considered: “20 s on every route, with per-route overrides.” Source: `adr/ADR-010.md` (**2026-09-23**)
- ADR-010 Consequences: “Proposed, not accepted. The live value was set by the team on 2026-08-24 at 25 s; this document still says 20 s.” Source: `adr/ADR-010.md` (**2026-09-23**)

So, based on memory, **20 s is not the current policy**; the remembered live decision is **25 s** from **2026-08-24**, and ADR-010 still only proposes 20 s. Source: `adr/ADR-010.md` (**2026-09-23**).

## m08 [ru / contradiction] В runbook катовера написано, что владелец отката TBD. Кто на самом деле?
**expected:** Лена, решение 2026-10-05; runbook от 2026-09-29 устарел  
**expected sources:** {'sources': ['docs/runbook-cutover-serverless.md', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 4.5s, 2 tool calls)
queries: ['runbook катовера откат владелец TBD кто actually owner rollback runbook cutover', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202"]

Это Lena Kim.

Источник: решение от 2026-10-05 в `meetings/2026-10-05-cutover-planning.txt`:
“Rollback for both cutovers is assigned to Lena, and Vanya will update the runbook.”

В runbook это было TBD, но в силе уже другое решение.

### memory-eval-graph (completed, 4.8s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'})\nWHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'})\nWHERE d.text CONTAIN"]

На самом деле владелец отката — Лена. Это зафиксировано в решении от 2026-10-05: “Rollback for both cutovers is assigned to Lena, and Vanya will update the runbook.” Источник: `meetings/2026-10-05-cutover-planning.txt`.

Дополнительно, более ранняя запись от 2026-09-21 тоже указывает на Лену как владельца rollback runbook, но актуальная формулировка — из решения от 2026-10-05.

### memory-eval-vector (completed, 2.6s, 1 tool calls)
queries: ['В runbook катовера написано, что владелец отката TBD. Кто на самом деле?']

На самом деле владелец отката — **Lena Kim**.  
Источник: `meetings/2026-09-21-weekly-sync.txt`, **2026-09-21** — в решении указано: “The rollback runbook will be owned by Lena… Owner: Lena Kim.”

Примечание: запись в runbook от **2026-09-24** говорит лишь, что владелец “named in the cutover decision”, то есть она опирается на это решение и не противоречит ему.

## m09 [ru / crosslingual] Что на митингах называли «провижнд конкаренси» и почему без этого не проходит SLO?
**expected:** provisioned concurrency: прогретые инстансы Lambda на /deliver; без них p95 3.4 с при SLO 2 с, с ними 1.9 с (PoC-3)  
**expected sources:** {'sources': ['docs/poc-lambda-report.md', 'meetings/2026-07-27-poc-review.txt', 'adr/ADR-006.md']}

### memory-eval-both (completed, 6.8s, 3 tool calls)
queries: ['"провижнд конкаренси" SLO meeting why without it SLO does not pass', 'provisioned concurrency SLO why without it SLO does not pass', "MATCH (m:Meeting {date:'2026-07-27'})<-[:DECIDED_IN]-(d:Decision) RETURN d.id, d"]

На митингах под «провижнд конкаренси» имели в виду **provisioned concurrency на `deliver`** для Lambda.

Почему без этого не проходит SLO:
- в обсуждении это прямо сказали: **«провижнд конкаренси на deliver обязательно без него не проходим»** — `meetings/2026-07-27-poc-review.txt`, 2026-07-27;
- в оценке PoC написано: **«Within the 2 s SLO only with provisioned concurrency; without it the SLO is missed.»** — `docs/poc-lambda-report.md`, 2026-07-24;
- и это же закреплено решением: **«Provisioned concurrency on deliver is mandatory for Lambda to be viable.»** — `meetings/2026-07-27-poc-review.txt`, 2026-07-27.

Контекст SLO:
- SLO по задержке — **2 s** для первой попытки доставки, а не для ответа клиента — `docs/slo.md`, 2026-01-28;
- на встрече это уточнили: **«SLO две секунды это про первую попытку доставки а не про ответ клиента»** — `meetings/2026-07-27-poc-review.txt`, 2026-07-27.

Итого: без provisioned concurrency Lambda не укладывалась в 2-секундный SLO на первую попытку доставки.

### memory-eval-graph (completed, 8.1s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE d.text CONTAINS 'p", "MATCH (m:Meeting)<-[:DECIDED_IN]-(d:Decision) WHERE d.text CONTAINS 'provisioned"]

На митингах под «провижнд конкаренси» имели в виду **provisioned concurrency на deliver** для Lambda. Это прямо сказано в решениях:

- **2026-07-13**, `meetings/2026-07-13-weekly-sync.txt`: «Ivan will rewrite the handlers to use provisioned concurrency and SQS between intake and delivery.»
- **2026-07-27**, `meetings/2026-07-27-poc-review.txt`: «Provisioned concurrency on deliver is mandatory for Lambda to be viable.»
- **2026-08-03**, `meetings/2026-08-03-architecture-committee.txt`: «Relay moves to Lambda with provisioned concurrency on deliver.»

Почему без этого не проходит SLO:
- SLO зафиксирован как **p95 end-to-end latency 2 s over a 5-minute window** и **monthly delivery success rate 99.5%** — `meetings/2026-01-26-weekly-sync.txt`, 2026-01-26.
- На обсуждении PoC зафиксировано, что **p95 с provisioned concurrency — 1.9 seconds**; это единственная найденная в графе явная связка между concurrency и достижением целевого latency — `meetings/2026-07-27-poc-review.txt`, 2026-07-27.
- Поэтому в мемори это оформлено как необходимость: **без provisioned concurrency Lambda считается нежизнеспособной для целевого SLO** — `meetings/2026-07-27-poc-review.txt`, 2026-07-27.

Если хотите, 

### memory-eval-vector (completed, 10.7s, 3 tool calls)
queries: ['Что на митингах называли «провижнд конкаренси» и почему без этого не проходит SL', 'провижнд конкаренси SLO митинг Relay', 'provisioned concurrency SLO meeting Relay']

На митингах под «провижнд конкаренси» имели в виду **Lambda provisioned concurrency на `/deliver`** — то есть заранее прогретые инстансы для хендлера доставки. Это прямо сказано на ревью PoC и на архитектурном комитете: «провижнд конкаренси на deliver» и «лямбда с провижнд конкаренси на deliver».  
Источник: `meetings/2026-07-27-poc-review.txt` (2026-07-27), `meetings/2026-08-03-architecture-committee.txt` (2026-08-03).

Почему без этого не проходит SLO:
- В PoC зафиксировали, что **в пределах 2 s SLO проходит только с provisioned concurrency; без него SLO miss**.  
  Источник: `docs/poc-lambda-report.md` (updated 2026-07-24).
- В ADR это потом закрепили как решение: **“Provisioned concurrency on /deliver is a condition, not an optimisation: without it the SLO is missed.”**  
  Источник: `adr/ADR-006.md` (updated 2026-08-05).
- На митинге уточнили сам SLO: **2 секунды — это до первой попытки доставки**, а не до ответа клиента; при p95 1.9 s это считается проходом, но без warm instances было “на грани SLO”.  
  Источники: `docs/slo.md` (updated 2026-01-28), `meetings/2026-07-27-poc-review.txt` (2026-07-27).

Коротко: **это заранее прогретые Lambda-инстансы для `/deliver`; без них пе

## m10 [en / crosslingual] What did the team mean by 'дрифт' and what rule came out of it?
**expected:** drift detection: stacks diverging from reality after manual console changes; after the 2026-02-23 incident manual prod changes were frozen and nightly DetectStackDrift runs with alerts  
**expected sources:** {'sources': ['meetings/2026-02-23-incident-review.txt', 'docs/drift-detection.md']}

### memory-eval-both (completed, 5.3s, 3 tool calls)
queries: ['дрифт meaning rule came out of it Relay webhook delivery', 'drift what it meant rule came out of it Relay webhook delivery', 'дрифт relay change freeze template wins intended not intended in sync']

They meant **infrastructure drift**: a Relay stack can “drift” when someone changes AWS resources by hand and the live stack no longer matches the template.

The rule that came out of it was:

1. **No manual changes in the AWS console for production resources that belong to a Relay stack.**
2. **Every Relay stack runs `DetectStackDrift` nightly at 01:00.**
3. **A stack in `DRIFTED` state blocks the pipeline until it is reconciled.**

Source:
- `docs/drift-detection.md` — updated `2026-02-25`
- The incident review that led to it: `meetings/2026-02-23-incident-review.txt` — `2026-02-23`

Assumption: by “дрифт” you meant the infra/config drift discussed in the incident and drift-detection docs.

### memory-eval-graph (completed, 7.5s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.text CONTAINS 'д", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE toLower(d.text) CO", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE toLower(d.text) CO"]

By “дрифт” the team meant **drift detection** for infrastructure, not a separate term. The rule that came out of it was:

- **Enable drift detection immediately on the new stack** — `2026-02-02`, source `meetings/2026-02-02-weekly-sync.txt`.
- That was later tightened to **nightly drift detection on all stacks with alerts** — `2026-02-23`, source `meetings/2026-02-23-incident-review.txt`.

So the main rule in force became: **drift detection runs nightly on all stacks with alerts**. `2026-02-23`, source `meetings/2026-02-23-incident-review.txt`.

### memory-eval-vector (completed, 4.5s, 3 tool calls)
queries: ["What did the team mean by 'дрифт' and what rule came out of it?", 'дрифт rule came out of it', 'What did the team mean by drift and what rule came out of it?']

By **“дрифт”** the team meant **configuration drift**: the stack in AWS had diverged from the deployed template because someone made a **manual console change**. This is described in the incident review, where they say they “don’t see drift until we hit it” and tie it to the manual change in the console.  
**Source:** `meetings/2026-02-23-incident-review.txt` — **2026-02-23**

The rule that came out of it was:

1. **No manual changes in the AWS console for production Relay resources.**
2. **Nightly drift detection must run on all stacks, with alerts.**
3. **A `DRIFTED` stack blocks the pipeline until reconciled.**

**Source:** `docs/drift-detection.md` — **2026-02-25**

There is also the incident-review decision that specifically says: **manual changes in prod are forbidden; nightly drift detection on all stacks with alerts**.  
**Source:** `meetings/2026-02-23-incident-review.txt` — **2026-02-23**

If you want, I can also quote the exact Russian lines from the meeting.

## m11 [en / multi_hop] Why were gateway retries on /deliver turned off in August, when they had been turned on in June?
**expected:** June: retries enabled (max 3, budget 15%) once idempotency keys were mandatory; August: Lambda intake is asynchronous and a gateway retry enqueues twice, so retries moved to SQS with a DLQ (ADR-009) and gateway retries were turned off  
**expected sources:** {'sources': ['meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt', 'adr/ADR-009.md']}

### memory-eval-both (completed, 8.6s, 5 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'}) WHERE d.date <= '202", 'gateway retries /deliver turned off August turned on June why', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.date <= '202", 'retries /deliver August turned off because duplicated deliveries gateway policy ', 'ретраи /deliver август выключили почему gateway policy дублировались доставки']

Assumption: by “in August” you mean the August 24 decision to turn `/deliver` retries off.

They were turned off because the team changed the retry mechanism from the gateway to SQS/DLQ, so a gateway retry would enqueue the delivery twice.

Sources:
- `meetings/2026-08-24-weekly-sync.txt` — 2026-08-24: “ретраи на лямбде гейтвей ретраить не должен прием кладет сообщение в sqs доставка из очереди пять попыток потом дед леттер и алерт ретраи на гейтвее на deliver выключаем”
- `adr/ADR-009.md` — 2026-08-26: “Retries in SQS with a dead-letter queue after 5 attempts; gateway retries off on /deliver (chosen)”
- `docs/retries-dlq.md` — 2026-08-27: “Gateway retries on `POST /relay/deliver` are off; a gateway retry would enqueue twice.”

For contrast, the earlier June plan had gateway retries on `/deliver`:
- `meetings/2026-06-15-weekly-sync.txt` — 2026-06-15: “Retries on deliver should be enabled at the gateway with a maximum of 3 attempts and a 15% retry budget.”

So the August change was driven by the move to queue-based retries, not by re-enabling the June gateway policy.

### memory-eval-graph (completed, 6.1s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'}) WHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) RETURN d.text, d.dat", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway'}) RETURN d.text, d.dat"]

Gateway retries on `/deliver` were turned off in August because the retry strategy moved from the gateway to SQS with a dead letter queue after 5 attempts.

What I found:
- On 2026-06-15, the plan was to enable gateway retries on deliver with a maximum of 3 attempts and a 15% retry budget. Source: `meetings/2026-06-15-weekly-sync.txt`
- On 2026-08-24, that was changed to: “Retries move to SQS with a dead letter queue after 5 attempts, and gateway retries on deliver are turned off.” Source: `meetings/2026-08-24-weekly-sync.txt`

So the August reason recorded in memory is the move to SQS/DLQ handling instead of gateway retries.

### memory-eval-vector (completed, 5.4s, 3 tool calls)
queries: ['Why were gateway retries on /deliver turned off in August, when they had been tu', 'gateway retries /deliver turned off August turned on June reason', 'retries on /deliver turned off in August after turned on in June why']

Gateway retries on `/deliver` were turned off because a retried delivery could reach the customer twice, and `/deliver` was not idempotent yet.

What I found:
- `docs/idempotency.md` — updated 2026-05-20: “Gateway retries on `/deliver` were disabled on 2026-03-30 because a retried delivery could reach a customer twice.”
- `docs/gateway.md` — updated 2026-03-18: “Retries on `POST /deliver` are disabled … a delivery is not idempotent yet, and a retried request can reach the customer twice.”
- `adr/ADR-002.md` — updated 2026-03-04: “Retries are disabled on POST /deliver until idempotency keys exist, because a retried delivery can reach a customer twice.”

I did not find a separate August-specific reason for turning them off; the memory I retrieved says they were already disabled on 2026-03-30 for the idempotency/duplicate-delivery reason. Also, `docs/retries-dlq.md` — updated 2026-08-27 says retries are no longer a gateway policy, but that appears to be a later change, not the reason for the June/August disablement.

## m12 [ru / multi_hop] Какая цепочка событий привела к тому, что сеть осталась в Terraform?
**expected:** январь: решение переехать целиком на CloudFormation (ADR-001, Тимур против); апрель: Серёжа принёс цифры (кастомные ресурсы для пиринга и DNS, 4 недели), Паша возражал, приняли гибрид (ADR-004, заменяет ADR-001)  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-04-13-weekly-sync.txt', 'meetings/2026-04-20-weekly-sync.txt', 'adr/ADR-004.md']}

### memory-eval-both (completed, 9.3s, 4 tool calls)
queries: ['сеть осталась в Terraform why stayed in Terraform chain events network Terraform', 'network stayed in Terraform chain of events reason Terraform', 'MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision) WHERE (cur)-[:ABOUT', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.date <= '2026-06"]

Если я правильно понял вопрос как «какая последовательность решений привела к тому, что сеть в итоге осталась в Terraform», то цепочка такая:

1. **2026-03-30** — сначала сеть уже была перенесена в CloudFormation:  
   «The network stack has been moved to CloudFormation and the peering was imported without recreation after the third attempt.»  
   Источник: `meetings/2026-03-30-weekly-sync.txt`

2. **2026-04-13** — затем решили отложить окончательное изменение плана и вернуться к нему после оценки:  
   «The team will revisit the network migration with numbers next week before changing the plan.»  
   Источник: `meetings/2026-04-13-weekly-sync.txt`

3. **2026-04-20** — после этого зафиксировали гибридный вариант:  
   «Hybrid networking stays in Terraform and application stacks move to CloudFormation, with the boundary documented in an ADR.»  
   Источник: `meetings/2026-04-20-weekly-sync.txt`

4. **2026-04-22** — это было закреплено в ADR-004:  
   «Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation.»  
   Источник: `adr/ADR-004.md`

5. **2026-06-01** — текущее состояние подтверждено повторно:  
   «The network remains in Terraform

### memory-eval-graph (completed, 7.2s, 1 tool calls)
queries: ['MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision)\nWHERE cur.text CONT']

Цепочка была такой:

1. **2026-01-12** — решили мигрировать Relay из Terraform в CloudFormation по модулю за раз.  
   Источник: `meetings/2026-01-12-weekly-sync.txt`  
   Дата: `2026-01-12`

2. **2026-01-19** — план уточнили: начать с compute, а сеть оставить на потом.  
   Источник: `meetings/2026-01-19-weekly-sync.txt`  
   Дата: `2026-01-19`

3. **2026-03-30** — сеть уже считали перенесённой в CloudFormation; peering импортировали без пересоздания после третьей попытки.  
   Источник: `meetings/2026-03-30-weekly-sync.txt`  
   Дата: `2026-03-30`

4. **2026-04-13** — потом решили ещё раз вернуться к миграции сети и проверить цифры перед изменением плана.  
   Источник: `meetings/2026-04-13-weekly-sync.txt`  
   Дата: `2026-04-13`

5. **2026-04-20** — итоговый активный статус: **гибридная сеть осталась в Terraform**, а в CloudFormation ушли application stacks; границу зафиксируют в ADR.  
   Источник: `meetings/2026-04-20-weekly-sync.txt`  
   Дата: `2026-04-20`

Если хотите, я могу ещё показать **полную цепочку supersedes** по этим решениям в одном списке.

### memory-eval-vector (completed, 7.8s, 3 tool calls)
queries: ['Какая цепочка событий привела к тому, что сеть осталась в Terraform?', 'What chain of events led to the network staying in Terraform?', 'цепочка событий сеть осталась в Terraform']

Цепочка событий в памяти такая:

1. **Сначала** было решение ADR-001: хотели **перенести инфраструктуру из Terraform в CloudFormation**.  
   Источник: `adr/ADR-001.md`, 2026-01-14.  
   В контексте сказано, что в Terraform были модули, к которым давно не прикасались, а остальной AWS-аккаунт уже жил в CloudFormation.  
   Источник: `adr/ADR-001.md`, 2026-01-14.

2. **Потом** выяснилось, что **сетевой модуль был последним и самым сложным для переноса**: для cross-account peering и DNS delegation в CloudFormation нужны custom resources, а сама сеть уже была нативно описана в Terraform, который поддерживает network team для всей компании.  
   Источник: `adr/ADR-004.md`, 2026-04-22.

3. **В итоге** приняли новое решение ADR-004: **гибридный подход** — **сеть остается в Terraform**, а application stacks идут в CloudFormation. Это решение **supersedes ADR-001**, то есть заменяет прежний план полного переноса.  
   Источник: `adr/ADR-004.md`, 2026-04-22.

4. Позже это еще раз зафиксировали в рабочем решении: **“The network remains in Terraform”**.  
   Источник: `meetings/2026-06-01-weekly-sync.txt`, 2026-06-01.

Если коротко: **план полного переноса в CloudFormation наткнулся на сложнос

## m13 [en / multi_hop] Which decision closed the longest-standing open item, who took it, and how many times had it been raised before?
**expected:** D19 on 2026-08-10: Sergey took the DynamoDB dry run (due 2026-09-04); raised 2026-05-04 and again on 05-18, 06-15, 06-29, 07-20 (four times)  
**expected sources:** {'sources': ['meetings/2026-05-04-poc-review.txt', 'meetings/2026-08-10-weekly-sync.txt']}

### memory-eval-both (completed, 4.3s, 1 tool calls)
queries: ["MATCH (o:OpenItem {status:'closed'}) OPTIONAL MATCH (c:Decision)-[:CLOSES]->(o) "]

The longest-standing closed open item was **Q31: “Write a rollback runbook for the serverless cutover.”**

- **Decision that closed it:** “The rollback runbook will be owned by Lena and written by the end of the week.”
- **Date:** 2026-09-21
- **Source:** `meetings/2026-09-21-weekly-sync.txt`
- **Who took it:** **Lena Kim**
- **Raised before:** **1 time** total, i.e. **0 times raised_again** (`raised_again: []`)

Assumption: I treated “how many times had it been raised before?” as the number of times after the initial raise, which is 0 here; total raises recorded = 1.

### memory-eval-graph (completed, 5.2s, 1 tool calls)
queries: ["MATCH (o:OpenItem {status:'closed'}) OPTIONAL MATCH (c:Decision)-[:CLOSES]->(o) "]

The longest-standing open item was closed by the decision **“The rollback runbook will be owned by Lena and written by the end of the week.”** It was decided on **2026-09-21** in **meetings/2026-09-21-weekly-sync.txt**.

- **Who took it:** **Lena Kim**  
  Source: **meetings/2026-09-21-weekly-sync.txt**, **2026-09-21**
- **How many times it had been raised before:** **1 time** total, with **0 raised_again** entries  
  Raised on **2026-08-24**; no additional raisings listed.  
  Source: **open item Q31**, **2026-08-24**; **meetings/2026-09-21-weekly-sync.txt**, **2026-09-21**

Assumption: by “how many times had it been raised before” I counted the original raise plus any `raised_again` entries, per the memory rules.

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['Which decision closed the longest-standing open item, who took it, and how many ', 'longest-standing open item decision closed who took it how many times raised bef', 'decision closed open item raised before times who took it oldest open item']

The longest-standing open item I found that was later closed is the **database dry run** item.

- **Decision / closure:** it was closed when **Marat Yusupov** took ownership on **2026-07-20**.
- **Who took it:** **Marat Yusupov**
- **How many times it had been raised before closure:** **3 times total** — first on **2026-06-15**, then again on **2026-06-29** and **2026-07-20**. So it had been **raised twice before** the final taking/closure event.

**Source:** `meetings/2026-06-15-weekly-sync.txt` (2026-06-15), claim Q21.

## m14 [ru / multi_hop] Кто возражал против переезда на CloudFormation в январе и какую позицию он занял в апреле, когда обсуждали гибрид?
**expected:** Тимур возражал в январе (ADR-001); в апреле поддержал гибрид Серёжи («тулинг надо выбирать по задаче»); возражал в апреле уже Паша  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 6.2s, 3 tool calls)
queries: ['CloudFormation January objected hybrid April migration decision meeting', 'CloudFormation январь возражал гибрид апрель переезд', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (a:Person"]

Против переезда на CloudFormation в январе возражал **Тимур Алиев**.

В апреле, когда обсуждали гибрид, его позиция в памяти зафиксирована как **возражение против гибридного варианта тоже** — в исходной январской записи Тимур сказал: «я против но не блокирую запишите мое возражение», а в апреле гибрид был оформлен как выбранный вариант, при этом возражение в ADR-004 записано уже от Павла Гришина.

Источники:
- `meetings/2026-01-12-weekly-sync.txt` — 2026-01-12
- `adr/ADR-001.md` — 2026-01-14
- `adr/ADR-004.md` — 2026-04-22
- `meetings/2026-04-20-weekly-sync.txt` — 2026-04-20

Если хотите, я могу ещё коротко свести это в одну строку: кто возражал в январе и кто возражал в апреле.

### memory-eval-graph (completed, 11.6s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.date >= '2026-01", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.date >= '2026-04", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.date >= '2026-01", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE d.date >= '2026-01"]

В январе против переезда на CloudFormation возражал Тимур Алиев; его возражение относится к решению от 2026-01-12 в файле `meetings/2026-01-12-weekly-sync.txt`.

В апреле, когда обсуждали гибрид, против решения также возражал Павел Гришин; речь о решении от 2026-04-20 в файле `meetings/2026-04-20-weekly-sync.txt`, где зафиксировано: “Hybrid networking stays in Terraform and application stacks move to CloudFormation, with the boundary documented in an ADR.”

Если брать именно “какую позицию он занял”, то в апреле у него была позиция против этого гибридного разделения ответственности.

### memory-eval-vector (completed, 6.1s, 3 tool calls)
queries: ['Кто возражал против переезда на CloudFormation в январе и какую позицию он занял', 'возражал против переезда на CloudFormation в январе гибрид апреле позиция', 'CloudFormation January opposed hybrid April stance']

В январе против переезда на CloudFormation возражал **Тимур Алиев** — это записано в **meetings/2026-01-12-weekly-sync.txt** от **2026-01-12** и в **ADR-001** от **2026-01-14**.

В апреле, когда обсуждали гибрид, он занял позицию **против полного завершения миграции**: в **ADR-004** от **2026-04-22** зафиксировано решение про гибрид — **Terraform для networking, CloudFormation для application stacks**, и там записано возражение от **Pavel Grishin**.  
То есть по найденным записям в апреле возражал уже **Павел Гришин**, а не Тимур.

Источники:
- **meetings/2026-01-12-weekly-sync.txt**, **2026-01-12** — Тимур: «я против но не блокирую»
- **ADR-001**, **2026-01-14** — objection from Timur Aliev
- **ADR-004**, **2026-04-22** — hybrid IaC accepted; objection recorded from Pavel Grishin

Если хотите, я могу ещё коротко сопоставить, как именно формулировались их аргументы в январе и апреле.

## m15 [en / point_in_time] On 2026-07-01, who owned retries, who owned the serverless PoC, and was the dry run owned?
**expected:** retries: Anna (since 06-01); serverless PoC: Sergey (until 07-13); dry run: no owner  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-06-29-weekly-sync.txt']}

### memory-eval-both (completed, 6.8s, 3 tool calls)
queries: ['MATCH (p:Person)-[o:OWNS]->(x) WHERE o.from <= $D AND (o.to IS NULL OR o.to > $D', 'dry run ownership 2026-07-01 Relay database migration open item owned', 'serverless PoC owner 2026-07-01 Relay']

On 2026-07-01:

- **Retries** was owned by **Anna Sokolova**. Source: `confluence/team-roster.xhtml` (updated `2026-07-08`), which says “retries since 2026-06-01”; the ownership was in force on `2026-07-01`.
- **Serverless PoC** was owned by **Sergey Belov** on that date. Source: `confluence/team-roster.xhtml` (updated `2026-07-08`) says “The serverless PoC is being handed from Sergey to Ivan,” and the graph shows Sergey owning the PoC from `2026-06-15` through `2026-07-06`.
- **The dry run** was **not owned** on `2026-07-01`. Source: `meetings/2026-05-04-poc-review.txt` and the related open-item claim say “No owner,” and there was no ownership yet by `2026-07-01`.

Assumption: “the dry run” refers to the database migration dry run open item.

### memory-eval-graph (completed, 5.7s, 3 tool calls)
queries: ['MATCH (p:Person)-[o:OWNS]->(x {key:$retries}) WHERE o.from <= $d AND (o.to IS NU', 'MATCH (p:Person)-[o:OWNS]->(x {key:$poc}) WHERE o.from <= $d AND (o.to IS NULL O', 'MATCH (p:Person)-[o:OWNS]->(x {key:$dry}) WHERE o.from <= $d AND (o.to IS NULL O']

На 2026-07-01:

- retries owned by Anna Sokolova, from 2026-06-01 to 2026-09-07, source: memory graph via OWNS edge dated 2026-06-01.
- the serverless PoC was owned by Sergey Belov, from 2026-06-15 to 2026-07-06, source: memory graph via OWNS edge dated 2026-06-15.
- the dry run was owned by Sergey Belov, from 2026-05-04 onward, so yes, it was owned on that date, source: memory graph via OWNS edge dated 2026-05-04.

Assumption: “the dry run” means the DynamoDB migration dry run on topic:database.

### memory-eval-vector (completed, 9.8s, 3 tool calls)
queries: ['On 2026-07-01, who owned retries, who owned the serverless PoC, and was the dry ', 'retries serverless PoC dry run ownership 2026-07-01', '2026-07-01 retries serverless PoC dry run owner']

On **2026-07-01**:

- **Retries:** not in memory for that exact date. The newest relevant ownership I found says **Anna Sokolova** owns retries **since 2026-06-01** in **`confluence/team-roster.xhtml`** (updated **2026-07-08**). A separate doc says retries were owned by the Relay core lead until serverless cutover in **`docs/retries-dlq.md`** (updated **2026-08-27**). These are not in conflict for 2026-07-01, but the roster gives the explicit owner.  
- **Serverless PoC:** **not in memory** for 2026-07-01 as a finalized owner. The roster says **Ivan Melnik** owns it **since 2026-07-06** and also notes it was being handed from Sergey to Ivan in **`confluence/team-roster.xhtml`** (updated **2026-07-08**). So on 2026-07-01, the handoff was still pending.  
- **Dry run:** **no owner**. The relevant decision says the dry run topic remained open without an owner in **`meetings/2026-05-18-weekly-sync.txt`** (dated **2026-05-18**). Earlier, the meeting on **2026-05-04** also recorded it as open without an owner in **`meetings/2026-05-04-poc-review.txt`**.

Retrieved items:
- `confluence/team-roster.xhtml` — **2026-07-08**
- `docs/retries-dlq.md` — **2026-08-27**
- `meetings/2026-05-18-week

## m16 [ru / point_in_time] Какой таймаут на gateway действовал 1 июля 2026 и кто был его владельцем?
**expected:** 30 с (решение 2026-05-18, заменило 10 с), владелец Паша  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt']}

### memory-eval-both (completed, 4.4s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20", "MATCH (p:Person)-[o:OWNS]->(x {key:'topic:timeouts'}) WHERE o.from <= '2026-07-0"]

На 2026-07-01 на gateway действовал таймаут **30 s**: в силе была decision от **2026-05-18** — *“The integration timeout is increased from 10 s to 30 s while synchronous mode remains enabled.”*  
Источник: `meetings/2026-05-18-weekly-sync.txt`, дата `2026-05-18`.

Владельцем тогда был **Павел Гришин**.  
Источник: `OWNS` на `topic:timeouts`, `from=2026-05-18`, `to=2026-08-24`.

### memory-eval-graph (completed, 5.0s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20", "MATCH (p:Person)-[o:OWNS]->(d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}"]

На 2026-07-01 на gateway действовал таймаут **30 s**; в решении сказано, что **integration timeout increased from 10 s to 30 s while synchronous mode remains enabled**.  
Источник: `meetings/2026-05-18-weekly-sync.txt`, дата решения `2026-05-18`.

Владелец на эту дату — **Pavel Grishin**.  
Источник: `meetings/2026-05-18-weekly-sync.txt`, дата решения `2026-05-18`.

Если хотите, могу ещё показать цепочку изменений таймаута до этой даты.

### memory-eval-vector (completed, 4.7s, 3 tool calls)
queries: ['Какой таймаут на gateway действовал 1 июля 2026 и кто был его владельцем?', 'таймаут gateway 1 июля 2026 владелец', 'gateway timeout owner July 1 2026']

На 1 июля 2026 в памяти есть **две связанные, но не одинаковые** записи, и они **не противоречат напрямую**, потому что одна про общий gateway, а другая — про таймаут:

- **Таймаут gateway:** в памяти есть решение от **2026-05-11**: **gateway keeps a 10 s limit**. Источник: `meetings/2026-05-11-weekly-sync.txt` (claim A25).  
- **Владелец gateway:** в памяти есть ownership от **2026-03-02**: **Pavel Grishin owns gateway** (current). Источник: `memory/decisions.jsonl` (ownership:gateway:2026-03-02).

Итого на **1 июля 2026**:
- **таймаут:** **10 s**
- **владелец:** **Pavel Grishin**

Если нужно, я могу также проверить, есть ли более позднее решение, которое изменило таймаут после 2026-05-11.

## m17 [en / aggregate] Which decisions were made at the architecture committee on 2026-08-03 and which open item was raised there?
**expected:** D17 Lambda with provisioned concurrency (ADR-006), D18 keep EKS rejected (ADR-007); open item: provisioned concurrency sizing, taken by Ivan on 08-10  
**expected sources:** {'sources': ['meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 2.9s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:DECIDED_IN]->(m:Meeting {date:'2026-08-03'}) RETURN d.id, d", "MATCH (o:OpenItem)-[:RAISED_IN]->(m:Meeting {date:'2026-08-03'}) OPTIONAL MATCH "]

At the architecture committee on 2026-08-03, the decision made was:

- **A48** — “Relay moves to Lambda with provisioned concurrency on deliver.”  
  Source: `meetings/2026-08-03-architecture-committee.txt`, date `2026-08-03`, status `active`.

The open item raised there was:

- **Q27** — “Provisioned concurrency sizing remains open: how many instances to keep.”  
  Raised: `2026-08-03`  
  Raised again: none  
  Owner: **Ivan Melnik**  
  Source: `meetings/2026-08-03-architecture-committee.txt`

### memory-eval-graph (completed, 4.6s, 1 tool calls)
queries: ['MATCH (m:Meeting {date:$D})<-[:DECIDED_IN]-(d:Decision)\nOPTIONAL MATCH (o:OpenIt']

At the architecture committee on 2026-08-03, one decision was made:

- **A48** — “Relay moves to Lambda with provisioned concurrency on deliver.”  
  **Status:** active  
  **Source:** `meetings/2026-08-03-architecture-committee.txt`  
  **Date:** 2026-08-03

The open item raised there was:

- **Q27** — “Provisioned concurrency sizing remains open: how many instances to keep.”  
  **Status:** closed  
  **Raised:** 2026-08-03  
  **Raised again:** none  
  **Source:** `meetings/2026-08-03-architecture-committee.txt`  
  **Date:** 2026-08-03



### memory-eval-vector (completed, 6.6s, 3 tool calls)
queries: ['Which decisions were made at the architecture committee on 2026-08-03 and which ', 'architecture committee 2026-08-03 decisions open item', 'architecture committee meeting 2026-08-03 decision open item']

На архитектурном комитете 2026-08-03 были зафиксированы такие решения:

1. **Relay переезжает на Lambda с provisioned concurrency на deliver**  
   - **ADR 006 принят**, **ADR 007 отклонён**.  
   - **Владелец: Ваня**.  
   - Возражение Тимура записано.  
   - **Источник:** `meetings/2026-08-03-architecture-committee.txt` (2026-08-03), фрагмент 00:01:11–00:01:55.

2. В обсуждении compute также было зафиксировано, что вариант Lambda был выбран **в голосовании** против EKS с условием нагрузочного теста.  
   - **Источник:** `meetings/2026-08-03-architecture-committee.txt` (2026-08-03), фрагмент 00:00:06–00:00:39 и 00:01:11–00:01:55.

Открытый пункт, поднятый там:
- **Sizing provisioned concurrency** — сколько инстансов держать.  
- На момент записи это был **open item**, и в найденной памяти он же оформлен как пункт с **Иваном Мельником** как владельцем с 2026-08-03.  
- **Источник:** `meetings/2026-08-03-architecture-committee.txt` (2026-08-03), фрагмент 00:01:42–00:01:55; также claim `Q27` в `meetings/2026-08-03-architecture-committee.txt` (2026-08-03).

Если хотите, я могу отдельно перечислить решения именно в формате **“decision / status / owner”**.

## m18 [ru / aggregate] Сколько раз менялась политика ретраев и кто владел ею на каждом шаге?
**expected:** три решения: 03-30 выключены (Никита), 06-15 включены на gateway, 3 попытки, бюджет 15% (Аня), 08-24 перенесены в SQS с DLQ (Аня, с 09-07 Ваня)  
**expected sources:** {'sources': ['meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 5.1s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) OPTIONAL MATCH (p:Pe"]

Политика ретраев менялась 4 раза.

Шаги и владельцы:
1. 2026-03-30 — `meetings/2026-03-30-weekly-sync.txt`  
   Политика: «Deliver retries are disabled until idempotency keys exist, and read-side retries are capped at two attempts.»  
   Владелец: Nikita Frolov

2. 2026-06-01 — `meetings/2026-06-01-weekly-sync.txt`  
   Политика: «Retries are handed over from Nikita to Anna starting today.»  
   Владелец: Anna Sokolova

3. 2026-08-24 — `meetings/2026-08-24-weekly-sync.txt`  
   Политика: «Retries move to SQS with a dead letter queue after 5 attempts, and gateway retries on deliver are turned off.»  
   Владелец: Anna Sokolova

4. 2026-09-07 — `meetings/2026-09-07-security-review.txt`  
   Политика: «Retry ownership for the SQS pipeline is transferred from Anna to Vanya starting today.»  
   Владелец: Ivan Melnik

Если нужно, могу ещё показать, кто был владельцем на любую конкретную дату.

### memory-eval-graph (completed, 8.6s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nOPTIONAL MATCH (p:Pe"]

Политика ретраев менялась 5 раз.

По шагам владелец был такой:

1. 2026-03-30 — Nikita Frolov  
   Источник: `meetings/2026-03-30-weekly-sync.txt`  
   Решение: `A17` — “Deliver retries are disabled until idempotency keys exist, and read-side retries are capped at two attempts.”  
   Статус: `active`

2. 2026-06-01 — Anna Sokolova  
   Источник: `meetings/2026-06-01-weekly-sync.txt`  
   Решение: `A35` — “Retries are handed over from Nikita to Anna starting today.”  
   Статус: `active`

3. 2026-06-15 — Anna Sokolova  
   Источник: `meetings/2026-06-15-weekly-sync.txt`  
   Решение: `A37` — “Retries on deliver should be enabled at the gateway with a maximum of 3 attempts and a 15% retry budget.”  
   Статус: `superseded`

4. 2026-08-24 — Anna Sokolova  
   Источник: `meetings/2026-08-24-weekly-sync.txt`  
   Решение: `A49` — “Retries move to SQS with a dead letter queue after 5 attempts, and gateway retries on deliver are turned off.”  
   Статус: `active`

5. 2026-09-07 — Ivan Melnik  
   Источник: `meetings/2026-09-07-security-review.txt`  
   Решение: `A51` — “Retry ownership for the SQS pipeline is transferred from Anna to Vanya starting today.”  
   Статус: `active`

Если счит

### memory-eval-vector (completed, 6.2s, 3 tool calls)
queries: ['Сколько раз менялась политика ретраев и кто владел ею на каждом шаге?', 'политика ретраев ownership changes decision', 'retry policy ownership history decisions']

Политика ретраев менялась **3 раза**; по найденным записям цепочка такая:

1. **2026-03-30** — ретраи были у **Никиты Фролова**.  
   Source: `meetings/2026-03-30-weekly-sync.txt` / claim `A17`, date `2026-03-30`.

2. **2026-06-01** — ретраи перешли к **Анне Соколовой**.  
   Source: `meetings/2026-06-01-weekly-sync.txt` / claim `A35`, date `2026-06-01`.

3. **2026-09-07** — ретраи перешли к **Ивану Мельнику**.  
   Source: `meetings/2026-09-07-security-review.txt` / claim `ownership:retries:2026-09-07`, date `2026-09-07`.

Важно: в памяти есть и более ранняя запись **2026-03-16** про open item “Gateway retries cannot be enabled yet” без владельца.  
Source: `meetings/2026-03-16-weekly-sync.txt` / claim `Q7`, date `2026-03-16`.  
Но это не назначение владельца, поэтому я не считаю это отдельным шагом владения.

Если хотите, я могу отдельно разложить **не только владение, но и сами изменения политики ретраев по сути** — какие были правила на каждом этапе.

## m19 [en / unowned] What is still unowned as of 2026-10-05 and how many times has each been raised?
**expected:** 10x load test on Lambda (raised 07-27, again 08-17, 09-14); DocumentDB credential rotation (raised 09-07, again 09-28, 10-05); DocumentDB decommission date (raised 05-18, again 08-10, 10-05) has no date rather than no owner  
**expected sources:** {'sources': ['meetings/2026-07-27-poc-review.txt', 'meetings/2026-09-07-security-review.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 63.1s, 1 tool calls)
queries: ["MATCH (o:OpenItem) WHERE o.raised <= '2026-10-05' AND NOT EXISTS { MATCH (o)<-[:"]

As of 2026-10-05, these open items are still unowned, with how many times each has been raised:

- **Q1** — “Review timeout behavior for slow endpoints and queue growth.”  
  Raised **1** time: 2026-01-19  
  Source: graph open-item record; date: 2026-01-19

- **Q2** — “Add cost center tags to all resources starting this quarter.”  
  Raised **1** time: 2026-01-26  
  Source: graph open-item record; date: 2026-01-26

- **Q3** — “Enable drift detection on the new stack.”  
  Raised **1** time: 2026-02-02  
  Source: graph open-item record; date: 2026-02-02

- **Q4** — “The DocumentDB read p99 is 9 ms at peak and keeps growing every month.”  
  Raised **1** time: 2026-02-02  
  Source: graph open-item record; date: 2026-02-02

- **Q5** — “The queue of undelivered messages is not decreasing.”  
  Raised **1** time: 2026-02-02  
  Source: graph open-item record; date: 2026-02-02

- **Q6** — “Set up an alert routing path into on-call because current alerts go to a channel nobody reads.”  
  Raised **1** time: 2026-02-23  
  Source: graph open-item record; date: 2026-02-23

- **Q7** — “Gateway retries cannot be enabled yet.”  
  Raised **1** time: 2026-03-16  
  Source: graph open-item r

### memory-eval-graph (completed, 40.7s, 1 tool calls)
queries: ['MATCH (o:OpenItem)\nWHERE o.raised <= $D\n  AND NOT EXISTS { MATCH (o)<-[w:OWNS]-(']

As of 2026-10-05, these open items are still unowned. I counted each item’s raises as `1 + size(raised_again)`.

- Q1 — “Review timeout behavior for slow endpoints and queue growth.” — raised 1 time — source file not returned in this query; date 2026-01-19
- Q2 — “Add cost center tags to all resources starting this quarter.” — raised 1 time — source file not returned in this query; date 2026-01-26
- Q3 — “Enable drift detection on the new stack.” — raised 1 time — source file not returned in this query; date 2026-02-02
- Q4 — “The DocumentDB read p99 is 9 ms at peak and keeps growing every month.” — raised 1 time — source file not returned in this query; date 2026-02-02
- Q5 — “The queue of undelivered messages is not decreasing.” — raised 1 time — source file not returned in this query; date 2026-02-02
- Q6 — “Set up an alert routing path into on-call because current alerts go to a channel nobody reads.” — raised 1 time — source file not returned in this query; date 2026-02-23
- Q7 — “Gateway retries cannot be enabled yet.” — raised 1 time — source file not returned in this query; date 2026-03-16
- Q9 — “Start the database work in April.” — raised 1 time — source file not returned

### memory-eval-vector (completed, 8.9s, 3 tool calls)
queries: ['What is still unowned as of 2026-10-05 and how many times has each been raised?', 'unowned as of 2026-10-05 raised count open item owner', 'no owner raised date count open items Relay webhook delivery project']

As of 2026-10-05, the items in memory that are still **unowned** are:

- **Cutover** — raised **4 times**  
  Sources:  
  - `meetings/2026-09-14-weekly-sync.txt` (2026-09-14)  
  - `meetings/2026-09-21-weekly-sync.txt` (2026-09-21)  
  - `meetings/2026-09-28-weekly-sync.txt` (2026-09-28)  
  - `meetings/2026-10-05-cutover-planning.txt` (2026-10-05)

- **Database** — raised **3 times**  
  Sources:  
  - `meetings/2026-05-04-poc-review.txt` (2026-05-04)  
  - `meetings/2026-05-18-weekly-sync.txt` (2026-05-18)  
  - `meetings/2026-09-14-weekly-sync.txt` (2026-09-14)

- **Compute** — raised **2 times**  
  Sources:  
  - `meetings/2026-06-29-weekly-sync.txt` (2026-06-29)  
  - `meetings/2026-08-17-weekly-sync.txt` (2026-08-17)

- **Retries** — raised **2 times**  
  Sources:  
  - `meetings/2026-02-02-weekly-sync.txt` (2026-02-02)  
  - `meetings/2026-03-16-weekly-sync.txt` (2026-03-16)

- **Security** — raised **1 time**  
  Source: `meetings/2026-09-28-weekly-sync.txt` (2026-09-28)

- **Ownership** — raised **1 time**  
  Source: `meetings/2026-07-06-weekly-sync.txt` (2026-07-06)

I counted only items marked with **No owner** in the retrieved memory.  
If you want, I can also list 

## m20 [ru / dependency] Что должно произойти до серверлес-катовера 19 октября и в каком порядке?
**expected:** катовер базы на DynamoDB 12 октября (за неделю), dual write до 26 октября; нагрузочный тест на 10x всё ещё не сделан; runbook отката с владельцем Леной  
**expected sources:** {'sources': ['meetings/2026-10-05-cutover-planning.txt', 'docs/runbook-cutover-serverless.md', 'docs/load-testing.md']}

### memory-eval-both (completed, 10.1s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202", 'серверлес-катовер 19 октября что должно произойти до него и в каком порядке runb', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202"]

Считаю, что вы имеете в виду серверлес-катовер 19.10, и беру порядок из runbook для него.

Что должно произойти до катовера и в каком порядке:

1. За 24 часа до него заморозить изменения endpoint’ов.  
   Источник: `docs/runbook-cutover-serverless.md`, обновлён `2026-09-29`.

2. Переключить gateway-интеграции для `POST /relay/deliver` и `GET /relay/*` с VPC link на Lambda integrations.  
   Источник: `docs/runbook-cutover-serverless.md`, обновлён `2026-09-29`.

3. Уменьшить EKS deployments до 0 replicas, но оставить кластер на 7 дней.  
   Источник: `docs/runbook-cutover-serverless.md`, обновлён `2026-09-29`.

4. После переключения наблюдать `delivery p95`, глубину DLQ и `intake 5xx` в течение 30 минут.  
   Источник: `docs/runbook-cutover-serverless.md`, обновлён `2026-09-29`.

Дополнительно из планирования:
- сам серверлес-катовер запланирован на `2026-10-19 09:00`; источник: `meetings/2026-10-05-cutover-planning.txt`, дата `2026-10-05`.
- rollback за оба катовера назначен на Лену, а Ваня должен обновить runbook; источник: `meetings/2026-10-05-cutover-planning.txt`, дата `2026-10-05`.

Если хотите, я могу следующим сообщением свести это в короткий чек-лист “к дате 19 октября”.

### memory-eval-graph (completed, 7.8s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:cutover'}) WHERE d.date <= '202"]

До серверлес-катовера 2026-10-19 должно произойти следующее, по порядку:

1. Нужно, чтобы rollback runbook был подготовлен и закреплён за Леной к концу недели.  
   Источник: `meetings/2026-09-21-weekly-sync.txt`, 2026-09-21.  
   Решение: `A54` — “The rollback runbook will be owned by Lena and written by the end of the week.”

2. Для катовера назначен rollback на Лену, а Ваня должен обновить runbook.  
   Источник: `meetings/2026-10-05-cutover-planning.txt`, 2026-10-05.  
   Решение: `A56` — “Rollback for both cutovers is assigned to Lena, and Vanya will update the runbook.”

3. Сам serverless cutover запланирован на 2026-10-19 at 09:00.  
   Источник: `meetings/2026-10-05-cutover-planning.txt`, 2026-10-05.  
   Решение: `A55` — “The serverless cutover is scheduled for 2026-10-19 at 09:00.”

В памяти не нашлось явных зависимостей `DEPENDS_ON` между этими решениями, поэтому я перечислил их в хронологическом порядке по дате.

### memory-eval-vector (completed, 7.1s, 3 tool calls)
queries: ['Что должно произойти до серверлес-катовера 19 октября и в каком порядке?', 'serverless cutover October 19 what should happen before and in what order', 'серверлес катовера 19 октября порядок до него']

До серверлес-катовера 19 октября должны произойти вот эти шаги, в таком порядке:

1. **Сначала переключить базу** — до **12 октября**, то есть **за неделю до** serverless cutover.  
   Источник: `meetings/2026-10-05-cutover-planning.txt` — 2026-10-05.  
   Встреча: Денис сказал: «**базу переключаем раньше двенадцатого октября за неделю до**».

2. **Потом серверлес-катовер** — **19 октября в 09:00**.  
   Источник: `meetings/2026-10-05-cutover-planning.txt` — 2026-10-05.  
   Также это зафиксировано в claim `A55` из того же источника как активное решение.  
   Источник: `meetings/2026-10-05-cutover-planning.txt` — 2026-10-05.

3. **После этого, 26 октября, выключить dual write**.  
   Источник: `meetings/2026-10-05-cutover-planning.txt` — 2026-10-05.  
   Встреча: «**dual write до двадцать шестого**».

Дополнительно: в runbook есть более общий порядок для serverless cutover:
- заморозить изменения endpoint’ов за 24 часа,
- переключить gateway integrations на Lambda,
- уменьшить EKS до 0 реплик,
- 30 минут наблюдать метрики.  
Источник: `docs/runbook-cutover-serverless.md` — 2026-09-29.

Если хочешь, я могу отдельно свести это в короткий таймлайн по датам.

## m21 [en / temporal] Has the SLO ever changed? What is it right now?
**expected:** yes: p95 2 s from 2026-01-26; relaxed to 3 s for 30 days after the serverless cutover (decided 2026-10-05, Marat objected), then back to 2 s; success rate 99.5% unchanged  
**expected sources:** {'sources': ['meetings/2026-01-26-weekly-sync.txt', 'meetings/2026-10-05-cutover-planning.txt', 'docs/slo.md']}

### memory-eval-both (completed, 4.6s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) OPTIONAL MATCH (d)-[:SUP"]

Yes — the SLO has changed.

What was decided:
- 2026-01-26, `meetings/2026-01-26-weekly-sync.txt`: “The team set the SLOs to p95 end-to-end latency of 2 s over a 5-minute window and a monthly delivery success rate of 99.5%.”
- 2026-10-05, `meetings/2026-10-05-cutover-planning.txt`: “For 30 days after cutover, p95 will be relaxed to 3 seconds, then returned to 2 seconds.”

Current SLO in force:
- 2026-10-05, `meetings/2026-10-05-cutover-planning.txt`: p95 is relaxed to 3 seconds for 30 days after cutover, then returns to 2 seconds.
- The latest active decision also still includes the monthly delivery success rate of 99.5% from 2026-01-26.

Assumption: “SLO” here refers to the SLO topic in the memory, which includes latency and delivery success rate.

### memory-eval-graph (completed, 4.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

Yes — the SLO has changed.

Current SLO in force now:
- p95 end-to-end latency of 2 s over a 5-minute window
- monthly delivery success rate of 99.5%

Source: `meetings/2026-01-26-weekly-sync.txt`, 2026-01-26.  
That was later updated by a cutover plan:
- for 30 days after cutover, p95 is relaxed to 3 seconds, then returned to 2 seconds

Source: `meetings/2026-10-05-cutover-planning.txt`, 2026-10-05.

So the SLO changed on 2026-10-05, but the current baseline after that temporary window is back to 2 seconds / 99.5%.

### memory-eval-vector (completed, 7.3s, 3 tool calls)
queries: ['Has the SLO ever changed? What is it right now?', 'SLO changed current SLO Relay webhook delivery', 'SLO history Relay webhook delivery']

Yes — the SLO has changed.

What I found:
- On **2026-01-26**, the team set the SLOs to **p95 latency of 2 s over a 5-minute window** and **monthly delivery success rate of 99.5%**. Source: `meetings/2026-01-26-weekly-sync.txt` (`decision:slo:2026-01-26`, status **active**).
- The current SLO page, updated **2026-01-28**, states the same objectives:
  - **Delivery latency, p95** from `POST /deliver` accepted to the first delivery attempt sent: **2 s** over **5 minutes**
  - **Delivery success rate**: **99.5%** over the **calendar month**
  - `GET /deliveries/*` latency, p95: **500 ms** over **5 minutes**
  Source: `docs/slo.md` (updated **2026-01-28**).

There is also an older decision on **2026-01-19** about a **60 s delivery timeout**, but that is about timeouts, not the SLO. Source: `meetings/2026-01-19-weekly-sync.txt` (`decision:timeouts:2026-01-19`, status **active**).

So, as far as memory shows, the **current SLO is unchanged from the 2026-01-26 decision**:
- **2 s p95 latency** for first delivery attempt, 5-minute window
- **99.5% delivery success rate** per calendar month
- **500 ms p95** for `GET /deliveries/*`

If you want, I can also trace whether the meaning of “2 s” 

## m22 [ru / fact] Почему ADR-007 отклонили, какие цифры были у EKS?
**expected:** p95 0.4 с, но $6,100 в месяц, в 1.7 раза дороже Lambda, и второй кластер, который платформа не хочет эксплуатировать  
**expected sources:** {'sources': ['adr/ADR-007.md', 'docs/poc-eks-report.md', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 5.6s, 4 tool calls)
queries: ['ADR-007 context why rejected EKS numbers', 'ADR-007 Контекст почему отклонили EKS цифры', 'MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:$id}) RETURN n.id, n.title']

ADR-007 отклонили из-за компромисса между производительностью и стоимостью: в тексте ADR сказано, что это решение дало **p95 0.4 s**, но стоило **в 1.7 раза дороже в месяц** и означало **ещё одну платформу для поддержки**.

По цифрам про EKS:
- **p95 0.4 s**
- **1.7x monthly cost**
- в последствиях ADR также сказано, что **p95 в пять раз лучше, чем у Lambda**, но цена — **1.7x**, и команде платформы пришлось бы стать **Kubernetes team**.

Источник: `adr/ADR-007.md`, дата `2026-08-05`.

Графовая проверка по ADR-007 в базе ничего не вернула, поэтому статус и причина взяты из текста ADR.

### memory-eval-graph (completed, 5.5s, 3 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.date, a.file", "MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:'ADR-007'}) RETURN n.id, n.title, n.statu", "MATCH (d:Decision)-[:RECORDED_IN]->(:ADR {id:'ADR-007'}) OPTIONAL MATCH (p:Perso"]

ADR-007 был отклонён, потому что для темы был живой выбор в пользу Lambda: команда решила оставить Lambda предпочтительным вариантом, так как стоимость была на 41% ниже, чем у EKS, а измеренный p95 с provisioned concurrency — 1.9 секунды. Источник: `meetings/2026-07-27-poc-review.txt`, 2026-07-27.  
ADR-007: `Keep Relay on EKS with autoscaling`, статус `Rejected`, файл `adr/ADR-007.md`, дата 2026-08-05.

Про EKS в найденной записи есть только сравнение по стоимости: EKS был дороже, а именно база для сравнения — «41% lower than EKS»; числовое значение p95 в этой записи относится к Lambda (`1.9 seconds`), не к EKS. Источник: `meetings/2026-07-27-poc-review.txt`, 2026-07-27.

Если вы имели в виду другие цифры по EKS, в памяти по этой ADR я их не нашёл.

### memory-eval-vector (completed, 4.9s, 3 tool calls)
queries: ['Почему ADR-007 отклонили, какие цифры были у EKS?', 'ADR-007 отклонили EKS цифры', 'ADR-007 rejected EKS numbers']

ADR-007 отклонили, потому что, хотя у EKS была хорошая задержка, месячная стоимость была выше, а также это означало бы вторую платформу в поддержке. В памяти есть формулировки:

- **Decision**: `p95 0.4 s but 1.7x the monthly cost and a second platform to run` — **adr/ADR-007.md**, updated **2026-08-05**.
- **Consequences**: `p95 is five times better than Lambda but monthly cost is 1.7x and the platform team would have to become a Kubernetes team` — **adr/ADR-007.md**, updated **2026-08-05**.
- **Context**: ADR-007 was the alternative to ADR-006: keep Relay on EKS, add autoscaling and accept the cost — **adr/ADR-007.md**, updated **2026-08-05**.

По цифрам у EKS в памяти есть:
- **p95 = 0.4 s**
- **monthly cost = 1.7x** относительно альтернативы

Источник: **adr/ADR-007.md**, updated **2026-08-05**.

Если хотите, я могу ещё сопоставить это с ADR-006, чтобы показать, против чего именно сравнивали EKS.

## t01 [en / current] What is the current decision on infrastructure as code, and when was it made?
**expected:** Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation (decided 2026-04-20, owner Pavel Grishin)  
**expected sources:** {'sources': ['meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 3.4s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERSE"]

The current decision on infrastructure as code is: “The state has been cleaned up.” It was made on 2026-06-01.

Source: `meetings/2026-06-01-weekly-sync.txt`  
Status: active

### memory-eval-graph (completed, 3.6s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) WHERE NOT (d)<-[:SUPERSE"]

Current decision on infrastructure as code: **“The state has been cleaned up.”**  
It was made on **2026-06-01**.  
Source: **meetings/2026-06-01-weekly-sync.txt**.

### memory-eval-vector (completed, 4.6s, 3 tool calls)
queries: ['What is the current decision on infrastructure as code, and when was it made?', 'current decision on infrastructure as code when was it made', 'infrastructure as code decision date current']

The current decision on infrastructure as code is:

- **Hybrid IaC: networking in Terraform, application stacks in CloudFormation (ADR-004)** — **current** as of **2026-04-20**. Source: **confluence/decision-log.xhtml** (updated 2026-06-03), entry dated **2026-04-20**.  
- This **supersedes ADR-001** (“Migrate infrastructure code from Terraform to CloudFormation”), which is now **superseded**. Source: **confluence/decision-log.xhtml** (updated 2026-06-03), entry dated **2026-01-12** marked **SUPERSEDED**; and **adr/ADR-001.md** (updated 2026-01-14), marked superseded by ADR-004.

What I retrieved:
- **confluence/decision-log.xhtml** — 2026-06-03
- **adr/ADR-001.md** — 2026-01-14



## t02 [ru / history] Как менялось решение по теме «infrastructure as code»? Перечисли по датам.
**expected:** 2026-01-12: Migrate Relay infrastructure code from Terraform to CloudFormation, module by module, finishing by end of Q1 → 2026-02-09: One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway) → 2026-02-23: Manual console changes are frozen; nightly drift detection on every stack with alerts to on-call → 2026-04-20: Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-02-09-weekly-sync.txt', 'meetings/2026-02-23-incident-review.txt', 'meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 18.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (d)-[:SUP"]

По теме infrastructure as code решения менялись так:

- 2026-01-12 — **A01**: «Migrate Relay from Terraform to CloudFormation module by module by the end of Q1.»  
  source: `meetings/2026-01-12-weekly-sync.txt`  
  status: `superseded`

- 2026-01-19 — **A02**: «The migration to CFN will start with compute, with data network handled last.»  
  source: `meetings/2026-01-19-weekly-sync.txt`  
  status: `active`

- 2026-02-02 — **A06**: «The compute module was moved into a CloudFormation stack and imported without recreation, and deploys through the pipeline now work.»  
  source: `meetings/2026-02-02-weekly-sync.txt`  
  status: `active`

- 2026-02-02 — **A07**: «Enable drift detection immediately on the new stack.»  
  source: `meetings/2026-02-02-weekly-sync.txt`  
  status: `active`

- 2026-02-09 — **A09**: «Use one root stack per environment with nested stacks by component.»  
  source: `meetings/2026-02-09-weekly-sync.txt`  
  status: `active`

- 2026-02-23 — **A10**: «Nightly drift detection will run on all stacks with alerts.»  
  source: `meetings/2026-02-23-incident-review.txt`  
  status: `active`

- 2026-03-30 — **A15**: «The network stack has been moved to CloudFormation 

### memory-eval-graph (completed, 16.6s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (d)-[:SUP"]

По теме infrastructure as code решение менялось так:

- 2026-01-12 — «Migrate Relay from Terraform to CloudFormation module by module by the end of Q1.»  
  Статус: superseded. Источник: `meetings/2026-01-12-weekly-sync.txt`  
- 2026-01-19 — «The migration to CFN will start with compute, with data network handled last.»  
  Статус: active. Источник: `meetings/2026-01-19-weekly-sync.txt`  
- 2026-02-02 — «Enable drift detection immediately on the new stack.»  
  Статус: active. Источник: `meetings/2026-02-02-weekly-sync.txt`  
- 2026-02-02 — «The compute module was moved into a CloudFormation stack and imported without recreation, and deploys through the pipeline now work.»  
  Статус: active. Источник: `meetings/2026-02-02-weekly-sync.txt`  
- 2026-02-09 — «Use one root stack per environment with nested stacks by component.»  
  Статус: active. Источник: `meetings/2026-02-09-weekly-sync.txt`  
- 2026-02-23 — «Nightly drift detection will run on all stacks with alerts.»  
  Статус: active. Источник: `meetings/2026-02-23-incident-review.txt`  
- 2026-03-30 — «The network stack has been moved to CloudFormation and the peering was imported without recreation after the third attempt.»  

### memory-eval-vector (completed, 11.3s, 3 tool calls)
queries: ['Как менялось решение по теме «infrastructure as code»? Перечисли по датам.', 'infrastructure as code decision dates history', 'решение по теме infrastructure as code по датам']

Вот как менялось решение по теме **infrastructure as code** по датам:

- **2026-01-12** — принято решение **мигрировать инфраструктурный код с Terraform на CloudFormation**.  
  Источник: `confluence/decision-log.xhtml` (2026-06-03, запись про 2026-01-12), и ADR-001.  
  Статус в текущем виде: **superseded**.

- **2026-01-14** — оформлено ADR-001: **“Migrate infrastructure code from Terraform to CloudFormation”**; в документе решение описано как перенос **модуль за модулем** до конца Q1.  
  Источник: `adr/ADR-001.md` (updated 2026-01-14).  
  Статус: **Superseded (superseded by ADR-004)**.

- **2026-03-12** — в архитектурном документе уже зафиксировано, что **application stacks are CloudFormation**, а network module is being moved last.  
  Источник: `confluence/architecture.xhtml` (updated 2026-03-12).  
  Это похоже на промежуточное состояние, но документ не является решением.

- **2026-04-20** — принято новое решение: **гибридный IaC** — **Terraform для networking, CloudFormation для application stacks**. Это **supersedes ADR-001**.  
  Источник: `confluence/decision-log.xhtml` (updated 2026-06-03, запись 2026-04-20); также `adr/ADR-004.md` (updated 2026-04-22).  
  Статус: **A

## t03 [en / current] What is the current decision on gateway timeout, and when was it made?
**expected:** Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom (decided 2026-08-24, owner Ivan Melnik)  
**expected sources:** {'sources': ['meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 5.3s, 4 tool calls)
queries: ['gateway timeout current decision made when', 'таймаут gateway текущее решение когда принято', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE NOT (d)<-[:SU", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20"]

Current decision on gateway timeout: **the gateway timeout is set to 25 seconds instead of 30 seconds**. It was made on **2026-08-24**.

Source: `meetings/2026-08-24-weekly-sync.txt`  
Decision status: `active`

### memory-eval-graph (completed, 3.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE NOT (d)<-[:SU"]

The current decision on gateway timeout is: “The gateway timeout is set to 25 seconds instead of 30 seconds.” It was made on 2026-08-24. Source: `meetings/2026-08-24-weekly-sync.txt` (decision date 2026-08-24).

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['What is the current decision on gateway timeout, and when was it made?', 'gateway timeout decision current made date', 'gateway timeout']

The current decision in memory is:

- **Gateway timeout is set to 25 seconds instead of 30 seconds** — **made on 2026-08-24**.  
  Source: `meetings/2026-08-24-weekly-sync.txt` via claim **A50** (`decision:timeouts:2026-08-24`), status **active**.

Note: I also found an older document saying the integration timeout is **10 seconds** for Relay routes, decided **2026-03-16** in `docs/gateway.md`, but that appears to be about the API gateway integration policy, not the specific “gateway timeout” decision you asked about.

## t04 [ru / history] Как менялось решение по теме «gateway timeout»? Перечисли по датам.
**expected:** 2026-03-16: Gateway integration timeout 10 s on every Relay route → 2026-05-18: Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14 → 2026-08-24: Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom  
**expected sources:** {'sources': ['meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 5.2s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.text CONTAI", 'gateway timeout 25 seconds 30 seconds decision rationale']

По теме **gateway timeout** в памяти найдено одно решение:

- **2026-08-24** — “The gateway timeout is set to 25 seconds instead of 30 seconds.”  
  **status:** active  
  **source:** `meetings/2026-08-24-weekly-sync.txt`  
  Это решение **A50** и оно **supersedes A47**.

Если нужен именно **полный список цепочки изменений** по этой теме, могу перечислить ещё и предыдущее решение, которое было заменено.

### memory-eval-graph (completed, 6.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) RETURN d.text, d.da"]

По теме «gateway timeout» решение менялось так, по датам:

- 2026-01-19 — «Relay will keep a 60 s delivery timeout for now because there is no gateway yet.»  
  Источник: `meetings/2026-01-19-weekly-sync.txt`  
  Статус: `active`

- 2026-03-16 — «Set the integration timeout to 10 s for all routes.»  
  Источник: `meetings/2026-03-16-weekly-sync.txt`  
  Статус: `superseded`

- 2026-05-18 — «The integration timeout is increased from 10 s to 30 s while synchronous mode remains enabled.»  
  Источник: `meetings/2026-05-18-weekly-sync.txt`  
  Статус: `active`

- 2026-07-27 — «The team agreed that the SLO is 2 seconds for the first delivery attempt, not for the client response.»  
  Источник: `meetings/2026-07-27-poc-review.txt`  
  Статус: `superseded`

- 2026-08-24 — «The gateway timeout is set to 25 seconds instead of 30 seconds.»  
  Источник: `meetings/2026-08-24-weekly-sync.txt`  
  Статус: `active`

Если нужно, могу ещё отдельно показать, какое решение сейчас в силе на этой теме.

### memory-eval-vector (completed, 10.5s, 3 tool calls)
queries: ['Как менялось решение по теме «gateway timeout»? Перечисли по датам.', 'gateway timeout решение по датам', 'изменения решения gateway timeout']

По теме **gateway timeout** в памяти есть такие решения по датам:

- **2026-01-19** — Relay будет держать **60 s** delivery timeout, потому что gateway ещё не было.  
  Источник: `meetings/2026-01-19-weekly-sync.txt` (claim A03), статус `active`.

- **2026-03-16** — для gateway интеграции установлен timeout **10 s** на каждый маршрут.  
  Это отражено в документе, обновлённом **2026-03-18**.  
  Источник: `docs/gateway.md` (раздел `Timeouts`), `updated 2026-03-18`.

- **2026-05-11** — gateway будет сохранять лимит **10 s**; медленные клиенты могут держать доставку дольше и получать `504`.  
  Источник: `meetings/2026-05-11-weekly-sync.txt` (claim A25), статус `active`.  
  Это согласуется с решением от 2026-03-16, то есть отдельного изменения тут в памяти нет.

- **2026-08-24** — gateway timeout изменён на **25 s вместо 30 s**.  
  Источник: `meetings/2026-08-24-weekly-sync.txt` (claim A50), статус `active`, **supersedes A47**.

- **2026-09-23** — в ADR-010 зафиксировано, что после ADR-006 timeout **30 s** вообще не применялся, потому что жёсткий лимит gateway — **29 s**; ADR-010 лишь **предлагает** политику для Lambda integrations, а не утверждает новое решение.  
  Источник: `adr

## t05 [en / chain] The current decision on gateway timeout replaced an earlier one. What did that earlier decision itself replace, and when?
**expected:** Gateway integration timeout lowered from 30 s to 25 s: the gateway's hard limit is 29 s and Lambda needs headroom (2026-08-24) replaced 'Gateway integration timeout raised from 10 s to 30 s after the slow-target incident of 2026-05-14' (2026-05-18), which replaced 'Gateway integration timeout 10 s on every Relay route' (2026-03-16)  
**expected sources:** {'sources': ['meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 9.4s, 3 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE NOT (cur)<-", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.date <= '20", 'gateway timeout earlier decision replaced by A03 supersedes predecessor replace ']

Assumption: by “gateway timeout” you mean the timeout decision on the **timeouts** topic.

I found the current timeout decision in force on **2026-01-19**:

- **A03** — “Relay will keep a 60 s delivery timeout for now because there is no gateway yet.”  
  Source: `meetings/2026-01-19-weekly-sync.txt`  
  Date: `2026-01-19`  
  Status: `active`

But I did **not** find an earlier decision that A03 itself replaced. In the graph, A03 has no `SUPERSEDES` link, so there is no predecessor recorded for it.

So the answer is: **nothing in memory shows that the earlier gateway timeout decision replaced another one; A03 appears to be the earliest recorded decision on that timeout topic.**

### memory-eval-graph (completed, 7.2s, 2 tool calls)
queries: ["MATCH (cur:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'})\nWHERE cur.text CO", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'})\nWHERE d.text CONTAI"]

The earlier decision was: “The team agreed that the SLO is 2 seconds for the first delivery attempt, not for the client response.” It was made on 2026-07-27 and is marked superseded; source: `meetings/2026-07-27-poc-review.txt`.

That earlier decision itself replaced: “The gateway timeout is 30 seconds.” It was made on 2026-07-13 and is also superseded; source: `meetings/2026-07-13-weekly-sync.txt`.

Source chain:
- current gateway-timeout decision: `meetings/2026-08-24-weekly-sync.txt`, 2026-08-24
- earlier decision it superseded: `meetings/2026-07-27-poc-review.txt`, 2026-07-27
- decision replaced by that earlier one: `meetings/2026-07-13-weekly-sync.txt`, 2026-07-13

### memory-eval-vector (completed, 3.8s, 3 tool calls)
queries: ['The current decision on gateway timeout replaced an earlier one. What did that e', 'gateway timeout decision replaced earlier decision what did it replace when', 'gateway timeout replaced by earlier decision replaced what when']

The earlier decision was **A47**, and the memory says the current gateway-timeout decision on **2026-08-24** “**Supersedes A47**” in **meetings/2026-08-24-weekly-sync.txt**.

I could not find what **A47 itself replaced** in the retrieved chunks. So the answer is **not in memory** from what I retrieved.

Retrieved:
- **meetings/2026-08-24-weekly-sync.txt** — 2026-08-24: current decision says “Supersedes A47.”
- **adr/ADR-010.md** — 2026-09-23: context mentions the 30 s timeout and later policy discussion, but not A47’s predecessor.


## t06 [en / current] What is the current decision on retries, and when was it made?
**expected:** Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off (decided 2026-08-24, owner Anna Sokolova)  
**expected sources:** {'sources': ['meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 3.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (d)<-[:SUP"]

The current decision on retries is:

- “Retry ownership for the SQS pipeline is transferred from Anna to Vanya starting today.”
- Date made: 2026-09-07
- Status: active
- Source: meetings/2026-09-07-security-review.txt



### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) WHERE NOT (d)<-[:SUP"]

Current decision on retries: “Retry ownership for the SQS pipeline is transferred from Anna to Vanya starting today.” It was made on 2026-09-07. Source: `meetings/2026-09-07-security-review.txt`.

I’m assuming “current decision” means the latest non-superseded active decision on `topic:retries`.

### memory-eval-vector (completed, 3.4s, 3 tool calls)
queries: ['What is the current decision on retries, and when was it made?', 'current decision retries made date Relay webhook delivery', 'retries decision status date source Relay']

The current decision on retries is that **retries are no longer a gateway policy**. This was decided on **2026-08-24** in **ADR-009**.

Source:
- **docs/retries-dlq.md** — updated **2026-08-27**; says “Decided 2026-08-24 (ADR-009). Retries are no longer a gateway policy.”

Note: I also found older, conflicting entries saying retries were disabled on `POST /deliver` or under gateway policy, but those are older than the 2026-08-24 decision.

## t07 [ru / history] Как менялось решение по теме «retries»? Перечисли по датам.
**expected:** 2026-03-30: Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice → 2026-06-15: Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15% → 2026-08-24: Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off  
**expected sources:** {'sources': ['meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 7.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) OPTIONAL MATCH (d)-["]

По теме **retries** зафиксированы такие решения, по датам:

- **2026-03-30** — *A17* — `active`  
  «Deliver retries are disabled until idempotency keys exist, and read-side retries are capped at two attempts.»  
  source: `meetings/2026-03-30-weekly-sync.txt`

- **2026-06-01** — *A35* — `active`  
  «Retries are handed over from Nikita to Anna starting today.»  
  source: `meetings/2026-06-01-weekly-sync.txt`

- **2026-06-15** — *A37* — `superseded`  
  «Retries on deliver should be enabled at the gateway with a maximum of 3 attempts and a 15% retry budget.»  
  source: `meetings/2026-06-15-weekly-sync.txt`

- **2026-08-24** — *A49* — `active`  
  «Retries move to SQS with a dead letter queue after 5 attempts, and gateway retries on deliver are turned off.»  
  source: `meetings/2026-08-24-weekly-sync.txt`

- **2026-09-07** — *A51* — `active`  
  «Retry ownership for the SQS pipeline is transferred from Anna to Vanya starting today.»  
  source: `meetings/2026-09-07-security-review.txt`

Если нужно, я могу ещё отдельно показать **цепочку смены именно технического решения** по retries, без строк про ownership.

### memory-eval-graph (completed, 6.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) OPTIONAL MATCH (d)-["]

По теме **retries** решение менялось так, по датам:

- **2026-03-30** — `Deliver retries are disabled until idempotency keys exist, and read-side retries are capped at two attempts.`  
  Источник: `meetings/2026-03-30-weekly-sync.txt`

- **2026-06-01** — `Retries are handed over from Nikita to Anna starting today.`  
  Источник: `meetings/2026-06-01-weekly-sync.txt`

- **2026-06-15** — `Retries on deliver should be enabled at the gateway with a maximum of 3 attempts and a 15% retry budget.`  
  Источник: `meetings/2026-06-15-weekly-sync.txt`

- **2026-08-24** — `Retries move to SQS with a dead letter queue after 5 attempts, and gateway retries on deliver are turned off.`  
  Это решение **поправило** решение от 2026-06-15.  
  Источник: `meetings/2026-08-24-weekly-sync.txt`

- **2026-09-07** — `Retry ownership for the SQS pipeline is transferred from Anna to Vanya starting today.`  
  Источник: `meetings/2026-09-07-security-review.txt`

Если хочешь, я могу ещё отдельно показать **какое решение сейчас в силе** по retries.

### memory-eval-vector (completed, 6.4s, 3 tool calls)
queries: ['Как менялось решение по теме «retries»? Перечисли по датам.', 'retries решение по датам', 'topic retries decision dates']

По теме **retries** в памяти есть такие решения по датам:

1. **2026-03-30** — **deliver retries disabled**, пока не появятся idempotency keys; **read-side retries capped at two attempts**.  
   Источник: `meetings/2026-03-30-weekly-sync.txt` / claim `A17` (active), дата **2026-03-30**.

2. **2026-08-24** — retries **перенесены из gateway в SQS + dead-letter queue**; после **5 попыток** сообщение уходит в DLQ, а **gateway retries on /deliver turned off**.  
   Источник: `meetings/2026-08-24-weekly-sync.txt` / claim `A49` (active), дата **2026-08-24**.  
   Это же решение зафиксировано в **ADR-009**: `adr/ADR-009.md`, дата **2026-08-26** (updated 2026-08-26), но сама decision date — **2026-08-24**.

Что вижу по истории:
- Есть более ранний **open item** от **2026-03-16**: “Gateway retries cannot be enabled yet.”  
  Источник: `meetings/2026-03-16-weekly-sync.txt` / claim `Q7`, дата **2026-03-16**.

Если хочешь, могу ещё оформить это как **хронологию изменений** с пометкой, какое решение **сейчас актуально**, а какое **устарело/superseded**.

## t08 [en / chain] The current decision on retries replaced an earlier one. What did that earlier decision itself replace, and when?
**expected:** Retries move out of the gateway into SQS with a dead-letter queue after 5 attempts; gateway retries on /deliver are turned off (2026-08-24) replaced 'Retries enabled on POST /deliver at the gateway: max 3 attempts, retry budget 15%' (2026-06-15), which replaced 'Retries disabled on POST /deliver at the gateway until idempotency keys exist; read routes may retry twice' (2026-03-30)  
**expected sources:** {'sources': ['meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 5.4s, 2 tool calls)
queries: ['MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision) WHERE (cur)-[:ABOUT', "MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision) WHERE cur.id='A37' "]

The earlier retries decision was **A37**:

- **A37** — “Retries on deliver should be enabled at the gateway with a maximum of 3 attempts and a 15% retry budget.”
- **Date:** 2026-06-15
- **Status:** superseded
- **Source:** meetings/2026-06-15-weekly-sync.txt

I checked whether **A37** itself superseded an even earlier decision, but I found no supersession chain for A37 in memory. So the earlier decision appears to have **replaced nothing recorded here**.

### memory-eval-graph (completed, 5.1s, 1 tool calls)
queries: ['MATCH path=(cur:Decision)-[:SUPERSEDES*1..5]->(old:Decision)\nWHERE (cur)-[:ABOUT']

The earlier retries decision was:

- “Retries on deliver should be enabled at the gateway with a maximum of 3 attempts and a 15% retry budget.”  
  Source: `meetings/2026-06-15-weekly-sync.txt`  
  Date: `2026-06-15`

From the supersession chain, that earlier decision itself did not replace any prior retries decision in memory; it is the oldest decision in the chain I retrieved.

### memory-eval-vector (completed, 5.6s, 3 tool calls)
queries: ['The current decision on retries replaced an earlier one. What did that earlier d', 'retries decision replaced earlier one what did it replace and when', 'retries replace earlier decision replace when']

The earlier retries decision was **A37**, which said: **retries on `POST /deliver` should be enabled at the gateway with a maximum of 3 attempts and a 15% retry budget**. It was dated **2026-06-15** and is marked **superseded** by **A49**. Source: `meetings/2026-06-15-weekly-sync.txt` (2026-06-15).

What A37 itself replaced is **not in memory** from the retrieved chunks. I retrieved:
- **A49** — `meetings/2026-08-24-weekly-sync.txt` (2026-08-24), supersedes A37
- **A37** — `meetings/2026-06-15-weekly-sync.txt` (2026-06-15), superseded by A49
- **ADR-009 / docs/retries-dlq.md** — `adr/ADR-009.md` (2026-08-26) and `docs/retries-dlq.md` (updated 2026-08-27) confirming the current decision

## t09 [en / current] What is the current decision on compute platform, and when was it made?
**expected:** Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances (decided 2026-08-03, owner Ivan Melnik)  
**expected sources:** {'sources': ['meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 3.7s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE NOT (d)<-[:SUP"]

The current decision on compute platform is: “Relay moves to Lambda with provisioned concurrency on deliver.”  
It was made on 2026-08-03.

Source: `meetings/2026-08-03-architecture-committee.txt`  
Status: active

### memory-eval-graph (completed, 2.9s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) WHERE NOT (d)<-[:SUP"]

The current decision on compute platform is: “Relay moves to Lambda with provisioned concurrency on deliver.”  
It was made on 2026-08-03. Source: `meetings/2026-08-03-architecture-committee.txt`.

For context, the latest live decisions on the same topic before that were already pointing toward Lambda/provisioned concurrency.

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['What is the current decision on compute platform, and when was it made?', 'current decision compute platform made date Relay webhook delivery project', 'compute platform decision status current superseded Relay']

The current decision on compute platform is: **Relay moves to Lambda with provisioned concurrency on `/deliver`**. It was made on **2026-08-03**.

Source:
- **meetings/2026-08-03-architecture-committee.txt** — decision claim **A48** (`compute`), dated **2026-08-03**, status **active**
- **adr/ADR-006.md** — updated **2026-08-05**, status **Accepted**, says **“Run Relay on Lambda with provisioned concurrency”** and lists **Deciders: Relay weekly sync, 2026-08-03**

I also found a related older document:
- **adr/ADR-007.md** — updated **2026-08-05**, status **Rejected**, describing the rejected EKS-with-autoscaling alternative.

## t10 [ru / history] Как менялось решение по теме «compute platform»? Перечисли по датам.
**expected:** 2026-06-15: Run two compute PoCs in parallel: EKS with autoscaling (Timur) and Lambda (Sergey); decide on cost and p95 by end of July → 2026-08-03: Relay moves to Lambda with provisioned concurrency on /deliver; PoC-3 showed 41% lower monthly cost and p95 1.9 s with warm instances  
**expected sources:** {'sources': ['meetings/2026-06-15-weekly-sync.txt', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 12.1s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) OPTIONAL MATCH (d)-["]

По теме «compute platform» решение менялось так:

- 2026-06-15 — **A36**: «The team will run poc-2 on EKS with autoscaling led by Timur and poc-3 on Lambda led by Sergey in parallel, and choose the option by the end of July based on monthly cost and p95.»  
  источник: `meetings/2026-06-15-weekly-sync.txt`

- 2026-06-29 — **A38**: «PoC-2 on EKS with Carpenter is under load and its p95 is 0.4 s.»  
  источник: `meetings/2026-06-29-weekly-sync.txt`  
  статус: superseded

- 2026-06-29 — **A39**: «PoC-3 on Lambda has a working basic variant, but the hybrid and state work took a week.»  
  источник: `meetings/2026-06-29-weekly-sync.txt`

- 2026-07-13 — **A41**: «PoC-3 for Relay on Lambda is transferred from Sergey to Ivan.»  
  источник: `meetings/2026-07-13-weekly-sync.txt`

- 2026-07-13 — **A42**: «Ivan will rewrite the handlers to use provisioned concurrency and SQS between intake and delivery.»  
  источник: `meetings/2026-07-13-weekly-sync.txt`

- 2026-07-13 — **A43**: «The cold start issue during long delivery is the main question to verify in PoC-3.»  
  источник: `meetings/2026-07-13-weekly-sync.txt`

- 2026-07-27 — **A44**: «The team decided to keep Lambda as the preferred opt

### memory-eval-graph (completed, 11.6s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:compute'}) OPTIONAL MATCH (d)-["]

По теме **compute platform** решение менялось так, по датам:

- **2026-06-15** — принято, что команда **параллельно** проверяет два варианта: **poc-2 на EKS** и **poc-3 на Lambda**, а выбор сделают к концу июля по **monthly cost** и **p95**.  
  Источник: `meetings/2026-06-15-weekly-sync.txt`, решение `A36` (active). Дата: `2026-06-15`.

- **2026-06-29** — по Lambda сообщено, что **базовый вариант работает**, но **hybrid/state** заняли неделю; по EKS зафиксировано, что PoC-2 под нагрузкой и **p95 = 0.4 s**.  
  Источник: `meetings/2026-06-29-weekly-sync.txt`, решения `A39` и `A38`. Дата: `2026-06-29`.

- **2026-07-13** — уточнение по PoC-3: главная проверка — **cold start** при долгой доставке; Ивану поручено переписать handlers на **provisioned concurrency** и **SQS between intake and delivery**; PoC-3 передан от Сергея Ивану.  
  Источник: `meetings/2026-07-13-weekly-sync.txt`, решения `A43`, `A42`, `A41`. Дата: `2026-07-13`.

- **2026-07-27** — решение в пользу Lambda было **уточнено/заменено**: теперь **provisioned concurrency on deliver is mandatory** для жизнеспособности Lambda.  
  Источник: `meetings/2026-07-27-poc-review.txt`, решение `A45` (active), а прежнее предпочтение

### memory-eval-vector (completed, 9.2s, 4 tool calls)
queries: ['Как менялось решение по теме «compute platform»? Перечисли по датам.', 'compute platform', 'compute platform decision', 'compute platform PoC EKS Lambda ADR-005']

По теме **compute platform** решения менялись так:

- **2026-06-17** — решили **запустить два PoC параллельно: EKS с autoscaling и Lambda**, чтобы выбрать по стоимости и p95 к концу июля.  
  Источник: `adr/ADR-005.md` (2026-06-17), статус **Superseded**.

- **2026-08-05** — предыдущее решение было **заменено**: **Relay переводится на Lambda с provisioned concurrency** на `/deliver`. Основание: PoC-3 показал **41% ниже стоимость** и **p95 1.9 s** при warm instances.  
  Источник: `adr/ADR-006.md` (2026-08-05), статус **Accepted, supersedes ADR-005**.

- **2026-08-05** — альтернатива **оставить Relay на EKS с autoscaling** была **отклонена**: p95 лучше, но стоимость **1.7x** и платформа не хотела становиться Kubernetes-командой.  
  Источник: `adr/ADR-007.md` (2026-08-05), статус **Rejected**.

Что я нашёл дополнительно, но это не было именно решением по compute platform:
- `confluence/migration-roadmap.xhtml` (2026-06-20) — compute platform был в статусе **PENDING POC**.
- `docs/overview.md` (2026-01-20) — compute platform был только пунктом программы, без решения.

Если хочешь, я могу ещё собрать это в виде короткой хронологии “решение → пересмотр → финальный выбор”.

## t11 [en / current] What is the current decision on SLO, and when was it made?
**expected:** Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s (decided 2026-10-05, owner Lena Kim)  
**expected sources:** {'sources': ['meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 3.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

The current SLO decision is:

- **“For 30 days after cutover, p95 will be relaxed to 3 seconds, then returned to 2 seconds.”**
- **Made on:** **2026-10-05**
- **Status:** active
- **Source:** `meetings/2026-10-05-cutover-planning.txt`

### memory-eval-graph (completed, 3.4s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) WHERE NOT (d)<-[:SUPERSE"]

Current decision on SLO: “For 30 days after cutover, p95 will be relaxed to 3 seconds, then returned to 2 seconds.” Source: `meetings/2026-10-05-cutover-planning.txt`, dated `2026-10-05`.



### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['What is the current decision on SLO, and when was it made?', 'current decision on SLO made date Relay webhook delivery project', 'SLO decision date Relay webhook delivery']

The current decision on SLO is:

- p95 end-to-end delivery latency of **2 s** over a **5-minute window**
- monthly delivery success rate of **99.5%**

It was made on **2026-01-26**. Source: `meetings/2026-01-26-weekly-sync.txt` (`claim:decision:slo:2026-01-26`, status **active**).

Note: the document `docs/slo.md` was updated on **2026-01-28** and says “Decided 2026-01-26,” which is consistent with that decision.

## t12 [ru / history] Как менялось решение по теме «SLO»? Перечисли по датам.
**expected:** 2026-01-26: Delivery SLO: p95 end-to-end delivery latency 2 s over 5 minutes; monthly delivery success rate 99.5% → 2026-10-05: Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after the serverless cutover, then back to 2 s  
**expected sources:** {'sources': ['meetings/2026-01-26-weekly-sync.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 6.8s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) OPTIONAL MATCH (d)-[:SUP"]

По теме **SLO** решение менялось так:

- **2026-01-26** — зафиксировали SLO: **p95 end-to-end latency 2 s** в окне **5 минут** и **monthly delivery success rate 99.5%**.  
  Источник: `meetings/2026-01-26-weekly-sync.txt` — решение `A05`.

- **2026-05-11** — по SLO в этом решении изменения не было; записано, что **вопрос synchronous mode** будут пересматривать на следующем встрече.  
  Источник: `meetings/2026-05-11-weekly-sync.txt` — решение `A27`.

- **2026-07-27** — новое решение по SLO для Lambda: **p95 допустим только 1.9 секунды**, без запаса, и перед rollout нужен **10x load test**.  
  Источник: `meetings/2026-07-27-poc-review.txt` — решение `A46` (потом **superseded**).

- **2026-10-05** — текущая версия: **на 30 дней после cutover p95 можно ослабить до 3 секунд, затем вернуть к 2 секундам**.  
  Источник: `meetings/2026-10-05-cutover-planning.txt` — решение `A58`.

Если хочешь, могу ещё отдельно показать **какое решение сейчас в силе** и **какое было superseded**.

### memory-eval-graph (completed, 7.0s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) RETURN d.id, d.text, d.d"]

По теме **SLO** в памяти есть такие решения по датам:

- **2026-01-26** — установили SLO: **p95 end-to-end latency 2 s** в окне **5 минут** и **monthly delivery success rate 99.5%**.  
  Источник: `meetings/2026-01-26-weekly-sync.txt`

- **2026-05-11** — зафиксировали, что **вопрос synchronous mode** будут пересматривать на следующем собрании.  
  Источник: `meetings/2026-05-11-weekly-sync.txt`

- **2026-07-27** — для Lambda признали допустимым вариант **только если p95 держится на 1.9 s** и **без запаса**, поэтому требуется **10x load test** перед rollout.  
  Это решение позже помечено как **superseded**.  
  Источник: `meetings/2026-07-27-poc-review.txt`

- **2026-10-05** — на **30 дней после cutover** p95 будет **ослаблен до 3 s**, затем возвращён к **2 s**.  
  Источник: `meetings/2026-10-05-cutover-planning.txt`

Если хочешь, я могу ещё отдельно показать **текущее решение по SLO** или **хронологию только активных решений без superseded**.

### memory-eval-vector (completed, 8.8s, 3 tool calls)
queries: ['Как менялось решение по теме «SLO»? Перечисли по датам.', 'SLO decision timeline dates', 'решение по теме SLO по датам']

По теме **SLO** в памяти есть такие решения и связанные записи:

- **2026-01-26** — приняли SLO для доставки: **p95 end-to-end latency 2 s за 5 минут** и **monthly delivery success rate 99.5%**.  
  Источник: `meetings/2026-01-26-weekly-sync.txt` (claim `A05`, дата `2026-01-26`, статус `active`).  
  Это же зафиксировано в `docs/slo.md` (обновлено `2026-01-28`), где написано, что решение было принято `2026-01-26`.

- **2026-05-11** — есть **open item** по теме `slo`: решить вопрос synchronous mode на следующей встрече.  
  Источник: `meetings/2026-05-11-weekly-sync.txt` (claim `Q17`, дата `2026-05-11`, статус `open`, **no owner**).

- **2026-07-27** — в обсуждении PoC уточнили, что SLO в 2 секунды относится **к первой попытке доставки, а не к ответу клиента**.  
  Источник: `meetings/2026-07-27-poc-review.txt` (claim `A47`, дата `2026-07-27`, статус `superseded`).

Важно: запись от **2026-07-27** помечена как **superseded**, то есть это история, а не текущая действующая формулировка решения.  
Если нужен именно **текущий** ответ по SLO, в памяти сейчас есть только решение от **2026-01-26**; более позднее изменение по сути в найденных фрагментах не зафиксировано как действующее реше

## t13 [ru / owner_now] Кто сейчас владеет темой «retries» и с какой даты?
**expected:** Ivan Melnik, с 2026-09-07  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 3.5s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.to IS NULL RE"]

Тему «retries» сейчас владеет Иван Мельник с 2026-09-07.

Источник: граф памяти, связка OWNS к теме `topic:retries` (дата владения: 2026-09-07).

### memory-eval-graph (completed, 3.1s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.to IS NULL RE"]

Темой «retries» сейчас владеет Ivan Melnik, с 2026-09-07. Источник: граф памяти; дата владения из OWNS-ребра на topic:retries.

### memory-eval-vector (completed, 3.3s, 3 tool calls)
queries: ['Кто сейчас владеет темой «retries» и с какой даты?', 'Who owns retries now and since what date?', 'ownership retries from date owner current']

Сейчас тему **«retries»** владеет **Ivan Melnik** — **с 2026-09-07**.  
Источник: `memory/decisions.jsonl`, запись `ownership:retries:2026-09-07` (2026-09-07).

Есть более старая, уже superseded запись: **Anna Sokolova** владела `retries` с **2026-06-01** до **2026-09-07**.  
Источник: `memory/decisions.jsonl`, запись `ownership:retries:2026-06-01` (2026-06-01).

## t14 [en / owner_at] Who owned retries on 2026-06-15?
**expected:** Anna Sokolova (from 2026-06-01 to 2026-09-07)  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 2.3s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(x {key:'topic:retries'}) WHERE o.from <= '2026-06-15"]

Anna Sokolova owned retries on 2026-06-15.

Source: ownership edge in the graph; from 2026-06-01 to 2026-09-07.

### memory-eval-graph (completed, 4.3s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:retries'}) WHERE o.from <= '2026"]

On 2026-06-15, retries was owned by Anna Sokolova; the OWNS edge started 2026-06-01 and was still in force on that date. Source: graph memory via OWNS on topic:retries, dated 2026-06-01.

### memory-eval-vector (completed, 2.8s, 1 tool calls)
queries: ['Who owned retries on 2026-06-15?']

On 2026-06-15, **Anna Sokolova** owned retries.

Sources:
- `memory/decisions.jsonl` — `2026-06-01`: Anna Sokolova owns retries from 2026-06-01 to 2026-09-07.
- `meetings/2026-06-01-weekly-sync.txt` — `2026-06-01`: “Retries are handed over from Nikita to Anna starting today.”

I also found a newer ownership claim:
- `memory/decisions.jsonl` — `2026-09-07`: Ivan Melnik owns retries from 2026-09-07 (current).



## t15 [ru / owner_now] Кто сейчас владеет темой «compute platform» и с какой даты?
**expected:** Ivan Melnik, с 2026-07-13  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt']}

### memory-eval-both (completed, 2.8s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.to IS NULL RE"]

Темой «compute platform» сейчас владеет **Ivan Melnik** с **2026-08-03**.

Источник: граф знаний; тема `topic:compute`, связь OWNS без даты окончания.

### memory-eval-graph (completed, 3.8s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.to IS NULL RE"]

Темой «compute platform» сейчас владеет **Ivan Melnik** с **2026-08-03**. Источник: граф памяти, связь `OWNS` к теме `topic:compute`; дата начала владения — `2026-08-03`.

### memory-eval-vector (completed, 2.7s, 1 tool calls)
queries: ['Кто сейчас владеет темой «compute platform» и с какой даты?']

Сейчас тему **compute** владеет **Ivan Melnik** с **2026-08-03**. Источник: `memory/decisions.jsonl` (claim ownership | compute | 2026-08-03).

В памяти есть и более старые, уже **superseded** записи:
- **Marat Yusupov** — с 2026-06-08 до 2026-08-03, `memory/decisions.jsonl`
- **Timur Aliev** — с 2026-06-15 до 2026-08-03, `memory/decisions.jsonl`

Если хотите, могу ещё проверить, нет ли отдельной темы именно **«compute platform»** как отличной от `compute`.

## t16 [en / owner_at] Who owned compute platform on 2026-06-28?
**expected:** Sergey Belov (from 2026-06-15 to 2026-07-13)  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt']}

### memory-eval-both (completed, 3.7s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.from <= '2026"]

On 2026-06-28, **Marat Yusupov** and **Timur Aliev** both owned the compute platform.

- **Marat Yusupov** — ownership from **2026-06-08** to **2026-08-03**
- **Timur Aliev** — ownership from **2026-06-15** to **2026-08-03**

Source: graph `OWNS` edges for `topic:compute` (no document file; ownership records in the database).

### memory-eval-graph (completed, 3.6s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:compute'}) WHERE o.from <= '2026"]

On 2026-06-28, compute platform was owned by **Timur Aliev** and **Marat Yusupov**.

- Timur Aliev — OWNS from **2026-06-15** to **2026-08-03**; source: memory graph, topic **compute platform**.
- Marat Yusupov — OWNS from **2026-06-08** to **2026-08-03**; source: memory graph, topic **compute platform**.

If you want, I can also check who owned it “now” or on another date.

### memory-eval-vector (completed, 2.3s, 1 tool calls)
queries: ['Who owned compute platform on 2026-06-28?']

Timur Aliev owned compute platform on 2026-06-28, based on the ownership decision dated 2026-06-15 in `memory/decisions.jsonl`.

Note: that claim was later superseded by a newer ownership decision dated 2026-08-03, which says Ivan Melnik owns compute from 2026-08-03 (current), also in `memory/decisions.jsonl`.

## t17 [ru / owner_now] Кто сейчас владеет темой «idempotency» и с какой даты?
**expected:** Anna Sokolova, с 2026-06-01  
**expected sources:** {'sources': []}

### memory-eval-both (completed, 3.3s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.to IS NUL"]

Сейчас темой «idempotency» владеет **Анна Соколова** с **2026-06-01**.  
Источник: граф OWNS, дата начала владения `2026-06-01`.

### memory-eval-graph (completed, 3.1s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.to IS NUL"]

Темой «idempotency» сейчас владеет Anna Sokolova с 2026-06-01. Источник: граф памяти, связь OWNS к теме `topic:idempotency`; дата владения: 2026-06-01.

### memory-eval-vector (completed, 3.3s, 3 tool calls)
queries: ['Кто сейчас владеет темой «idempotency» и с какой даты?', 'кто владеет idempotency сейчас дата с какой даты', 'ownership idempotency from date owner current']

Сейчас тему **idempotency** владеет **Anna Sokolova** с **2026-06-01**.

Источник:
- `memory/decisions.jsonl`, 2026-06-01 — `Anna Sokolova owns idempotency from 2026-06-01 (current).`
- `meetings/2026-06-01-weekly-sync.txt`, 2026-06-01 — `Idempotency is handed over from Nikita to Anna starting today.`

Также найдено более раннее, уже **superseded**:
- `memory/decisions.jsonl`, 2026-04-27 — `Nikita Frolov owns idempotency from 2026-04-27 to 2026-06-01.`

## t18 [en / owner_at] Who owned idempotency on 2026-05-28?
**expected:** Nikita Frolov (from 2026-05-18 to 2026-06-01)  
**expected sources:** {'sources': []}

### memory-eval-both (completed, 3.4s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.from <= '"]

On 2026-05-28, idempotency was owned by Nikita Frolov, from 2026-04-27 to 2026-06-01.

### memory-eval-graph (completed, 3.0s, 1 tool calls)
queries: ["MATCH (p:Person)-[o:OWNS]->(t:Topic {key:'topic:idempotency'}) WHERE o.from <= '"]

Nikita Frolov owned idempotency on 2026-05-28. Source: memory graph ownership edge on topic:idempotency, from 2026-04-27 to 2026-06-01.

### memory-eval-vector (completed, 3.3s, 3 tool calls)
queries: ['Who owned idempotency on 2026-05-28?', 'idempotency ownership 2026-05-28', 'owner of idempotency on 2026-05-28']

On 2026-05-28, **Nikita Frolov** owned idempotency.

Source:
- `memory/decisions.jsonl` — 2026-04-27: “Nikita Frolov owns idempotency from 2026-04-27 to 2026-06-01.”
- `meetings/2026-05-11-weekly-sync.txt` — 2026-05-11: idempotency ownership still listed with **Nikita Frolov**.
- `meetings/2026-06-01-weekly-sync.txt` — 2026-06-01: ownership handed over to **Anna Sokolova**, so this is after your date.

## t19 [ru / objector] Кто предложил и кто возражал против решения «Migrate Relay infrastructure code from Terraform to CloudFor…»?
**expected:** proposer Pavel Grishin, objector Timur Aliev, 2026-01-12  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt']}

### memory-eval-both (completed, 3.6s, 3 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Migrate Relay infrastructure code f", '"Migrate Relay infrastructure code from Terraform to CloudFor" proposed objected', '"Migrate Relay infrastructure code from Terraform to CloudFormation" proposed ob']

Предположу, что вы имеете в виду решение **“Migrate Relay infrastructure code from Terraform to CloudFormation”** из ADR-001.

- **Предложил:** **Pavel Grishin** — источник: `adr/ADR-001.md`, дата `2026-01-14`
- **Возражал:** **Timur Aliev** — источник: `adr/ADR-001.md`, дата `2026-01-14`

Подтверждение из текста ADR:  
“**Objection recorded from Timur Aliev.**”

### memory-eval-graph (completed, 7.2s, 4 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Migrate Relay infrastructure code f", "MATCH (d:Decision) WHERE d.text CONTAINS 'Migrate Relay infrastructure code from", "MATCH (d:Decision) WHERE d.text CONTAINS 'Terraform' AND d.text CONTAINS 'CloudF", "MATCH (d:Decision) WHERE d.text CONTAINS 'Migrate Relay from Terraform to CloudF"]

Предложил Pavel Grishin, возражал Timur Aliev — решение: “Migrate Relay from Terraform to CloudFormation module by module by the end of Q1.”  
Источник: `meetings/2026-01-12-weekly-sync.txt`, дата `2026-01-12`, статус `superseded`.

### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Migrate Relay infrastructure code f', 'Кто предложил и кто возражал против решения Migrate Relay infrastructure code fr', 'предложил и возражал против решения Migrate Relay infrastructure code from Terra']

Решение предложил **Pavel Grishin**, а возражал **Timur Aliev**.

Источники:
- `meetings/2026-01-12-weekly-sync.txt` — 2026-01-12: “Proposed by Pavel Grishin; objection from Timur Aliev.”  
- `adr/ADR-001.md` — 2026-01-14: “Objection recorded from Timur Aliev.”  
- `adr/ADR-001.md` — 2026-01-14: ADR-001 помечен как **Superseded** (устарело, superseded by ADR-004).

## t20 [en / objector] Who proposed and who objected to the decision 'Gateway integration timeout 10 s on every Relay route…'?
**expected:** proposer Pavel Grishin, objector Anna Sokolova, 2026-03-16  
**expected sources:** {'sources': ['meetings/2026-03-16-weekly-sync.txt']}

### memory-eval-both (completed, 6.5s, 3 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout 10 s on", '"Gateway integration timeout 10 s on every Relay route" proposed objected', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) WHERE d.text STARTS"]

Assumption: you mean the accepted timeout decision about Relay route integration timeouts.

I found the decision text in memory, but the graph query did not return proposer/objector links for the exact wording. From the document memory, the decision was authored by Pavel Grishin:

- Proposer: Pavel Grishin — `adr/ADR-002.md` / `docs/gateway.md`, dated `2026-03-04` and `2026-03-18`
- Objector: not in memory for this exact decision wording

Relevant source text:
- `adr/ADR-002.md` (updated `2026-03-04`): “The integration timeout on every Relay route is 10 seconds...”
- `docs/gateway.md` (updated `2026-03-18`): same timeout statement

If you want, I can also look up the decision by its exact decision node/ID and try a broader graph search for the proposer and any objector.

### memory-eval-graph (completed, 7.4s, 3 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout 10 s on", "MATCH (d:Decision) WHERE toLower(d.text) CONTAINS 'gateway integration timeout 1", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) OPTIONAL MATCH (a:P"]

I found the matching decision as: **“Set the integration timeout to 10 s for all routes.”**  
- **Proposed by:** Marat Yusupov — source: `meetings/2026-03-16-weekly-sync.txt`, date: `2026-03-16`
- **Objected by:** no objector recorded — source: `meetings/2026-03-16-weekly-sync.txt`, date: `2026-03-16`

Assumption: I matched your quoted decision to the closest decision text in memory, which is the 2026-03-16 decision about setting the integration timeout to 10 s.

### memory-eval-vector (completed, 3.2s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'Gateway integration timeout 10 s ", 'Gateway integration timeout 10 s on every Relay route proposed objected', 'gateway integration timeout 10 s every relay route decision proposer objector']

The decision was **proposed by Marat Yusupov** and **objected to by Anna Sokolova**.

Sources:
- `meetings/2026-03-16-weekly-sync.txt` — 2026-03-16: “Proposed by Marat Yusupov; objection from Anna Sokolova.”  
- `docs/gateway.md` — updated 2026-03-18: confirms the timeout decision was 10 seconds on every Relay route, decided 2026-03-16.

## t21 [ru / objector] Кто предложил и кто возражал против решения «Hybrid IaC: networking (VPC, peering, DNS) stays in Terrafor…»?
**expected:** proposer Sergey Belov, objector Pavel Grishin, 2026-04-20  
**expected sources:** {'sources': ['meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 8.6s, 4 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Hybrid IaC: networking (VPC, peerin", "MATCH (d:Decision) WHERE d.text CONTAINS 'Hybrid IaC' AND d.text CONTAINS 'netwo", '"Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform" proposed objecte', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'iac'}) WHERE d.text CONTAINS 'Hybrid "]

По памяти видно только возражение: против этого решения возражал **Павел Гришин**.

Кто предложил — **в памяти не нашёлся**.

Источник: `adr/ADR-004.md`, дата `2026-04-22`:
- “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation.”
- “Objection recorded from Pavel Grishin.”

Assumption: вы имеете в виду именно ADR-004 с этим текстом.

### memory-eval-graph (completed, 8.5s, 6 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Hybrid IaC: networking (VPC, peerin", "MATCH (d:Decision) WHERE toLower(d.text) CONTAINS 'hybrid iac' AND toLower(d.tex", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) RETURN d.text AS text, d", 'MATCH (d:Decision) RETURN d.text AS text, d.date AS date, d.source AS source WHE', "MATCH (d:Decision) WHERE d.text CONTAINS 'Hybrid IaC' RETURN d.text AS text, d.d", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:iac'}) OPTIONAL MATCH (a:Person"]

Предложил **Сергей Белов**, возражал **Павел Гришин**.  
Источник: `meetings/2026-04-20-weekly-sync.txt`, дата `2026-04-20`.

### memory-eval-vector (completed, 4.4s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Hybrid IaC: networking (VPC, peerin', 'Кто предложил и кто возражал против решения Hybrid IaC networking VPC peering DN', 'Hybrid IaC networking VPC peering DNS stays in Terraform proposed objected']

Решение **предложил Sergey Belov**; это видно в ADR-004, где само решение зафиксировано и указан автор записи **Sergey Belov**.  
**Возражал Pavel Grishin** — в том же ADR-004 прямо сказано: **“Objection recorded from Pavel Grishin.”**

Источники:
- `adr/ADR-004.md` — **2026-04-22**: решение “Hybrid IaC: networking (VPC, peering, DNS) stays in Terraform; application stacks are CloudFormation.”
- `adr/ADR-004.md` — **2026-04-22**: “Objection recorded from Pavel Grishin.”

Если хотите, могу также показать, где в памяти лежит формулировка про выбранный вариант и чем он отличается от ADR-001.

## t22 [en / objector] Who proposed and who objected to the decision 'DynamoDB single-table design, chosen on PoC-1 results (p99 r…'?
**expected:** proposer Denis Orlov, objector Timur Aliev, 2026-05-04  
**expected sources:** {'sources': ['meetings/2026-05-04-poc-review.txt']}

### memory-eval-both (completed, 3.8s, 2 tool calls)
queries: ['"DynamoDB single-table design, chosen on PoC-1 results" proposed objected', "MATCH (d:Decision) WHERE d.text STARTS WITH 'DynamoDB single-table design, chose"]

Assumption: the quoted decision is the ADR-003 decision “DynamoDB single-table design, chosen on PoC-1 results…”

Proposed by: Denis Orlov  
Objected to by: Timur Aliev

Source: `adr/ADR-003.md` — updated `2026-05-06`  
The vector memory also records the objection from Timur and the decision text there.

### memory-eval-graph (completed, 6.5s, 3 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'DynamoDB single-table design, chose", "MATCH (d:Decision) WHERE d.text CONTAINS 'DynamoDB single-table design' OPTIONAL", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'database'}) RETURN d.text, d.date, d."]

I couldn’t find that decision in memory from the text fragment you provided, so I can’t identify the proposer or objector without guessing.

What I tried:
- Searched for a decision starting with `DynamoDB single-table design, chosen on PoC-1 results (p99 r…`
- Searched for decisions containing `DynamoDB single-table design`
- Searched the `database` topic decisions

All three searches returned no rows.

If you want, I can keep looking if you give me a longer exact quote or the decision id/date.

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'DynamoDB single-table design, cho", 'Who proposed and who objected to the decision DynamoDB single-table design chose', 'DynamoDB single-table design PoC-1 results p99 read latency proposed objected']

Proposed by **Marat Yusupov** and objected by **Timur Aliev**.

Sources:
- `meetings/2026-05-04-poc-review.txt` — 2026-05-04: “Proposed by Marat Yusupov; objection from Timur Aliev.”
- `adr/ADR-003.md` — 2026-05-06: “Objection recorded from Timur Aliev.”

I also found an older related decision:
- `meetings/2026-04-06-weekly-sync.txt` — 2026-04-06: the earlier evaluation was proposed by Denis Orlov, but that is a different decision item.

## t23 [en / objector] Who proposed and who objected to the decision 'Gateway integration timeout raised from 10 s to 30 s after t…'?
**expected:** proposer Anna Sokolova, objector Lena Kim, 2026-05-18  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt']}

### memory-eval-both (completed, 2.9s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout raised ", '"Gateway integration timeout raised from 10 s to 30 s after t" proposed objected']

Assumption: the quoted decision is the timeouts decision that starts “Gateway integration timeout raised from 10 s to 30 s…”.

Proposed by: Anna Sokolova  
Objected by: Lena Kim

Source: `meetings/2026-05-18-weekly-sync.txt`  
Date: `2026-05-18`

### memory-eval-graph (completed, 7.5s, 3 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Gateway integration timeout raised ", "MATCH (d:Decision) WHERE d.text CONTAINS 'Gateway integration timeout raised fro", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:timeouts'}) OPTIONAL MATCH (a:P"]

Assuming your quoted decision is the 2026-05-18 timeout decision on the timeouts topic.

- Proposed by: Anna Sokolova — source `meetings/2026-05-18-weekly-sync.txt`, date `2026-05-18`
- Objected by: Lena Kim — source `meetings/2026-05-18-weekly-sync.txt`, date `2026-05-18`

Decision text: `The integration timeout is increased from 10 s to 30 s while synchronous mode remains enabled.`  
Source: `meetings/2026-05-18-weekly-sync.txt`, date `2026-05-18`

### memory-eval-vector (completed, 3.8s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'Gateway integration timeout raise", 'Gateway integration timeout raised from 10 s to 30 s after t… proposal objection', 'gateway integration timeout 10 s 30 s proposed objected']

The decision you mean appears to be **A30**.

- **Proposed by:** **Anna Sokolova**
- **Objected by:** **Lena Kim**

Source: **meetings/2026-05-18-weekly-sync.txt** via claim **A30**, dated **2026-05-18**.

Note: I also found an older related decision, **A13** (2026-03-16), which was superseded:
- Proposed by **Marat Yusupov**
- Objected by **Anna Sokolova**
Source: **meetings/2026-03-16-weekly-sync.txt**.

## t24 [ru / objector] Кто предложил и кто возражал против решения «Relay moves to Lambda with provisioned concurrency on /deliv…»?
**expected:** proposer Olga Petrova, objector Timur Aliev, 2026-08-03  
**expected sources:** {'sources': ['meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 3.5s, 2 tool calls)
queries: ['"Relay moves to Lambda with provisioned concurrency on /deliv" proposed objected', "MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio"]

Предложил **Марат Юсупов**, возражал **Тимур Алиев**.

Источник: `meetings/2026-08-03-architecture-committee.txt`, дата `2026-08-03`.

### memory-eval-graph (completed, 4.8s, 2 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio", "MATCH (d:Decision) WHERE d.text CONTAINS 'Relay moves to Lambda with provisioned"]

Предложил **Марат Юсупов**, возражал **Тимур Алиев**.  
Решение: **“Relay moves to Lambda with provisioned concurrency on deliver.”** — дата **2026-08-03**, статус **active**, источник **meetings/2026-08-03-architecture-committee.txt**.

### memory-eval-vector (completed, 3.9s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Relay moves to Lambda with provisio', 'Who proposed and who objected to the decision “Relay moves to Lambda with provis', 'Relay moves to Lambda with provisioned concurrency on /deliv']

Решение **«Relay moves to Lambda with provisioned concurrency on /deliver»**:

- **Предложил:** **Marat Yusupov** — источник: `meetings/2026-08-03-architecture-committee.txt` / claim A48, дата **2026-08-03**.
- **Возражал:** **Timur Aliev** — источник: `meetings/2026-08-03-architecture-committee.txt` / claim A48, дата **2026-08-03**.

Дополнительно:
- В `adr/ADR-006.md` это же решение зафиксировано как принятое; там сказано, что возражение было от **Timur Aliev** — дата **2026-08-05**.
- По найденным записям я не вижу расхождений по автору предложения и возражению.

## t25 [ru / objector] Кто предложил и кто возражал против решения «Retries move out of the gateway into SQS with a dead-letter …»?
**expected:** proposer Ivan Melnik, objector Anna Sokolova, 2026-08-24  
**expected sources:** {'sources': ['meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 5.0s, 3 tool calls)
queries: ['"Retries move out of the gateway into SQS with a dead-letter" proposed objected ', "MATCH (d:Decision) WHERE d.text STARTS WITH 'Retries move out of the gateway int", 'ADR-009 Context objection proposed Anna Ivan Melnik retries gateway SQS dead-let']

Предложил: **Ivan Melnik**; возражала: **Anna Sokolova**.

Источник: **adr/ADR-009.md**, дата **2026-08-26**.  
В тексте ADR-009 прямо сказано: “Retries move out of the gateway into SQS with a dead-letter queue…” и “Objection recorded from Anna Sokolova.”

### memory-eval-graph (completed, 7.9s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nWHERE d.text STARTS ", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nWHERE d.text CONTAIN", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nRETURN d.text AS tex", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'})\nWHERE d.text STARTS "]

Предложил Иван Мельник, возражала Анна Соколова.  
Источник: `meetings/2026-08-24-weekly-sync.txt`, дата `2026-08-24`.

Принятое решение: «Retries move to SQS with a dead letter queue after 5 attempts, and gateway retries on deliver are turned off.»

### memory-eval-vector (completed, 3.2s, 3 tool calls)
queries: ['Кто предложил и кто возражал против решения «Retries move out of the gateway int', 'Retries move out of the gateway into SQS with a dead-letter кто предложил кто во', 'Retries move out of the gateway into SQS with a dead-letter']

Предложил **Ivan Melnik**, возражала **Anna Sokolova**.

Источник: `meetings/2026-08-24-weekly-sync.txt` — 2026-08-24, в записи решения указано: “Proposed by Ivan Melnik; objection from Anna Sokolova.”  
Дополнительно это подтверждает `adr/ADR-009.md` — 2026-08-26, где сказано, что возражение было от Anna Sokolova.

## t26 [en / objector] Who proposed and who objected to the decision 'Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after t…'?
**expected:** proposer Lena Kim, objector Marat Yusupov, 2026-10-05  
**expected sources:** {'sources': ['meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 6.1s, 3 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Delivery p95 SLO relaxed from 2 s t", '"Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after" proposed objected', '"Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after"']

Assumption: you mean the later SLO decision about relaxing p95 to 3 seconds for 30 days after cutover.

- Proposed by: **Lena Kim** — source: `meetings/2026-10-05-cutover-planning.txt`, date `2026-10-05`
- Objected to by: **Marat Yusupov** — source: `meetings/2026-10-05-cutover-planning.txt`, date `2026-10-05`

The decision text in memory says: “For 30 days after cutover, p95 will be relaxed to 3 seconds, then returned to 2 seconds.”

### memory-eval-graph (completed, 6.4s, 3 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Delivery p95 SLO relaxed from 2 s t", "MATCH (d:Decision) WHERE d.text CONTAINS 'Delivery p95 SLO relaxed from 2 s to 3", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:slo'}) OPTIONAL MATCH (a:Person"]

I found the decision, but there is no recorded objector.

- Proposed by Lena Kim — source: `meetings/2026-10-05-cutover-planning.txt`, date: `2026-10-05`
- Objected by no one recorded in memory — source: `meetings/2026-10-05-cutover-planning.txt`, date: `2026-10-05`

Assumption: I matched your truncated quote to the decision text `For 30 days after cutover, p95 will be relaxed to 3 seconds, then returned to 2 seconds.`

### memory-eval-vector (completed, 2.9s, 3 tool calls)
queries: ["Who proposed and who objected to the decision 'Delivery p95 SLO relaxed from 2 s", 'Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after t…', 'Delivery p95 SLO relaxed from 2 s to 3 s for 30 days after t']

The decision was **proposed by Lena Kim** and **objected to by Marat Yusupov**.

Source: `meetings/2026-10-05-cutover-planning.txt` / claim A58, dated **2026-10-05**.

## t27 [en / aggregate] How many decisions have been superseded, and on which topics?
**expected:** 7: D01 (infrastructure as code, 2026-01-12); D02 (SLO, 2026-01-26); D06 (gateway timeout, 2026-03-16); D07 (retries, 2026-03-30); D12 (gateway timeout, 2026-05-18); D14 (retries, 2026-06-15); D15 (compute platform, 2026-06-15)  
**expected sources:** {'sources': ['meetings/2026-01-12-weekly-sync.txt', 'meetings/2026-01-26-weekly-sync.txt', 'meetings/2026-03-16-weekly-sync.txt', 'meetings/2026-03-30-weekly-sync.txt', 'meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-06-15-weekly-sync.txt']}

### memory-eval-both (completed, 4.5s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:SUPERSEDES]->(old:Decision)\nMATCH (old)-[:ABOUT]->(t:Topic)', 'MATCH (d:Decision)-[:SUPERSEDES]->(old:Decision)\nMATCH (old)-[:ABOUT]->(t:Topic)']

11 decisions have been superseded.

Topics:
- topic:iac — infrastructure as code
- topic:gateway — API gateway
- topic:timeouts — gateway timeout
- topic:compute — compute platform
- topic:retries — retries
- topic:slo — SLO

Source: graph query over Decision-[:SUPERSEDES]->Decision and their ABOUT topics.

### memory-eval-graph (completed, 4.8s, 1 tool calls)
queries: ["MATCH (d:Decision {status:'superseded'})-[:ABOUT]->(t:Topic) RETURN count(d) AS "]

11 decisions have status **superseded**. Source: `Decision` nodes in the graph, as of the decision dates in memory.

They are on these topics:
- `topic:iac` — infrastructure as code
- `topic:gateway` — API gateway
- `topic:timeouts` — gateway timeout
- `topic:retries` — retries
- `topic:compute` — compute platform
- `topic:slo` — SLO

Source: graph memory query over `Decision` → `Topic`; decision records are in their source files and dates, but the count/topic list above comes from the graph state.

### memory-eval-vector (completed, 6.2s, 3 tool calls)
queries: ['How many decisions have been superseded, and on which topics?', 'superseded decisions topics count', 'decisions marked superseded topics']

I found **7 superseded decisions** in memory, on these topics:

1. **iac** — superseded decisions on:
   - 2026-01-12, file `meetings/2026-01-12-weekly-sync.txt`
   - 2026-03-30, file `meetings/2026-03-30-weekly-sync.txt`
   - 2026-04-13, file `meetings/2026-04-13-weekly-sync.txt`

2. **gateway** — superseded decision on:
   - 2026-03-02, file `meetings/2026-03-02-weekly-sync.txt`

3. **retries** — superseded decision on:
   - 2026-06-15, file `meetings/2026-06-15-weekly-sync.txt`

4. **compute** — superseded decision on:
   - 2026-07-27, file `meetings/2026-07-27-poc-review.txt`

5. **ADR-005 / compute PoCs** — superseded ADR document:
   - updated 2026-06-17, file `adr/ADR-005.md`

Notes:
- The topic **iac** has **3** superseded decisions.
- The topic **compute** appears in **2** superseded items if you count the ADR-005 document and the later decision; otherwise, as a decision topic alone, it has **1** superseded decision.
- The retrieved hits also included some non-decision and duplicate/document entries, which I did not count as separate decisions.

Source files and dates are as listed above from the retrieved chunks.

## t28 [ru / aggregate] Какими действующими решениями владеет Anna Sokolova? Сколько их?
**expected:** 2: D13 Retries and idempotency ownership moves from Nikit; D21 Retries move out of the gateway into SQS with a de  
**expected sources:** {'sources': ['meetings/2026-06-01-weekly-sync.txt', 'meetings/2026-08-24-weekly-sync.txt']}

### memory-eval-both (completed, 4.9s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:anna-sokolova'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

Anna Sokolova currently владеет 5 действующими решениями.

Список:
1. 2026-01-19 — `Relay will keep a 60 s delivery timeout for now because there is no gateway yet.`  
   source: `meetings/2026-01-19-weekly-sync.txt`

2. 2026-06-01 — `Idempotency is handed over from Nikita to Anna starting today.`  
   source: `meetings/2026-06-01-weekly-sync.txt`

3. 2026-06-01 — `Idempotency keys are required starting today, with a two-week grace period, and all four callers must send them.`  
   source: `meetings/2026-06-01-weekly-sync.txt`

4. 2026-06-01 — `Retries are handed over from Nikita to Anna starting today.`  
   source: `meetings/2026-06-01-weekly-sync.txt`

5. 2026-08-24 — `Retries move to SQS with a dead letter queue after 5 attempts, and gateway retries on deliver are turned off.`  
   source: `meetings/2026-08-24-weekly-sync.txt`

### memory-eval-graph (completed, 7.2s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:anna-sokolova'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

Anna Sokolova владеет 5 действующими решениями. Источник: `meetings/2026-01-19-weekly-sync.txt` (2026-01-19), `meetings/2026-06-01-weekly-sync.txt` (2026-06-01), `meetings/2026-08-24-weekly-sync.txt` (2026-08-24).

Список:
- `A03` — “Relay will keep a 60 s delivery timeout for now because there is no gateway yet.” — `meetings/2026-01-19-weekly-sync.txt` — 2026-01-19
- `A33` — “Idempotency is handed over from Nikita to Anna starting today.” — `meetings/2026-06-01-weekly-sync.txt` — 2026-06-01
- `A34` — “Idempotency keys are required starting today, with a two-week grace period, and all four callers must send them.” — `meetings/2026-06-01-weekly-sync.txt` — 2026-06-01
- `A35` — “Retries are handed over from Nikita to Anna starting today.” — `meetings/2026-06-01-weekly-sync.txt` — 2026-06-01
- `A49` — “Retries move to SQS with a dead letter queue after 5 attempts, and gateway retries on deliver are turned off.” — `meetings/2026-08-24-weekly-sync.txt` — 2026-08-24

### memory-eval-vector (completed, 5.5s, 3 tool calls)
queries: ['Какими действующими решениями владеет Anna Sokolova? Сколько их?', 'Anna Sokolova ownership current decisions', 'Anna Sokolova owns open decisions current']

У Anna Sokolova есть **2 действующих решения/области владения**:

1. **idempotency** — current, с 2026-06-01  
   Source: `memory/decisions.jsonl`, 2026-06-01 (`ownership:idempotency:2026-06-01`)

2. **retries** — в памяти есть более новый активный переход владения на Anna с 2026-06-01, а более старое владение до 2026-09-07 помечено как superseded  
   Source: `meetings/2026-06-01-weekly-sync.txt`, 2026-06-01 (`A35`); более новый/решающий для текущего состояния в `meetings/2026-09-07-security-review.txt`, 2026-09-07 (`A51`) показывает, что владение retries перешло дальше, поэтому текущее владение Anna по retries **не действует**.  

Итого: **1 действующее владение** у Anna Sokolova.

Примечание: найденные источники **разнятся** по retries:  
- `memory/decisions.jsonl`, 2026-06-01 — Anna владеет retries (current)  
- `meetings/2026-09-07-security-review.txt`, 2026-09-07 — retries передано Ivan Melnik, значит это более новое решение и оно актуальнее.

## t29 [ru / aggregate] Какими действующими решениями владеет Pavel Grishin? Сколько их?
**expected:** 3: D03 One CloudFormation root stack per environment with; D05 Front Relay with the API gateway; the gateway and ; D09 Hybrid IaC: networking (VPC, peering, DNS) stays i  
**expected sources:** {'sources': ['meetings/2026-02-09-weekly-sync.txt', 'meetings/2026-03-02-weekly-sync.txt', 'meetings/2026-04-20-weekly-sync.txt']}

### memory-eval-both (completed, 6.0s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:pavel-grishin'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

Pavel Grishin владеет 6 действующими решениями.

Список:
- A02 — 2026-01-19 — `meetings/2026-01-19-weekly-sync.txt`  
  «The migration to CFN will start with compute, with data network handled last.»
- A06 — 2026-02-02 — `meetings/2026-02-02-weekly-sync.txt`  
  «The compute module was moved into a CloudFormation stack and imported without recreation, and deploys through the pipeline now work.»
- A09 — 2026-02-09 — `meetings/2026-02-09-weekly-sync.txt`  
  «Use one root stack per environment with nested stacks by component.»
- A21 — 2026-04-20 — `meetings/2026-04-20-weekly-sync.txt`  
  «Hybrid networking stays in Terraform and application stacks move to CloudFormation, with the boundary documented in an ADR.»
- A30 — 2026-05-18 — `meetings/2026-05-18-weekly-sync.txt`  
  «The integration timeout is increased from 10 s to 30 s while synchronous mode remains enabled.»
- A32 — 2026-06-01 — `meetings/2026-06-01-weekly-sync.txt`  
  «The state has been cleaned up.»

Если хотите, могу также сгруппировать их по теме или показать, какие из них уже устарели.

### memory-eval-graph (completed, 6.5s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:pavel-grishin'})-[o:OWNS]->(d:Decision) WHERE o.to I"]

У Pavel Grishin — 6 действующих решений.

1. **2026-01-19** — “The migration to CFN will start with compute, with data network handled last.”  
   source: `meetings/2026-01-19-weekly-sync.txt`

2. **2026-02-02** — “The compute module was moved into a CloudFormation stack and imported without recreation, and deploys through the pipeline now work.”  
   source: `meetings/2026-02-02-weekly-sync.txt`

3. **2026-02-09** — “Use one root stack per environment with nested stacks by component.”  
   source: `meetings/2026-02-09-weekly-sync.txt`

4. **2026-04-20** — “Hybrid networking stays in Terraform and application stacks move to CloudFormation, with the boundary documented in an ADR.”  
   source: `meetings/2026-04-20-weekly-sync.txt`

5. **2026-05-18** — “The integration timeout is increased from 10 s to 30 s while synchronous mode remains enabled.”  
   source: `meetings/2026-05-18-weekly-sync.txt`

6. **2026-06-01** — “The state has been cleaned up.”  
   source: `meetings/2026-06-01-weekly-sync.txt`

If you want, I can also group these by topic.

### memory-eval-vector (completed, 3.3s, 3 tool calls)
queries: ['Какими действующими решениями владеет Pavel Grishin? Сколько их?', 'Pavel Grishin current ownership decisions active how many', 'Pavel Grishin owns what current decisions count']

У Pavel Grishin в памяти есть 2 действующих владения:

1. **gateway** — действует с **2026-03-02**  
   Источник: `memory/decisions.jsonl`, 2026-03-02.

2. **iac** — действует с **2026-01-12**  
   Источник: `memory/decisions.jsonl`, 2026-01-12.

Итого: **2**.

Я также нашёл запись про **timeouts** от 2026-05-18, но она помечена как **superseded**, то есть это не действующее решение.  
Источник: `memory/decisions.jsonl`, 2026-05-18.

## t30 [ru / aggregate] Какими действующими решениями владеет Ivan Melnik? Сколько их?
**expected:** 5: D16 Serverless PoC ownership moves from Sergey to Ivan; D17 Relay moves to Lambda with provisioned concurrency; D20 Gateway integration timeout lowered from 30 s to 2; D22 Retries ownership moves from Anna to Ivan, who own; D25 Serverless cutover on 2026-10-19 at 09:00 local, i  
**expected sources:** {'sources': ['meetings/2026-07-13-weekly-sync.txt', 'meetings/2026-08-03-architecture-committee.txt', 'meetings/2026-08-24-weekly-sync.txt', 'meetings/2026-09-07-security-review.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 9.4s, 2 tool calls)
queries: ["MATCH (p:Person {key:'person:ivan-melnik'})-[o:OWNS]->(d:Decision)\nWHERE o.to IS", "MATCH (p:Person {key:'person:ivan-melnik'})-[o:OWNS]->(d:Decision)\nWHERE o.to IS"]

Ivan Melnik владеет 8 действующими решениями.

Действующие решения:
- 2026-06-29 — “PoC-3 should be handed over to Ivan Melnik when he joins on 2026-07-06.”  
  source: `meetings/2026-06-29-weekly-sync.txt`
- 2026-07-13 — “The cold start issue during long delivery is the main question to verify in PoC-3.”  
  source: `meetings/2026-07-13-weekly-sync.txt`
- 2026-07-13 — “Ivan will rewrite the handlers to use provisioned concurrency and SQS between intake and delivery.”  
  source: `meetings/2026-07-13-weekly-sync.txt`
- 2026-07-13 — “PoC-3 for Relay on Lambda is transferred from Sergey to Ivan.”  
  source: `meetings/2026-07-13-weekly-sync.txt`
- 2026-07-27 — “Provisioned concurrency on deliver is mandatory for Lambda to be viable.”  
  source: `meetings/2026-07-27-poc-review.txt`
- 2026-08-03 — “Relay moves to Lambda with provisioned concurrency on deliver.”  
  source: `meetings/2026-08-03-architecture-committee.txt`
- 2026-08-24 — “The gateway timeout is set to 25 seconds instead of 30 seconds.”  
  source: `meetings/2026-08-24-weekly-sync.txt`
- 2026-09-07 — “Retry ownership for the SQS pipeline is transferred from Anna to Vanya starting today.”  
  source: `meetings/2026-09-07-

### memory-eval-graph (completed, 7.5s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:ivan-melnik'})-[o:OWNS]->(d:Decision) WHERE o.to IS "]

Ivan Melnik владеет 8 действующими решениями.

- PoC-3 should be handed over to Ivan Melnik when he joins on 2026-07-06. — 2026-06-29 — `meetings/2026-06-29-weekly-sync.txt`
- The cold start issue during long delivery is the main question to verify in PoC-3. — 2026-07-13 — `meetings/2026-07-13-weekly-sync.txt`
- Ivan will rewrite the handlers to use provisioned concurrency and SQS between intake and delivery. — 2026-07-13 — `meetings/2026-07-13-weekly-sync.txt`
- PoC-3 for Relay on Lambda is transferred from Sergey to Ivan. — 2026-07-13 — `meetings/2026-07-13-weekly-sync.txt`
- Provisioned concurrency on deliver is mandatory for Lambda to be viable. — 2026-07-27 — `meetings/2026-07-27-poc-review.txt`
- Relay moves to Lambda with provisioned concurrency on deliver. — 2026-08-03 — `meetings/2026-08-03-architecture-committee.txt`
- The gateway timeout is set to 25 seconds instead of 30 seconds. — 2026-08-24 — `meetings/2026-08-24-weekly-sync.txt`
- Retry ownership for the SQS pipeline is transferred from Anna to Vanya starting today. — 2026-09-07 — `meetings/2026-09-07-security-review.txt`

Источник: действующие `OWNS`-связи от `person:ivan-melnik` к `Decision` со статусом `active`.

### memory-eval-vector (completed, 5.3s, 3 tool calls)
queries: ['Какими действующими решениями владеет Ivan Melnik? Сколько их?', 'Ivan Melnik active decisions owner current', 'Ivan Melnik owns decisions no superseded current']

У Ivan Melnik есть 4 действующих решения об ownership:

1. `retries` — с 2026-09-07, active  
   Источник: `memory/decisions.jsonl` (2026-09-07)

2. `timeouts` — с 2026-08-24, active  
   Источник: `memory/decisions.jsonl` (2026-08-24)

3. `compute` — с 2026-08-03, active  
   Источник: `memory/decisions.jsonl` (2026-08-03)

4. `ownership` — с 2026-07-06, active  
   Источник: `memory/decisions.jsonl` (2026-07-06)

Итого: 4.

Примечание: я также нашёл более раннее решение в `meetings/2026-06-29-weekly-sync.txt` от 2026-06-29 про передачу PoC-3 Ivan Melnik, но оно относится к тому же topic `ownership` и не добавляет отдельного действующего решения.

## t31 [ru / aggregate] Какими действующими решениями владеет Lena Kim? Сколько их?
**expected:** 3: D04 Manual console changes are frozen; nightly drift d; D27 Rollback owner for both cutovers is Lena; D28 Delivery p95 SLO relaxed from 2 s to 3 s for 30 da  
**expected sources:** {'sources': ['meetings/2026-02-23-incident-review.txt', 'meetings/2026-10-05-cutover-planning.txt']}

### memory-eval-both (completed, 8.0s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:lena-kim'})-[o:OWNS]->(d:Decision) WHERE o.to IS NUL"]

Lena Kim владеет 7 действующими решениями.

Вот они:
- 2026-01-26 — `The team set the SLOs to p95 end-to-end latency of 2 s over a 5-minute window and a monthly delivery success rate of 99.5%.`  
  source: `meetings/2026-01-26-weekly-sync.txt`
- 2026-02-02 — `Enable drift detection immediately on the new stack.`  
  source: `meetings/2026-02-02-weekly-sync.txt`
- 2026-02-23 — `Nightly drift detection will run on all stacks with alerts.`  
  source: `meetings/2026-02-23-incident-review.txt`
- 2026-02-23 — `Manual changes in production are forbidden.`  
  source: `meetings/2026-02-23-incident-review.txt`
- 2026-05-11 — `The gateway will keep a 10 s limit, even though slow clients may hold delivery longer and receive 504 responses.`  
  source: `meetings/2026-05-11-weekly-sync.txt`
- 2026-09-21 — `The rollback runbook will be owned by Lena and written by the end of the week.`  
  source: `meetings/2026-09-21-weekly-sync.txt`
- 2026-10-05 — `Rollback for both cutovers is assigned to Lena, and Vanya will update the runbook.`  
  source: `meetings/2026-10-05-cutover-planning.txt`

Assumption: “действующие решения” = active decisions with an open OWNS edge to Lena.

### memory-eval-graph (completed, 7.3s, 1 tool calls)
queries: ["MATCH (:Person {key:'person:lena-kim'})-[o:OWNS]->(d:Decision) WHERE o.to IS NUL"]

Lena Kim владеет 7 действующими решениями.

- 2026-01-26, `meetings/2026-01-26-weekly-sync.txt`: “The team set the SLOs to p95 end-to-end latency of 2 s over a 5-minute window and a monthly delivery success rate of 99.5%.”
- 2026-02-02, `meetings/2026-02-02-weekly-sync.txt`: “Enable drift detection immediately on the new stack.”
- 2026-02-23, `meetings/2026-02-23-incident-review.txt`: “Nightly drift detection will run on all stacks with alerts.”
- 2026-02-23, `meetings/2026-02-23-incident-review.txt`: “Manual changes in production are forbidden.”
- 2026-05-11, `meetings/2026-05-11-weekly-sync.txt`: “The gateway will keep a 10 s limit, even though slow clients may hold delivery longer and receive 504 responses.”
- 2026-09-21, `meetings/2026-09-21-weekly-sync.txt`: “The rollback runbook will be owned by Lena and written by the end of the week.”
- 2026-10-05, `meetings/2026-10-05-cutover-planning.txt`: “Rollback for both cutovers is assigned to Lena, and Vanya will update the runbook.”

Источник: `OWNS`-связи от `person:lena-kim` к активным решениям; дата — дата каждого решения.

### memory-eval-vector (completed, 6.3s, 3 tool calls)
queries: ['Какими действующими решениями владеет Lena Kim? Сколько их?', 'Lena Kim owns active decisions count', 'Lena Kim current ownership decisions']

В памяти есть 5 действующих решений, которыми владеет Lena Kim:

1. **cutover** — Lena Kim owns cutover from **2026-09-21** (current)  
   Источник: `memory/decisions.jsonl` / `meetings/2026-09-21-weekly-sync.txt`, **2026-09-21**

2. **cutover** — Rollback for both cutovers is assigned to Lena  
   Источник: `meetings/2026-10-05-cutover-planning.txt`, **2026-10-05**

3. **security** — Manual changes in production are forbidden  
   Источник: `meetings/2026-02-23-incident-review.txt`, **2026-02-23**

4. **iac** — Nightly drift detection will run on all stacks with alerts  
   Источник: `meetings/2026-02-23-incident-review.txt`, **2026-02-23**

5. **gateway** — The gateway will keep a 10 s limit  
   Источник: `meetings/2026-05-11-weekly-sync.txt`, **2026-05-11**

Итого: **5**.

Примечание: по `cutover` в памяти есть несколько записей; самая новая — от **2026-10-05**, она дополняет более раннюю запись от **2026-09-21**.

## t32 [en / aggregate] Which ADRs are not Accepted, and what is their status?
**expected:** Superseded: ADR-001, ADR-005; Rejected: ADR-007; Proposed: ADR-010  
**expected sources:** {'sources': ['adr/ADR-001.md', 'adr/ADR-005.md', 'adr/ADR-007.md', 'adr/ADR-010.md']}

### memory-eval-both (completed, 4.5s, 1 tool calls)
queries: ["MATCH (a:ADR) WHERE a.status <> 'Accepted' RETURN a.id, a.title, a.status, a.fil"]

The ADRs that are not Accepted are:

- ADR-001 — Superseded — “Migrate infrastructure code from Terraform to CloudFormation” — source: `adr/ADR-001.md`
- ADR-005 — Superseded — “Evaluate EKS and Lambda with two proofs of concept” — source: `adr/ADR-005.md`
- ADR-007 — Rejected — “Keep Relay on EKS with autoscaling” — source: `adr/ADR-007.md`
- ADR-010 — Proposed — “Gateway timeout policy for Lambda integrations” — source: `adr/ADR-010.md`

Query date: current memory state.

### memory-eval-graph (completed, 3.2s, 1 tool calls)
queries: ["MATCH (a:ADR) WHERE a.status <> 'Accepted' RETURN a.id, a.title, a.status, a.fil"]

The ADRs that are not Accepted are:

- ADR-001 — status: Superseded — source: `adr/ADR-001.md`
- ADR-005 — status: Superseded — source: `adr/ADR-005.md`
- ADR-007 — status: Rejected — source: `adr/ADR-007.md`
- ADR-010 — status: Proposed — source: `adr/ADR-010.md`

I used the ADR records as stored in memory.

### memory-eval-vector (completed, 4.9s, 3 tool calls)
queries: ['Which ADRs are not Accepted, and what is their status?', 'ADRs not Accepted status', 'accepted ADR status rejected proposed superseded']

From memory, the ADRs that are **not Accepted** are:

- **ADR-005: Evaluate EKS and Lambda with two proofs of concept** — **Superseded (superseded by ADR-006)**. Source: `adr/ADR-005.md`, updated **2026-06-17**.
- **ADR-007: Keep Relay on EKS with autoscaling** — **Rejected**. Source: `adr/ADR-007.md`, updated **2026-08-05**.
- **ADR-010: Gateway timeout policy for Lambda integrations** — **Proposed**. Source: `adr/ADR-010.md`, updated **2026-09-23**.

Notes:
- I also retrieved **ADR-002**, **ADR-004**, **ADR-006**, and **ADR-008**, but they are **Accepted** and therefore not included above.
- The retrieved chunks for **ADR-010** agree that it is **Proposed / not accepted**. Source: `adr/ADR-010.md`, updated **2026-09-23**.

If you want, I can also list the ADRs with their full decision dates and whether any are superseded by others.

## t33 [ru / unowned_at] Какие открытые вопросы были без владельца на 2026-06-15?
**expected:** O1 DynamoDB migration dry run on a production snapshot (raised 2026-05-04); O4 DocumentDB decommission date (raised 2026-05-18)  
**expected sources:** {'sources': ['meetings/2026-05-04-poc-review.txt', 'meetings/2026-05-18-weekly-sync.txt']}

### memory-eval-both (completed, 13.9s, 1 tool calls)
queries: ["MATCH (o:OpenItem) WHERE o.raised <= '2026-06-15' AND NOT EXISTS { MATCH (o)<-[w"]

На 2026-06-15 без владельца были такие открытые вопросы:

- Q1 — “Review timeout behavior for slow endpoints and queue growth.”  
  raised: 2026-01-19; raised_again: []; status: open

- Q2 — “Add cost center tags to all resources starting this quarter.”  
  raised: 2026-01-26; raised_again: []; status: open

- Q3 — “Enable drift detection on the new stack.”  
  raised: 2026-02-02; raised_again: []; status: open

- Q4 — “The DocumentDB read p99 is 9 ms at peak and keeps growing every month.”  
  raised: 2026-02-02; raised_again: []; status: open

- Q5 — “The queue of undelivered messages is not decreasing.”  
  raised: 2026-02-02; raised_again: []; status: open

- Q6 — “Set up an alert routing path into on-call because current alerts go to a channel nobody reads.”  
  raised: 2026-02-23; raised_again: []; status: open

- Q7 — “Gateway retries cannot be enabled yet.”  
  raised: 2026-03-16; raised_again: []; status: open

- Q9 — “Start the database work in April.”  
  raised: 2026-03-23; raised_again: []; status: open

- Q10 — “Define a retry budget so enabling retries does not cause a storm.”  
  raised: 2026-03-30; raised_again: []; status: open

- Q11 — “Assess DynamoDB for poc-1 

### memory-eval-graph (completed, 30.9s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На 2026-06-15 без владельца были такие открытые вопросы.

- Q1 — «Review timeout behavior for slow endpoints and queue growth.»  
  raised: 2026-01-19; raised_again: []; status: open  
  source: **not in the graph as a separate file**; дата вопроса: 2026-01-19

- Q2 — «Add cost center tags to all resources starting this quarter.»  
  raised: 2026-01-26; raised_again: []; status: open  
  source: **not in the graph as a separate file**; дата вопроса: 2026-01-26

- Q3 — «Enable drift detection on the new stack.»  
  raised: 2026-02-02; raised_again: []; status: open  
  source: **not in the graph as a separate file**; дата вопроса: 2026-02-02

- Q4 — «The DocumentDB read p99 is 9 ms at peak and keeps growing every month.»  
  raised: 2026-02-02; raised_again: []; status: open  
  source: **not in the graph as a separate file**; дата вопроса: 2026-02-02

- Q5 — «The queue of undelivered messages is not decreasing.»  
  raised: 2026-02-02; raised_again: []; status: open  
  source: **not in the graph as a separate file**; дата вопроса: 2026-02-02

- Q6 — «Set up an alert routing path into on-call because current alerts go to a channel nobody reads.»  
  raised: 2026-02-23; raised_again

### memory-eval-vector (completed, 6.9s, 3 tool calls)
queries: ['Какие открытые вопросы были без владельца на 2026-06-15?', 'open items with no owner as of 2026-06-15', 'вопросы без владельца 2026-06-15 открытые']

На **2026-06-15** в памяти есть один явно найденный открытый вопрос **без владельца**:

- **dry run** — «знаю без владельца», на встрече **Relay weekly sync 2026-06-15**. Источник: `meetings/2026-06-15-weekly-sync.txt`, дата **2026-06-15**.

Что я ещё извлёк, но это не ответ именно на дату 2026-06-15:
- `meetings/2026-05-04-poc-review.txt` — open item по **database**, без владельца, дата **2026-05-04**
- `meetings/2026-05-18-weekly-sync.txt` — open item по **database**, но статус там `closed`, дата **2026-05-18**
- `meetings/2026-06-29-weekly-sync.txt` — open item по **compute**, дата **2026-06-29**
- более поздние open items в `meetings/2026-07-06-weekly-sync.txt`, `meetings/2026-08-17-weekly-sync.txt`, `meetings/2026-09-14-weekly-sync.txt`, `meetings/2026-09-28-weekly-sync.txt`, `meetings/2026-10-05-cutover-planning.txt`

Если хотите, я могу следующим сообщением собрать **полный список всех open items без владельца, которые были известны на 2026-06-15**, с учётом только тех, что уже существовали к этой дате.

## t34 [ru / unowned_at] Какие открытые вопросы были без владельца на 2026-08-17?
**expected:** O3 Load test on Lambda at 10x current volume (raised 2026-07-27); O4 DocumentDB decommission date (raised 2026-05-18)  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-07-27-poc-review.txt']}

### memory-eval-both (completed, 52.7s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На 2026-08-17 без владельца были следующие открытые вопросы.

Считаю владельцем только явный `OWNS`; где такого ребра не было, вопрос считается без владельца.

- **Q1** — “Review timeout behavior for slow endpoints and queue growth.”  
  raised: 2026-01-19, raised_again: []  
  source: `graph` / дата вопроса: 2026-01-19

- **Q2** — “Add cost center tags to all resources starting this quarter.”  
  raised: 2026-01-26, raised_again: []  
  source: `graph` / дата вопроса: 2026-01-26

- **Q3** — “Enable drift detection on the new stack.”  
  raised: 2026-02-02, raised_again: []  
  source: `graph` / дата вопроса: 2026-02-02

- **Q4** — “The DocumentDB read p99 is 9 ms at peak and keeps growing every month.”  
  raised: 2026-02-02, raised_again: []  
  source: `graph` / дата вопроса: 2026-02-02

- **Q5** — “The queue of undelivered messages is not decreasing.”  
  raised: 2026-02-02, raised_again: []  
  source: `graph` / дата вопроса: 2026-02-02

- **Q6** — “Set up an alert routing path into on-call because current alerts go to a channel nobody reads.”  
  raised: 2026-02-23, raised_again: []  
  source: `graph` / дата вопроса: 2026-02-23

- **Q7** — “Gateway retries cannot be enabled 

### memory-eval-graph (completed, 32.6s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

На **2026-08-17** без владельца были такие открытые вопросы:

- **Q1** — «Review timeout behavior for slow endpoints and queue growth.» — raised **2026-01-19**; raised_again: **[]**; status: **open**.  
- **Q2** — «Add cost center tags to all resources starting this quarter.» — raised **2026-01-26**; raised_again: **[]**; status: **open**.  
- **Q3** — «Enable drift detection on the new stack.» — raised **2026-02-02**; raised_again: **[]**; status: **open**.  
- **Q4** — «The DocumentDB read p99 is 9 ms at peak and keeps growing every month.» — raised **2026-02-02**; raised_again: **[]**; status: **open**.  
- **Q5** — «The queue of undelivered messages is not decreasing.» — raised **2026-02-02**; raised_again: **[]**; status: **open**.  
- **Q6** — «Set up an alert routing path into on-call because current alerts go to a channel nobody reads.» — raised **2026-02-23**; raised_again: **[]**; status: **open**.  
- **Q7** — «Gateway retries cannot be enabled yet.» — raised **2026-03-16**; raised_again: **[]**; status: **open**.  
- **Q9** — «Start the database work in April.» — raised **2026-03-23**; raised_again: **[]**; status: **open**.  
- **Q10** — «Define a retry budget so enabl

### memory-eval-vector (completed, 5.7s, 3 tool calls)
queries: ['Какие открытые вопросы были без владельца на 2026-08-17?', 'What open items were without an owner on 2026-08-17?', 'open items no owner as of 2026-08-17']

На 2026-08-17 в памяти есть один открытый вопрос без владельца:

- **Load test at 10x has not been taken by anyone yet** — raised **2026-08-17**, **no owner**. Источник: `meetings/2026-08-17-weekly-sync.txt` (claim Q29, дата 2026-08-17).

Также в памяти есть более ранние и более поздние open items без владельца, но они не на 2026-08-17:
- **The dry run migration item remains open without an owner** — `meetings/2026-05-04-poc-review.txt` (2026-05-04)
- **оформим передачу** — `meetings/2026-07-06-weekly-sync.txt` (2026-07-06)
- другие, но они датированы позже 2026-08-17.

## t35 [en / unowned_at] Which open items had no owner on 2026-10-05?
**expected:** O3 Load test on Lambda at 10x current volume (raised 2026-07-27); O4 DocumentDB decommission date (raised 2026-05-18); O7 Rotate DocumentDB credentials before decommission (raised 2026-09-07)  
**expected sources:** {'sources': ['meetings/2026-05-18-weekly-sync.txt', 'meetings/2026-07-27-poc-review.txt', 'meetings/2026-09-07-security-review.txt']}

### memory-eval-both (completed, 32.3s, 1 tool calls)
queries: ["MATCH (o:OpenItem) WHERE o.raised <= '2026-10-05' AND NOT EXISTS { MATCH (o)<-[w"]

Assumption: “no owner on 2026-10-05” means open items raised on or before 2026-10-05 with no OWNS edge active by that date and not already closed.

- Q1 — “Review timeout behavior for slow endpoints and queue growth.” — raised 2026-01-19 — no owner
- Q2 — “Add cost center tags to all resources starting this quarter.” — raised 2026-01-26 — no owner
- Q3 — “Enable drift detection on the new stack.” — raised 2026-02-02 — no owner
- Q4 — “The DocumentDB read p99 is 9 ms at peak and keeps growing every month.” — raised 2026-02-02 — no owner
- Q5 — “The queue of undelivered messages is not decreasing.” — raised 2026-02-02 — no owner
- Q6 — “Set up an alert routing path into on-call because current alerts go to a channel nobody reads.” — raised 2026-02-23 — no owner
- Q7 — “Gateway retries cannot be enabled yet.” — raised 2026-03-16 — no owner
- Q9 — “Start the database work in April.” — raised 2026-03-23 — no owner
- Q10 — “Define a retry budget so enabling retries does not cause a storm.” — raised 2026-03-30 — no owner
- Q11 — “Assess DynamoDB for poc-1 by comparing single-table vs multi-table on real access patterns and report p99 read latency, cost at projected volume, and query compl

### memory-eval-graph (completed, 35.7s, 1 tool calls)
queries: ['MATCH (o:OpenItem) WHERE o.raised <= $D AND NOT EXISTS { MATCH (o)<-[w:OWNS]-() ']

On 2026-10-05, these open items had no owner.

Source: memory graph query on open items unowned as of 2026-10-05.

- Q1 — “Review timeout behavior for slow endpoints and queue growth.” — raised 2026-01-19; raised_again []; status open
- Q10 — “Define a retry budget so enabling retries does not cause a storm.” — raised 2026-03-30; raised_again []; status open
- Q11 — “Assess DynamoDB for poc-1 by comparing single-table vs multi-table on real access patterns and report p99 read latency, cost at projected volume, and query complexity.” — raised 2026-04-06; raised_again []; status open
- Q12 — “Bring numbers for the network migration decision next week.” — raised 2026-04-13; raised_again []; status open
- Q17 — “Decide the synchronous mode question at the next meeting.” — raised 2026-05-11; raised_again []; status open
- Q19 — “Decide when to turn off DocumentDB after migration.” — raised 2026-05-18; raised_again []; status open
- Q2 — “Add cost center tags to all resources starting this quarter.” — raised 2026-01-26; raised_again []; status open
- Q20 — “Compare EKS with autoscaling versus Lambda for relay delivery workloads and decide by the end of July.” — raised 2026-06-15; raised_

### memory-eval-vector (completed, 8.7s, 3 tool calls)
queries: ['Which open items had no owner on 2026-10-05?', 'open items no owner 2026-10-05', 'items with no owner raised on 2026-10-05']

On 2026-10-05, the open items with no owner in memory were:

- **cutover** — “Rollback details are TBD in the runbook.”  
  Source: `meetings/2026-10-05-cutover-planning.txt` (2026-10-05), claim Q38
- **security** — “Rotate credentials before decommission.”  
  Source: `meetings/2026-10-05-cutover-planning.txt` (2026-10-05), claim Q40

I also retrieved older open/no-owner items, but they are earlier than 2026-10-05 and therefore not the set for that date:
- **database** — `meetings/2026-05-04-poc-review.txt` (2026-05-04), claim Q16
- **ownership** — `meetings/2026-07-06-weekly-sync.txt` (2026-07-06), claim Q23
- **retries** — `meetings/2026-02-02-weekly-sync.txt` (2026-02-02), claim Q5
- **compute** — `meetings/2026-08-17-weekly-sync.txt` and `meetings/2026-06-29-weekly-sync.txt`, claims Q29 and Q22
- **cutover** — `meetings/2026-09-14-weekly-sync.txt` and `meetings/2026-09-28-weekly-sync.txt`, claims Q33 and Q37
- **security** — `meetings/2026-09-28-weekly-sync.txt` (2026-09-28), claim Q36

If you want, I can also list only the items that were open and unowned **as of** 2026-10-05, including those raised earlier and still open then.

## t36 [en / stale_docs] Which documents were out of date on 2026-07-01, and why?
**expected:** docs/iac-cloudformation.md (updated 2026-02-11): says all infrastructure including networking moves to CloudFormation, changed by D09 on 2026-04-20; docs/gateway.md (updated 2026-03-18): says the integration timeout is 10 s, changed by D12 on 2026-05-18; docs/gateway.md (updated 2026-03-18): says retries are disabled on /deliver, changed by D14 on 2026-06-15; docs/onboarding.md (updated 2026-03-10): lists Nikita as retries owner and does not list Sergey or Ivan, changed by D13 on 2026-06-01; confluence/architecture.xhtml (updated 2026-03-12): shows DocumentDB, changed by D10 on 2026-05-04; confluence/decision-log.xhtml (updated 2026-06-03): stops at 2026-06-01, changed by D14 on 2026-06-15  
**expected sources:** {'sources': ['confluence/architecture.xhtml', 'confluence/decision-log.xhtml', 'docs/gateway.md', 'docs/iac-cloudformation.md', 'docs/onboarding.md']}

### memory-eval-both (completed, 9.1s, 3 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ', 'MATCH (doc:Document) WHERE doc.updated <= $D AND EXISTS { MATCH (dec:Decision)-[', 'documents out of date on 2026-07-01 stale updated decision changed fact']

I couldn’t find any documents marked stale on or before 2026-07-01 in the graph, so I don’t have a memory-backed list of out-of-date documents for that date.

What I checked:
- Graph stale-document query for decisions making documents stale on 2026-07-01 returned no rows.
- I also checked for decisions after each document’s update date that would make them stale, and that also returned no rows.

Assumption: “out of date on 2026-07-01” means stale as of that date, using document update dates versus later decisions.

One related document in memory is:
- `docs/db-migration-plan.md` — updated 2026-05-26, but no staleness edge was found on 2026-07-01.
- `confluence/decision-log.xhtml` — updated 2026-06-03, likewise no stale edge was found on 2026-07-01.

If you want, I can do a broader search for documents whose content appears contradicted by later decisions, even if the explicit stale edge isn’t present in the graph.

### memory-eval-graph (completed, 7.7s, 4 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ', 'MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) RETURN doc.file AS file, do', 'MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE dec.date > doc.update', 'MATCH (doc:Document) WHERE EXISTS { MATCH (dec:Decision)-[:MAKES_STALE]->(doc) W']

No documents were out of date on 2026-07-01.

Source: I checked all `MAKES_STALE` links against decisions dated after each document’s `updated` date and up to 2026-07-01, and the graph returned no matching documents.

### memory-eval-vector (completed, 8.3s, 3 tool calls)
queries: ['Which documents were out of date on 2026-07-01, and why?', 'documents out of date on 2026-07-01 why', 'out of date documents 2026-07-01 date why document updated decision newer stale']

Not in memory for a complete list of documents that were out of date on **2026-07-01**.

What I did retrieve:
- **docs/secrets.md** — updated **2026-09-10**; it says the DocumentDB credentials rotation was **overdue** because the last rotation was **January 2026** and they had to be rotated before decommission. Source: `docs/secrets.md` (**2026-09-10**).
- **docs/db-migration-plan.md** — updated **2026-05-26**; it says the DocumentDB decommission had **no date**. Source: `docs/db-migration-plan.md` (**2026-05-26**).
- **docs/documentdb-runbook.md** — updated **2026-02-02**; it says application credentials were last rotated in **January 2026**. Source: `docs/documentdb-runbook.md` (**2026-02-02**).

I also retrieved open items from meetings about DocumentDB decommission timing and credentials rotation:
- `meetings/2026-08-10-weekly-sync.txt` (**2026-08-10**) — date of DocumentDB decommission remained open and was after cutover.
- `meetings/2026-09-07-security-review.txt` (**2026-09-07**) — rotate DocumentDB credentials before decommission.
- `meetings/2026-09-28-weekly-sync.txt` (**2026-09-28**) — credential rotation for the document DB was still unowned.
- `meetings/2026-10-05-cuto

## t37 [en / stale_docs] Which documents were out of date on 2026-10-05, and why?
**expected:** docs/iac-cloudformation.md (updated 2026-02-11): says all infrastructure including networking moves to CloudFormation, changed by D09 on 2026-04-20; docs/gateway.md (updated 2026-03-18): says the integration timeout is 10 s, changed by D12 on 2026-05-18; docs/gateway.md (updated 2026-03-18): says retries are disabled on /deliver, changed by D14 on 2026-06-15; docs/gateway.md (updated 2026-03-18): describes gateway retries at all, changed by D21 on 2026-08-24; docs/slo.md (updated 2026-01-28): says p95 2 s with no stabilisation window, changed by D28 on 2026-10-05; docs/documentdb-runbook.md (updated 2026-02-02): describes DocumentDB as the system of record, changed by D26 on 2026-10-05; docs/db-migration-plan.md (updated 2026-05-26): says the dry run has no owner, changed by D19 on 2026-08-10; docs/db-migration-plan.md (updated 2026-05-26): has no cutover date, changed by D26 on 2026-10-05; docs/runbook-cutover-serverless.md (updated 2026-09-29): says rollback owner TBD, changed by D27 on 2026-10-05; docs/runbook-cutover-serverless.md (updated 2026-09-29): has no cutover date, changed by D25 on 2026-10-05; docs/onboarding.md (updated 2026-03-10): lists Nikita as retries owner and does not list Sergey or Ivan, changed by D13 on 2026-06-01; confluence/architecture.xhtml (updated 2026-03-12): shows EKS as the runtime, changed by D17 on 2026-08-03; confluence/architecture.xhtml (updated 2026-03-12): shows DocumentDB, changed by D10 on 2026-05-04; confluence/decision-log.xhtml (updated 2026-06-03): stops at 2026-06-01, changed by D14 on 2026-06-15; confluence/team-roster.xhtml (updated 2026-07-08): lists Anna as retries owner, changed by D22 on 2026-09-07; confluence/migration-roadmap.xhtml (updated 2026-06-20): lists compute decision as pending PoC, changed by D17 on 2026-08-03  
**expected sources:** {'sources': ['confluence/architecture.xhtml', 'confluence/decision-log.xhtml', 'confluence/migration-roadmap.xhtml', 'confluence/team-roster.xhtml', 'docs/db-migration-plan.md', 'docs/documentdb-runbook.md', 'docs/gateway.md', 'docs/iac-cloudformation.md', 'docs/onboarding.md', 'docs/runbook-cutover-serverless.md', 'docs/slo.md']}

### memory-eval-both (completed, 23.5s, 3 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ', 'MATCH (doc:Document) WHERE doc.updated <= $D OPTIONAL MATCH (dec:Decision)-[s:MA', 'out of date documents 2026-10-05 stale why decisions changed facts document upda']

Assumption: “out of date” means stale relative to decisions dated on or before 2026-10-05, i.e. the document’s `updated` date is earlier than a later decision that changed a fact it contains.

From the graph, the repository has these documents marked stale by later decisions on or before 2026-10-05:

- `confluence/architecture.xhtml` — updated 2026-03-12. I couldn’t recover the stale-fact edge details from the graph query, so I can only confirm it is considered stale.
- `confluence/decision-log.xhtml` — updated 2026-06-03. Stale.
- `confluence/migration-roadmap.xhtml` — updated 2026-06-20. Stale.
- `confluence/team-roster.xhtml` — updated 2026-07-08. Stale.
- `docs/cost-model.md` — updated 2026-09-23. Stale.
- `docs/db-migration-plan.md` — updated 2026-05-26. Stale.
- `docs/documentdb-runbook.md` — updated 2026-02-02. Stale.
- `docs/drift-detection.md` — updated 2026-02-25. Stale.
- `docs/dynamodb-data-model.md` — updated 2026-05-12. Stale.
- `docs/gateway-auth.md` — updated 2026-03-25. Stale.
- `docs/gateway.md` — updated 2026-03-18. Stale.
- `docs/iac-cloudformation.md` — updated 2026-02-11. Stale.
- `docs/iac-hybrid.md` — updated 2026-04-24. Stale.
- `docs/idempotency.md` — upda

### memory-eval-graph (completed, 4.5s, 2 tool calls)
queries: ['MATCH (dec:Decision)-[s:MAKES_STALE]->(doc:Document) WHERE s.since <= $D RETURN ', 'MATCH (doc:Document) WHERE doc.updated <= $D AND EXISTS { MATCH (dec:Decision)-[']

On 2026-10-05, I found no documents that were out of date in memory.

What I checked:
- documents made stale by later decisions with `MAKES_STALE` effective by 2026-10-05
- documents with a later decision date after `doc.updated` and on or before 2026-10-05

Result:
- none returned

Source:
- memory graph, checked against document `updated` dates and decision dates on 2026-10-05

### memory-eval-vector (completed, 13.4s, 3 tool calls)
queries: ['Which documents were out of date on 2026-10-05, and why?', 'documents out of date on 2026-10-05 why', 'out of date documents 2026-10-05 stale superseded updated date']

I found a few documents/items that were out of date by 2026-10-05, but the memory does not contain a full inventory of all documents to check. So this is **not a complete list**; it’s what I retrieved.

### Retrieved as out of date / stale

1. **`docs/secrets.md` — “Secrets handling”**  
   - **Updated:** 2026-09-10  
   - **Why out of date:** it says `/relay/prod/docdb/credentials` was **“overdue”**, last rotated in January 2026, and must be rotated **before DocumentDB decommission**.  
   - **Source:** `docs/secrets.md` (updated 2026-09-10)

2. **`docs/db-migration-plan.md` — “DocumentDB to DynamoDB migration plan”**  
   - **Updated:** 2026-05-26  
   - **Why out of date:** the document says **DocumentDB decommission has no date** and that credentials must be rotated before decommission. On 2026-10-05, a meeting record still shows the decommission date as open/TBD, so the document remains incomplete/stale on that point.  
   - **Source:** `docs/db-migration-plan.md` (updated 2026-05-26)  
   - **Supporting newer source:** `meetings/2026-10-05-cutover-planning.txt` (2026-10-05), which records that the DocumentDB decommission date is still open.

### Related open items on 2026-10-

## t38 [ru / poc_basis] На каком PoC и на каких цифрах основано решение «DynamoDB single-table design, chosen on PoC-1 results (p99 r…»?
**expected:** PoC-1: DynamoDB single-table vs multi-table: {"single_table_p99_read_ms": 4, "multi_table_p99_read_ms": 11, "single_table_cost_delta_pct": -38, "documentdb_p99_read_ms": 9}; report docs/poc-dynamodb-report.md  
**expected sources:** {'sources': ['docs/poc-dynamodb-report.md', 'meetings/2026-05-04-poc-review.txt']}

### memory-eval-both (completed, 3.9s, 2 tool calls)
queries: ['"DynamoDB single-table design, chosen on PoC-1 results" p99 r', "MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'DynamoDB singl"]

Основано на PoC-1, то есть на сравнении DynamoDB single-table vs multi-table.

Цифры из отчёта PoC-1:
- read p99: 4 ms у single-table против 11 ms у multi-table
- cost at projected volume: на 38% ниже, чем у DocumentDB
- в отчёте также указано, что single-table обходит baseline DocumentDB по read p99: 4 ms vs 9 ms

Источник: `docs/poc-dynamodb-report.md`, 2026-05-01.  
В самом ADR это сформулировано так же: `ADR-003: Replace DocumentDB with DynamoDB using a single-table design`, дата 2026-05-06, status Accepted.

### memory-eval-graph (completed, 12.5s, 5 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(p:PoC) WHERE d.text STARTS WITH 'DynamoDB singl", "MATCH (d:Decision)-[:BASED_ON]->(p:PoC) WHERE d.text CONTAINS 'DynamoDB single-t", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:database'}) WHERE d.text CONTAI", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:database'}) WHERE d.text CONTAI", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:database'})-[:OWNS]-(p:Person) "]

Решение основано на PoC-1 — **“DynamoDB single-table vs multi-table”**; источник: `meetings/2026-05-04-poc-review.txt`, дата решения: `2026-05-04`.

Цифры из PoC:
- набор данных: **90 days of production-shaped deliveries**
- объём: **14,000,000 items**
- нагрузка: **six Relay access patterns at 1x and 3x current volume**
- `documentdb_read_p99`: **9 ms**
- `documentdb_write_p99`: **14 ms**
- `documentdb_monthly_cost`: **$5,200**
- `dynamodb_multi_table_read_p99`: **11 ms**
- `dynamodb_multi_table_write_p99`: **9 ms**
- `dynamodb_multi_table_monthly_cost`: **$5,100**
- `dynamodb_single_table_read_p99`: **4 ms**
- `dynamodb_single_table_write_p99`: **8 ms**
- `dynamodb_single_table_monthly_cost`: **$3,200 (-38%)**

Само решение: **“Adopt DynamoDB single-table for Relay.”**
Источник: `meetings/2026-05-04-poc-review.txt`, дата: `2026-05-04`.

Если хотите, я могу ещё показать, какая именно формулировка в решении ссылается на PoC-1.

### memory-eval-vector (completed, 6.5s, 3 tool calls)
queries: ['На каком PoC и на каких цифрах основано решение «DynamoDB single-table design, c', 'DynamoDB single-table design, chosen on PoC-1 results p99 r', 'single-table design chosen on PoC-1 results p99']

Решение основано на **PoC-1** — в документе указано, что это **DynamoDB single-table vs multi-table** на production-shaped dataset. Источник: **`docs/poc-dynamodb-report.md`**, дата **2026-05-01**.

Цифры, на которых оно основано:
- **Read p99:** single-table **4 ms** vs multi-table **11 ms**
- **Cost at projected volume:** single-table **$3,200**, что на **38% ниже**
- Дополнительно в PoC-1 report указано, что baseline DocumentDB был **9 ms** read p99 и **$5,200**/month  
Источник: **`docs/poc-dynamodb-report.md`**, дата **2026-05-01**.

Само решение зафиксировано в ADR:
- **`adr/ADR-003.md`**, дата **2026-05-06**: “DynamoDB single-table design, chosen on PoC-1 results (p99 read 4 ms vs 11 ms; 38% lower cost at projected volume).”

Если хотите, могу ещё вытащить точный фрагмент про период PoC-1, датасет и нагрузку.

## t39 [ru / poc_basis] На каком PoC и на каких цифрах основано решение «Relay moves to Lambda with provisioned concurrency on /deliv…»?
**expected:** PoC-3: Relay on Lambda: {"p95_warm_s": 1.9, "p95_cold_s": 3.4, "cold_start_s": 1.2, "monthly_cost_usd": 3600, "cost_delta_vs_eks_pct": -41}; report docs/poc-lambda-report.md  
**expected sources:** {'sources': ['docs/poc-lambda-report.md', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 6.9s, 3 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio", '"Relay moves to Lambda with provisioned concurrency on /deliv" PoC цифры results', '"Relay moves to Lambda with provisioned concurrency on /deliv" PoC numbers metri']

Решение **«Relay moves to Lambda with provisioned concurrency on /deliver»** основано на **PoC-3** — *Relay on Lambda*.

Цифры из отчёта PoC-3:
- **p95 latency с provisioned concurrency на `/deliver` — 1.9 s**
- **p95 latency без provisioned concurrency — 3.4 s**
- **cold start — 1.2 s**
- **monthly cost at current volume — $3,600**, то есть **-41% vs EKS**
- **scale-out to 3x volume — immediate**
- **operations — no cluster; Lambda, SQS and the gateway are managed**

Источник:
- `docs/poc-lambda-report.md` — обновлён **2026-07-24**
- ADR, где это зафиксировано: `adr/ADR-006.md` — обновлён **2026-08-05**

Если коротко: **PoC-3 показал 1.9 s p95 и 41% lower monthly cost, поэтому и выбрали Lambda с provisioned concurrency**.

### memory-eval-graph (completed, 8.9s, 4 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Relay moves to Lambda with provisio", "MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text CONTAINS 'provisioned concu", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'compute'}) WHERE d.text CONTAINS 'Lam", 'MATCH (d:Decision)-[:BASED_ON]->(c:PoC) RETURN d.text, d.date, d.status, d.sourc']

Основано на PoC-3 **Relay on Lambda**. По памяти графа для решения **“Relay moves to Lambda with provisioned concurrency on deliver.”** используются такие цифры:

- **p95 latency с provisioned concurrency на deliver:** **1.9 s**
- **p95 latency без provisioned concurrency:** **3.4 s**
- **cold start:** **1.2 s**
- **monthly cost at current volume:** **$3,600 (-41% vs EKS)**
- **scale out to 3x volume:** **immediate**
- **operations:** **no cluster; Lambda, SQS and the gateway are managed**

Источники:
- decision: `meetings/2026-08-03-architecture-committee.txt`, дата **2026-08-03**
- PoC report: `docs/poc-lambda-report.md`, дата PoC в связанной decision-цепочке **2026-08-03**

Если нужно, могу ещё показать, какие именно более ранние решения по этому PoC были потом superseded.

### memory-eval-vector (completed, 8.2s, 3 tool calls)
queries: ['На каком PoC и на каких цифрах основано решение «Relay moves to Lambda with prov', 'Relay moves to Lambda with provisioned concurrency on /deliv PoC цифры решение', 'Relay moves to Lambda with provisioned concurrency on /deliv decision PoC metric']

Решение основано на **PoC-3**.

Что именно использовали:
- **p95 latency на `/deliver` с provisioned concurrency**: **1.9 s**
- **p95 latency без provisioned concurrency**: **3.4 s**
- **Cold start**: **1.2 s**
- **Monthly cost at current volume**: **$3,600**, это **-41% vs EKS**
- В решении также зафиксировано, что **без provisioned concurrency SLO не проходит**

Источники:
- **ADR-006: Run Relay on Lambda with provisioned concurrency**, 2026-08-05 — decision/context/consequences
- **“PoC-3 report: Relay on Lambda”**, 2026-07-24 — results
- **Relay PoC review 2026-07-27**, 2026-07-27 — подтверждение, что provisioned concurrency обязателен и что **1.9 s проходит**, а **0.4 s против 1.9 s** обсуждалось как компромисс

Если коротко: решение «Relay moves to Lambda with provisioned concurrency on /deliv…» опирается на **PoC-3**, где Lambda с provisioned concurrency дала **1.9 s p95** и **41% экономии**, при этом без provisioned concurrency было **3.4 s** и SLO считался проваленным.

## t40 [ru / poc_basis] На каком PoC и на каких цифрах основано решение «Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but …»?
**expected:** PoC-2: Relay on EKS with autoscaling: {"p95_s": 0.4, "monthly_cost_usd": 6100, "ops_effort": "a second platform team"}; report docs/poc-eks-report.md  
**expected sources:** {'sources': ['docs/poc-eks-report.md', 'meetings/2026-08-03-architecture-committee.txt']}

### memory-eval-both (completed, 4.6s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(c:PoC) WHERE d.text STARTS WITH 'Keep Relay on ", '"Keep Relay on EKS with autoscaling" PoC p95 0.4 s autoscaling', '"Keep Relay on EKS with autoscaling" "p95 0.4 s" "autoscaling"']

Основано на PoC-2 — **Relay on EKS with autoscaling**.

Цифры из отчёта PoC:
- **Delivery latency p95:** **0.4 s**
- **Delivery latency p99:** **0.9 s**
- **Monthly cost at current volume:** **$6,100**
- **Scale-out to 3x volume:** **90 s**

Именно это затем отражено в ADR-007, где решение отклонено как:
- **p95 0.4 s**, но
- **1.7x the monthly cost** и
- **a second platform to run**

Источник:
- `docs/poc-eks-report.md` — updated **2026-07-24**
- `adr/ADR-007.md` — updated **2026-08-05**

Если нужно, могу ещё показать, на каком именно решении/ADR это базируется и кто был decider.

### memory-eval-graph (completed, 7.2s, 4 tool calls)
queries: ["MATCH (d:Decision)-[:BASED_ON]->(p:PoC)\nWHERE d.text STARTS WITH 'Keep Relay on ", "MATCH (d:Decision)\nWHERE d.text CONTAINS 'Keep Relay on EKS with autoscaling'\nRE", "MATCH (d:Decision)\nWHERE d.text CONTAINS 'EKS with autoscaling'\nRETURN d.text, d", "MATCH (d:Decision)-[:BASED_ON]->(p:PoC)\nWHERE d.id = 'A36'\nRETURN d.text, d.date"]

Решение основано на PoC **«Relay on EKS with autoscaling»**; в графе оно привязано к решению **A36**.  
Источник решения: **meetings/2026-06-15-weekly-sync.txt**, дата **2026-06-15**.

Цифры из PoC:
- **p95 delivery latency: 0.4 s**
- **p99 delivery latency: 0.9 s**
- **monthly cost at current volume: $6,100**
- **scale-out to 3x volume: 90 s**
- также отмечены операционные издержки: **second cluster, upgrades, node images, Karpenter, 24/7 on-call**

Источник PoC-результатов: **docs/poc-eks-report.md**.

### memory-eval-vector (completed, 10.3s, 3 tool calls)
queries: ['На каком PoC и на каких цифрах основано решение «Keep Relay on EKS with autoscal', 'Keep Relay on EKS with autoscaling rejected p95 0.4 s PoC цифры', 'PoC цифры decision Keep Relay on EKS with autoscaling p95 0.4 s']

Решение основано на **PoC-2: Relay on EKS with autoscaling**.

Что в памяти есть по цифрам и аргументам:

- **p95 delivery latency = 0.4 s** — из отчёта PoC-2; это же повторено в ADR-007 как основание решения.  
  Источник: `docs/poc-eks-report.md` (2026-07-24) и `adr/ADR-007.md` (2026-08-05).

- **Monthly cost at current volume = $6,100** — в отчёте PoC-2.  
  Источник: `docs/poc-eks-report.md` (2026-07-24).

- В ADR-007 это сформулировано как: **“rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run”**.  
  Источник: `adr/ADR-007.md` (2026-08-05).

- В обсуждении PoC-2 сказано, что это **“стабильно автоскейлинг карпентер”** и что ключевой минус — **“второй кластер”**, который нужно эксплуатировать; там же называют **$6,100/мес** при текущем объёме.  
  Источник: `meetings/2026-07-27-poc-review.txt` (2026-07-27).

Итого: решение опирается на **PoC-2 (EKS + autoscaling/Karpenter)** с результатами **p95 0.4 s** и **$6,100/мес**, но было отклонено из-за **1.7× стоимости** и необходимости поддерживать **вторую платформу/кластер**.

Если хочешь, я могу ещё отдельно вытащить, **с чем именно сравнивали эти 1.7×** — это есть в памяти тоже.

## t41 [en / adr_status] What is the status of ADR-001 ('Migrate infrastructure code from Terraform to CloudFormation')?
**expected:** Superseded, superseded by ADR-004  
**expected sources:** {'sources': ['adr/ADR-001.md']}

### memory-eval-both (completed, 2.7s, 2 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-001'}) RETURN a.id, a.title, a.status, a.date, a.file", 'ADR-001 Context']

ADR-001 is **Superseded**.

- **ADR:** `ADR-001: Migrate infrastructure code from Terraform to CloudFormation`
- **Status:** `Superseded`
- **Date:** `2026-01-14`
- **File:** `adr/ADR-001.md`

It is superseded by **ADR-004**.

### memory-eval-graph (completed, 4.4s, 2 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:$id}) RETURN n.id, n.title']

ADR-001 is **Superseded**.  
Source: `adr/ADR-001.md`, dated `2026-01-14`.

It was superseded by **ADR-004**: “Hybrid IaC: Terraform for networking, CloudFormation for application stacks”.  
Source: `adr/ADR-004.md`, dated `2026-01-14` (the superseding ADR’s record is present in memory; ADR-001 itself is the cited source here).

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ["What is the status of ADR-001 ('Migrate infrastructure code from Terraform to Cl", 'ADR-001 Migrate infrastructure code from Terraform to CloudFormation status', 'status of ADR-001 migrate infrastructure code from Terraform to CloudFormation']

ADR-001 is **Superseded (superseded by ADR-004)**. Source: `adr/ADR-001.md`, dated **2026-01-14**.

I retrieved multiple matching chunks for ADR-001, and they all agree on that status:
- `adr/ADR-001.md` — **Status: Superseded (superseded by ADR-004)** — **2026-01-14**
- `adr/ADR-001.md` — decision section also marked **Superseded (superseded by ADR-004)** — **2026-01-14**



## t42 [en / adr_status] What is the status of ADR-005 ('Evaluate EKS and Lambda with two proofs of concept')?
**expected:** Superseded, superseded by ADR-006  
**expected sources:** {'sources': ['adr/ADR-005.md']}

### memory-eval-both (completed, 2.2s, 2 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:$id}) RETURN n.id, n.title']

ADR-005 is **Superseded**.

- **ADR-005** — *Evaluate EKS and Lambda with two proofs of concept*  
  Date: **2026-06-17**  
  Source: **adr/ADR-005.md**

It was superseded by:

- **ADR-006** — *Run Relay on Lambda with provisioned concurrency*  
  Source: **adr/ADR-006.md**

### memory-eval-graph (completed, 4.5s, 2 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:$id}) RETURN n.id, n.title']

ADR-005 is **Superseded**.

- **ADR-005** — “Evaluate EKS and Lambda with two proofs of concept”  
  - status: **Superseded**  
  - date: **2026-06-17**  
  - file: **adr/ADR-005.md**

It was superseded by **ADR-006** — “Run Relay on Lambda with provisioned concurrency”.

### memory-eval-vector (completed, 2.3s, 1 tool calls)
queries: ["What is the status of ADR-005 ('Evaluate EKS and Lambda with two proofs of conce"]

ADR-005 is **superseded by ADR-006**, so its current status is **Superseded**.

Source: `adr/ADR-005.md` — updated `2026-06-17` — status shown as `Superseded (superseded by ADR-006)`.

## t43 [en / adr_status] What is the status of ADR-007 ('Keep Relay on EKS with autoscaling')?
**expected:** Rejected  
**expected sources:** {'sources': ['adr/ADR-007.md']}

### memory-eval-both (completed, 4.6s, 3 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:$id}) RETURN n.id, n.title', 'ADR-007 Keep Relay on EKS with autoscaling context reason rejected']

ADR-007 is **Rejected**.

- **ADR-007: Keep Relay on EKS with autoscaling**
- **Date:** 2026-08-05
- **File:** `adr/ADR-007.md`

Reason from the ADR context:
- “Alternative to ADR-006 put forward by the architect: keep Relay on EKS, add autoscaling and accept the cost.”
- The decision line says it was rejected because “p95 0.4 s but 1.7x the monthly cost and a second platform to run.”

The graph query shows no newer ADR superseding ADR-007.

### memory-eval-graph (completed, 7.4s, 3 tool calls)
queries: ["MATCH (a:ADR {id:'ADR-007'}) RETURN a.id, a.title, a.status, a.date, a.file; MAT", 'MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:$id}) RETURN n.id, n.title']

ADR-007 is **Rejected**. Source: `adr/ADR-007.md`, dated `2026-08-05`.

No newer ADR was found superseding it.

### memory-eval-vector (completed, 3.5s, 1 tool calls)
queries: ["What is the status of ADR-007 ('Keep Relay on EKS with autoscaling')?"]

ADR-007 is **Rejected**. Source: `adr/ADR-007.md`, updated **2026-08-05**.

Relevant retrieved chunks:
- Decision section: status **Rejected**; “Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a second platform to run).” Source: `adr/ADR-007.md`, **2026-08-05**
- Header/status chunk: **Status: Rejected**, **Date: 2026-08-05**, **Deciders: Relay weekly sync, 2026-08-03**. Source: `adr/ADR-007.md`, **2026-08-05**



## t44 [en / adr_status] What is the status of ADR-010 ('Gateway timeout policy for Lambda integrations')?
**expected:** Proposed; Never accepted; D20 (25 s) is the live decision and the ADR still proposes 20 s  
**expected sources:** {'sources': ['adr/ADR-010.md']}

### memory-eval-both (completed, 3.5s, 3 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:$id}) RETURN n.id, n.title']

ADR-010 is **Proposed**.

- **ADR-010 — "Gateway timeout policy for Lambda integrations"**
- Date: **2026-09-23**
- File: **adr/ADR-010.md**

No newer ADR was found that supersedes it, so its recorded status stands.

### memory-eval-graph (completed, 3.8s, 2 tool calls)
queries: ['MATCH (a:ADR {id:$id}) RETURN a.id, a.title, a.status, a.date, a.file', 'MATCH (n:ADR)-[:SUPERSEDES]->(:ADR {id:$id}) RETURN n.id, n.title']

ADR-010 is **Proposed**. Source: `adr/ADR-010.md`, dated `2026-09-23`.

I also checked whether anything supersedes it and found **no superseding ADR** in memory.

### memory-eval-vector (completed, 3.5s, 3 tool calls)
queries: ["What is the status of ADR-010 ('Gateway timeout policy for Lambda integrations')", 'ADR-010 Gateway timeout policy for Lambda integrations status', 'Gateway timeout policy for Lambda integrations ADR-010']

ADR-010 is **Proposed**. The ADR says **“No decision recorded; see Status.”**  
Source: `adr/ADR-010.md` (updated **2026-09-23**).

I also found a note in the ADR consequences section saying it is **“Proposed, not accepted”** and that the live value was set separately on **2026-08-24** at **25 s**.  
Source: `adr/ADR-010.md` (updated **2026-09-23**).



## t45 [en / dependency] What did the decision 'Front Relay with the API gateway; the gateway and its routes…' depend on?
**expected:** One CloudFormation root stack per environment with nested stacks per component (network, data, compute, gateway) (2026-02-09)  
**expected sources:** {'sources': ['meetings/2026-02-09-weekly-sync.txt', 'meetings/2026-03-02-weekly-sync.txt']}

### memory-eval-both (completed, 5.4s, 3 tool calls)
queries: ['MATCH (d:Decision) WHERE d.text STARTS WITH $prefix OPTIONAL MATCH (d)-[:DEPENDS', '"Front Relay with the API gateway; the gateway and its routes" depend on', "MATCH (d:Decision) WHERE d.text STARTS WITH 'Front Relay with the API gateway' O"]

I found no `DEPENDS_ON` edge for that decision in the graph.

Assumption: you mean the ADR/decision starting with “Front Relay with the API gateway; the gateway and its routes…”.

What the memory does show is the rationale in ADR-002:
- Relay is fronted by the account’s API gateway.
- Desired properties were per-caller authentication, per-route timeouts and retries, and one place to see traffic.
- The chosen option was to put routes and policies in the gateway nested stack.

Sources:
- `adr/ADR-002.md` — updated `2026-03-04`
- `docs/gateway.md` — updated `2026-03-18`

If you want, I can also look for what decision it was based on, if any `BASED_ON` relation exists.

### memory-eval-graph (completed, 8.7s, 5 tool calls)
queries: ["MATCH (d:Decision) WHERE d.text STARTS WITH 'Front Relay with the API gateway; t", "MATCH (d:Decision) WHERE d.text STARTS WITH 'Front Relay with the API gateway' O", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'gateway'}) WHERE d.text CONTAINS 'API", "MATCH (d:Decision)-[:DEPENDS_ON]->(e:Decision) WHERE d.text CONTAINS 'gateway' O", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'gateway'}) RETURN d.text, d.date, d.s"]

I couldn’t find a matching decision in memory for that quoted text, so I can’t reliably name its dependencies.

What I retrieved:
- No decision matching `Front Relay with the API gateway; the gateway and its routes…`
- No gateway-topic decisions returned in memory
- No `DEPENDS_ON` links involving a gateway decision were found in the graph

Source: memory graph lookup, no matching decision node found.

### memory-eval-vector (completed, 5.8s, 3 tool calls)
queries: ["What did the decision 'Front Relay with the API gateway; the gateway and its rou", 'Front Relay with the API gateway; the gateway and its routes depend on', 'Decision Front Relay with the API gateway gateway routes depend on']

The decision itself says only that:

- “Front Relay with the API gateway; the gateway and its routes are defined in the gateway nested stack.”  
  Source: `adr/ADR-002.md`, Decision, 2026-03-04.

From the retrieved memory, the **context** for that decision was:

- callers were reaching Relay through an internal load balancer with a shared API key,
- the team wanted authentication per caller,
- per-route timeouts and retries,
- and one place to see traffic,
- plus the account’s API gateway already fronted two other services.  
  Source: `adr/ADR-002.md`, Context, 2026-03-04.

The **options considered** were:

- keep the load balancer and add auth in the service,
- or front Relay with the API gateway, with routes and policies in the gateway nested stack.  
  Source: `adr/ADR-002.md`, Options considered, 2026-03-04.

So, in memory, the decision depends on the context above and the chosen option. I did not find a separate explicit “depends on” statement.
