
## q01 [en / fact] What is the p95 latency SLO for POST /charge?
**expected:** 200 ms over 5 minutes  
**expected sources:** {'sources': ['docs/slo.md', 'meetings/2026-08-24-ledger-sync.txt']}

### memory-eval-both (completed, 3.9s, 1 tool calls)
queries: ['p95 latency SLO POST /charge']

The p95 latency SLO for `POST /charge` is **200 ms over 5 minutes**.

Sources:
- `meetings/2026-08-24-ledger-sync.txt` — 2026-08-24: “POST /charge p95 latency SLO 200 ms over 5 minutes”
- `docs/slo.md` — updated 2026-08-27: `POST /charge` latency, p95 over 5 minutes = **200 ms**

The document is newer than the meeting and confirms the same value.

### memory-eval-graph (completed, 8.7s, 2 tool calls)
queries: ["MATCH (t:Topic)<-[:ABOUT]-(d:Decision)\nWHERE toLower(t.name) CONTAINS 'post /cha", "MATCH (t:Topic)<-[:ABOUT]-(d:Decision)\nWHERE toLower(t.name) CONTAINS 'charge' O"]

The p95 latency SLO for POST /charge is **200 ms over 5 minutes**.

Source: **meetings/2026-08-24-ledger-sync.txt**, dated **2026-08-24**.

### memory-eval-vector (completed, 4.7s, 3 tool calls)
queries: ['What is the p95 latency SLO for POST /charge?', 'p95 latency SLO POST /charge', 'POST /charge latency SLO p95']

The p95 latency SLO for `POST /charge` is **200 ms over 5 minutes**.

Sources:
- `meetings/2026-08-24-ledger-sync.txt` — 2026-08-24: decision recorded as “POST /charge p95 latency SLO 200 ms over 5 minutes” (`claim D02`).
- `docs/slo.md` — updated 2026-08-27: table lists `POST /charge` latency, p95 over 5 minutes = **200 ms**.

The newer doc agrees with the earlier decision.

## q02 [ru / fact] Сколько хранится ключ идемпотентности у charge и с какой даты он обязателен?
**expected:** 24 часа; обязателен с 2026-09-15, две недели grace period  
**expected sources:** {'sources': ['docs/idempotency.md', 'meetings/2026-09-07-ledger-sync.txt']}

### memory-eval-both (completed, 4.1s, 1 tool calls)
queries: ['идемпотентность ключ charge хранится сколько с какой даты обязателен charge idem']

Ключ идемпотентности у `charge` хранится **24 часа**, а обязательным он стал **с 2026-09-15**.

Источники:
- `docs/idempotency.md` — обновлено **2026-09-12**: “Ledger stores the key with the charge for 24 hours” и “required from 2026-09-15”.
- `meetings/2026-09-07-ledger-sync.txt` — дата **2026-09-07**: “храним сутки” и “с пятнадцатого сентября обязательно”.

Если хотите, могу ещё проверить, нет ли более позднего решения, которое это изменило.

### memory-eval-graph (completed, 7.5s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'idempot' ", "MATCH (o:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'idempot' ", "MATCH (doc:Document)\nWHERE toLower(doc.title) CONTAINS 'idempot' OR toLower(doc."]

В памяти есть решение по теме идемпотентности для **/charge**:

- **Ключ идемпотентности хранится 24 часа** — источник: `meetings/2026-09-07-ledger-sync.txt`, дата: `2026-09-07`.
- **Обязателен с 2026-09-15** — источник: `meetings/2026-09-07-ledger-sync.txt`, дата: `2026-09-07`.

Есть также документ `docs/idempotency.md` (обновлён), но для этого вопроса он **устаревает по сравнению с решением**, если в нём указан другой срок; в найденном фрагменте сам срок из документа не извлечён.

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['Сколько хранится ключ идемпотентности у charge и с какой даты он обязателен?', 'идемпотентности charge хранится обязателен дата', 'key idempotency charge retention mandatory date']

Ключ идемпотентности для `POST /charge` хранится **24 часа**. Источник: `docs/idempotency.md` (обновлён **2026-09-12**) и решение `meetings/2026-09-07-ledger-sync.txt` / claim `D05` (дата **2026-09-07**).

Он обязателен **с 2026-09-15**. Источники: `docs/idempotency.md` (обновлён **2026-09-12**) и решение `meetings/2026-09-07-ledger-sync.txt` / claim `D05` (**2026-09-07**).

Если нужно, могу ещё показать, был ли у этого решения grace period и как это связано с ретраями на `/ledger/charge`.

## q03 [en / fact] Why does tariff v2 keep a legacy_code field?
**expected:** finance reconciles by the v1 code; finance-export writes legacy_code until the finance warehouse mapping is live  
**expected sources:** {'sources': ['docs/tariffs-v2.md', 'meetings/2026-09-07-ledger-sync.txt']}

### memory-eval-both (completed, 3.4s, 1 tool calls)
queries: ['tariff v2 legacy_code field why keep legacy_code field rationale']

Tariff v2 keeps `legacy_code` because finance still reconciles charges by the v1 tariff code, and `finance-export` must write that legacy value until the finance warehouse/mapping migration is complete.

Sources:
- `docs/tariffs-v2.md` — updated `2026-09-10`: “Finance systems reconcile charges by the v1 tariff code. Until the finance warehouse is migrated, every v2 tariff carries its v1 code in `legacy_code`, and `finance-export` writes `legacy_code`, not `code`, into the CSV.”
- `meetings/2026-09-07-ledger-sync.txt` — `2026-09-07`: Tim said the old code needs to stay in exports until their mapping is rebuilt, and Dasha agreed to make `legacy_code` mandatory.
- `confluence/tariff-migration-plan.xhtml` — updated `2026-09-16`: finance reconciliation still depends on v1 code; `finance-export` keeps writing `legacy_code` until finance confirms the mapping is live.

The current decision is that `legacy_code` is mandatory.

### memory-eval-graph (completed, 6.5s, 1 tool calls)
queries: ["MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'tariff' OR toLower(t.key) CONTAI"]

Tariff v2 keeps `legacy_code` because the current decision says: “Tariff v2 keeps a mandatory legacy_code field; finance-export writes legacy_code.” Source: `meetings/2026-09-07-ledger-sync.txt`, dated 2026-09-07, decision `D04`.  

I also found related documents:
- `docs/tariffs-v2.md` — updated date not returned in the store result, so I can’t compare it directly here.
- `confluence/tariff-migration-plan.xhtml` — updated date not returned in the store result.

Based on the decision, the field is retained to support `finance-export` writing `legacy_code`. Source: `meetings/2026-09-07-ledger-sync.txt`, 2026-09-07.

### memory-eval-vector (completed, 4.6s, 3 tool calls)
queries: ['Why does tariff v2 keep a legacy_code field?', 'tariff v2 legacy_code field why', 'legacy_code tariff v2']

Tariff v2 keeps `legacy_code` because finance systems still reconcile charges by the v1 tariff code, and `finance-export` must write that old code until the finance warehouse migration/mapping is complete. Sources: `docs/tariffs-v2.md` updated 2026-09-10; `meetings/2026-09-07-ledger-sync.txt` dated 2026-09-07; `confluence/tariff-migration-plan.xhtml` updated 2026-09-16.

Retrieved:
- `docs/tariffs-v2.md` (2026-09-10): says every v2 tariff carries its v1 code in `legacy_code`, and `finance-export` writes `legacy_code`, not `code`.
- `meetings/2026-09-07-ledger-sync.txt` (2026-09-07): says they need the old code in exports until they rebuild their mapping.
- `confluence/tariff-migration-plan.xhtml` (2026-09-16): says finance warehouse reconciles by v1 code and `finance-export` keeps writing `legacy_code` until finance confirms the mapping is live.

## q04 [ru / fact] Что такое retry budget и какое значение выбрали?
**expected:** доля повторных запросов от всех запросов к роуту за минуту, выше которой gateway перестаёт ретраить; 20%  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-21-ledger-sync.txt']}

### memory-eval-both (completed, 3.4s, 1 tool calls)
queries: ['retry budget what is it and what value was chosen Ledger billing project']

