
## q01 [en / fact] What is the p95 latency SLO for POST /charge?
**expected:** 200 ms over 5 minutes  
**expected sources:** {'sources': ['docs/slo.md', 'meetings/2026-08-24-ledger-sync.txt']}

### memory-eval-both (completed, 2.5s, 1 tool calls)
queries: ['p95 latency SLO POST /charge']

The p95 latency SLO for `POST /charge` is **200 ms over 5 minutes**.

Sources:
- `confluence/decision-log.xhtml` — **2026-08-24**: “POST /charge p95 latency SLO 200 ms.”
- `docs/slo.md` — **2026-08-27**: “`POST /charge` has a latency objective of 200 ms p95 over 5 minutes.”



### memory-eval-graph (completed, 7.2s, 2 tool calls)
queries: ["MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'post /charge' OR toLower(t.key) ", "MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'charge' OR toLower(t.key) CONTAI"]

The p95 latency SLO for **POST /charge** is **200 ms over 5 minutes**.

Source: **docs/slo.md**, decision **decision:charge:2026-08-27**.  
Date in memory: **2026-08-27**.

I also found a newer POST /charge-related decision in **docs/idempotency.md** dated **2026-09-12**, but it is about idempotency, not latency, so it does not change the latency SLO.

### memory-eval-vector (completed, 2.5s, 1 tool calls)
queries: ['What is the p95 latency SLO for POST /charge?']

The p95 latency SLO for `POST /charge` is **200 ms over 5 minutes**.

Sources:
- `confluence/decision-log.xhtml` — 2026-08-24: “POST /charge p95 latency SLO 200 ms.”
- `docs/slo.md` — 2026-08-27: “`POST /charge` has a latency objective of 200 ms p95 over 5 minutes.”

The newer document and the decision agree.

## q02 [ru / fact] Сколько хранится ключ идемпотентности у charge и с какой даты он обязателен?
**expected:** 24 часа; обязателен с 2026-09-15, две недели grace period  
**expected sources:** {'sources': ['docs/idempotency.md', 'meetings/2026-09-07-ledger-sync.txt']}

### memory-eval-both (completed, 4.0s, 1 tool calls)
queries: ['идемпотентность ключ charge хранится сколько обязательен с какой даты charge ide']

В памяти есть два связанных факта про **/charge**:

- **Ключ идемпотентности хранится 24 часа** — источник: `docs/idempotency.md`, дата **2026-09-12**.
- **Он обязателен с 2026-09-15** — источник: `docs/idempotency.md`, дата **2026-09-12**; также есть решение в `confluence/decision-log.xhtml`, дата **2026-09-07**, что ключи становятся обязательными на `/charge` с **2026-09-15**.

Если хотите, я могу ещё проверить, нет ли более нового решения, которое это изменяет.

### memory-eval-graph (completed, 12.5s, 5 tool calls)
queries: ["MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'charge' AND (toLower(t.name) CON", "MATCH (oi:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'charge' ", "MATCH (doc:Document)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'charge'", "MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'charge'\nOPTIONAL MATCH (d:Decisi", "MATCH (d:Decision)\nWHERE d.source = 'docs/idempotency.md'\nRETURN d.date AS date,"]

Ключ идемпотентности для `POST /charge` хранится **24 часа**; это указано в `docs/idempotency.md` (документ, дата в памяти не заполнена).

Обязателен он **с 2026-09-15**; это также указано в `docs/idempotency.md`.

Что я нашёл в памяти:
- `docs/idempotency.md`: «Ledger stores the key with the charge for 24 hours.»
- `docs/idempotency.md`: «The key is required from 2026-09-15.»

Если хотите, я могу ещё проверить, есть ли для этого темы/решения более свежая запись, которая уточняет или заменяет документ.

### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['Сколько хранится ключ идемпотентности у charge и с какой даты он обязателен?', 'идемпотентности charge хранится обязателен дата', 'ключ идемпотентности charge срок хранения обязательный с какого числа']

Ключ идемпотентности для `/charge` хранится **24 часа** — источник: `docs/idempotency.md` от **2026-09-12**.

Обязателен он **с 2026-09-15** — источники:
- `confluence/decision-log.xhtml` от **2026-09-07**: “Idempotency keys become mandatory on /charge from 2026-09-15, two-week grace period.”
- `docs/idempotency.md` от **2026-09-12**: “The key is required from 2026-09-15.”

Если нужно, могу ещё уточнить, что происходит с запросами без ключа после этой даты.

## q03 [en / fact] Why does tariff v2 keep a legacy_code field?
**expected:** finance reconciles by the v1 code; finance-export writes legacy_code until the finance warehouse mapping is live  
**expected sources:** {'sources': ['docs/tariffs-v2.md', 'meetings/2026-09-07-ledger-sync.txt']}

### memory-eval-both (completed, 5.1s, 2 tool calls)
queries: ['tariff v2 legacy_code field why keep legacy_code field rationale', 'tariff v2 legacy_code finance export v1 tariff code reconcile charges why mandat']

Tariff v2 keeps `legacy_code` for the finance export because finance systems still reconcile charges by the v1 tariff code, so `finance-export` writes `legacy_code` to the CSV until the finance warehouse mapping is migrated and confirmed live. The field is mandatory.

Sources:
- `confluence/decision-log.xhtml` — 2026-09-07: “Tariff v2 keeps legacy_code for the finance export; the field is mandatory.”
- `docs/tariffs-v2.md` — 2026-09-10: “Finance systems reconcile charges by the v1 tariff code… finance-export writes legacy_code, not code, into the CSV.”
- `confluence/tariff-migration-plan.xhtml` — 2026-09-16: “finance-export keeps writing legacy_code until finance confirms their mapping is live.”

### memory-eval-graph (completed, 9.0s, 4 tool calls)
queries: ["MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'tariff' AND toLower(t.name) CONT", "MATCH (t:Topic)<-[:ABOUT]-(doc:Document)\nWHERE toLower(t.name) CONTAINS 'tariff'", 'MATCH (n)\nWHERE (n:Decision OR n:Topic OR n:OpenItem OR n:Document) AND (toLower', "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(d.text) CONTAINS 'legacy_co"]

Tariff v2 keeps `legacy_code` for the finance export, and the field is mandatory. Source: `confluence/decision-log.xhtml`, dated 2026-09-07.  
A matching meeting decision says v2 adds `legacy_code` as required and the export writes it instead of the new code. Source: `meetings/2026-09-07-ledger-sync.txt`, dated 2026-09-07.

I did not find a separate decision explaining any other reason in memory.

### memory-eval-vector (completed, 3.9s, 3 tool calls)
queries: ['Why does tariff v2 keep a legacy_code field?', 'tariff v2 legacy_code field reason', 'tariff v2 legacy_code']

Tariff v2 keeps `legacy_code` for the finance export because finance systems still reconcile charges by the v1 tariff code, and the export writes `legacy_code` rather than the new `code` until finance’s mapping is live. The field is also mandatory.

Sources:
- `confluence/decision-log.xhtml` — 2026-09-07: “Tariff v2 keeps legacy_code for the finance export; the field is mandatory.”
- `docs/tariffs-v2.md` — 2026-09-10: “Finance systems reconcile charges by the v1 tariff code. Until the finance warehouse is migrated, every v2 tariff carries its v1 code in legacy_code, and finance-export writes legacy_code, not code, into the CSV.”
- `confluence/tariff-migration-plan.xhtml` — 2026-09-16: finance-export keeps writing `legacy_code` until finance confirms their mapping is live.

The retrieved items agree; the newest supporting note is the 2026-09-16 migration plan.

## q04 [ru / fact] Что такое retry budget и какое значение выбрали?
**expected:** доля повторных запросов от всех запросов к роуту за минуту, выше которой gateway перестаёт ретраить; 20%  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-21-ledger-sync.txt']}

### memory-eval-both (completed, 4.8s, 2 tool calls)
queries: ['retry budget what is it and what value was chosen Ledger billing project retry b', 'retry budget chosen value number percent policy gateway limit budget retries sto']

Retry budget — это лимит на долю/объём повторных запросов, который позволяет ретраям не устроить «шторм» на роуте. В памяти есть несколько упоминаний про ретраи и бюджет.

Выбранное значение: **20%**.

Источники:
- **meetings/2026-09-28-ledger-sync.txt** — 2026-09-28: «Таймаут десять секунд с бюджетом ретраев двадцать процентов.»
- **meetings/2026-09-21-ledger-sync.txt** — 2026-09-21: «Бюджет ретраев для charge: 20%.»
- **meetings/2026-10-02-ledger-sync.txt** — 2026-10-02: «таймаут 10 секунд, ретраи 2, бюджет 20»

Если нужно, могу ещё сказать, к какому именно роуту это относится и как это соотносится с политикой retries.

### memory-eval-graph (completed, 5.7s, 3 tool calls)
queries: ["MATCH (t:Topic) WHERE toLower(t.name) CONTAINS 'retry budget' OR toLower(t.key) ", "MATCH (doc:Document)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'retry b", "MATCH (o:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'retry bud"]

Не в памяти.

Я искал в графе по теме “retry budget”, но ничего не нашёл:
- Topic/Decision: пусто
- Document: пусто
- OpenItem: пусто

Если хотите, могу попробовать поискать по близкому формулированию термина или по связанному документу/встрече, если вы дадите подсказку.

### memory-eval-vector (completed, 5.1s, 3 tool calls)
queries: ['Что такое retry budget и какое значение выбрали?', 'retry budget value chosen', 'budget retries selected value']

Retry budget — это лимит на количество/долю повторов запросов, чтобы повторы не устроили «шторм»; в памяти это описано как «retry budget на роуты где повторы есть, чтобы не было шторма». Источник: `meetings/2026-08-31-ledger-sync.txt`, 2026-08-31.

Выбрали значение **20%**. Это подтверждается двумя записями:
- `meetings/2026-09-21-ledger-sync.txt`, 2026-09-21: «Бюджет ретраев для charge: 20%».
- `meetings/2026-09-28-ledger-sync.txt`, 2026-09-28: «Таймаут десять секунд с бюджетом ретраев двадцать процентов».

Также есть более поздняя запись:
- `meetings/2026-10-02-ledger-sync.txt`, 2026-10-02: «таймаут 10 секунд, ретраи 2, бюджет 20».

Если хотите, могу отдельно показать, к чему именно относится этот budget — к `charge` или к политике gateway.

## q05 [ru / temporal] Какой сейчас таймаут на gateway для Ledger и как он менялся?
**expected:** сейчас 10 с с retry budget 20% (2026-09-28); история: 5 с (08-24) → 15 с временно после инцидента (09-14) → 10 с (09-28)  
**expected sources:** {'sources': ['meetings/2026-08-24-ledger-sync.txt', 'meetings/2026-09-14-ledger-sync.txt', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 10.0s, 3 tool calls)
queries: ['gateway timeout Ledger timeout current changed history gateway for Ledger', 'MATCH (t:Topic {key:$key})<-[:ABOUT]-(d:Decision) RETURN d.key AS key, d.date AS', 'MATCH (t:Topic {key:$key})<-[:ABOUT]-(f:Fact) RETURN f.key AS key, f.date AS dat']

Сейчас таймаут на gateway для Ledger — **10 секунд**. Это зафиксировано в решении от **2026-10-02**: «политика на проде таймаут 10 секунд…» (`meetings/2026-10-02-ledger-sync.txt`, 2026-10-02).

Как он менялся по найденным решениям:
- **2026-08-24** — **5 s** (`confluence/decision-log.xhtml`, 2026-08-24)
- **2026-08-31** — **5 s** (`meetings/2026-08-31-ledger-sync.txt`, 2026-08-31)
- **2026-09-07** — **5 s** на staging (`meetings/2026-09-07-ledger-sync.txt`, 2026-09-07)
- **2026-09-14** — **15 s** временно (`meetings/2026-09-14-ledger-sync.txt`, 2026-09-14)
- **2026-09-28** — **10 s**, но это решение помечено как **superseded** (`meetings/2026-09-28-ledger-sync.txt`, 2026-09-28)
- **2026-10-02** — **10 s** на prod, это текущая активная запись (`meetings/2026-10-02-ledger-sync.txt`, 2026-10-02)

Важно: в памяти есть и более ранний активный факт на **5 s** из `confluence/decision-log.xhtml` (2026-08-24), но он **устарел** по сравнению с более поздними решениями от 2026-09-14 и 2026-10-02.

Если хотите, могу ещё свести это в короткую хронологическую таблицу с пометкой, какие записи superseded, а какие текущие.

### memory-eval-graph (completed, 14.4s, 4 tool calls)
queries: ["MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'gateway' AND toLower(t.name) CON", "MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'gateway'\nOPTIONAL MATCH (d:Decis", "MATCH (d:Decision)\nWHERE toLower(d.text) CONTAINS 'gateway' AND toLower(d.text) ", "MATCH (oi:OpenItem)\nWHERE toLower(oi.text) CONTAINS 'gateway' AND toLower(oi.tex"]

Сейчас актуальный таймаут на gateway для Ledger — **10 секунд**. Это следует из текущего решения по теме **gateway-timeout** от **2026-10-02**: «политика на проде таймаут 10 секунд, ретраи 2, бюджет 20, ранбук в доке» (источник: **meeting:2026-10-02**; статус: **active**).

Как менялся таймаут по памяти:
- **2026-08-24** — **5 секунд** на все Ledger routes (источник: **meeting:2026-08-24**; решение: `Gateway upstream timeout 5 s on all Ledger routes.`; статус: **active**).  
- **2026-08-31** — **5 секунд** внесён в gateway md (источник: **meeting:2026-08-31**; статус: **active**).  
- **2026-09-07** — на gateway/staging переведён таймаут **5 секунд** (источник: **meeting:2026-09-07**; статус: **active**).  
- **2026-09-14** — таймаут **15 секунд** временно, с пересмотром через две недели (источник: **meeting:2026-09-14**; статус: **active**).  
- **2026-09-28** — зафиксирован **10 секунд**, но это решение позже помечено как **superseded** (источник: документ/решение с датой **2026-09-28**).  
- **2026-10-02** — текущая политика: **10 секунд** (источник: **meeting:2026-10-02**; статус: **active**).

Примечание: решение от **2026-09-28** про 10 секунд считается историческим, потому ч

### memory-eval-vector (completed, 5.5s, 3 tool calls)
queries: ['Какой сейчас таймаут на gateway для Ledger и как он менялся?', 'таймаут gateway Ledger', 'gateway timeout Ledger']

Сейчас таймаут на gateway для Ledger — **5 секунд**. Источник: `confluence/decision-log.xhtml` (2026-08-24), решение “Gateway upstream timeout 5 s on all Ledger routes”.

Как менялся:
- В памяти найдено подтверждение на встрече 2026-08-31, что **“таймаут пять секунд из прошлой встречи уже внесен в gateway md”** — то есть значение 5 секунд уже было принято ранее. Источник: `meetings/2026-08-31-ledger-sync.txt` (2026-08-31).
- В найденных кусках **не видно более раннего или иного значения**, поэтому по памяти нельзя показать историю изменения от другого числа к 5 секундам.

Что я нашёл:
- `confluence/decision-log.xhtml` — 2026-08-24: upstream timeout **5 s**.
- `meetings/2026-08-31-ledger-sync.txt` — 2026-08-31: подтверждение, что таймаут **5 секунд** уже внесён.
- `docs/slo.md` — 2026-08-27: упоминание, что gateway timeouts учитываются в availability, но без значения таймаута.

Если хочешь, я могу отдельно попробовать найти именно **предыдущее значение таймаута** и сказать, когда оно было изменено.

## q06 [en / temporal] What is the current gateway timeout for Ledger routes?
**expected:** 10 s with a 20% retry budget, decided 2026-09-28; the 15 s value was temporary  
**expected sources:** {'sources': ['meetings/2026-09-28-ledger-sync.txt', 'docs/runbook-cutover.md']}

### memory-eval-both (completed, 2.2s, 1 tool calls)
queries: ['current gateway timeout for Ledger routes gateway timeout routes current value']

The current gateway timeout for Ledger routes is **5 seconds**.

Sources:
- **confluence/decision-log.xhtml** — **2026-08-24**: “Gateway upstream timeout 5 s on all Ledger routes.”  
- **meetings/2026-08-24-ledger-sync.txt** — **2026-08-24**: “...five seconds on all routes ledger...”

No newer conflicting decision was found in memory.

### memory-eval-graph (completed, 10.1s, 4 tool calls)
queries: ["MATCH (t:Topic) WHERE toLower(t.name) CONTAINS 'gateway timeout' OR toLower(t.na", "MATCH (d:Decision)-[:ABOUT]->(t:Topic) WHERE (toLower(t.name) CONTAINS 'gateway ", "MATCH (d:Decision)-[:ABOUT]->(t:Topic) WHERE toLower(d.text) CONTAINS 'gateway' ", "MATCH (o:OpenItem)-[:ABOUT]->(t:Topic) WHERE toLower(o.text) CONTAINS 'gateway' "]

Current gateway timeout for Ledger routes is 10 seconds. Source: `meetings/2026-10-02-ledger-sync.txt` dated 2026-10-02, decision `decision:gateway-timeout:2026-10-02` (“политика на проде таймаут 10 секунд, ретраи 2, бюджет 20, ранбук в доке”).

Why I used that:
- There is a newer current decision on the same topic than the older 15-second decision from 2026-09-14.
- The 2026-09-28 decision saying 10 seconds is marked `superseded`, so it is not current.
- The 2026-10-02 decision has no incoming `SUPERSEDES`, so it is the current decision.

Retrieved but not used as current:
- `meetings/2026-09-14-ledger-sync.txt` dated 2026-09-14: 15 seconds, temporary review in two weeks.
- `meetings/2026-09-28-ledger-sync.txt` dated 2026-09-28: 10 seconds, status `superseded`.
- `meetings/2026-09-21-ledger-sync.txt` dated 2026-09-21: open item asking about 15 seconds.


### memory-eval-vector (completed, 3.2s, 3 tool calls)
queries: ['What is the current gateway timeout for Ledger routes?', 'current gateway timeout Ledger routes', 'timeout for routes gateway Ledger']

The current gateway upstream timeout for Ledger routes is **5 s**. Source: **confluence/decision-log.xhtml** (decision, **2026-08-24**): “Gateway upstream timeout 5 s on all Ledger routes.”

I also found a matching meeting note in **meetings/2026-08-24-ledger-sync.txt** (**2026-08-24**) saying “пять секунд на все роуты ledger,” and a later note in **meetings/2026-08-31-ledger-sync.txt** (**2026-08-31**) saying the 5-second timeout was already added to gateway.md.

## q07 [ru / temporal] Разрешены ли сейчас ретраи на /charge?
**expected:** да, с 2026-09-21: максимум 2 повтора, бюджет 20%, потому что ключи идемпотентности обязательны; до этого были запрещены  
**expected sources:** {'sources': ['meetings/2026-09-21-ledger-sync.txt', 'meetings/2026-08-31-ledger-sync.txt']}

### memory-eval-both (completed, 6.2s, 3 tool calls)
queries: ['/charge retries retry retryable allowed current decision', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'retries'})\nRETURN d.date AS date, d.", "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'charge'})\nRETURN d.date AS date, d.s"]