Retry budget — это ограничение на долю повторных запросов в окне в 1 минуту: шлюз разрешает ретраи только пока доля retry-запросов ниже заданного процента от всех запросов на роут. Это нужно, чтобы защитить Ledger от “retry storm” во время инцидента.

Выбранное значение: **20%**.

Источники:
- `docs/gateway.md`, раздел **Retry budget**, updated **2026-09-02** — определение retry budget и указание, что значение задаётся в gateway policy.
- `meetings/2026-09-21-ledger-sync.txt`, **2026-09-21**, 00:00:29–00:00:55 — зафиксировано, что budget ретраев **двадцать процентов**.
- `docs/runbook-cutover.md`, раздел **Gateway policy at cutover**, updated **2026-09-30** — таблица политики гейтвея показывает retry budget **20%** для маршрутов.

### memory-eval-graph (completed, 6.6s, 2 tool calls)
queries: ["MATCH (t:Topic)<-[:ABOUT]-(d:Decision)\nWHERE toLower(t.name) CONTAINS 'retry bud", 'MATCH (n)\nWHERE (n:Decision OR n:OpenItem OR n:Topic)\n  AND (toLower(coalesce(n.']

Retry budget — это доля запросов, на которые разрешено тратить ретраи; в найденной записи для `/ledger/charge` выбрали **20%**. Источник: `meetings/2026-09-21-ledger-sync.txt` от **2026-09-21**; также это подтверждено более поздней записью `meetings/2026-09-28-ledger-sync.txt` от **2026-09-28**, где указано: “Gateway timeout lowered to 10 s with a 20% retry budget”.

Если хотите, я могу также показать, как это связано с лимитом “max 2 retries”.

### memory-eval-vector (completed, 4.4s, 3 tool calls)
queries: ['Что такое retry budget и какое значение выбрали?', 'retry budget значение выбрали', 'retry budget']

Retry budget — это ограничение на долю ретраев среди всех запросов к роуту за окно в одну минуту: gateway разрешает ретраи только пока их доля не превышает бюджет. Например, 20% значит максимум один ретрай на пять запросов; дальше gateway временно перестаёт ретраить, чтобы защититься от retry storm. Источник: `docs/gateway.md`, 2026-09-02.

Выбранное значение — **20%**. Это подтверждают:
- `meetings/2026-09-21-ledger-sync.txt`, 2026-09-21 — «бюджет ретраев обязательно двадцать процентов».
- `docs/runbook-cutover.md`, 2026-09-30 — для `/ledger/charge`, `/ledger/invoice/*`, `/ledger/tariffs` указан retry budget **20%**.

В найденных записях есть также более старая формулировка о том, что budget задаётся в policy gateway, а не в Ledger: `docs/gateway.md`, 2026-09-02.