Да, сейчас ретраи на `/charge` разрешены, но только при использовании `Idempotency-Key`.

Источник:
- `docs/idempotency.md`, 2026-09-12: “To make POST /charge safe to retry, callers send an Idempotency-Key header... A second request with the same key returns the original charge id and does not bill again.”
- `confluence/decision-log.xhtml`, 2026-08-31: “No retries on /ledger/charge until idempotency is in place. Retry policy owned by Oleg.”

Почему так:
- Решение от 2026-08-31 запрещало ретраи без идемпотентности.
- Более новое решение от 2026-09-12 ввело `Idempotency-Key`, то есть условие для безопасных ретраев.
- Значит, текущее состояние — ретраи разрешены только с idempotency key.

### memory-eval-graph (completed, 6.6s, 2 tool calls)
queries: ["MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'charge' OR toLower(t.key) CONTAI", "MATCH (d:Decision {key:'decision:charge:2026-09-12'})-[:ABOUT]->(t:Topic)\nOPTION"]

Да — сейчас ретраи на `/charge` разрешены, но только через `Idempotency-Key`:
- `docs/idempotency.md`, решение `decision:charge:2026-09-12` от `2026-09-12`, статус `active`: `POST /charge` safe to retry, если caller отправляет `Idempotency-Key`; повтор с тем же ключом возвращает исходный `charge id` и не списывает деньги повторно.

Ничего более свежего, что бы это отменяло, в памяти не найдено.

### memory-eval-vector (completed, 4.1s, 3 tool calls)
queries: ['Разрешены ли сейчас ретраи на /charge?', 'ретраи на /charge', '/charge retries']

Да. Самое новое решение в памяти — ретраи на `/charge` разрешены, максимум **два повтора**. Источник: `meetings/2026-09-21-ledger-sync.txt` от **2026-09-21**.

Есть более старые записи, которые этому противоречат:
- `meetings/2026-08-31-ledger-sync.txt` от **2026-08-31**: «ретраи на charge выключены совсем».
- `meetings/2026-08-31-ledger-sync.txt` от **2026-08-31**: «пока нет ключей идемпотентности, ретраи на charge нельзя».
- `meetings/2026-08-24-ledger-sync.txt` от **2026-08-24**: открытый вопрос о ретраях, charge неидемпотентный.

Если нужно, могу отдельно перечислить, кто сейчас владеет политикой ретраев для `charge`.

## q08 [en / contradiction] docs/gateway.md says the timeout is 5 seconds. Is that still true?
**expected:** no; the doc is stale (updated 2026-09-02). The timeout went to 15 s on 2026-09-14 and to 10 s on 2026-09-28; the cutover runbook has the current value  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-14-ledger-sync.txt', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 3.8s, 2 tool calls)
queries: ['gateway timeout 5 seconds docs/gateway.md timeout current decision superseded', 'docs/gateway.md timeout 15 seconds gateway timeout revised current']

No — the memory has a newer decision than `docs/gateway.md`.

- Current decision: gateway upstream timeout is **5 s** on all Ledger routes, from `confluence/decision-log.xhtml` dated **2026-08-24**.
- Newer update: on **2026-09-28**, a decision changed it to **10 seconds** with a retry budget of 20%, from `meetings/2026-09-28-ledger-sync.txt`.

So `docs/gateway.md` is stale if it still says 5 seconds.

### memory-eval-graph (completed, 11.7s, 3 tool calls)
queries: ['MATCH (d:Document {file:$file})-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAI', "MATCH (dec:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'gateway", "MATCH (d:Document)\nWHERE toLower(d.file) CONTAINS 'gateway' OR toLower(d.key) CO"]

No — the memory has newer decisions that supersede the 5-second timeout.

- Current decision on `gateway-timeout`: timeout is 10 seconds in production, with retries 2 and budget 20, from `meetings/2026-10-02-ledger-sync.txt` dated 2026-10-02. This decision is marked active.
- There is also a current decision from `meetings/2026-09-14-ledger-sync.txt` dated 2026-09-14 saying the timeout is temporarily 15 seconds.
- Earlier 5-second decisions exist, including:
  - `meetings/2026-09-07-ledger-sync.txt` dated 2026-09-07: “таймаут пять секунд…”
  - `meetings/2026-08-31-ledger-sync.txt` dated 2026-08-31: “таймаут пять секунд внесен в gateway md”
  - `confluence/decision-log.xhtml` dated 2026-08-24: “Gateway upstream timeout 5 s on all Ledger routes.”

So `docs/gateway.md` is stale relative to the newer decisions. I did not find a `Document` node for `docs/gateway.md` in memory, so I can’t cite its updated date from memory.

Retrieved:
- Current decisions on `gateway-timeout` from `meetings/2026-10-02-ledger-sync.txt` and `meetings/2026-09-14-ledger-sync.txt`
- Older 5-second decisions from `meetings/2026-09-07-ledger-sync.txt`, `meetings/2026-08-31-ledger-sync.txt`, and `confluence/decis

### memory-eval-vector (completed, 2.9s, 3 tool calls)
queries: ['docs/gateway.md says the timeout is 5 seconds. Is that still true?', 'gateway timeout 5 seconds updated decision', 'docs/gateway.md timeout 5 seconds']

No — the memory has a newer note that the gateway timeout was changed to **15 seconds**.

- **Current older decision:** “Gateway upstream timeout 5 s on all Ledger routes.” — **confluence/decision-log.xhtml**, **2026-08-24**.
- **Newer item:** “Таймаут: 15 секунд; пересмотр на следующей неделе.” — **meetings/2026-09-21-ledger-sync.txt**, **2026-09-21**.

So **docs/gateway.md is stale** if it still says 5 seconds; the newer memory says 15 seconds.

## q09 [ru / contradiction] В документации написано, что ретраи на /ledger/charge выключены. Это актуально?
**expected:** нет, gateway.md устарел; с 2026-09-21 ретраи на charge включены, 2 повтора, бюджет 20%  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-21-ledger-sync.txt']}

### memory-eval-both (completed, 7.0s, 2 tool calls)
queries: ['ретраи на /ledger/charge выключены актуально retry /ledger/charge disabled', '/ledger/charge retries documentation updated stale current decision no retries i']

Да, **по памяти это не актуально**: есть более новое подтверждение, что ретраи на **/ledger/charge** всё ещё **выключены**, пока не внедрена идемпотентность.

Что нашёл:
- **2026-08-31**, `meetings/2026-08-31-ledger-sync.txt` — решение: **“No retries on /ledger/charge until idempotency is in place.”**  
- **2026-08-31**, `meetings/2026-08-31-ledger-sync.txt` — решение: **“ретраи на charge выключены совсем”**.  
- **2026-09-12**, `docs/idempotency.md` — сказано, что ретраи на `/charge` можно будет включить **после того, как все начнут присылать idempotency keys**; это подтверждает, что на тот момент они ещё не включены.

Если говорить строго про актуальность документации:
- если ваша документация старее **2026-08-31** или **2026-09-12**, она **устарела**;
- текущая позиция в памяти: **ретраи на /ledger/charge выключены**.

Источники:
- `meetings/2026-08-31-ledger-sync.txt` — 2026-08-31
- `docs/idempotency.md` — 2026-09-12



### memory-eval-graph (completed, 5.8s, 2 tool calls)
queries: ["MATCH (t:Topic)<-[:ABOUT]-(d:Decision)\nWHERE toLower(t.name) CONTAINS '/ledger/c", "MATCH (doc:Document)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS '/ledger"]

Да, это **актуально**: в памяти есть актуальное решение, что **ретраи на /ledger/charge выключены**.  
- Источник: `confluence/decision-log.xhtml`, **2026-08-31** — решение: “No retries on /ledger/charge until idempotency is in place.”  
- Это решение **не помечено как superseded**, значит оно текущее.

Дополнительно в памяти есть более новое решение по соседней теме:  
- Источник: `docs/idempotency.md`, **2026-09-12** — для `POST /charge` предусмотрен `Idempotency-Key`, чтобы вызов был безопасен для повторов.

Но в доступной памяти я **не нашёл отдельного документа именно про `/ledger/charge`**, только решения по `charge` и `retries`.

### memory-eval-vector (completed, 5.6s, 3 tool calls)
queries: ['В документации написано, что ретраи на /ledger/charge выключены. Это актуально?', 'ретраи на /ledger/charge выключены актуально?', '/ledger/charge retries disabled current status']

Да, актуально.

Что нашёл:
- **2026-08-31, `meetings/2026-08-31-ledger-sync.txt`** — решение: **«ретраи на charge выключены совсем; на чтение можно до двух повторов; политика ретраев за олегом.»**
- **2026-08-31, `confluence/decision-log.xhtml`** — решение: **«No retries on /ledger/charge until idempotency is in place. Retry policy owned by Oleg.»**

Есть ещё более поздний документ:
- **2026-09-12, `docs/idempotency.md`** — сказано, что для **`POST /charge`** можно безопасно ретраить с `Idempotency-Key`.

Но он **не отменяет** решение про выключенные ретраи на `/ledger/charge`, потому что в памяти нет более позднего решения, которое бы это меняло. Значит текущее состояние по памяти — **ретраи на `/ledger/charge` выключены**.

Если хотите, могу ещё проверить, не было ли после 2026-09-12 решения, которое это изменило.

## q10 [en / contradiction] Who owns the rollback in the cutover runbook?
**expected:** the runbook says TBD but it is stale; Irina took rollback ownership on 2026-10-02  
**expected sources:** {'sources': ['docs/runbook-cutover.md', 'meetings/2026-10-02-ledger-sync.txt']}

### memory-eval-both (completed, 4.9s, 2 tool calls)
queries: ["MATCH (d:Document)-[:ABOUT]->(t:Topic) WHERE toLower(d.file) CONTAINS 'cutover r", 'cutover runbook rollback owner owns rollback']

The rollback owner is **not in memory** as an assigned owner. The remembered runbook text says **“The rollback owner is TBD.”** in **docs/runbook-cutover.md** dated **2026-10-09**.

What I retrieved:
- **docs/runbook-cutover.md** — “The rollback owner is TBD.” — **2026-10-09**
- **docs/runbook-cutover.md** — “Oleg Prikhodko is the owner of docs/runbook-cutover.md.” — **2026-09-30**
- **docs/runbook-cutover.md** — “The gateway cutover runbook is updated on 2026-09-30.” — **2026-09-30**

So, for the rollback specifically, there is **no owner yet / TBD** in memory.

### memory-eval-graph (completed, 9.2s, 6 tool calls)
queries: ["MATCH (t:Topic)<-[:ABOUT]-(d:Document)\nWHERE toLower(t.name) CONTAINS 'rollback'", "MATCH (p:Person)-[o:OWNS]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'rollback' A", "MATCH (d:Document)-[:ABOUT]->(t:Topic)\nWHERE toLower(d.file) CONTAINS 'runbook' ", "MATCH (p:Person)-[o:OWNS]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'rollback' O", "MATCH (t:Topic)<-[:ABOUT]-(d:Document {file:'docs/runbook-cutover.md'})\nRETURN t", "MATCH (p:Person)-[o:OWNS]->(t:Topic {name:'cutover'})\nRETURN p.name AS owner, o."]

The memory shows the cutover topic is owned by Oleg Prikhodko, from an OWNS edge on topic **cutover**; source: the graph memory record for topic ownership, date: not stored in the returned result. Document found: **docs/runbook-cutover.md**. There is no separate rollback topic or owner in memory, so for “the rollback in the cutover runbook” I can only say it is **not explicitly in memory**; the retrieved document is **docs/runbook-cutover.md** and the owned topic it maps to is **cutover**.

What I retrieved:
- **docs/runbook-cutover.md** → topic **cutover**
- **cutover** → owned by **Oleg Prikhodko**

If you want, I can keep searching for a more specific rollback entry, but based on memory alone: **not in memory**.

### memory-eval-vector (completed, 2.0s, 1 tool calls)
queries: ['Who owns the rollback in the cutover runbook?']

The rollback owner is **TBD** in `docs/runbook-cutover.md` dated **2026-10-09**.

Retrieved:
- `docs/runbook-cutover.md` — “The rollback owner is TBD.” (`open_item`, active, 2026-10-09)

This is the latest item I found on that topic.

## q11 [ru / attribution] Кто сейчас отвечает за политику ретраев и с какого момента?
**expected:** Даша, с 2026-09-21; до этого Олег  
**expected sources:** {'sources': ['meetings/2026-09-21-ledger-sync.txt', 'meetings/2026-08-31-ledger-sync.txt']}

### memory-eval-both (completed, 8.2s, 4 tool calls)
queries: ['MATCH (t:Topic {name:$name})<-[:ABOUT]-(p:Person)-[o:OWNS]->(t) WHERE o.to IS NU', 'политика ретраев owner owns from date retry policy current who owns', 'ретраи политика retry policy topic ownership Dasha Oleg who owns from date', 'MATCH (t:Topic)<-[:ABOUT]-(p:Person)-[o:OWNS]->(t) WHERE toLower(t.name) CONTAIN']

Сейчас за политику ретраев отвечает **Олег**; это подтверждено решением от **2026-08-31** из `meetings/2026-08-31-ledger-sync.txt` и записью в `confluence/decision-log.xhtml` от **2026-08-31**: “Retry policy owned by Oleg”.

Также в памяти есть более ранняя встреча `meetings/2026-08-31-ledger-sync.txt` с формулировкой: “политика ретраев за олегом” — дата **2026-08-31**.

Что я нашёл:
- `meetings/2026-08-31-ledger-sync.txt` — **2026-08-31**: политика ретраев за Олегом.
- `confluence/decision-log.xhtml` — **2026-08-31**: Retry policy owned by Oleg.

Более свежей смены владельца политики ретраев в памяти не нашёл.

### memory-eval-graph (completed, 8.3s, 2 tool calls)
queries: ["MATCH (t:Topic)<-[:ABOUT]-(d:Decision)\nWHERE toLower(t.name) CONTAINS 'retry' OR", "MATCH (p:Person)-[o:OWNS]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'retry' OR t"]

Не могу уверенно ответить из памяти: в графе есть запись о политике ретраев, но нет явного текущего владельца в данных OWNS.

Что я нашёл:
- Тема **retries** в `confluence/decision-log.xhtml` — решение/запись от даты, которая в ответе не представлена как нормальная дата, со статусом `active`: «No retries on /ledger/charge until idempotency is in place. Retry policy owned by Oleg.»
- Текущий владелец через `OWNS` для темы retries в памяти **не найден**.
- Также есть связанная запись `docs/idempotency.md` про идемпотентность для `charge`, но это про другую тему.

Итог: **not in memory** — в графе нет подтверждённого текущего владельца политики ретраев и даты начала владения.

### memory-eval-vector (completed, 4.3s, 3 tool calls)
queries: ['Кто сейчас отвечает за политику ретраев и с какого момента?', 'кто владелец политики ретраев сейчас и с какого момента', 'политика ретраев ownership from date current owner']

Сейчас за политику ретраев отвечает **Даша**, и это действует **с 2026-09-21**. Источник: `meetings/2026-09-21-ledger-sync.txt` (2026-09-21), где сказано: «Политика ретраев для charge переходит от Олега к Даше с 2026-09-21».

Но в памяти есть и более раннее решение, что **до этого** политика ретраев была у **Олега**:
- `meetings/2026-08-31-ledger-sync.txt` (2026-08-31): «политика ретраев за олегом»
- `confluence/decision-log.xhtml` (2026-08-31): «Retry policy owned by Oleg»

Если хотите, могу также перечислить, что именно относится к этой политике по памяти.

## q12 [en / attribution] Who proposed raising the timeout to 15 seconds, and who objected?
**expected:** Oleg proposed it after the 2026-09-14 staging incident; Irina objected (it masks the problem), then agreed on a review date  
**expected sources:** {'sources': ['meetings/2026-09-14-ledger-sync.txt']}

### memory-eval-both (completed, 8.4s, 2 tool calls)
queries: ['timeout 15 seconds proposed objected raised to 15 seconds who proposed who objec', 'gateway-timeout objected objection 15 seconds meeting September 14 2026 Oleg Mar']

In memory, I found two relevant statements about the 15-second timeout, both from **meetings/2026-09-14-ledger-sync.txt** dated **2026-09-14**:

- **Oleg Prikhodko** proposed it: “temporarily raise the timeout to fifteen seconds…”  
  Source: `meetings/2026-09-14-ledger-sync.txt` — **2026-09-14**

- **Marat Yusupov** also recorded it as the timeout to be fixed temporarily: “фиксируем таймаут пятнадцать секунд…”  
  Source: `meetings/2026-09-14-ledger-sync.txt` — **2026-09-14**

I did **not** find a clear objection in memory to that proposal. The retrieved items only show agreement / related follow-up, not an explicit objector.

Retrieved:
- `meetings/2026-09-14-ledger-sync.txt` — **2026-09-14**: Oleg proposed 15 seconds.
- `meetings/2026-09-14-ledger-sync.txt` — **2026-09-14**: Marat recorded the temporary 15-second timeout.
- `meetings/2026-09-21-ledger-sync.txt` — **2026-09-21**: timeout still 15 seconds, review next week.

So the answer is: **Oleg Prikhodko proposed raising it to 15 seconds; no objector is in memory.**

### memory-eval-graph (completed, 10.0s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'timeout' ", "MATCH (o:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'timeout' ", "MATCH (d:Decision)-[:ABOUT]->(t:Topic {name:'gateway-timeout'})\nOPTIONAL MATCH ("]

I found the timeout topic in memory, but I **cannot identify who proposed 15 seconds vs who objected** from the retrieved records.

What I retrieved:
- **2026-09-14**, `meetings/2026-09-14-ledger-sync.txt`: “фиксируем таймаут пятнадцать секунд временно пересмотр через две недели олег владелец”
- **2026-09-14**, `meetings/2026-09-14-ledger-sync.txt`: open item “временно но с датой пересмотра”
- Related current decision history on `gateway-timeout`:
  - **2026-08-24**, `confluence/decision-log.xhtml`: timeout 5 s
  - **2026-08-31**, `meetings/2026-08-31-ledger-sync.txt`: timeout 5 s
  - **2026-09-07**, `meetings/2026-09-07-ledger-sync.txt`: timeout 5 s
  - **2026-09-14**, `meetings/2026-09-14-ledger-sync.txt`: timeout 15 s, owner(s) listed as Oleg Prikhodko and Marat Yusupov
  - **2026-09-28**, `meetings/2026-09-28-ledger-sync.txt`: timeout 10 s, superseded later
  - **2026-10-02**, `meetings/2026-10-02-ledger-sync.txt`: timeout 10 s

So, for your exact question, the answer is **not in memory**.

### memory-eval-vector (completed, 4.3s, 3 tool calls)
queries: ['Who proposed raising the timeout to 15 seconds, and who objected?', 'raised the timeout to 15 seconds objected', 'timeout to 15 seconds proposal objection']

The proposal to raise the timeout to 15 seconds was made by **Oleg Prikhodko**. Source: **meetings/2026-09-14-ledger-sync.txt** (2026-09-14).

The memory hits I retrieved do **not** show a specific objection to that proposal. I found:
- **Marat Yusupov**: “фиксируем таймаут пятнадцать секунд…” on **meetings/2026-09-14-ledger-sync.txt** (2026-09-14)
- **Marat Yusupov**: “Таймаут: 15 секунд; пересмотр на следующей неделе.” on **meetings/2026-09-21-ledger-sync.txt** (2026-09-21)

So, based on memory, **the objector is not in memory**.

## q13 [ru / attribution] Кто из финансов участвует и что он обещал?
**expected:** Тим Хорват (с 2026-09-07): мэппинг кодов тарифов у финансов, в проде с 2026-10-01; сверку сумм после dry run, но не сам прогон  
**expected sources:** {'sources': ['meetings/2026-09-07-ledger-sync.txt', 'meetings/2026-10-02-ledger-sync.txt', 'confluence/tariff-migration-plan.xhtml']}

### memory-eval-both (completed, 8.1s, 2 tool calls)
queries: ['финансы участвуют обещал обещали участие finance promised who from finance', 'финансы обещал кто из финансов участвует обещал сделать mapping confirmation liv']

В памяти есть только косвенные совпадения по теме «финансы», но не явное имя человека из финансов, который участвует.

Что удалось найти:
- **Tim Horvat** — в документе про миграцию тарифов сказано, что он **owns the confirmation**: «finance-export keeps writing legacy_code until finance confirms their mapping is live; Tim Horvat owns that confirmation».  
  **Источник:** `confluence/tariff-migration-plan.xhtml`, **2026-09-16**
- Также есть запись: «Мэппинг кодов у финансов в тесте на следующей неделе.»  
  **Источник:** `meetings/2026-09-21-ledger-sync.txt`, **2026-09-21**

Но на вопрос **«Кто из финансов участвует и что он обещал?»** памяти не хватает однозначного ответа: я не вижу, чтобы явно был назван «человек из финансов» с обещанием в одной записи. Поэтому это **not in memory** в явном виде.

Если хотите, я могу дальше искать по:
1. именам людей, связанным с finance/tariffs,
2. обещаниям про mapping / test / confirmation,
3. или по конкретной встрече, если вы ее помните.

### memory-eval-graph (completed, 9.5s, 3 tool calls)
queries: ["MATCH (p:Person)-[:OWNS]->(t:Topic)\nWHERE toLower(p.name) CONTAINS 'finance' OR ", "MATCH (p:Person)\nWHERE toLower(p.name) CONTAINS 'finance' OR toLower(p.key) CONT", 'MATCH (p:Person)-[:OWNS]->(d:Decision)\nWHERE NOT (d)<-[:SUPERSEDES]-()\nOPTIONAL ']

В памяти есть несколько людей из финансов, но по вашему вопросу однозначно могу назвать только участие **Tim Horvat**.

- **Tim Horvat** участвует в теме **tariffs**.  
  Источник: `meetings/2026-09-21-ledger-sync.txt` и `meetings/2026-09-07-ledger-sync.txt`  
  Даты: **2026-09-21**, **2026-09-07**  
  Что обещал / зафиксировано за ним:
  - «Мэппинг кодов у финансов в тесте на следующей неделе.» — `meetings/2026-09-21-ledger-sync.txt`, **2026-09-21**
  - «в v2 добавляю поле legacy code обязательное и экспорт пишет его а не новый код» — `meetings/2026-09-07-ledger-sync.txt`, **2026-09-07**

Если вы имели в виду **конкретного человека из финансов** или **конкретное обещание**, то в памяти это не выделено отдельным явным вопросом.  
Что я дополнительно просмотрел: владельцев решений по людям с совпадением на “finance”, и общего списка активных решений. Там также есть **Dasha Volkova**, **Marat Yusupov**, **Oleg Prikhodko**, но связь именно с “финансами” в явном виде по результату запроса не подтверждена.

### memory-eval-vector (completed, 4.6s, 3 tool calls)
queries: ['Кто из финансов участвует и что он обещал?', 'финансы участвует обещал', 'кто из финансов участвует что обещал']

Из финансов в памяти фигурирует **Tim Horvat**.

Что он обещал:
- **«Мэппинг кодов у финансов в тесте на следующей неделе.»** — источник: `meetings/2026-09-21-ledger-sync.txt`, дата **2026-09-21**.
- Также в документе указано, что **Tim Horvat owns confirmation** по запуску mapping’а: finance-export продолжает писать `legacy_code`, пока finance не подтвердит, что их mapping live. — источник: `confluence/tariff-migration-plan.xhtml`, дата **2026-09-16**.

Если вам нужен именно ответ на вопрос «кто из финансов участвует» в смысле присутствует в встречах, в памяти есть только эти упоминания; там **не сказано, что он сам “из финансов”**, но он связан с подтверждением mapping’а. Источники: `meetings/2026-09-21-ledger-sync.txt` (2026-09-21), `confluence/tariff-migration-plan.xhtml` (2026-09-16).

## q14 [ru / unowned] Кто делает dry run миграции тарифов на копии прода?
**expected:** никто; вопрос поднимался 08-31, 09-07, 09-14, 09-21, 09-28, 10-02 и остался без владельца, записан в риски катовера  
**expected sources:** {'sources': ['meetings/2026-08-31-ledger-sync.txt', 'meetings/2026-10-02-ledger-sync.txt', 'confluence/tariff-migration-plan.xhtml']}

### memory-eval-both (completed, 4.9s, 1 tool calls)
queries: ['dry run миграции тарифов на копии прода кто делает ownership owner person dry ru']

В памяти **не найдено, кто именно делает** dry run миграции тарифов на копии прода.

Что удалось найти:
- **2026-10-02**, `meetings/2026-10-02-ledger-sync.txt` — открытый item: “Dry run миграции на копии прода.”, **без владельца**.
- **2026-08-31**, `meetings/2026-08-31-ledger-sync.txt` — открытый item: “кто сделает dry run миграции тарифов на копии прода до бэкфила — это обязательно.”, **без владельца**.
- **2026-09-09**, `confluence/decision-log.xhtml` — open item: “tariff migration dry run on a copy of production data — no owner yet.”

Итого: **no owner** по найденным записям, даты: **2026-08-31, 2026-09-09, 2026-10-02**.

### memory-eval-graph (completed, 8.2s, 4 tool calls)
queries: ["MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'dry run' OR toLower(t.name) CONT", "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(d.text) CONTAINS 'dry run' ", "MATCH (oi:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(oi.text) CONTAINS 'dry run", "MATCH (oi:OpenItem {key:'openitem:tariffs:2026-10-02'})-[:ABOUT]->(t:Topic)\nOPTI"]

В памяти это **не назначено**: у open item `openitem:tariffs:2026-10-02` на тему **tariffs** нет владельца.  
- Источник: **openitem:tariffs:2026-10-02**  
- Дата: **2026-10-02**  
- Текст: “Dry run миграции на копии прода”  

Также есть более ранние open item’ы по той же теме без владельца:
- **openitem:tariffs:2026-09-09** — “tariff migration dry run on a copy of production data — no owner yet.”  
- **openitem:tariffs:2026-09-07** — “дрy ран миграции тарифов кто нибудь взял?”  
- **openitem:tariffs:2026-08-31** — “dry run миграции тарифов на копии прода до бэкфила без владельца”

Если хотите, могу ещё проверить, не было ли позже решения, которое назначило ответственного.

### memory-eval-vector (completed, 6.3s, 3 tool calls)
queries: ['Кто делает dry run миграции тарифов на копии прода?', 'dry run миграции тарифов копия прода кто делает', 'миграция тарифов dry run prod copy owner']

В памяти это **не назначено**: для dry run миграции тарифов на копии прода найдено, что **владелец отсутствует / вопрос открыт**.

Что нашёл:
- `meetings/2026-08-31-ledger-sync.txt` — 2026-08-31: «кто сделает dry run миграции тарифов на копии прода до бэкфила — это обязательно»; статус **open_item**, **без владельца**.
- `meetings/2026-08-31-ledger-sync.txt` — 2026-08-31: «dry run миграции тарифов на копии прода до бэкфила пока без владельца; вопрос открыт».
- `confluence/decision-log.xhtml` — 2026-09-09: «tariff migration dry run on a copy of production data — no owner yet».
- `meetings/2026-10-02-ledger-sync.txt` — 2026-10-02: «Dry run миграции на копии прода»; тоже как **active open_item**.

Итого: **no owner** по состоянию на самые свежие записи в памяти.

## q15 [en / unowned] What is blocking phase 1 of the tariff migration?
**expected:** phase 0, the dry run on a production snapshot, has no owner  
**expected sources:** {'sources': ['confluence/tariff-migration-plan.xhtml', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 3.3s, 1 tool calls)
queries: ['blocking phase 1 tariff migration blocker phase 1 tariff migration open item dec']

Phase 1 of the tariff migration is blocked by Phase 0.

- **Source:** `confluence/tariff-migration-plan.xhtml` — **2026-09-16**
- Retrieved claim: “Tariff v2 migration plan. Phase 0 has no owner. Phase 1 is blocked on it.”

What I found:
- **Phase 0**: dry run of the backfill script against a production snapshot; compare row counts and sums per `legacy_code` with the finance export; **owner TBD**; target before Phase 1.
- **Phase 1**: create v2 tables, backfill from v1; owner Dasha; target 2026-09-23.

So the blocker is the unfinished **Phase 0** work, specifically the dry run/comparison step.

### memory-eval-graph (completed, 7.1s, 3 tool calls)
queries: ["MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'tariff migration' OR toLower(t.k", "MATCH (oi:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(oi.text) CONTAINS 'phase 1", "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'tariff mi"]

Not in memory.

I searched the graph memory for:
- a topic matching “tariff migration” — nothing found
- open items mentioning “phase 1” and tariff — nothing found
- decisions mentioning “tariff migration” — nothing found

Because the stores do not contain a matching topic, decision, or open item, I can’t determine what is blocking phase 1 from memory.

### memory-eval-vector (completed, 5.3s, 3 tool calls)
queries: ['What is blocking phase 1 of the tariff migration?', 'phase 1 tariff migration blocked by', 'tariff migration phase 1 blocker']

Phase 1 of the tariff migration is blocked by Phase 0 being unfinished: “Phase 0 has no owner. Phase 1 is blocked on it.” Source: `confluence/tariff-migration-plan.xhtml` (2026-09-16).

Related retrieved items:
- Phase 0: “Dry run of the backfill script against a production snapshot; compare row counts and sums per legacy_code with the finance export. Owner TBD. Target before phase 1.” Source: `confluence/tariff-migration-plan.xhtml` (2026-09-16).
- Phase 1: “Create v2 tables, backfill from v1. Owner Dasha. Target 2026-09-23.” Source: `confluence/tariff-migration-plan.xhtml` (2026-09-16).

So, in memory, the blocker is Phase 0’s unresolved ownership/completion.

## q16 [ru / crosslingual] Что в митингах называли бюджетом ретраев и где это описано в документации?
**expected:** retry budget из docs/gateway.md: доля повторов за минуту, 20%; в митингах 'бюджет ретраев' / 'повторы'  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-21-ledger-sync.txt', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 8.0s, 3 tool calls)
queries: ['бюджет ретраев retry budget meetings documentation what was called retry budget ', 'gateway policy retry limit budget retries documentation policy gateway policy re', 'policy gateway retries budget document retry budget gateway policy source docs']

В митингах под **«бюджетом ретраев»** называли лимит/политику повторов на уровне **gateway** и **роутов с повторами**, чтобы не устроить шторм:

- **«retry budget на роуты где повторы есть, чтобы не было шторма»** — источник: `meetings/2026-08-31-ledger-sync.txt`, дата **2026-08-31**.
- **«бюджет ретраев будет в политике гейтвея, олег опишет это в доке»** — источник: `meetings/2026-08-31-ledger-sync.txt`, дата **2026-08-31**.

Где это описано в документации:
- `docs/idempotency.md`, дата **2026-09-12**:  
  **«the gateway can enable retries on /ledger/charge; see the gateway policy for the retry limit and budget.»**

Также есть связанная запись-решение:
- `confluence/decision-log.xhtml`, дата **2026-08-31**:  
  **«No retries on /ledger/charge until idempotency is in place. Retry policy owned by Oleg.»**

Итог: в митингах это связывали с **retry policy / retry budget для gateway**, а в документации прямой отсылкой к **gateway policy** в `docs/idempotency.md` от **2026-09-12**.

### memory-eval-graph (completed, 7.3s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'retry' OR", "MATCH (doc:Document)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'retry' ", "MATCH (f:Fact)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'retry' OR toL"]

В митингах «бюджетом ретраев» называли **retries / retry policy**: в записи решения от **2026-08-31** сказано: «**Retry policy owned by Oleg**» и что на `/ledger/charge` пока **no retries** до появления idempotency. Источник: **confluence/decision-log.xhtml**, дата **2026-08-31**.

В документации ближайшее описание — документ **docs/idempotency.md** от **2026-09-12**: там говорится, что для безопасного повтора `POST /charge` нужен **Idempotency-Key**, который хранится 24 часа, и повторный запрос с тем же ключом возвращает исходный `charge id` и не списывает деньги повторно. Источник: **docs/idempotency.md**, дата **2026-09-12**.

Что я нашёл в памяти:
- **Decision:** `decision:retries:2026-08-31` — про retry policy. Источник: **confluence/decision-log.xhtml**, **2026-08-31**.
- **Decision:** `decision:charge:2026-09-12` — про idempotency для повторов `/charge`. Источник: **docs/idempotency.md**, **2026-09-12**.

Если хотите, я могу ещё попробовать найти, есть ли в памяти прямое употребление именно фразы **«бюджет ретраев»**.

### memory-eval-vector (completed, 5.8s, 3 tool calls)
queries: ['Что в митингах называли бюджетом ретраев и где это описано в документации?', 'бюджет ретраев', 'retry budget']

В митингах под «бюджетом ретраев» называли лимит/процент ретраев в политике gateway для `/ledger/charge`:

- 2026-09-21: «Бюджет ретраев для charge: 20%.» — источник: `meetings/2026-09-21-ledger-sync.txt`  
- 2026-09-28: «Таймаут десять секунд с бюджетом ретраев двадцать процентов.» — источник: `meetings/2026-09-28-ledger-sync.txt`  
- 2026-10-02: «таймаут 10 секунд, ретраи 2, бюджет 20, ранбук в доке» — источник: `meetings/2026-10-02-ledger-sync.txt`

В документации это описано в:

- `docs/idempotency.md` от 2026-09-12: «Once every caller sends keys, the gateway can enable retries on /ledger/charge; see the gateway policy for the retry limit and budget.»

Смысл по памяти: ретраи для charge включаются на gateway, а сам лимит/бюджет ретраев вынесен в gateway policy. Источник: `docs/idempotency.md` (2026-09-12) и митинги выше.

Если хотите, я могу отдельно собрать, **какая именно формулировка про “retry budget” встречалась в доке gateway policy**, если она есть в памяти.

## q17 [en / crosslingual] When was the cutover date agreed and what did the team say about the error budget?
**expected:** 2026-09-28; cutover on 2026-10-09 at 10:00 fits within the half of the monthly error budget reserved for planned work  
**expected sources:** {'sources': ['meetings/2026-09-28-ledger-sync.txt', 'docs/slo.md']}

### memory-eval-both (completed, 5.7s, 2 tool calls)
queries: ['cutover date agreed error budget team said error budget cutover', "MATCH (t:Topic) WHERE t.key CONTAINS 'cutover' OR toLower(t.name) CONTAINS 'cuto"]

The cutover date was agreed as **9 October 2026**, from **meetings/2026-09-28-ledger-sync.txt** dated **2026-09-28**.

About the error budget, the team said **half of the downtime/error budget is reserved for planned work such as the gateway cutover; the other half is the operational budget**. Source: **meetings/2026-08-31-ledger-sync.txt** dated **2026-08-31**. A matching document note also says **half of the downtime budget is reserved for planned work such as the gateway cutover** in **docs/slo.md** dated **2026-08-27**.

Retrieved:
- **meetings/2026-09-28-ledger-sync.txt** — cutover on 2026-10-09
- **meetings/2026-08-31-ledger-sync.txt** — half the budget reserved for planned work
- **docs/slo.md** — same error-budget note



### memory-eval-graph (completed, 8.1s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'cutover' ", 'MATCH (x)\nWHERE (x:Decision OR x:Fact OR x:OpenItem) AND (toLower(coalesce(x.tex', "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'slo' OR t"]

The cutover date was agreed on **2026-09-28** in **meetings/2026-09-28-ledger-sync.txt**; the decision text says **“Катовер девятого октября.”** The matching cutover decision is **decision:cutover:2026-09-28**. Source/date: **meetings/2026-09-28-ledger-sync.txt, 2026-09-28**.

About the error budget, the team said on **2026-08-31** in **meetings/2026-08-31-ledger-sync.txt**: **“200 ms p95, три девятки, половина бюджета ошибок под плановые работы”**. Source/date: **meetings/2026-08-31-ledger-sync.txt, 2026-08-31**.

If you want, I can also pull the exact meeting entries or check whether there is a newer cutover decision that supersedes the 2026-09-28 one.

### memory-eval-vector (completed, 5.8s, 3 tool calls)
queries: ['When was the cutover date agreed and what did the team say about the error budge', 'cutover date agreed error budget team said', 'agreed cutover date error budget']

I found memory on the cutover and the budget, but not a single chunk that states the exact agreed cutover date.

What I did retrieve:
- `docs/slo.md` (2026-08-27): “Half of the downtime budget is reserved for planned work such as the gateway cutover; the other half is the operational budget.”
- `meetings/2026-08-31-ledger-sync.txt` (2026-08-31): “slo док выложила 200 ms p95, три девятки, половина бюджета ошибок под плановые работы.”  
- `docs/runbook-cutover.md` (2026-09-30): the cutover runbook was updated, but this chunk does not state the cutover date itself.

So, from memory:
- Error budget: the team said half of the downtime/error budget was reserved for planned work like the gateway cutover, and the other half was for operational use (`docs/slo.md`, 2026-08-27; `meetings/2026-08-31-ledger-sync.txt`, 2026-08-31).
- Cutover date agreed: not in memory.

## q18 [en / temporal] List every decision about the gateway timeout in order with dates.
**expected:** 2026-08-24 5 s (Oleg); 2026-09-14 15 s temporary (Oleg, Irina objected); 2026-09-28 10 s with 20% retry budget (Irina's proposal, Oleg owner)  
**expected sources:** {'sources': ['memory/decisions.jsonl']}

### memory-eval-both (completed, 7.2s, 3 tool calls)
queries: ['gateway timeout decision', 'gateway timeout superseded', 'topic gateway-timeout decision 10 seconds 15 seconds 5 seconds']

Here are the gateway-timeout decisions in date order, from memory:

1. **2026-08-24** — Gateway upstream timeout set to **5 s on all Ledger routes**.  
   Source: `confluence/decision-log.xhtml` (`2026-08-24-gateway-timeout`), dated **2026-08-24**.

2. **2026-09-14** — Timeout temporarily raised to **15 s** while the database issue is investigated; review in two weeks.  
   Source: `meetings/2026-09-14-ledger-sync.txt`, dated **2026-09-14**.

3. **2026-09-28** — Timeout set to **10 s** with a **20% retry budget**.  
   Source: `meetings/2026-09-28-ledger-sync.txt`, dated **2026-09-28**.

Notes:
- I also found an **open item** on **2026-09-21** saying “Таймаут: 15 секунд; пересмотр на следующей неделе,” but it was marked as an **open_item**, not a decision. Source: `meetings/2026-09-21-ledger-sync.txt`, dated **2026-09-21**.

If you want, I can also include the related owner/history details for each decision.

### memory-eval-graph (completed, 14.6s, 4 tool calls)
queries: ["MATCH (t:Topic)<-[:ABOUT]-(d:Decision)\nWHERE toLower(t.name) CONTAINS 'gateway t", "MATCH (d:Decision)\nWHERE toLower(d.text) CONTAINS 'gateway timeout' OR toLower(d", "MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'timeout' OR toLower(t.key) CONTA", "MATCH (t:Topic)<-[:ABOUT]-(d:Decision)\nWHERE t.key IN ['gateway-timeout','topic:"]

Here are the gateway-timeout decisions in chronological order, using the current decision records in memory:

1. 2026-08-24 — “Gateway upstream timeout 5 s on all Ledger routes.”  
   Source: `confluence/decision-log.xhtml`  
   Status: active  
   Topic: `gateway-timeout`

2. 2026-08-24 — “на новом гейтвее пять секунд на все роуты ledger”  
   Source: `meetings/2026-08-24-ledger-sync.txt`  
   Status: active  
   Topic: `topic:gateway-timeout`

3. 2026-08-24 — “Gateway upstream timeout 5 s on all Ledger routes.”  
   Source: `confluence/decision-log.xhtml`  
   Status: active  
   Topic: `topic:gateway-timeout`

4. 2026-08-31 — “таймаут пять секунд внесен в gateway md”  
   Source: `meetings/2026-08-31-ledger-sync.txt`  
   Status: active  
   Topic: `gateway-timeout`

5. 2026-09-07 — “по гейтвею стейджинг переведен таймаут пять секунд работает”  
   Source: `meetings/2026-09-07-ledger-sync.txt`  
   Status: active  
   Topic: `gateway-timeout`

6. 2026-09-14 — “фиксируем таймаут пятнадцать секунд временно пересмотр через две недели олег владелец”  
   Source: `meetings/2026-09-14-ledger-sync.txt`  
   Status: active  
   Topic: `gateway-timeout`

7. 2026-09-28 — “Таймаут десять с

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['List every decision about the gateway timeout in order with dates.', 'gateway timeout decision', 'timeout gateway']

Here are the gateway-timeout decisions in date order:

1. **2026-08-24** — **Gateway upstream timeout 5 s on all Ledger routes.**  
   Source: `confluence/decision-log.xhtml` (decision log), dated **2026-08-24**.

2. **2026-09-28** — **Таймаут десять секунд с бюджетом ретраев двадцать процентов.**  
   Source: `meetings/2026-09-28-ledger-sync.txt`, dated **2026-09-28**.

These two chunks disagree: the newer decision changes the timeout from **5 s** to **10 s**. The current decision is the newer one unless there is a later superseding decision in memory, and I did not retrieve one.

## q19 [ru / fact] Когда катовер и во сколько?
**expected:** 2026-10-09 в 10:00  
**expected sources:** {'sources': ['meetings/2026-09-28-ledger-sync.txt', 'docs/runbook-cutover.md']}

### memory-eval-both (completed, 4.0s, 2 tool calls)
queries: ['катовер дата и время cutover when at what time Ledger billing', 'cutover runbook date time scheduled at what time ledger traffic nginx front edge']

Не нашёл в памяти конкретных даты и времени катовера.

Что удалось найти:
- Есть решение/упоминание о катовере Ledger traffic с nginx front на Edge gateway в `docs/runbook-cutover.md` от **2026-09-30**.
- Также есть связь с cutover в `docs/slo.md` от **2026-08-27**: часть downtime budget зарезервирована для planned work, включая gateway cutover.

Но **время катовера** в найденных записях не указано.  
Если хотите, я могу ещё поискать по meeting notes или decision log, где могло быть расписание.

### memory-eval-graph (completed, 5.7s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(t.name) CONTAINS 'катовер' ", "MATCH (d:Decision {key:'decision:cutover:2026-10-09'}) RETURN d.date AS date, d."]

Катовер — **9 октября**. Источник: `meetings/2026-09-28-ledger-sync.txt`, дата **2026-09-28**.  

Во сколько — **в памяти не найдено**. Я нашёл только:
- `meetings/2026-09-28-ledger-sync.txt` — «Катовер девятого октября», дата **2026-09-28**
- `docs/runbook-cutover.md` — «Cutover of Ledger traffic from the nginx front to the Edge gateway», дата **не удалось извлечь из памяти**

### memory-eval-vector (completed, 3.0s, 3 tool calls)
queries: ['Когда катовер и во сколько?', 'катовер дата время', 'cutover date time']

Катовер — **9 октября 2026**. В найденных записях **время не указано**.

Источник: `meetings/2026-09-28-ledger-sync.txt` (решение от **2026-09-28**: «Катовер девятого октября.»).

Нашёл также обновлённый runbook: `docs/runbook-cutover.md` (**2026-09-30**), но там есть только описание катовера, без времени.

Если хотите, могу ещё поискать точное время катовера в памяти.

## q20 [ru / contradiction] Decision log в Confluence актуален?
**expected:** нет, последняя версия 2026-09-09; в нём нет решений после 09-07: 15 с, ретраи на charge, передача ретраев Даше, 10 с, дата катовера, владелец отката  
**expected sources:** {'sources': ['confluence/decision-log.xhtml', 'memory/decisions.jsonl']}

### memory-eval-both (completed, 5.7s, 2 tool calls)
queries: ['Decision log Confluence актуален current up to date stale updated decision log C', 'confluence decision log updated date current stale superseded latest entry decis']

В memory есть записи из `confluence/decision-log.xhtml`, но по ним нельзя подтвердить, что весь Decision log «актуален» целиком.

Что удалось найти:
- `2026-09-09` — запись по topic `tariffs`, kind `open_item` (“tariff migration dry run on a copy of production data — no owner yet”) в `confluence/decision-log.xhtml` от `2026-09-09`.
- `2026-09-07` — decision по `idempotency` в `confluence/decision-log.xhtml`.
- `2026-08-31` — decision по `retries` в `confluence/decision-log.xhtml`.
- `2026-08-24` — decisions по `slo` и `gateway-timeout` в `confluence/decision-log.xhtml`.

Но ответа «да, актуален» или «нет, не актуален» в памяти нет: я не вижу отдельного статуса актуальности всего документа, только отдельные записи внутри него.  
Итого: **not in memory** для вопроса о полной актуальности документа.

Источник: `confluence/decision-log.xhtml`, даты записей `2026-09-09`, `2026-09-07`, `2026-08-31`, `2026-08-24`.

### memory-eval-graph (completed, 6.8s, 4 tool calls)
queries: ["MATCH (d:Document) WHERE toLower(d.file) CONTAINS 'decision log' OR toLower(d.ke", "MATCH (dec:Decision)-[:ABOUT]->(t:Topic) WHERE toLower(t.name) CONTAINS 'decisio", 'MATCH (d:Document) RETURN d.file AS file, d.key AS key, d.updated AS updated ORD', "MATCH (d:Document {file:'confluence/decision-log.xhtml'})-[:ABOUT]->(x) RETURN l"]

Не могу подтвердить актуальность Decision log в Confluence по памяти: в графе есть документ `confluence/decision-log.xhtml`, но у него нет даты обновления, и я не нашёл связанных решений/тем, чтобы сравнить и определить, устарел ли он.

Что удалось извлечь:
- `confluence/decision-log.xhtml` — найден как документ, `updated: null`, source: memory graph.
- Поиск по теме/решениям с “decision log” ничего не дал, source: memory graph.

Итого: **not in memory**.

### memory-eval-vector (completed, 6.3s, 3 tool calls)
queries: ['Decision log в Confluence актуален?', 'Актуален ли decision log в Confluence?', 'Decision log Confluence updated decision stale current']

В памяти есть только сам `confluence/decision-log.xhtml`, но не отдельное утверждение о том, что он **актуален / неактуален** как общий документ.

Что я нашёл:
- `confluence/decision-log.xhtml` — 2026-09-09: есть записи по тарифам, в т.ч. open item “tariff migration dry run on a copy of production data — no owner yet”. Источник: `confluence/decision-log.xhtml`, дата `2026-09-09`.
- `confluence/decision-log.xhtml` — 2026-09-07: decision по тарифам “Tariff v2 keeps legacy_code for the finance export; the field is mandatory.” Источник: `confluence/decision-log.xhtml`, дата `2026-09-07`.
- `confluence/decision-log.xhtml` — 2026-08-31: decision по retries “No retries on /ledger/charge until idempotency is in place.” Источник: `confluence/decision-log.xhtml`, дата `2026-08-31`.
- `confluence/decision-log.xhtml` — 2026-08-24: decision по SLO “POST /charge p95 latency SLO 200 ms.” Источник: `confluence/decision-log.xhtml`, дата `2026-08-24`.

Итог: **not in memory** — нет записи, которая прямо говорит, актуален ли decision log в Confluence как документ в целом. Могу только подтвердить, что в нём есть свежие записи на `2026-09-09`.

## q21 [en / attribution] Which decisions does Dasha own?
**expected:** tariff v2 with legacy_code (with Tim), idempotency keys, retry policy from 2026-09-21 including retries on /charge  
**expected sources:** {'sources': ['memory/decisions.jsonl']}

### memory-eval-both (completed, 11.7s, 4 tool calls)
queries: ['MATCH (p:Person {name:$name})-[:OWNS]->(d:Decision)\nRETURN d.key AS key, d.date ', 'MATCH (p:Person {name:$name})-[r:OWNS]->(d:Decision)\nRETURN d.key AS key, d.date', 'Dasha owns decisions owner Dasha OWNS Decision', "MATCH (p:Person)-[r:OWNS]->(d:Decision)\nWHERE toLower(p.name) CONTAINS 'dasha' O"]

Dasha owns these decisions in memory:

- `decision:tariffs:2026-10-02` — source: `meetings/2026-10-02-ledger-sync.txt` (date not available from graph result, retrieved via vector memory)
- `decision:idempotency:2026-09-12` — source: `docs/idempotency.md` (date not available from graph result, retrieved via vector memory)
- `decision:charge:2026-09-12` — source: `docs/idempotency.md` (date not available from graph result, retrieved via vector memory)
- `decision:idempotency:2026-09-12:body-mismatch` — source: `docs/idempotency.md` (date not available from graph result, retrieved via vector memory)
- `decision:tariffs:2026-09-07` — source: `confluence/decision-log.xhtml` (date not available from graph result, retrieved via vector memory)
- `decision:idempotency:2026-09-07` — source: `confluence/decision-log.xhtml` (date not available from graph result, retrieved via vector memory)
- `decision:idempotency:2026-08-31` — source: `meetings/2026-08-31-ledger-sync.txt` (date not available from graph result, retrieved via vector memory)
- `decision:tariffs:2026-08-24` — source: `meetings/2026-08-24-ledger-sync.txt` (date not available from graph result, retrieved via vector memory)
- `decis