## q05 [ru / temporal] Какой сейчас таймаут на gateway для Ledger и как он менялся?
**expected:** сейчас 10 с с retry budget 20% (2026-09-28); история: 5 с (08-24) → 15 с временно после инцидента (09-14) → 10 с (09-28)  
**expected sources:** {'sources': ['meetings/2026-08-24-ledger-sync.txt', 'meetings/2026-09-14-ledger-sync.txt', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 5.7s, 2 tool calls)
queries: ['gateway timeout Ledger current timeout changed history decision document', 'gateway timeout Ledger active superseded 2026-09-28 2026-09-14 2026-08-24 docs/g']

Сейчас таймаут gateway для Ledger — **10 s**.

Как менялся:
- **2026-08-24** — **5 s** on all Ledger routes; затем это решение было **superseded**.
  - Source: `meetings/2026-08-24-ledger-sync.txt` via claim `decision:gateway-timeout:2026-08-24`.
- **2026-09-14** — **15 s** temporarily after the staging incident; затем это решение было **superseded**.
  - Source: `meetings/2026-09-14-ledger-sync.txt` via claim `decision:gateway-timeout:2026-09-14`.
- **2026-09-28** — **10 s** with a **20% retry budget**; this is the current active decision.
  - Source: `meetings/2026-09-28-ledger-sync.txt` via claim `decision:gateway-timeout:2026-09-28`.

Дополнительно: `docs/gateway.md` updated **2026-09-02** still says **5 seconds**, so этот документ устарел по сравнению с более поздними решениями.
- Source: `docs/gateway.md`, updated `2026-09-02`.

### memory-eval-graph (completed, 8.8s, 2 tool calls)
queries: ["MATCH (t:Topic)<-[:ABOUT]-(d:Decision)\nWHERE toLower(t.name) CONTAINS 'gateway' ", "MATCH (t:Topic)<-[:ABOUT]-(oi:OpenItem)\nWHERE toLower(t.name) CONTAINS 'gateway'"]

Сейчас таймаут gateway для Ledger — **10 s**. Источник: **meetings/2026-09-28-ledger-sync.txt**, решение от **2026-09-28**; это текущее решение по теме, потому что оно **не имеет входящих `SUPERSEDES`** и **заменяет** решение от 2026-09-14.

Как менялся:
- **5 s** — решение от **2026-08-24** в **meetings/2026-08-24-ledger-sync.txt**: “Gateway upstream timeout 5 s on all Ledger routes”.
- **15 s** — решение от **2026-09-14** в **meetings/2026-09-14-ledger-sync.txt**: “Gateway timeout raised to 15 s temporarily after the staging incident; review in two weeks”. Это решение **суперседировано** решением от 2026-09-28.
- **10 s** — решение от **2026-09-28** в **meetings/2026-09-28-ledger-sync.txt**: “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value”.

Дополнительно: open items по этой теме в памяти не нашёл.

### memory-eval-vector (completed, 8.2s, 3 tool calls)
queries: ['Какой сейчас таймаут на gateway для Ledger и как он менялся?', 'таймаут gateway Ledger current timeout history', 'gateway timeout Ledger updated changed decision']

Сейчас в памяти есть **два противоречащих состояния** по gateway timeout, и более новое решение **перекрывает** старое:

- **10 секунд** — активное решение от **2026-09-28**: “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value.” Источник: `meetings/2026-09-28-ledger-sync.txt` / claim `D09`.
- **5 секунд** — более старое решение от **2026-08-24**, но оно **superseded**. Источник: `meetings/2026-08-24-ledger-sync.txt` / claim `D01`.
- **15 секунд** — временное значение от **2026-09-14**, тоже **superseded**. Источник: `meetings/2026-09-14-ledger-sync.txt` / claim `D06`.

Итого: **сейчас актуальный таймаут — 10 секунд**.  
Как менялся:
1. **5 s** — 2026-08-24, затем устарело.
2. **15 s** — 2026-09-14, временно, затем устарело.
3. **10 s** — 2026-09-28, текущее значение.

Что я нашёл:
- `meetings/2026-09-28-ledger-sync.txt` — активное решение про **10 s**.
- `meetings/2026-09-14-ledger-sync.txt` — временное **15 s**, superseded.
- `meetings/2026-08-24-ledger-sync.txt` — исходное **5 s**, superseded.
- `docs/gateway.md` updated **2026-09-02** — всё ещё говорит **5 s**, но этот документ **устарел** относительно решения от **2026-09-28**.

## q06 [en / temporal] What is the current gateway timeout for Ledger routes?
**expected:** 10 s with a 20% retry budget, decided 2026-09-28; the 15 s value was temporary  
**expected sources:** {'sources': ['meetings/2026-09-28-ledger-sync.txt', 'docs/runbook-cutover.md']}

### memory-eval-both (completed, 3.2s, 1 tool calls)
queries: ['current gateway timeout for Ledger routes timeout routes gateway timeout Ledger']

The current gateway timeout for Ledger routes is **10 seconds**.

Source:
- `meetings/2026-09-28-ledger-sync.txt` — decision dated **2026-09-28**: “Gateway timeout lowered to 10 s with a 20% retry budget” (`claim decision:gateway-timeout:2026-09-28`, status **active**)

Note:
- There is an older decision from **2026-08-24** saying **5 seconds**, but it is marked **superseded**.
- The docs I found from **2026-09-30** also reflect **10 s**, but the current controlling source is the **2026-09-28 decision**.

### memory-eval-graph (completed, 4.9s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'gateway t"]

The current gateway timeout for Ledger routes is **10 s**. It was decided in **meetings/2026-09-28-ledger-sync.txt** on **2026-09-28**; the decision text says: “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value.”

Earlier values are superseded:
- **15 s** in **meetings/2026-09-14-ledger-sync.txt** on **2026-09-14** — superseded.
- **5 s** in **meetings/2026-08-24-ledger-sync.txt** on **2026-08-24** — superseded.

### memory-eval-vector (completed, 3.5s, 3 tool calls)
queries: ['What is the current gateway timeout for Ledger routes?', 'current gateway timeout Ledger routes', 'gateway timeout routes Ledger']

The current gateway timeout for Ledger routes is **10 seconds**.

Source:
- `meetings/2026-09-28-ledger-sync.txt` — decision `D09`, dated **2026-09-28**, status **active**: “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value.”
- `docs/runbook-cutover.md` — updated **2026-09-30**: route table shows `/ledger/charge`, `/ledger/invoice/*`, and `/ledger/tariffs` at **10 s**.

Note: the older 5-second setting in `meetings/2026-08-24-ledger-sync.txt` / `docs/gateway.md` is superseded by the newer 2026-09-28 decision.

## q07 [ru / temporal] Разрешены ли сейчас ретраи на /charge?
**expected:** да, с 2026-09-21: максимум 2 повтора, бюджет 20%, потому что ключи идемпотентности обязательны; до этого были запрещены  
**expected sources:** {'sources': ['meetings/2026-09-21-ledger-sync.txt', 'meetings/2026-08-31-ledger-sync.txt']}

### memory-eval-both (completed, 4.2s, 2 tool calls)
queries: ['/charge retries allowed current decision retry on /charge Ledger billing', 'current decision retries /ledger/charge supersedes stale docs gateway 2026-09-21']

Да, сейчас ретраи на `/charge` разрешены.

- Решение: **Retries enabled on `/ledger/charge`: max 2 retries, retry budget 20%** — источник: `meetings/2026-09-21-ledger-sync.txt`, дата **2026-09-21**.
- Более новый документ `docs/runbook-cutover.md` тоже говорит, что **Retries on `/ledger/charge` are allowed now that idempotency keys are mandatory** — источник: `docs/runbook-cutover.md`, дата **2026-09-30**.

При этом старый документ `docs/gateway.md` от **2026-09-02** еще содержит устаревшую формулировку, что ретраи на `/ledger/charge` отключены.

### memory-eval-graph (completed, 9.8s, 4 tool calls)
queries: ["MATCH (t:Topic)<-[:ABOUT]-(d:Decision)\nWHERE t.key CONTAINS 'charge' OR t.name C", "MATCH (o:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE t.key CONTAINS 'charge' OR t.name C", "MATCH (t:Topic)<-[:ABOUT]-(d:Decision)\nWHERE toLower(t.key) CONTAINS 'charge' OR", "MATCH (o:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.key) CONTAINS 'charge' OR"]

not in memory.

Я искал в памяти решения и открытые items по темам, связанным с `/charge`, `charge` и `retry`, но ничего не нашёл:
- Decision по этим темам: ничего не найдено.
- OpenItem по этим темам: ничего не найдено.

Если хотите, я могу попробовать поискать по связанным формулировкам или по конкретному документу/встрече, если вы знаете примерное название.

### memory-eval-vector (completed, 3.5s, 3 tool calls)
queries: ['Разрешены ли сейчас ретраи на /charge?', 'ретраи на /charge', 'retries on /charge']

Сейчас — **да, разрешены**: в решении от **2026-09-21** сказано, что retries на `/ledger/charge` включены, максимум **2 повтора**, бюджет **20%**. Источник: `meetings/2026-09-21-ledger-sync.txt`, дата **2026-09-21**.

Но в памяти есть более старый документ, который этому противоречит: `docs/gateway.md`, обновлён **2026-09-02**, где сказано, что retries на `/ledger/charge` **disabled**. Этот документ **устарел**, потому что есть более новое решение от **2026-09-21**.

Нашёл и ещё более раннее решение, уже **superseded**: `meetings/2026-08-31-ledger-sync.txt`, дата **2026-08-31**, где retries были выключены.

## q08 [en / contradiction] docs/gateway.md says the timeout is 5 seconds. Is that still true?
**expected:** no; the doc is stale (updated 2026-09-02). The timeout went to 15 s on 2026-09-14 and to 10 s on 2026-09-28; the cutover runbook has the current value  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-14-ledger-sync.txt', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 2.5s, 1 tool calls)
queries: ['docs/gateway.md timeout 5 seconds current decision gateway timeout']

No — that document is stale.

- `docs/gateway.md` says the upstream timeout is **5 seconds** (`docs/gateway.md`, updated **2026-09-02**).
- A newer decision on the same topic says the gateway timeout was raised to **15 s temporarily** after the staging incident (`meetings/2026-09-14-ledger-sync.txt`, **2026-09-14**, status: superseded), and then later lowered to **10 s** with a 20% retry budget (`meetings/2026-09-28-ledger-sync.txt`, **2026-09-28**, status: active).

So the current value in memory is **10 s**, not 5 s.

### memory-eval-graph (completed, 5.5s, 3 tool calls)
queries: ['MATCH (d:Document {file:$file}) RETURN d.file AS file, d.updated AS updated, d.t', 'MATCH (doc:Document {file:$file})<-[:ABOUT]-(dec:Decision)-[:ABOUT]->(t:Topic)\nR', 'MATCH (d:Document {file:$file}) RETURN d.file AS file, d.updated AS updated, d.t']

I can’t confirm that from memory.

What I found:
- `docs/gateway.md` exists, titled **“Edge gateway integration”**, source `docs`. Its `updated` date is not available in the store I retrieved.
- I did **not** find any Decision linked to `docs/gateway.md` for the timeout topic.
- So I can’t tell whether the “5 seconds” value is still current, and I can’t cite a newer decision to supersede it.

Answer: **not in memory**.

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['docs/gateway.md says the timeout is 5 seconds. Is that still true?', 'gateway timeout 5 seconds', 'gateway timeout']

No. `docs/gateway.md` is stale.

- `docs/gateway.md` says the upstream timeout is **5 seconds**, updated **2026-09-02** (`docs/gateway.md`, 2026-09-02).
- A newer decision says the gateway timeout was raised to **15 s temporarily** after the staging incident on **2026-09-14** (`meetings/2026-09-14-ledger-sync.txt`, 2026-09-14; status: superseded).
- An even newer active decision says the gateway timeout was lowered to **10 s** with a 20% retry budget on **2026-09-28** (`meetings/2026-09-28-ledger-sync.txt`, 2026-09-28; status: active).

So the current answer in memory is **10 seconds**, not 5.

## q09 [ru / contradiction] В документации написано, что ретраи на /ledger/charge выключены. Это актуально?
**expected:** нет, gateway.md устарел; с 2026-09-21 ретраи на charge включены, 2 повтора, бюджет 20%  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-21-ledger-sync.txt']}

### memory-eval-both (completed, 4.2s, 1 tool calls)
queries: ['/ledger/charge retries disabled retry off documentation current актуально']

Нет, это **не актуально**.

Что есть в памяти:
- В `docs/gateway.md` от **2026-09-02** написано, что ретраи на **`/ledger/charge` disabled**.  
- Но более новая decision-запись от **2026-09-21** говорит: **Retries enabled on /ledger/charge: max 2 retries, retry budget 20%**. Это текущая запись, и она прямо отмечает, что старый текст в `docs/gateway.md` ещё говорит обратное.

Источник:
- `meetings/2026-09-21-ledger-sync.txt` — decision `decision:retries:2026-09-21`, дата **2026-09-21**
- `docs/gateway.md` — обновлено **2026-09-02**

Итог: документация **устарела**; актуальное состояние — ретраи **включены** на `/ledger/charge` (до 2 ретраев).

### memory-eval-graph (completed, 6.2s, 3 tool calls)
queries: ["MATCH (t:Topic) WHERE toLower(t.name) CONTAINS 'charge' AND toLower(t.name) CONT", "MATCH (d:Decision)-[:ABOUT]->(t:Topic) WHERE toLower(t.name) CONTAINS 'charge' A", "MATCH (doc:Document) WHERE toLower(doc.title) CONTAINS 'charge' OR toLower(doc.t"]

Не могу подтвердить по памяти: **not in memory**.

Что удалось извлечь:
- По теме с ключевыми словами **ledger + charge** не нашлось ни **Topic**, ни **Decision**. Источник: граф памяти, дата — не указана в найденных узлах.
- Нашлись документы:
  - `docs/idempotency.md` — **"Idempotency keys for /charge"** — updated: **не заполнено в памяти**
  - `confluence/ledger-architecture.xhtml` — **"Ledger architecture"** — updated: **не заполнено в памяти**
  - `docs/slo.md` — **"Ledger SLOs"** — updated: **не заполнено в памяти**
  - `docs/overview.md` — **"Ledger service overview"** — updated: **не заполнено в памяти**

Поскольку в памяти нет решения или темы про **ретраи на /ledger/charge**, я не могу сказать, актуально ли это.

### memory-eval-vector (completed, 3.3s, 1 tool calls)
queries: ['В документации написано, что ретраи на /ledger/charge выключены. Это актуально?']

Нет, это уже неактуально: в памяти есть более новое решение от **2026-09-21**, где сказано, что **ретраи на `/ledger/charge` включены** — максимум **2 retries**, retry budget **20%**. Источник: `meetings/2026-09-21-ledger-sync.txt` (decision `retries`, status `active`).

Документация `docs/gateway.md` с датой **2026-09-02** ещё говорит, что ретраи **disabled**, но она устарела по сравнению с решением от **2026-09-21**. Источник: `docs/gateway.md` (updated 2026-09-02).

Дополнительно в памяти есть старое, уже **superseded** решение от **2026-08-31**, где ретраи на `/ledger/charge` были выключены. Источник: `meetings/2026-08-31-ledger-sync.txt` (decision `retries`, superseded).

## q10 [en / contradiction] Who owns the rollback in the cutover runbook?
**expected:** the runbook says TBD but it is stale; Irina took rollback ownership on 2026-10-02  
**expected sources:** {'sources': ['docs/runbook-cutover.md', 'meetings/2026-10-02-ledger-sync.txt']}

### memory-eval-both (completed, 3.4s, 1 tool calls)
queries: ['rollback cutover runbook owner who owns rollback']

The rollback in the cutover runbook is owned by **Irina Belova**.

Sources:
- **meetings/2026-10-02-ledger-sync.txt** — 2026-10-02: “rollback owner in the runbook TBD” and “Ira: I’ll take rollback; it’s my duty” (`claim:decision:cutover:2026-10-02`, active).
- **docs/runbook-cutover.md** — updated 2026-09-30: says **“Rollback owner: TBD”**, so the doc is stale relative to the 2026-10-02 decision.



### memory-eval-graph (completed, 7.3s, 4 tool calls)
queries: ["MATCH (d:Document)-[:ABOUT]->(t:Topic)\nWHERE toLower(d.title) CONTAINS 'cutover ", "MATCH (p:Person)-[o:OWNS]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'rollback' O", "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'rollback'", "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE t.key = 'topic:cutover' AND NOT (d)"]

The rollback owner for the cutover is **Irina**. Source: **meetings/2026-10-02-ledger-sync.txt** on **2026-10-02**. The graph also notes that **docs/runbook-cutover.md** still said “rollback owner TBD,” so that document is stale relative to the newer decision.

### memory-eval-vector (completed, 2.5s, 3 tool calls)
queries: ['Who owns the rollback in the cutover runbook?', 'rollback cutover runbook owner', 'cutover runbook rollback ownership']

The rollback owner for the cutover is **Irina Belova**. Source: **meetings/2026-10-02-ledger-sync.txt** (decision dated **2026-10-02**).

Note: the runbook is stale on this point — **docs/runbook-cutover.md** (updated **2026-09-30**) still says **“Rollback owner: TBD.”**

## q11 [ru / attribution] Кто сейчас отвечает за политику ретраев и с какого момента?
**expected:** Даша, с 2026-09-21; до этого Олег  
**expected sources:** {'sources': ['meetings/2026-09-21-ledger-sync.txt', 'meetings/2026-08-31-ledger-sync.txt']}

### memory-eval-both (completed, 6.5s, 2 tool calls)
queries: ["MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'retry' OR toLower(t.key) CONTAIN", 'политика ретраев owner ownership current decision who owns retry policy']

Сейчас за политику ретраев отвечает **Даша Волкова**, с **2026-09-21**.

Что нашёл:
- **Активное владение**: `Retry policy ownership moves from Oleg to Dasha` — файл `meetings/2026-09-21-ledger-sync.txt`, дата **2026-09-21**.
- В той же встрече сказано: `политика ретраев переходит от олега к даше с сегодняшнего дня` — файл `meetings/2026-09-21-ledger-sync.txt`, дата **2026-09-21**.

Более ранняя запись:
- `retry policy owned by Oleg` — файл `meetings/2026-08-31-ledger-sync.txt`, дата **2026-08-31**; это устаревшее владение, потому что позже его заменили на Дашу.

Если хотите, я могу ещё проверить, есть ли отдельная тема/документ по ретраям и не устарел ли документ относительно этой передачи.

### memory-eval-graph (completed, 13.1s, 7 tool calls)
queries: ["MATCH (t:Topic) WHERE toLower(t.name) CONTAINS 'retry' OR toLower(t.key) CONTAIN", "MATCH (oi:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'retry' O", 'MATCH (t:Topic)\nRETURN t.key AS topicKey, t.name AS topicName\nORDER BY topicKey', "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(d.text) CONTAINS 'retry' OR", "MATCH (t:Topic {key:'topic:retries'})<-[:OWNS]-(p:Person)\nWHERE (p)-[o:OWNS]->(t", "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:retries'})\nWHERE NOT (d)<-[:SU", "MATCH (t:Topic {key:'topic:retries'})<- [o:OWNS] -(p:Person)\nWHERE o.to IS NULL\n"]

Сейчас за политику ретраев отвечает **Dasha Volkova** — дата начала владения есть в памяти, но в записи `OWNS` поле `from` вернулось как пустое значение, поэтому я не могу корректно назвать момент начала из хранилища.  
Источник: `topic:retries` / `OWNS` (в памяти найдено как текущий владелец), дата: не извлечена из записи.

Что ещё нашёл:
- По теме `retries` есть актуальное решение: **“Retries enabled on /ledger/charge: max 2 retries, retry budget 20%”** из `meetings/2026-09-21-ledger-sync.txt`, статус `active`.
- Более старое решение **“... retry policy owned by Oleg”** из `meetings/2026-08-31-ledger-sync.txt` помечено как `superseded`, то есть это уже не текущий статус.

Если хотите, я могу отдельно попытаться найти точную дату начала владения в соседних записях памяти.

### memory-eval-vector (completed, 3.5s, 3 tool calls)
queries: ['Кто сейчас отвечает за политику ретраев и с какого момента?', 'кто владелец политики ретраев сейчас и с какого момента', 'ownership retry policy from date current owner']

Сейчас за политику ретраев отвечает **Даша Волкова**; это решение от **2026-09-21**. Источник: `meetings/2026-09-21-ledger-sync.txt`, решение `decision:ownership:2026-09-21` (active).  

С какого момента: **с 2026-09-21, “с сегодняшнего дня”**. Источник: `meetings/2026-09-21-ledger-sync.txt`, фрагмент 00:00:55–00:01:12.

Важно: более раннее решение от **2026-08-31** назначало владельцем **Олега**, но оно помечено как **superseded**. Источник: `meetings/2026-08-31-ledger-sync.txt`, `decision:retries:2026-08-31`.

## q12 [en / attribution] Who proposed raising the timeout to 15 seconds, and who objected?
**expected:** Oleg proposed it after the 2026-09-14 staging incident; Irina objected (it masks the problem), then agreed on a review date  
**expected sources:** {'sources': ['meetings/2026-09-14-ledger-sync.txt']}

### memory-eval-both (completed, 5.7s, 2 tool calls)
queries: ['raised the timeout to 15 seconds proposed objected timeout 15 seconds', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {name:'gateway timeout'}) OPTIONAL MATCH ("]

Олег предложил поднять таймаут до 15 секунд, а Ира возразила.

Источники:
- `meetings/2026-09-14-ledger-sync.txt` — 2026-09-14: Олег сказал «временно поднять таймаут до пятнадцати секунд».
- `meetings/2026-09-14-ledger-sync.txt` — 2026-09-14: Ира сказала «я против…».

Также в памяти есть решение по теме:
- `meetings/2026-09-14-ledger-sync.txt` — 2026-09-14: временно фиксируем таймаут 15 секунд; владелец Олег Приходько.


### memory-eval-graph (completed, 10.9s, 4 tool calls)
queries: ["MATCH (oi:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(oi.text) CONTAINS 'timeout", "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(d.text) CONTAINS 'timeout' ", "MATCH (d:Decision)\nWHERE toLower(d.text) CONTAINS 'timeout' OR toLower(d.note) C", "MATCH (d:Decision {key:'decision:gateway-timeout:2026-09-14'})<-[:DECIDED_IN]-(m"]

I found the timeout decision, but I could not identify the specific proposer or objector from the memory graph.

What I retrieved:
- Decision: “Gateway timeout raised to 15 s temporarily after the staging incident; review in two weeks”
- Source file: `meetings/2026-09-14-ledger-sync.txt`
- Date: 2026-09-14
- Related topic: `gateway timeout`

I also found the later superseding decision:
- “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value”
- Source file: `meetings/2026-09-28-ledger-sync.txt`
- Date: 2026-09-28

But the stores did not contain the names of who proposed the 15-second timeout or who objected, so the answer is **not in memory**.

### memory-eval-vector (completed, 3.9s, 3 tool calls)
queries: ['Who proposed raising the timeout to 15 seconds, and who objected?', 'raising the timeout to 15 seconds proposed objected', 'timeout 15 seconds proposed objected']

Oleg proposed raising the timeout to 15 seconds, and Ira objected.

Sources:
- `meetings/2026-09-14-ledger-sync.txt` (2026-09-14), 00:00:50: Oleg: “temporarily raise the timeout to fifteen seconds…”
- `meetings/2026-09-14-ledger-sync.txt` (2026-09-14), 00:00:58: Ira: “I’m against it…”

The decision record also says the 15-second timeout was set temporarily after the incident:
- `meetings/2026-09-14-ledger-sync.txt` (2026-09-14), claim D06, status superseded: “Gateway timeout raised to 15 s temporarily…”

## q13 [ru / attribution] Кто из финансов участвует и что он обещал?
**expected:** Тим Хорват (с 2026-09-07): мэппинг кодов тарифов у финансов, в проде с 2026-10-01; сверку сумм после dry run, но не сам прогон  
**expected sources:** {'sources': ['meetings/2026-09-07-ledger-sync.txt', 'meetings/2026-10-02-ledger-sync.txt', 'confluence/tariff-migration-plan.xhtml']}

### memory-eval-both (completed, 10.6s, 3 tool calls)
queries: ['финансы участвует обещал promised finance who participated and what did he promi', "MATCH (p:Person)-[:ATTENDED]->(m:Meeting) WHERE toLower(p.role) CONTAINS 'financ", 'Tim Horvat promised promised finance mapping legacy code confirm mapping live wh']

Из финансов участвует **Tim Horvat** (`finance systems`).

Что он обещал/сказал:
- **09.07.2026, meeting `meetings/2026-09-07-ledger-sync.txt`** — он сказал, что в экспорте нужно оставить старый код, пока у них не перестроится мэппинг у себя; это займёт **“месяц-два”**.
- **21.09.2026, meeting `meetings/2026-09-21-ledger-sync.txt`** — он сказал, что **“мэппинг кодов у финансов в тесте на следующей неделе скажу точно”**.
- **02.10.2026, meeting `meetings/2026-10-02-ledger-sync.txt`** — он сказал, что **мэппинг кодов у финансов в проде с 1 октября**, и **уход от legacy code можно планировать, но не раньше ноября**.

Также в документе:
- **16.09.2026, `confluence/tariff-migration-plan.xhtml`** — сказано, что finance-export продолжает писать `legacy_code`, пока финансы не подтвердят, что их мэппинг жив; за это подтверждение отвечает **Tim Horvat**.

Если хочешь, я могу ещё отдельно проверить, **это текущая обязанность Тима или уже кто-то другой её заменил**.

### memory-eval-graph (completed, 6.0s, 2 tool calls)
queries: ["MATCH (p:Person)-[:ATTENDED]->(m:Meeting) WHERE toLower(p.role) CONTAINS 'financ", "MATCH (p:Person)-[:OWNS]->(d:Decision) WHERE toLower(p.role) CONTAINS 'finance' "]

Из финансов участвует Tim Horvat — его роль в памяти указана как **finance systems**. Он присутствовал на встречах:

- `meetings/2026-10-02-ledger-sync.txt` — 2026-10-02
- `meetings/2026-09-28-ledger-sync.txt` — 2026-09-28
- `meetings/2026-09-21-ledger-sync.txt` — 2026-09-21
- `meetings/2026-09-14-ledger-sync.txt` — 2026-09-14
- `meetings/2026-09-07-ledger-sync.txt` — 2026-09-07

Что он обещал:
- `meetings/2026-09-07-ledger-sync.txt` — 2026-09-07: **“Tariff v2 keeps a mandatory legacy_code field; finance-export writes legacy_code”**. Статус решения: `active` (`D04`).

Если нужно, я могу ещё проверить, есть ли у него другие обещания/решения в памяти.

### memory-eval-vector (completed, 4.5s, 3 tool calls)
queries: ['Кто из финансов участвует и что он обещал?', 'финансы участвует обещал', 'участвует обещал финансов']

По памяти, из финансов участвует **Тим Хорват** / **Тим**.

Что он обещал:
- **Сказать точно про мэппинг кодов у финансов в тесте на следующей неделе** — `meetings/2026-09-21-ledger-sync.txt` от **2026-09-21**: «мэппинг кодов у финансов в тесте на следующей неделе скажу точно».
- Позже было уточнение, что **мэппинг кодов у финансов в проде с 1 октября, и уход от legacy code можно планировать не раньше ноября** — `meetings/2026-10-02-ledger-sync.txt` от **2026-10-02**. Это более новый источник, поэтому он актуальнее.

Дополнительно:
- В документе `confluence/tariff-migration-plan.xhtml` от **2026-09-16** сказано, что **Tim Horvat owns the confirmation** о том, что мэппинг финансов живой.

Если хочешь, могу отдельно выписать, **что именно он должен был подтвердить** и **какой статус сейчас у этой зависимости**.

## q14 [ru / unowned] Кто делает dry run миграции тарифов на копии прода?
**expected:** никто; вопрос поднимался 08-31, 09-07, 09-14, 09-21, 09-28, 10-02 и остался без владельца, записан в риски катовера  
**expected sources:** {'sources': ['meetings/2026-08-31-ledger-sync.txt', 'meetings/2026-10-02-ledger-sync.txt', 'confluence/tariff-migration-plan.xhtml']}

### memory-eval-both (completed, 5.2s, 2 tool calls)
queries: ['dry run migration tariffs copies of prod who does it', 'MATCH (o:OpenItem {key:$key})-[:ABOUT]->(t:Topic) OPTIONAL MATCH (p:Person)-[r:O']

В памяти это **no owner**.

Источник:
- **meetings/2026-08-31-ledger-sync.txt** — open item **openitem:tariffs:2026-08-31**: “dry run of the tariff backfill on a production copy has no owner; raised again on 09-07, 09-21, 09-28, 10-02”.
- По графу для темы **tariffs** текущего владельца нет.

Если нужно, могу также показать, есть ли позже назначенный owner или решение по этому open item.

### memory-eval-graph (completed, 10.1s, 3 tool calls)
queries: ["MATCH (oi:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(oi.text) CONTAINS 'dry run", "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(d.text) CONTAINS 'dry run' ", "MATCH (p:Person)-[:OWNS]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'тариф' OR to"]

В памяти это **без владельца**.

- Open item: `OPEN: dry run of the tariff backfill on a production copy has no owner; raised again on 09-07, 09-21, 09-28, 10-02`
- Источник: `meetings/2026-08-31-ledger-sync.txt`
- Дата: `2026-08-31`

Больше подходящих решений или владельцев в памяти не найдено.

### memory-eval-vector (completed, 6.0s, 1 tool calls)
queries: ['Кто делает dry run миграции тарифов на копии прода?']

По памяти: **никто не назначен**.

Что я нашёл:
- Встреча **2026-08-31 Ledger sync**: марат спрашивает, кто сделает dry run миграции тарифов на копии прода; даша говорит, что не успеет; олег отвечает только про гейтвей. **Ответственного не назвали**. Источник: `meetings/2026-08-31-ledger-sync.txt` (2026-08-31).
- Open item **tariffs**: dry run backfill на копии прода **has no owner**. Источник: `meetings/2026-08-31-ledger-sync.txt` / claim `O01` (2026-08-31).
- Более поздняя встреча **2026-09-28 Ledger sync**: даша сказала, что dry run “так и не сделан”, марат спросил “кто берет”, олег ответил “не я”. **Новый владелец не появился**. Источник: `meetings/2026-09-28-ledger-sync.txt` (2026-09-28).
- Ещё более поздняя встреча **2026-10-02 Ledger sync**: марат снова поднял вопрос, даша сказала “нет марат”. **Ответственного всё ещё нет**. Источник: `meetings/2026-10-02-ledger-sync.txt` (2026-10-02).

Итог: **в памяти нет назначенного владельца; open item остаётся без owner**.

## q15 [en / unowned] What is blocking phase 1 of the tariff migration?
**expected:** phase 0, the dry run on a production snapshot, has no owner  
**expected sources:** {'sources': ['confluence/tariff-migration-plan.xhtml', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 3.0s, 1 tool calls)
queries: ['blocking phase 1 tariff migration blocked by why phase 1 tariff migration']

Phase 1 of the tariff migration is blocked by the finance dependency: the finance warehouse still reconciles by the v1 code, and `finance-export` keeps writing `legacy_code` until finance confirms its mapping is live. The plan says phase 1 is blocked on phase 0, and phase 0 is the production-snapshot dry run comparing row counts and sums per `legacy_code` with the finance export.

Sources:
- `confluence/tariff-migration-plan.xhtml` — “Tariff v2 migration plan”, section “Finance dependency”, updated 2026-09-16.
- `confluence/tariff-migration-plan.xhtml` — “Tariff v2 migration plan”, section “Phases”, updated 2026-09-16.

If you want, I can also look up who owns the blocking finance confirmation.

### memory-eval-graph (completed, 5.3s, 2 tool calls)
queries: ["MATCH (oi:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'tariff' ", "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'tariff' O"]

Not in memory.

What I found:
- Open item `openitem:tariffs:2026-08-31` on topic `tariffs`, source `meetings/2026-08-31-ledger-sync.txt`, status `open`. It says: “dry run of the tariff backfill on a production copy has no owner; raised again on 09-07, 09-21, 09-28, 10-02.” Date on the node was not populated in memory.
- I did not find any current Decision about “tariff migration” or “phase 1” in memory.

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['What is blocking phase 1 of the tariff migration?', 'phase 1 tariff migration blocking', 'tariff migration phase 1 blocker']

Phase 1 is blocked by phase 0: the dry run of the backfill script against a production snapshot, including comparing row counts and sums per `legacy_code` with the finance export. The finance dependency note says “Phase 0 has no owner. Phase 1 is blocked on it.” Sources: `confluence/tariff-migration-plan.xhtml` (updated 2026-09-16), section **Finance dependency**; and `confluence/tariff-migration-plan.xhtml` (updated 2026-09-16), section **Phases**.

Retrieved:
- `confluence/tariff-migration-plan.xhtml` — Finance dependency — updated 2026-09-16
- `confluence/tariff-migration-plan.xhtml` — Phases — updated 2026-09-16
- `docs/tariffs-v2.md` — Migration — updated 2026-09-10

## q16 [ru / crosslingual] Что в митингах называли бюджетом ретраев и где это описано в документации?
**expected:** retry budget из docs/gateway.md: доля повторов за минуту, 20%; в митингах 'бюджет ретраев' / 'повторы'  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-21-ledger-sync.txt', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 8.7s, 2 tool calls)
queries: ['бюджет ретраев retry budget in meetings what was said', 'документация бюджет ретраев retry budget docs described']

В митингах под **«бюджетом ретраев»** имели в виду лимит доли ретраев на роут/маршрут: в одном месте это описано как **20%**, то есть «на чтении», и как часть политики гейтвея.

Что нашёл в митингах:
- **2026-08-31, Ledger sync**: «retry budget на роуты где повторы есть чтобы не было шторма» и «бюджет ретраев будет в политике гейтвея» — файл `meetings/2026-08-31-ledger-sync.txt`, секция `00:00:36-00:01:00`.
- **2026-09-21, Ledger sync**: «бюджет ретраев обязательно двадцать процентов как на чтении» — файл `meetings/2026-09-21-ledger-sync.txt`, секция `00:00:29-00:00:55`.
- **2026-09-28, Ledger sync**: «есть ретраи с бюджетом… бюджетом ретраев двадцать процентов» — файл `meetings/2026-09-28-ledger-sync.txt`, секция `00:00:03-00:00:33`.

Где это описано в документации:
- **`docs/gateway.md` / “Edge gateway integration” / “Retry budget”**, updated **2026-09-02**:
  - retry budget — это фиксированная доля всех запросов за минутное окно;
  - **20%** означает, что не более одного из пяти запросов может быть ретраем;
  - бюджет защищает Ledger от retry storm;
  - значение задаётся в gateway policy, а не в Ledger.

Источник:
- `docs/gateway.md`, updated **2026-09-02** — это более формально

### memory-eval-graph (completed, 8.4s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'retry' OR", "MATCH (doc:Document)\nWHERE toLower(doc.title) CONTAINS 'retry' OR toLower(doc.so", "MATCH (oi:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'retry' O"]

В митингах «бюджет ретраев» называли **retry budget** — в записи от **2026-09-21** сказано: «**Retries enabled on /ledger/charge: max 2 retries, retry budget 20%**». Источник: `meetings/2026-09-21-ledger-sync.txt`, дата **2026-09-21**.

В документации это описано как **retries** в документе `docs/gateway.md`, но в найденных данных сам документ не вернулся; зато в решении из митинга есть пометка, что **`docs/gateway.md` still says retries are disabled on /ledger/charge**. То есть документация по этому вопросу в памяти выглядит **устаревшей** относительно решения от **2026-09-21**. Источник для этого замечания: `meetings/2026-09-21-ledger-sync.txt`, дата **2026-09-21**.

Что я смог достать:
- `decision:retries:2026-09-21` — retry budget 20%, `meetings/2026-09-21-ledger-sync.txt`, **2026-09-21**
- `decision:retries:2026-08-31` — старое правило про отсутствие retries, `meetings/2026-08-31-ledger-sync.txt`, **2026-08-31**
- в документах по ключу `retry` ничего не нашлось в текущем поиске

Если хотите, я могу ещё отдельно поискать, **в каком именно документе** это должно быть описано, но по текущей памяти документ с явным совпадением не найден.

### memory-eval-vector (completed, 10.4s, 3 tool calls)
queries: ['Что в митингах называли бюджетом ретраев и где это описано в документации?', 'бюджет ретраев', 'retry budget']

В митингах под **«бюджетом ретраев»** имели в виду **retry budget в gateway policy**: долю ретраев от всех запросов на маршрут, ограниченную окном в одну минуту. В документации это описано в **`docs/gateway.md`**.

Что именно нашли:
- **Митинг 2026-08-31**: «retry budget на роуты…», и Олег сказал, что **«бюджет ретраев будет в политике гейтвея»**; также упомянул, что опишет это в доке.  
  Источник: `meetings/2026-08-31-ledger-sync.txt`, дата `2026-08-31`.
- **Митинг 2026-09-21**: бюджет ретраев называли **20%** и привязывали к charge/чтению.  
  Источник: `meetings/2026-09-21-ledger-sync.txt`, дата `2026-09-21`.
- **Митинг 2026-09-28**: снова подтвердили **20%** и связали с тем, что теперь есть ретраи с бюджетом.  
  Источник: `meetings/2026-09-28-ledger-sync.txt`, дата `2026-09-28`.

Документация:
- **`docs/gateway.md`**, раздел **Retry budget**, updated `2026-09-02`:  
  там сказано, что retry budget — это фиксированная доля retried requests от всех запросов на route за минутное окно; **20% = максимум 1 из 5 запросов может быть ретраем**, и значение задаётся в gateway policy, а не в Ledger.  
  Источник: `docs/gateway.md`, дата `2026-09-02`.

Если коротко: в митингах это был **л

## q17 [en / crosslingual] When was the cutover date agreed and what did the team say about the error budget?
**expected:** 2026-09-28; cutover on 2026-10-09 at 10:00 fits within the half of the monthly error budget reserved for planned work  
**expected sources:** {'sources': ['meetings/2026-09-28-ledger-sync.txt', 'docs/slo.md']}

### memory-eval-both (completed, 2.3s, 1 tool calls)
queries: ['cutover date agreed error budget team said']

The cutover date was agreed on **2026-10-09 at 10:00**. The team said it was **within the planned-work error budget**; in the meeting, Ira added that it **passed because about half of the monthly error budget was available for planned work**.

Sources:
- **meetings/2026-09-28-ledger-sync.txt** — 2026-09-28
- **docs/runbook-cutover.md** — updated 2026-09-30

If you want, I can also quote the exact meeting lines.

### memory-eval-graph (completed, 5.3s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'cutover' ", "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(d.text) CONTAINS 'error bud"]

The cutover date was agreed for **2026-10-09 at 10:00**. Source: **meetings/2026-09-28-ledger-sync.txt**; date: **2026-09-28**.

About the error budget, the team said the cutover was **“within the planned-work error budget.”** Source: **meetings/2026-09-28-ledger-sync.txt**; date: **2026-09-28**.

### memory-eval-vector (completed, 4.6s, 3 tool calls)
queries: ['When was the cutover date agreed and what did the team say about the error budge', 'cutover date agreed error budget team said', 'agreed cutover date error budget']

The cutover date was agreed on **2026-09-28** in the meeting note **`meetings/2026-09-28-ledger-sync.txt`**: the team fixed **“9 October, 10:00”** / **“2026-10-09 at 10:00”**. The decision is recorded as an active decision dated **2026-09-28**.  

On the error budget, the team said it was **within the planned-work error budget**. In the same meeting, Ira added that it **fit half of the monthly budget for planned work**, described as consistent with SLOs.  

Sources:
- **`meetings/2026-09-28-ledger-sync.txt`**, dated **2026-09-28** — cutover fixed for **2026-10-09 10:00** and stated to be **within the planned-work error budget**.
- **`meetings/2026-09-28-ledger-sync.txt`**, dated **2026-09-28** — “half of the monthly budget for planned work” / SLO framing.

## q18 [en / temporal] List every decision about the gateway timeout in order with dates.
**expected:** 2026-08-24 5 s (Oleg); 2026-09-14 15 s temporary (Oleg, Irina objected); 2026-09-28 10 s with 20% retry budget (Irina's proposal, Oleg owner)  
**expected sources:** {'sources': ['memory/decisions.jsonl']}

### memory-eval-both (completed, 5.5s, 2 tool calls)
queries: ['gateway timeout decision', 'gateway timeout 5 15 10 decision superseded active']

Here are every decision about the gateway timeout I found, in date order:

1. **2026-08-24** — Gateway upstream timeout set to **5 s** on all Ledger routes.  
   Source: `meetings/2026-08-24-ledger-sync.txt` (`claim D01`, status: superseded)

2. **2026-09-14** — Gateway timeout raised to **15 s temporarily** after the staging incident; review in two weeks.  
   Source: `meetings/2026-09-14-ledger-sync.txt` (`claim D06`, status: superseded)

3. **2026-09-28** — Gateway timeout lowered to **10 s** with a **20% retry budget**; replaces the 15 s emergency value.  
   Source: `meetings/2026-09-28-ledger-sync.txt` (`claim D09`, status: active)

Current decision: **10 s** as of **2026-09-28**.  
Source: `meetings/2026-09-28-ledger-sync.txt` (`claim D09`)



### memory-eval-graph (completed, 4.2s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'gateway t"]

I found 3 decisions about the gateway timeout, in date order:

1. Gateway upstream timeout 5 s on all Ledger routes — source: `meetings/2026-08-24-ledger-sync.txt` — date: 2026-08-24  
2. Gateway timeout raised to 15 s temporarily after the staging incident; review in two weeks — source: `meetings/2026-09-14-ledger-sync.txt` — date: 2026-09-14  
3. Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value — source: `meetings/2026-09-28-ledger-sync.txt` — date: 2026-09-28  

Notes:
- The 2026-08-24 and 2026-09-14 decisions are marked `superseded`.
- The 2026-09-28 decision is the current one (`active`).

### memory-eval-vector (completed, 6.1s, 3 tool calls)
queries: ['List every decision about the gateway timeout in order with dates.', 'gateway timeout decision dates order', 'timeout gateway decision']

Here are the gateway timeout decisions in date order:

1. **2026-08-24** — Gateway upstream timeout set to **5 s on all Ledger routes**.  
   Source: **meetings/2026-08-24-ledger-sync.txt** (claim D01, status **superseded**).

2. **2026-09-14** — Gateway timeout **raised to 15 s temporarily** after the staging incident, with review in two weeks.  
   Source: **meetings/2026-09-14-ledger-sync.txt** (claim D06, status **superseded**).

3. **2026-09-28** — Gateway timeout **lowered to 10 s** with a **20% retry budget**, replacing the 15 s emergency value.  
   Source: **meetings/2026-09-28-ledger-sync.txt** (claim D09, status **active**).

Notes:
- The 2026-09-28 decision is the **current** one because nothing newer supersedes it.
- A 2026-09-30 runbook draft also says the 10-second timeout replaces the 15-second emergency value, but it is a document, not a decision. Source: **docs/runbook-cutover.md** (updated 2026-09-30).

## q19 [ru / fact] Когда катовер и во сколько?
**expected:** 2026-10-09 в 10:00  
**expected sources:** {'sources': ['meetings/2026-09-28-ledger-sync.txt', 'docs/runbook-cutover.md']}

### memory-eval-both (completed, 2.4s, 1 tool calls)
queries: ['cutover date time when is the cutover scheduled']

Катовер: **2026-10-09 в 10:00**.

Источник:
- `meetings/2026-09-28-ledger-sync.txt` — decision `cutover`, дата **2026-09-28**
- `docs/runbook-cutover.md` — updated **2026-09-30**, также указывает **2026-10-09, 10:00 local**

Судя по памяти, время указано как **10:00 local**.

### memory-eval-graph (completed, 5.3s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'cutover' ", "MATCH (o:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'cutover' "]

Катовер: **2026-10-09 в 10:00** — source: `meetings/2026-09-28-ledger-sync.txt`, date: `2026-09-28`.

Есть более новая запись по той же теме, но она **не про время катовера**: `Rollback owner for the cutover is Irina` — source: `meetings/2026-10-02-ledger-sync.txt`, date: `2026-10-02`. Поэтому время беру из решения от `2026-09-28`.

Если хотите, могу ещё проверить, не было ли позже переноса катовера.

### memory-eval-vector (completed, 3.1s, 3 tool calls)
queries: ['Когда катовер и во сколько?', 'катовер дата время', 'cutover date time']

Катовер запланирован на **9 октября 2026 в 10:00**.

Источник:
- **meetings/2026-09-28-ledger-sync.txt** — решение зафиксировано 2026-09-28: “фиксируем катовер девятого октября”, и в claim указано **2026-10-09 at 10:00**.
- **docs/runbook-cutover.md** — обновлено 2026-09-30, там тоже указано **2026-10-09, 10:00 local**.

Если нужно, могу еще сказать, это в каком часовом поясе/локальном времени.

## q20 [ru / contradiction] Decision log в Confluence актуален?
**expected:** нет, последняя версия 2026-09-09; в нём нет решений после 09-07: 15 с, ретраи на charge, передача ретраев Даше, 10 с, дата катовера, владелец отката  
**expected sources:** {'sources': ['confluence/decision-log.xhtml', 'memory/decisions.jsonl']}

### memory-eval-both (completed, 2.6s, 1 tool calls)
queries: ['Decision log Confluence актуален decision log updated current stale Confluence']

Да, в памяти есть актуальный Decision log в Confluence: он обновлён **2026-09-09**. Источник: **confluence/decision-log.xhtml**, дата документа **2026-09-09**.

Что я нашёл:
- **Decision log** — updated **2026-09-09** — источник: `confluence/decision-log.xhtml`
- Внутри есть записи и open item; документ помечен как текущий на момент последнего обновления.

Если хотите, могу ещё проверить, **не устарел ли он относительно более новых решений** по темам из этого лога.

### memory-eval-graph (completed, 5.0s, 2 tool calls)
queries: ["MATCH (d:Document) WHERE toLower(d.title) CONTAINS 'decision log' OR toLower(d.f", "MATCH (dec:Decision)-[:ABOUT]->(t:Topic) WHERE toLower(t.name) CONTAINS 'decisio"]

В памяти есть документ Confluence **“Decision log”**: файл `confluence/decision-log.xhtml`, источник `confluence` ([source], дата обновления в хранилище не распарсена) — поэтому **по самой памяти нельзя уверенно сказать, актуален ли он**.  
Я **не нашёл** связанных решений по теме “decision log” в графе ([source], запрос по Decision/Topic вернул пусто).

Итог: **not in memory** для проверки актуальности.  
Что удалось извлечь:
- Документ: `Decision log`, `confluence/decision-log.xhtml`, `confluence` ([source], дата обновления недоступна в ответе хранилища).
- Решения по теме “decision log”: **не найдены** ([source], без даты).

### memory-eval-vector (completed, 3.5s, 3 tool calls)
queries: ['Decision log в Confluence актуален?', 'актуален ли decision log в Confluence', 'Decision log Confluence updated date current status']

Да, **актуален**: в памяти есть страница **Decision log** в Confluence с датой обновления **2026-09-09** и пометкой, что она отражает решения weekly Ledger sync; если она расходится с записью встречи, приоритет у записи. Источник: **confluence/decision-log.xhtml**, **2026-09-09**.

Что я нашёл:
- **Decision log** — `updated 2026-09-09` — источник: `confluence/decision-log.xhtml` (**2026-09-09**)
- Вторая запись той же страницы с актуальным списком решений и open item — источник: `confluence/decision-log.xhtml` (**2026-09-09**)

Если хотите, могу ещё проверить, **нет ли более свежего решения, которое уже делает этот лог устаревшим**.

## q21 [en / attribution] Which decisions does Dasha own?
**expected:** tariff v2 with legacy_code (with Tim), idempotency keys, retry policy from 2026-09-21 including retries on /charge  
**expected sources:** {'sources': ['memory/decisions.jsonl']}

### memory-eval-both (completed, 6.4s, 2 tool calls)
queries: ['MATCH (p:Person)-[o:OWNS]->(d:Decision)\nWHERE p.name = $name AND o.to IS NULL\nOP', 'MATCH (p:Person)\nWHERE p.name = $name OR $name IN coalesce(p.aliases, [])\nRETURN']

not in memory

What I retrieved:
- Schema for Person/Decision/Topic ownership and decision relationships, dated by the underlying node properties.
- A lookup for a person named Dasha (including aliases) returned no match.
- A query for decisions owned by Dasha returned no results.

Because I couldn’t identify Dasha in memory, I can’t list any decisions she owns.

### memory-eval-graph (completed, 4.4s, 2 tool calls)
queries: ['MATCH (p:Person {name:$name})-[o:OWNS]->(d:Decision)\nWHERE o.to IS NULL\nOPTIONAL', 'MATCH (p:Person)\nWHERE p.name = $name OR $name IN coalesce(p.aliases, [])\nRETURN']

Not in memory.

I retrieved:
- The graph schema for `Person`, `Decision`, `Topic`, and `OWNS` relationships.
- A search for a person named Dasha or matching aliases: no person record found.
- A search for decisions owned by `Dasha`: no results.

Source/date:
- Schema metadata, no date field available in schema output.
- Query results contained no matching records.

### memory-eval-vector (completed, 5.2s, 1 tool calls)
queries: ['Which decisions does Dasha own?']

Dasha owns these decisions in memory:

- **Idempotency keys on `/charge`** — mandatory from 2026-09-15, with 24h retention and a two-week grace period. **Owner: Dasha Volkova.** Source: `meetings/2026-09-07-ledger-sync.txt` (2026-09-07).  
- **Retry policy for `/ledger/charge` / charge retries** — the retry policy moved from Oleg to Dasha. **Owner: Dasha Volkova.** Source: `meetings/2026-09-21-ledger-sync.txt` (2026-09-21).

Notes:
- The older decision log entry for retries says **Oleg** owned it on 2026-08-31, but that is superseded by the 2026-09-21 meeting decision. Sources: `meetings/2026-08-31-ledger-sync.txt` (2026-08-31) and `meetings/2026-09-21-ledger-sync.txt` (2026-09-21).
- I also found a decision log document updated 2026-09-09 listing Dasha for idempotency, but the newer 2026-09-07 meeting claim is the active decision. Source: `confluence/decision-log.xhtml` (updated 2026-09-09), superseded in substance by `meetings/2026-09-07-ledger-sync.txt` (2026-09-07).

If you want, I can also list these as a table with dates and status.

## q22 [en / fact] How long does the Edge gateway cache /ledger/tariffs?
**expected:** 60 s  
**expected sources:** {'sources': ['docs/gateway.md']}

### memory-eval-both (completed, 1.8s, 1 tool calls)
queries: ['Edge gateway cache /ledger/tariffs duration TTL cache /ledger/tariffs']

The Edge gateway caches `/ledger/tariffs` for **60 seconds**.

Source: `docs/gateway.md`, **updated 2026-09-02** (`Edge gateway integration` → `Routes`).

### memory-eval-graph (completed, 6.4s, 3 tool calls)
queries: ["MATCH (t:Topic)<-[:ABOUT]-(d:Decision)\nWHERE toLower(t.name) CONTAINS 'edge gate", "MATCH (o:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'edge gate", "MATCH (d:Decision {source:'meetings/2026-09-07-ledger-sync.txt'})-[:ABOUT]->(t:T"]

No encontré en memoria una decisión o documento sobre **cuánto tiempo cachea Edge gateway `/ledger/tariffs`**.

Lo que sí recuperé:
- **Tema `tariffs`** con una decisión activa del archivo **`meetings/2026-09-07-ledger-sync.txt`**: “Tariff v2 keeps a mandatory legacy_code field; finance-export writes legacy_code” (**fecha**: 2026-09-07).  
- **Open item `tariffs`** en **`meetings/2026-08-31-ledger-sync.txt`**: “OPEN: dry run of the tariff backfill on a production copy has no owner; raised again on 09-07, 09-21, 09-28, 10-02” (**fecha**: 2026-08-31).  

No apareció ninguna entrada sobre **caché de Edge gateway** ni sobre **`/ledger/tariffs`** específicamente, así que la respuesta es **not in memory**.

### memory-eval-vector (completed, 2.2s, 3 tool calls)
queries: ['How long does the Edge gateway cache /ledger/tariffs?', 'Edge gateway cache /ledger/tariffs duration', 'gateway cache /ledger/tariffs TTL']

The Edge gateway caches `/ledger/tariffs` for **60 s**.

Source: `docs/gateway.md` — **Edge gateway integration / Routes**, updated **2026-09-02**.