### memory-eval-graph (completed, 3.9s, 2 tool calls)
queries: ['MATCH (p:Person {name:$name})- [o:OWNS]->(d:Decision)\nRETURN d.key AS decision_k', 'MATCH (p:Person {name:$name})- [o:OWNS]->(t:Topic)\nRETURN t.key AS topic_key, t.']

Not in memory.

I checked the graph for:
- decisions owned by `Person{name:"Dasha"}` — no matches
- topics owned by `Person{name:"Dasha"}` — no matches

I couldn’t retrieve any ownership records for Dasha from the memory store, so I can’t list any decisions she owns.

### memory-eval-vector (completed, 7.0s, 3 tool calls)
queries: ['Which decisions does Dasha own?', 'Dasha owns decisions', 'Who owns decisions Dasha']

Dasha owns these decisions/topics in memory:

- **Tariffs** — “Backend, tariffs are owned by Dasha Volkova.” Source: `confluence/ledger-architecture.xhtml` (2026-08-29).
- **Idempotency** — “пока нет ключей идемпотентности, ретраи на charge нельзя.” attributed to Dasha in `meetings/2026-08-31-ledger-sync.txt` (2026-08-31). This is a decision, not an ownership claim, but it is the only Dasha decision hit on that topic.
- **Charge retry policy / charge** — ownership transferred to Dasha on 2026-09-21. Source: `meetings/2026-09-21-ledger-sync.txt` (2026-09-21): “Политика ретраев для charge переходит от Олега к Даше с 2026-09-21.”
- **Tariff v2 migration plan phases** — multiple Dasha-owned items in `confluence/tariff-migration-plan.xhtml` (2026-09-16):
  - Phase 1: create v2 tables, backfill from v1
  - Phase 2: dual-write v1 and v2
  - Phase 4: drop v1 after one billing cycle
  - Phase 3 is **jointly owned by Dasha and Oleg**.

Notes:
- The memory does **not** contain a single consolidated list of “all decisions Dasha owns.”
- It does show **tariffs** as an active ownership claim, and several Dasha-owned migration decisions/tasks under the tariff plan.

If you want, I can also turn t

## q22 [en / fact] How long does the Edge gateway cache /ledger/tariffs?
**expected:** 60 s  
**expected sources:** {'sources': ['docs/gateway.md']}

### memory-eval-both (completed, 6.8s, 2 tool calls)
queries: ['Edge gateway cache /ledger/tariffs TTL duration cache /ledger/tariffs', "MATCH (t:Topic)\nWHERE toLower(t.name) CONTAINS 'tariff' OR toLower(t.key) CONTAI"]

Not in memory.

I found memory about `/tariffs` and tariff schema/latency, but nothing that states how long the Edge gateway caches `/ledger/tariffs`.

Retrieved:
- `docs/overview.md` — 2026-08-20: “GET /tariffs returns the active tariff catalogue.”
- `docs/slo.md` — 2026-08-27: “GET /tariffs has a latency objective of 100 ms p95.”
- `meetings/2026-10-02-ledger-sync.txt` — 2026-10-02: tariff field discussion, not cache duration.
- `meetings/2026-09-21-ledger-sync.txt` — 2026-09-21: tariff mapping discussion, not cache duration.
- `meetings/2026-09-07-ledger-sync.txt` — 2026-09-07: legacy code/export discussion, not cache duration.
- `confluence/decision-log.xhtml` — 2026-09-07: tariff v2 decision, not cache duration.

If you want, I can also search for “Edge gateway”, “cache”, “TTL”, or “/ledger/tariffs” more narrowly.

### memory-eval-graph (completed, 6.6s, 3 tool calls)
queries: ["MATCH (t:Topic) WHERE toLower(t.name) CONTAINS 'edge gateway' OR toLower(t.key) ", "MATCH (d:Decision)-[:ABOUT]->(t:Topic)\nWHERE toLower(d.text) CONTAINS 'edge gate", "MATCH (o:OpenItem)-[:ABOUT]->(t:Topic)\nWHERE toLower(o.text) CONTAINS 'edge gate"]

Not in memory.

I retrieved:
- A current decision about the gateway, dated 2026-08-20: “Move ledger-api behind the Edge gateway instead of the old nginx front.” Source: decision `decision:gateway:2026-08-20`.
- A current decision about cutover, dated 2026-10-09: “Cutover of Ledger traffic from the nginx front to the Edge gateway.” Source: decision `decision:cutover:2026-10-09`.

I did not find any Topic, Decision, Document, or OpenItem in memory that mentions caching `/ledger/tariffs` or gives a cache duration.

### memory-eval-vector (completed, 4.6s, 3 tool calls)
queries: ['How long does the Edge gateway cache /ledger/tariffs?', 'Edge gateway cache /ledger/tariffs duration', 'cache /ledger/tariffs Edge gateway']

Not in memory.

What I retrieved:
- `docs/slo.md` (2026-08-27): “`GET /tariffs` has a latency objective of 100 ms p95.”
- `docs/runbook-cutover.md` (2026-09-30): cutover of Ledger traffic from nginx to the Edge gateway.
- `confluence/decision-log.xhtml` (2026-08-24): gateway upstream timeout is 5 s on all Ledger routes.
- `2026-08-24-ledger-sync.txt` (2026-08-24): meeting note about a 5 s gateway timeout for all Ledger routes.
- `docs/overview.md` (2026-08-20): ledger-api behind the Edge gateway / `/tariffs` endpoint exists.

I did not find a claim that states how long the Edge gateway caches `/ledger/tariffs`.
