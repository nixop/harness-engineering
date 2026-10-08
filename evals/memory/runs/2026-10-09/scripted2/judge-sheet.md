
## q01 [en / fact] What is the p95 latency SLO for POST /charge?
**expected:** 200 ms over 5 minutes  
**expected sources:** {'sources': ['docs/slo.md', 'meetings/2026-08-24-ledger-sync.txt']}

### memory-eval-both (completed, 2.2s, 1 tool calls)
queries: ['p95 latency SLO POST /charge topic:slo']

The p95 latency SLO for `POST /charge` is **200 ms over 5 minutes**.

Sources:
- `meetings/2026-08-24-ledger-sync.txt` — 2026-08-24
- `docs/slo.md` — updated 2026-08-27

The document `docs/slo.md` is newer than the meeting note, so it is the current source for this SLO.

### memory-eval-graph (completed, 3.4s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic}) WHERE NOT (d)<-[:SUPERSEDES]-']

The current p95 latency SLO for **POST /charge** is **200 ms over 5 minutes**.

Source: **meetings/2026-08-24-ledger-sync.txt**  
Date: **2026-08-24**

### memory-eval-vector (completed, 3.7s, 3 tool calls)
queries: ['What is the p95 latency SLO for POST /charge?', 'p95 latency SLO POST /charge', 'POST /charge latency SLO p95']

The p95 latency SLO for `POST /charge` is **200 ms over 5 minutes**.

Sources:
- `meetings/2026-08-24-ledger-sync.txt` — 2026-08-24: “POST /charge p95 latency SLO 200 ms over 5 minutes” and the meeting confirms “принимаем двести миллисекунд p95 на charge” (decision recorded as active).
- `docs/slo.md` — updated 2026-08-27: table lists `POST /charge | latency, p95 over 5 minutes | 200 ms`.



## q02 [ru / fact] Сколько хранится ключ идемпотентности у charge и с какой даты он обязателен?
**expected:** 24 часа; обязателен с 2026-09-15, две недели grace period  
**expected sources:** {'sources': ['docs/idempotency.md', 'meetings/2026-09-07-ledger-sync.txt']}

### memory-eval-both (completed, 2.6s, 1 tool calls)
queries: ['topic:idempotency charge how long is idempotency key retained mandatory from wha']

Ключ идемпотентности для `charge` хранится **24 часа** и обязателен **с 2026-09-15**.

Источники:
- `meetings/2026-09-07-ledger-sync.txt`, 2026-09-07 — «храним сутки… с пятнадцатого сентября обязательно»
- `docs/idempotency.md`, updated 2026-09-12 — «Ledger stores the key with the charge for 24 hours»; «The key is required from 2026-09-15»

### memory-eval-graph (completed, 3.7s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nWHERE NOT (d)<-[:SUPERSEDES]-']

Для **charge**:

- **Ключ идемпотентности хранится 24 часа** — источник: `meetings/2026-09-07-ledger-sync.txt`, дата решения **2026-09-07**.
- **Обязателен с 2026-09-15** — тот же источник и дата **2026-09-07**.

Если хотите, могу ещё проверить, есть ли у этого решения более ранняя история или связанные open item’ы по idempotency.

### memory-eval-vector (completed, 4.3s, 3 tool calls)
queries: ['Сколько хранится ключ идемпотентности у charge и с какой даты он обязателен?', 'ключ идемпотентности charge хранится сколько дней обязателен с какой даты', 'идемпотентности charge обязательный ключ дата хранения']

Ключ идемпотентности для `charge` хранится **24 часа**. Источник: `docs/idempotency.md` (updated **2026-09-12**) и подтверждение решением `meetings/2026-09-07-ledger-sync.txt` / claim D05 (**2026-09-07**).

Обязателен он **с 2026-09-15**. Источники:  
- `docs/idempotency.md` (updated **2026-09-12**) — “required from 2026-09-15”  
- `meetings/2026-09-07-ledger-sync.txt` (**2026-09-07**) — “с пятнадцатого сентября обязательно”  

If you want, I can also quote the exact lines from the sources.

## q03 [en / fact] Why does tariff v2 keep a legacy_code field?
**expected:** finance reconciles by the v1 code; finance-export writes legacy_code until the finance warehouse mapping is live  
**expected sources:** {'sources': ['docs/tariffs-v2.md', 'meetings/2026-09-07-ledger-sync.txt']}

### memory-eval-both (completed, 4.0s, 1 tool calls)
queries: ['tariff v2 legacy_code field why keep legacy_code rationale decision doc']

Tariff v2 keeps `legacy_code` because finance still reconciles charges by the v1 tariff code, and `finance-export` writes that legacy code into the CSV until the finance warehouse mapping is migrated. The field is mandatory.

Sources:
- `docs/tariffs-v2.md`, updated `2026-09-10`: “Finance systems reconcile charges by the v1 tariff code. Until the finance warehouse is migrated, every v2 tariff carries its v1 code in `legacy_code`, and `finance-export` writes `legacy_code`, not `code`, into the CSV.”
- `meetings/2026-09-07-ledger-sync.txt`, `2026-09-07`: “нам нужно чтобы в экспорте оставался старый код пока мы не перестроим мэппинг у себя…” and “в v2 добавляю поле legacy code обязательное…”

Also, there is a current decision on this topic:
- `meetings/2026-09-07-ledger-sync.txt`, decision dated `2026-09-07`: “Tariff v2 keeps a mandatory legacy_code field; finance-export writes legacy_code.”



### memory-eval-graph (completed, 3.4s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:tariffs'})\nWHERE NOT (d)<-[:SU"]

Tariff v2 keeps a mandatory `legacy_code` field because the current decision says so: “Tariff v2 keeps a mandatory legacy_code field; finance-export writes legacy_code.” Source: `meetings/2026-09-07-ledger-sync.txt`, dated `2026-09-07`.

There isn’t a rationale beyond that in memory — I only found the decision itself, not an explanatory note.

### memory-eval-vector (completed, 3.6s, 3 tool calls)
queries: ['Why does tariff v2 keep a legacy_code field?', 'tariff v2 legacy_code field', 'legacy_code tariff v2']

Tariff v2 keeps `legacy_code` because finance systems still reconcile charges by the v1 tariff code, and `finance-export` must write that old code into CSV until the finance warehouse is migrated. Source: `docs/tariffs-v2.md` (updated 2026-09-10), section `legacy_code`.

The underlying decision was made on 2026-09-07 in `meetings/2026-09-07-ledger-sync.txt`: v2 would add a mandatory `legacy_code` field so the export could keep using the old code while the team rebuilt its mapping. Source: `meetings/2026-09-07-ledger-sync.txt` (2026-09-07).

If you want, I can also quote the exact lines from the meeting note.

## q04 [ru / fact] Что такое retry budget и какое значение выбрали?
**expected:** доля повторных запросов от всех запросов к роуту за минуту, выше которой gateway перестаёт ретраить; 20%  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-21-ledger-sync.txt']}

### memory-eval-both (completed, 3.1s, 1 tool calls)
queries: ['retry budget chosen value topic:retries retry budget']

Retry budget — это ограничение на долю повторных запросов на маршрут: шлюз разрешает retries только пока число retried requests не превышает фиксированную долю от всех запросов за 1‑минутное окно. Это защищает Ledger от retry storm. Источник: `docs/gateway.md`, 2026-09-02.

Выбранное значение: **20%**. То есть не более одного retry на пять запросов; этот бюджет задаётся в gateway policy, а не в Ledger. Источник: `docs/gateway.md`, 2026-09-02.

Дополнительно в памяти есть решение по retries: на `/ledger/charge` разрешили максимум 2 retries и retry budget 20%. Источник: `meetings/2026-09-21-ledger-sync.txt`, 2026-09-21.

### memory-eval-graph (completed, 4.3s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nWHERE NOT (d)<-[:SUPERSEDES]-']

**Retry budget** — это доля запросов, которую можно потратить на повторные попытки (retries). В найденном решении выбрали **20%**.

Источник: `meetings/2026-09-21-ledger-sync.txt`, дата `2026-09-21`.  
Там же зафиксировано решение: “Retries enabled on /ledger/charge: max 2 retries, retry budget 20%”.

Также отмечено примечание, что `docs/gateway.md` всё ещё говорит, что retries отключены на `/ledger/charge`, то есть документ устарел относительно решения того же дня.

### memory-eval-vector (completed, 4.2s, 3 tool calls)
queries: ['Что такое retry budget и какое значение выбрали?', 'retry budget значение выбрали', 'retry budget chosen value']

Retry budget — это доля всех запросов к маршруту, которую gateway разрешает использовать как ретраи в скользящем окне в одну минуту; если доля превышена, новые ретраи временно блокируются, чтобы не получить retry storm. Источник: `docs/gateway.md`, 2026-09-02.

Выбранное значение — 20% для маршрутов с ретраями. Это подтверждают:
- `meetings/2026-09-21-ledger-sync.txt`, 2026-09-21: «бюджет ретраев обязательно двадцать процентов»
- `docs/runbook-cutover.md`, 2026-09-30: для `/ledger/charge`, `/ledger/invoice/*`, `/ledger/tariffs` указан retry budget 20%.

Если нужно, могу ещё уточнить, где именно это значение применяется и для каких роутов ретраи включены.

## q05 [ru / temporal] Какой сейчас таймаут на gateway для Ledger и как он менялся?
**expected:** сейчас 10 с с retry budget 20% (2026-09-28); история: 5 с (08-24) → 15 с временно после инцидента (09-14) → 10 с (09-28)  
**expected sources:** {'sources': ['meetings/2026-08-24-ledger-sync.txt', 'meetings/2026-09-14-ledger-sync.txt', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 5.6s, 2 tool calls)
queries: ['topic:gateway-timeout current timeout changed history gateway Ledger', 'topic:gateway-timeout retry budget 20% 10 s 15 s 5 s history']

Сейчас таймаут gateway для Ledger — **10 секунд**. Это зафиксировано как текущая активная decision от **2026-09-28**: «Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value» из `meetings/2026-09-28-ledger-sync.txt`.

Как менялся:
- **2026-08-24** — **5 секунд** на все Ledger routes (`meetings/2026-08-24-ledger-sync.txt`), эта decision сейчас **superseded**.
- **2026-09-14** — временно подняли до **15 секунд** после staging incident (`meetings/2026-09-14-ledger-sync.txt`), эта decision тоже **superseded**.
- **2026-09-28** — снизили до **10 секунд** с **retry budget 20%** (`meetings/2026-09-28-ledger-sync.txt`), это **current**.

Дополнительно: документ `docs/gateway.md`, updated **2026-09-02**, всё ещё говорит про **5 seconds**, но он устарел, потому что позже есть decision от **2026-09-14** и особенно текущая decision от **2026-09-28**.

### memory-eval-graph (completed, 7.2s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:$topic})\nWHERE NOT (d)<-[:SUPERSEDES]', 'MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:$topic})\nRETURN d.date AS date, d.sta']

Сейчас таймаут gateway для Ledger — **10 s**. Это зафиксировано решением от **2026-09-28** в `meetings/2026-09-28-ledger-sync.txt` (status: active): “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value”.

Как менялся:
- **2026-08-24** — **5 s** на всех маршрутах Ledger, `meetings/2026-08-24-ledger-sync.txt` (status: superseded).
- **2026-09-14** — **15 s** временно после инцидента на staging, `meetings/2026-09-14-ledger-sync.txt` (status: superseded).
- **2026-09-28** — **10 s** и 20% retry budget, `meetings/2026-09-28-ledger-sync.txt` (status: active).

Если хотите, могу ещё отдельно сказать, **какой документ сейчас устарел по этому вопросу**.

### memory-eval-vector (completed, 7.4s, 3 tool calls)
queries: ['Какой сейчас таймаут на gateway для Ledger и как он менялся?', 'таймаут gateway Ledger', 'gateway timeout Ledger']

Сейчас актуальный таймаут на gateway для Ledger — **10 секунд**. Это зафиксировано в решении **D09** от **2026-09-28**: “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value” (`meetings/2026-09-28-ledger-sync.txt`, 2026-09-28).

Как он менялся:
- **5 секунд** — изначальное решение от **2026-08-24** (`meetings/2026-08-24-ledger-sync.txt`, 2026-08-24), сейчас оно **superseded**.
- **15 секунд** — временно подняли после инцидента на стенде от **2026-09-14** (`meetings/2026-09-14-ledger-sync.txt`, 2026-09-14), это решение **superseded**.
- **10 секунд** — текущее значение с **2026-09-28** (`meetings/2026-09-28-ledger-sync.txt`, 2026-09-28), решение **active**.

Важно: документ `docs/gateway.md` от **2026-09-02** всё ещё говорит про **5 секунд**, но он **устарел**, потому что более новое решение от **2026-09-28** его заменило (`docs/gateway.md`, 2026-09-02; `meetings/2026-09-28-ledger-sync.txt`, 2026-09-28).

Если хочешь, могу ещё кратко собрать это в виде таймлайна с датами и причинами изменений.

## q06 [en / temporal] What is the current gateway timeout for Ledger routes?
**expected:** 10 s with a 20% retry budget, decided 2026-09-28; the 15 s value was temporary  
**expected sources:** {'sources': ['meetings/2026-09-28-ledger-sync.txt', 'docs/runbook-cutover.md']}

### memory-eval-both (completed, 3.5s, 1 tool calls)
queries: ['topic:gateway-timeout current gateway timeout for Ledger routes timeout value cu']

The current gateway timeout for Ledger routes is **10 seconds**.

Source:
- **meetings/2026-09-28-ledger-sync.txt** — decision dated **2026-09-28**, status **active**: “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value.”

I also found an older, now superseded decision:
- **meetings/2026-08-24-ledger-sync.txt** — decision dated **2026-08-24**, status **superseded**: “Gateway upstream timeout 5 s on all Ledger routes.”

There is also a document updated **2026-09-30** that reflects the 10 s policy at cutover, but the decision on **2026-09-28** is the current source of truth.

### memory-eval-graph (completed, 3.3s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nWHERE NOT (d)<-[:SUPERSEDES]-']

The current gateway timeout for Ledger routes is **10 s**.

Source: **meetings/2026-09-28-ledger-sync.txt**, decision dated **2026-09-28**: “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value.”

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['What is the current gateway timeout for Ledger routes?', 'gateway timeout Ledger routes', 'timeout for routes gateway Ledger']

The current gateway timeout for Ledger routes is **10 s**.

Sources:
- `meetings/2026-09-28-ledger-sync.txt` — decision `D09`, dated **2026-09-28**, status **active**: “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value.”
- `docs/runbook-cutover.md` — updated **2026-09-30**: gateway policy table shows `/ledger/charge`, `/ledger/invoice/*`, and `/ledger/tariffs` at **10 s**.

I also found an older, superseded decision:
- `meetings/2026-08-24-ledger-sync.txt` — decision `D01`, dated **2026-08-24**, status **superseded**: “Gateway upstream timeout 5 s on all Ledger routes.”



## q07 [ru / temporal] Разрешены ли сейчас ретраи на /charge?
**expected:** да, с 2026-09-21: максимум 2 повтора, бюджет 20%, потому что ключи идемпотентности обязательны; до этого были запрещены  
**expected sources:** {'sources': ['meetings/2026-09-21-ledger-sync.txt', 'meetings/2026-08-31-ledger-sync.txt']}

### memory-eval-both (completed, 5.9s, 2 tool calls)
queries: ['topic:retries /charge retries allowed current decision', "MATCH (t:Topic {key:'topic:retries'})<-[:ABOUT]-(d:Decision)\nOPTIONAL MATCH (d)-"]

Да — сейчас ретраи на `/ledger/charge` разрешены.

- Решение от **2026-09-21**: “Retries enabled on /ledger/charge: max 2 retries, retry budget 20%”  
  **Источник:** `meetings/2026-09-21-ledger-sync.txt`  
- Это решение **активное** и **переопределяет** решение от **2026-08-31**, где ретраи были запрещены.  
  **Источник:** `meetings/2026-09-21-ledger-sync.txt` и `meetings/2026-08-31-ledger-sync.txt`

Примечание: найденный документ `docs/gateway.md` от **2026-09-02** устарел, потому что более новое решение от **2026-09-21** уже разрешает ретраи.

### memory-eval-graph (completed, 3.8s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nWHERE NOT (d)<-[:SUPERSEDES]-']

Да, сейчас ретраи на `/charge` разрешены.

- Решение: ретраи включены на `/ledger/charge`, максимум 2 ретрая, retry budget 20%.
- Источник: `meetings/2026-09-21-ledger-sync.txt`, дата `2026-09-21`.

Примечание: в заметке к решению указано, что `docs/gateway.md` всё ещё говорит, что ретраи отключены на `/ledger/charge`, то есть документ устарел относительно решения от `2026-09-21`.

### memory-eval-vector (completed, 4.5s, 3 tool calls)
queries: ['Разрешены ли сейчас ретраи на /charge?', 'ретраи на /charge', '/charge retries']

Да, сейчас ретраи на `/charge` разрешены: в решении от **2026-09-21** указано **“Retries enabled on /ledger/charge: max 2 retries, retry budget 20%”** в файле **`meetings/2026-09-21-ledger-sync.txt`**.  

При этом более старый документ **`docs/gateway.md`** (обновлён **2026-09-02**) всё ещё говорит, что retries на `/ledger/charge` **disabled**, то есть этот документ устарел относительно решения от **2026-09-21**.  

Источники:
- **`meetings/2026-09-21-ledger-sync.txt`**, **2026-09-21** — retries enabled on `/ledger/charge`, max 2 retries, budget 20%.
- **`docs/gateway.md`**, **2026-09-02** — retries disabled on `/ledger/charge` (устарело).


## q08 [en / contradiction] docs/gateway.md says the timeout is 5 seconds. Is that still true?
**expected:** no; the doc is stale (updated 2026-09-02). The timeout went to 15 s on 2026-09-14 and to 10 s on 2026-09-28; the cutover runbook has the current value  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-14-ledger-sync.txt', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 4.7s, 2 tool calls)
queries: ['gateway timeout 5 seconds docs/gateway.md timeout current decision', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:gateway-timeout'})\nOPTIONAL MA"]

No — `docs/gateway.md` is stale.

The current decision on `topic:gateway-timeout` is **10 s**, not 5 s:
- **decision:gateway-timeout:2026-09-28** — “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value”  
  Source: `meetings/2026-09-28-ledger-sync.txt`, date **2026-09-28**.

The 5-second setting in `docs/gateway.md` is from:
- `docs/gateway.md` — “The upstream timeout for every Ledger route is 5 seconds.”  
  Source: `docs/gateway.md`, updated **2026-09-02**.

Because the decision is newer than the document, the document is stale.

### memory-eval-graph (completed, 6.3s, 3 tool calls)
queries: ['MATCH (doc:Document {file:$file}) RETURN doc.key AS key, doc.title AS title, doc', "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway-timeout'}) RETURN d.key", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway-timeout'}) WHERE NOT (d"]

No. The current decision is **10 s**, not 5 s.

- **Current decision:** “Gateway timeout lowered to 10 s with a 20% retry budget; replaces the 15 s emergency value” — source **meetings/2026-09-28-ledger-sync.txt**, date **2026-09-28**.
- The old **5 s** setting was decided earlier and is now **superseded**:
  - “Gateway upstream timeout 5 s on all Ledger routes” — source **meetings/2026-08-24-ledger-sync.txt**, date **2026-08-24**.
- `docs/gateway.md` is **stale** for this topic; it was updated on **2026-09-02**, but the newer decision on **2026-09-28** changed the timeout after that.



### memory-eval-vector (completed, 4.7s, 3 tool calls)
queries: ['docs/gateway.md says the timeout is 5 seconds. Is that still true?', 'gateway timeout 5 seconds', 'timeout gateway 5 seconds updated decision']

No — `docs/gateway.md` is stale.

- `docs/gateway.md` says the upstream timeout is **5 seconds** and was updated **2026-09-02**. Source: `docs/gateway.md` (`Edge gateway integration`, `Timeouts`), updated 2026-09-02.
- A newer decision on the same topic says the gateway timeout was raised to **15 s** after the staging incident on **2026-09-14**, and notes that `docs/gateway.md` was never updated. Source: `meetings/2026-09-14-ledger-sync.txt`, decision `gateway timeout`, dated 2026-09-14, status **superseded**.
- The current active decision is newer still: the gateway timeout was lowered to **10 s** with a 20% retry budget on **2026-09-28**. Source: `meetings/2026-09-28-ledger-sync.txt`, decision `gateway timeout`, dated 2026-09-28, status **active**.

So the doc’s 5-second value is no longer the current state.

## q09 [ru / contradiction] В документации написано, что ретраи на /ledger/charge выключены. Это актуально?
**expected:** нет, gateway.md устарел; с 2026-09-21 ретраи на charge включены, 2 повтора, бюджет 20%  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-21-ledger-sync.txt']}

### memory-eval-both (completed, 5.6s, 2 tool calls)
queries: ['ретраи /ledger/charge выключены актуально retries charge documentation', "MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:retries'})\nOPTIONAL MATCH (d)-"]

Нет, это уже неактуально.

Текущая decision по `topic:retries` от **2026-09-21**: **retries enabled on `/ledger/charge`**, максимум **2 retries**, retry budget **20%**. Источник: `meetings/2026-09-21-ledger-sync.txt`.  
Она **supersedes** старую decision от **2026-08-31**, где retries на `/ledger/charge` были выключены. Источник: `meetings/2026-08-31-ledger-sync.txt`.

Документация `docs/gateway.md` с `updated 2026-09-02` уже устарела относительно более новой decision.

### memory-eval-graph (completed, 5.2s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:$topic})\nWHERE NOT (d)<-[:SUPERSEDES]']

Нет, это **неактуально**.

Текущая запись по теме `retries` говорит, что на `/ledger/charge` **ретраи включены**: максимум **2 retries**, retry budget **20%**.  
Источник: `meetings/2026-09-21-ledger-sync.txt`, дата `2026-09-21`.

В заметке к решению прямо сказано, что `docs/gateway.md` всё ещё пишет, что ретраи выключены, то есть документация **устарела**.  
Источник: то же решение `decision:retries:2026-09-21` из `meetings/2026-09-21-ledger-sync.txt`, дата `2026-09-21`.

Если хотите, могу ещё проверить, есть ли более ранние/поздние решения по retries и показать историю.

### memory-eval-vector (completed, 5.2s, 3 tool calls)
queries: ['В документации написано, что ретраи на /ledger/charge выключены. Это актуально?', 'ретраи на /ledger/charge выключены актуально', '/ledger/charge retries disabled current']

Нет, это уже неактуально.

- В решении от **2026-09-21** указано, что **ретраи на `/ledger/charge` включены**: максимум **2 retry**, бюджет **20%**. Источник: `meetings/2026-09-21-ledger-sync.txt`.
- В той же записи прямо сказано, что `docs/gateway.md` всё ещё пишет, будто ретраи выключены — значит документация **устарела**. Источник: `meetings/2026-09-21-ledger-sync.txt` от **2026-09-21**.
- Более старая документация `docs/gateway.md` от **2026-09-02** действительно говорит, что ретраи **disabled** на `/ledger/charge`, но это перекрыто более новым решением. Источник: `docs/gateway.md` от **2026-09-02**.

Итого: актуальное состояние — **ретраи включены**.

## q10 [en / contradiction] Who owns the rollback in the cutover runbook?
**expected:** the runbook says TBD but it is stale; Irina took rollback ownership on 2026-10-02  
**expected sources:** {'sources': ['docs/runbook-cutover.md', 'meetings/2026-10-02-ledger-sync.txt']}

### memory-eval-both (completed, 3.3s, 1 tool calls)
queries: ['MATCH (t:Topic {key:$topic})<-[:ABOUT]-(d:Decision)<-[o:OWNS]-(p:Person)\nWHERE o']

Irina Belova owns the rollback in the cutover runbook.

Source: `meetings/2026-10-02-ledger-sync.txt`, 2026-10-02.

### memory-eval-graph (completed, 4.4s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic}) WHERE NOT (d)<-[:SUPERSEDES]-', 'MATCH (p:Person)-[o:OWNS]->(:Topic {key:$topic}) WHERE o.to IS NULL RETURN p.key']

The rollback owner for the cutover is **Irina Belova**.

Source: `meetings/2026-10-02-ledger-sync.txt` — decision dated **2026-10-02**: “Rollback owner for the cutover is Irina.”

Note: the same decision also says `docs/runbook-cutover.md` still had rollback owner as TBD, so that document is stale as of 2026-10-02.

### memory-eval-vector (completed, 3.1s, 3 tool calls)
queries: ['Who owns the rollback in the cutover runbook?', 'rollback cutover runbook owner', 'cutover runbook rollback ownership']

The rollback owner for the cutover is **Irina Belova**. Source: **meetings/2026-10-02-ledger-sync.txt** (decision dated **2026-10-02**).

Note: the runbook draft is stale here; **docs/runbook-cutover.md** (updated **2026-09-30**) still says **“Rollback owner: TBD.”**

## q11 [ru / attribution] Кто сейчас отвечает за политику ретраев и с какого момента?
**expected:** Даша, с 2026-09-21; до этого Олег  
**expected sources:** {'sources': ['meetings/2026-09-21-ledger-sync.txt', 'meetings/2026-08-31-ledger-sync.txt']}

### memory-eval-both (completed, 4.7s, 1 tool calls)
queries: ["MATCH (t:Topic {key:$topic})<-[:ABOUT]-(d:Decision)\nWHERE d.status <> 'supersede"]

Сейчас за политику ретраев отвечает **person:dasha-volkova**; текущая запись об ответственности начинается с **2026-09-21**.

Источник:
- Decision `decision:retries:2026-09-21`, дата `2026-09-21`, источник `meetings/2026-09-21-ledger-sync.txt`
- связь OWNS для `topic:retries`: `from=2026-09-21`, `to=null`

Если хотите, могу ещё показать, был ли кто-то до этого ответственным.

### memory-eval-graph (completed, 8.3s, 2 tool calls)
queries: ['MATCH (p:Person)-[o:OWNS]->(t:Topic {key:$topic}) WHERE o.to IS NULL RETURN p.ke', 'MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic}) WHERE NOT (d)<-[:SUPERSEDES]-']

Сейчас за политику ретраев отвечает **Даша Волкова**. Это действует **с 2026-09-21**. Источник: `meetings/2026-09-21-ledger-sync.txt`, дата решения `2026-09-21`.

Дополнительно: в памяти есть активное решение по теме ретраев от `2026-09-21`: «Retries enabled on /ledger/charge: max 2 retries, retry budget 20%».

### memory-eval-vector (completed, 3.8s, 3 tool calls)
queries: ['Кто сейчас отвечает за политику ретраев и с какого момента?', 'политика ретраев владелец с какого момента', 'кто владеет политикой ретраев сейчас']

Сейчас за политику ретраев отвечает **Даша Волкова**, **с 2026-09-21**.

Источник:
- `meetings/2026-09-21-ledger-sync.txt` — 2026-09-21: «политика ретраев переходит от олега к даше с сегодняшнего дня».
- Подтверждающая запись об ownership: `meetings/2026-09-21-ledger-sync.txt` — 2026-09-21: `Owner: Dasha Volkova`.

Для контекста:
- Более старая запись `meetings/2026-08-31-ledger-sync.txt` — 2026-08-31 — указывала владельцем **Олега**, но она **superseded** и больше не актуальна.

## q12 [en / attribution] Who proposed raising the timeout to 15 seconds, and who objected?
**expected:** Oleg proposed it after the 2026-09-14 staging incident; Irina objected (it masks the problem), then agreed on a review date  
**expected sources:** {'sources': ['meetings/2026-09-14-ledger-sync.txt']}

### memory-eval-both (completed, 3.0s, 1 tool calls)
queries: ['proposed raising the timeout to 15 seconds objected timeout 15 seconds gateway t']

The proposal to raise the timeout to 15 seconds came from **Oleg Prikhodko** on **2026-09-14** in `meetings/2026-09-14-ledger-sync.txt`.

The objection came from **Irina Belova** on **2026-09-14** in the same meeting file.

Sources:
- `meetings/2026-09-14-ledger-sync.txt` — proposed by Oleg at `00:00:50`, objected by Irina at `00:00:58`
- The meeting claim is also reflected in the decision chunk dated `2026-09-14` (`decision:gateway-timeout:2026-09-14`)

### memory-eval-graph (completed, 9.1s, 3 tool calls)
queries: ["MATCH (o:OpenItem)-[:ABOUT]->(:Topic {key:'topic:gateway-timeout'})\nOPTIONAL MAT", "MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:gateway-timeout'})\nOPTIONAL MAT", "MATCH (o:OpenItem)-[:ABOUT]->(:Topic {key:'topic:retries'})\nOPTIONAL MATCH (o)<-"]

The memory has the timeout decisions, but not who proposed 15 seconds or who objected.

What I found:
- A decision on 2026-09-14: “Gateway timeout raised to 15 s temporarily after the staging incident; review in two weeks” — file `meetings/2026-09-14-ledger-sync.txt`.
- That decision is now superseded by the 2026-09-28 decision lowering it to 10 s — file `meetings/2026-09-28-ledger-sync.txt`.

I could not retrieve any person-level attribution for the proposal or objection, so the answer is **not in memory**.

### memory-eval-vector (completed, 2.1s, 1 tool calls)
queries: ['Who proposed raising the timeout to 15 seconds, and who objected?']

Олег предложил поднять таймаут до 15 секунд, а Ира возразила. Источник: `meetings/2026-09-14-ledger-sync.txt` / claim `decision:gateway-timeout:2026-09-14`, 2026-09-14.

## q13 [ru / attribution] Кто из финансов участвует и что он обещал?
**expected:** Тим Хорват (с 2026-09-07): мэппинг кодов тарифов у финансов, в проде с 2026-10-01; сверку сумм после dry run, но не сам прогон  
**expected sources:** {'sources': ['meetings/2026-09-07-ledger-sync.txt', 'meetings/2026-10-02-ledger-sync.txt', 'confluence/tariff-migration-plan.xhtml']}

### memory-eval-both (completed, 7.0s, 2 tool calls)
queries: ['финансы участвуют обещал promised finance participant what promised promise fina', "MATCH (p:Person)-[:ATTENDED]->(m:Meeting) WHERE toLower(p.name) CONTAINS 'financ"]

Не в памяти.

Что я нашёл:
- В векторном поиске есть упоминания о «финансах» и обещании Тимом:
  - `meetings/2026-09-21-ledger-sync.txt` — Тим сказал: «мэппинг кодов у финансов в тесте на следующей неделе скажу точно».
  - `meetings/2026-10-02-ledger-sync.txt` — Тим сказал: «мэппинг кодов у финансов в проде с первого октября можно планировать уход от legacy code но не раньше ноября».
- В графе я не нашёл участника с именем/алиасом, содержащим `finance`, поэтому не могу надёжно ответить, кто именно «из финансов» участвует.

Если хотите, я могу дальше поискать по конкретному человеку из финансов или по встречам, где обсуждался мэппинг кодов/legacy code.

### memory-eval-graph (completed, 15.7s, 2 tool calls)
queries: ["MATCH (p:Person)\nWHERE toLower(p.role) CONTAINS 'finance' OR any(a IN coalesce(p", "MATCH (p:Person {key:'person:tim-horvat'})-[:ATTENDED]->(m:Meeting)<-[:DECIDED_I"]

Из финансов участвует Тим Хорват; его роль в памяти — **finance systems**. Источник: `person:tim-horvat` / дата `2026-09-07`.

Что он обещал на встречах:
- по `topic:idempotency`: сделал обязательным `Idempotency-Key` на `/charge` с `2026-09-15`, retention ключа 24 часа, grace period 2 недели. Источник: `meetings/2026-09-07-ledger-sync.txt` / дата `2026-09-07`.
- по `topic:tariffs`: `tariff v2` сохраняет обязательное поле `legacy_code`; `finance-export` пишет `legacy_code`. Источник: `meetings/2026-09-07-ledger-sync.txt` / дата `2026-09-07`.
- по `topic:gateway-timeout`: повышение таймаута до 15 s после staging-incident, с пересмотром через 2 недели. Источник: `meetings/2026-09-14-ledger-sync.txt` / дата `2026-09-14`.
- по `topic:retries`: retries включены на `/ledger/charge`, максимум 2 retries, retry budget 20%. Источник: `meetings/2026-09-21-ledger-sync.txt` / дата `2026-09-21`.
- по `topic:ownership`: ownership retry policy перешёл от Oleg к Dasha. Источник: `meetings/2026-09-21-ledger-sync.txt` / дата `2026-09-21`.
- по `topic:cutover`: cutover назначен на `2026-10-09 10:00` в пределах error budget. Источник: `meetings/2026-09-28-ledger-sync.txt` / дата `2026-09-28`.
- по `top

### memory-eval-vector (completed, 5.0s, 3 tool calls)
queries: ['Кто из финансов участвует и что он обещал?', 'финансы участвует обещал', 'участвует и что он обещал финансов']

Из финансов участвует **Тим Хорват** — в записи от **2026-09-16** сказано, что **он владеет подтверждением мэппинга**: “finance-export keeps writing legacy_code until finance confirms their mapping is live; Tim Horvat owns that confirmation.” Источник: **confluence/tariff-migration-plan.xhtml**, **2026-09-16**.

Что он обещал:
- **2026-09-21** — Тим сказал: **“мэппинг кодов у финансов в тесте на следующей неделе скажу точно”**. Источник: **meetings/2026-09-21-ledger-sync.txt**, **2026-09-21**.
- **2026-10-02** — Тим сказал: **“мэппинг кодов у финансов в проде с первого октября можно планировать уход от legacy code но не раньше ноября”**. Источник: **meetings/2026-10-02-ledger-sync.txt**, **2026-10-02**.

Если нужно, могу ещё уточнить, **это текущий владелец/обещание или есть более новая запись, которая их меняет**.

## q14 [ru / unowned] Кто делает dry run миграции тарифов на копии прода?
**expected:** никто; вопрос поднимался 08-31, 09-07, 09-14, 09-21, 09-28, 10-02 и остался без владельца, записан в риски катовера  
**expected sources:** {'sources': ['meetings/2026-08-31-ledger-sync.txt', 'meetings/2026-10-02-ledger-sync.txt', 'confluence/tariff-migration-plan.xhtml']}

### memory-eval-both (completed, 6.4s, 1 tool calls)
queries: ['dry run миграции тарифов копии прода кто делает']

Никто — в памяти это открытый пункт без владельца.

Источники:
- `meetings/2026-08-31-ledger-sync.txt` — 2026-08-31: марат спросил, кто сделает dry run миграции тарифов на копии прода, и даша сказала, что не успеет.
- `meetings/2026-09-07-ledger-sync.txt` — 2026-09-07: на вопрос «кто нибудь взял?» даша ответила «нет».
- `meetings/2026-09-28-ledger-sync.txt` — 2026-09-28: dry run «так и не сделан», на вопрос «кто берет» олег ответил «не я».
- `meetings/2026-10-02-ledger-sync.txt` — 2026-10-02: dry run migration on production copy remains without owner.
- `meetings/2026-08-31-ledger-sync.txt` — open item `O01`, raised 2026-08-31: “dry run of the tariff backfill on a production copy has no owner”.



### memory-eval-graph (completed, 7.1s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:tariffs'}) WHERE NOT (d)<-[:SU", "MATCH (p:Person)-[o:OWNS]->(:Topic {key:'topic:tariffs'}) WHERE o.to IS NULL RET", "MATCH (oi:OpenItem)-[:ABOUT]->(:Topic {key:'topic:tariffs'}) RETURN oi.key AS ke"]

Нет владельца. В памяти есть open item по тарифам: dry run миграции тарифов на копии прода **без владельца**, поднят **2026-08-31** и повторно отмечался **2026-09-07, 2026-09-21, 2026-09-28, 2026-10-02**.  
Источник: `meetings/2026-08-31-ledger-sync.txt` и запись open item `openitem:tariffs:2026-08-31` (date/raised: `2026-08-31`).

Также нашлась текущая активная decision по тарифам: `meetings/2026-09-07-ledger-sync.txt` от `2026-09-07`, но она про `legacy_code`, а не про владельца dry run.

### memory-eval-vector (completed, 6.5s, 3 tool calls)
queries: ['Кто делает dry run миграции тарифов на копии прода?', 'dry run миграции тарифов копия прода кто делает', 'миграция тарифов dry run прода копия owner']

В памяти **нет владельца** для dry run миграции тарифов на копии прода.

Что я нашёл:
- **meetings/2026-08-31-ledger-sync.txt** (2026-08-31): Марат спрашивает, кто сделает dry run; Даша говорит, что не успеет.
- **meetings/2026-09-07-ledger-sync.txt** (2026-09-07): Марат снова спрашивает, кто взял dry run; Даша отвечает: «нет».
- **meetings/2026-09-28-ledger-sync.txt** (2026-09-28): Даша говорит, что dry run ещё не сделан; Марат спрашивает «кто берет», Олег отвечает «не я».
- **meetings/2026-10-02-ledger-sync.txt** (2026-10-02): Марат снова поднимает вопрос; Даша говорит «нет, марат».
- **meetings/2026-08-31-ledger-sync.txt** — open item **O01** (2026-08-31): “dry run of the tariff backfill on a production copy has no owner”.

Итог: **no owner** по состоянию на последние найденные записи.

## q15 [en / unowned] What is blocking phase 1 of the tariff migration?
**expected:** phase 0, the dry run on a production snapshot, has no owner  
**expected sources:** {'sources': ['confluence/tariff-migration-plan.xhtml', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 3.0s, 1 tool calls)
queries: ['phase 1 tariff migration blocking blocker blocked why phase 1 tariff migration']

Phase 1 of the tariff migration is blocked by the finance dependency: the finance warehouse still reconciles by the v1 code, so `finance-export` keeps writing `legacy_code` until Finance confirms its mapping is live. The note says phase 0 has no owner and phase 1 is blocked on it. Source: `confluence/tariff-migration-plan.xhtml`, updated `2026-09-16`.

Also, the plan’s phases section says phase 1 is “Create v2 tables, backfill from v1,” owned by Dasha, target `2026-09-23`. Source: `confluence/tariff-migration-plan.xhtml`, updated `2026-09-16`.

### memory-eval-graph (completed, 7.3s, 2 tool calls)
queries: ['MATCH (o:OpenItem)-[:ABOUT]->(t:Topic {key:$topic}) OPTIONAL MATCH (o)-[:RAISED_', 'MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:$topic}) OPTIONAL MATCH (d)-[:DECIDED']

What’s blocking phase 1 of the tariff migration is **the dry run of the tariff backfill on a production copy has no owner**.

Source:
- **meetings/2026-08-31-ledger-sync.txt** — open item **openitem:tariffs:2026-08-31**, raised **2026-08-31**: “OPEN: dry run of the tariff backfill on a production copy has no owner; raised again on 09-07, 09-21, 09-28, 10-02”

What I retrieved:
- An open tariff item showing the blocker above.
- The current tariff decision I found is about **legacy_code** in v2, but it does not describe the phase 1 blocker.

If you want, I can also look for any newer tariff decisions or open items that mention “phase 1” specifically.

### memory-eval-vector (completed, 4.0s, 3 tool calls)
queries: ['What is blocking phase 1 of the tariff migration?', 'blocking phase 1 tariff migration', 'phase 1 tariff migration blocker']

Phase 1 is blocked by phase 0: the dry run of the backfill script against a production snapshot, including comparing row counts and sums per `legacy_code` with the finance export. The plan says phase 1 is “blocked on it.” Source: `confluence/tariff-migration-plan.xhtml` — updated 2026-09-16.

The underlying dependency is that the finance warehouse reconciles by the v1 code, and `finance-export` keeps writing `legacy_code` until finance confirms its mapping is live; Tim Horvat owns that confirmation. Source: `confluence/tariff-migration-plan.xhtml` — updated 2026-09-16.

I also found a related migration note saying the dry run “has not been scheduled yet.” Source: `docs/tariffs-v2.md` — updated 2026-09-10.

## q16 [ru / crosslingual] Что в митингах называли бюджетом ретраев и где это описано в документации?
**expected:** retry budget из docs/gateway.md: доля повторов за минуту, 20%; в митингах 'бюджет ретраев' / 'повторы'  
**expected sources:** {'sources': ['docs/gateway.md', 'meetings/2026-09-21-ledger-sync.txt', 'meetings/2026-09-28-ledger-sync.txt']}

### memory-eval-both (completed, 10.5s, 2 tool calls)
queries: ['бюджет ретраев ретраи budget retries meetings documentation ledger', 'retry budget gateway policy documentation ledger retries budget twenty percent g']

В митингах под **«бюджетом ретраев»** называли долю повторных запросов, которую шлюз разрешает на маршруте; в записях это формулировали как **«двадцать процентов»** и связывали с политикой ретраев для gateway.

Что нашёл:

- **2026-09-21, `meetings/2026-09-21-ledger-sync.txt`**:  
  Ира сказала: «**и бюджет ретраев обязательно двадцать процентов как на чтении**», Марат уточнил: «**фиксируем ретраи на charge два повтора бюджет двадцать процентов**».  
  Это источник митингового употребления термина.

- **2026-09-02, `docs/gateway.md`**:  
  Раздел **Retry budget** описывает это как фиксированную долю ретраев от всех запросов за минутное окно; **20% = не больше одного retry из пяти**. Там же сказано, что это защита от retry storm и что значение задаётся в **gateway policy**, а не в Ledger.

- **2026-09-30, `docs/runbook-cutover.md`**:  
  В таблице политики на cutover для `/ledger/charge`, `/ledger/invoice/*`, `/ledger/tariffs` указан **Retry budget = 20%**.  
  Но этот документ **новее** и, если нужен текущий контекст по ретраям, он уже дополняет/уточняет более раннюю политику.

Если коротко:  
**в митингах “retry budget” = лимит 20% retry-запросов на маршрут; в документации это опи

### memory-eval-graph (completed, 7.7s, 3 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(:Topic {key:'topic:retries'}) OPTIONAL MATCH (d)-[", "MATCH (p:Person)-[:AUTHORED]->(doc:Document) WHERE doc.title CONTAINS 'retry' OR", "MATCH (doc:Document) WHERE toLower(doc.title) CONTAINS 'retry' OR toLower(doc.fi"]

В митингах «бюджетом ретраев» называли **retry budget 20%**. Это зафиксировано в решении от **2026-09-21** в митинге **`meetings/2026-09-21-ledger-sync.txt`**:  
- `Retries enabled on /ledger/charge: max 2 retries, retry budget 20%`

Что есть в памяти по этой теме:
- Более раннее решение от **2026-08-31** в **`meetings/2026-08-31-ledger-sync.txt`**:  
  - `No retries on /ledger/charge until idempotency is in place; up to 2 retries on read routes; retry policy owned by Oleg`  
  - это **superseded** последующим решением от 2026-09-21.

По документации я **не нашёл** ни одного документа, связанного с retry / retries / retry budget. Поэтому ответ по документации: **not in memory** — документов с описанием этого термина в графе нет.

Если хотите, я могу ещё проверить, нет ли документа по теме **idempotency**, где это могло быть описано косвенно.

### memory-eval-vector (completed, 11.3s, 3 tool calls)
queries: ['Что в митингах называли бюджетом ретраев и где это описано в документации?', 'бюджет ретраев', 'retry budget']

В митингах «бюджетом ретраев» называли ограничение доли ретраев на маршрут: в обсуждениях это формулировали как «20%», то есть примерно один ретрай на пять запросов, и это было про gateway policy для маршрутов с повторами.  
- Встреча: `meetings/2026-08-31-ledger-sync.txt` — 2026-08-31, где Ира говорит: «retry budget на роуты где повторы есть чтобы не было шторма», а Олег: «бюджет ретраев будет в политике гейтвея я опишу в доке».  
- Встреча: `meetings/2026-09-21-ledger-sync.txt` — 2026-09-21, где фиксируют: «бюджет ретраев обязательно двадцать процентов».  
- Встреча: `meetings/2026-09-28-ledger-sync.txt` — 2026-09-28, где снова подтверждают: «с бюджетом ретраев двадцать процентов».  

В документации это описано в `docs/gateway.md` — `Edge gateway integration`, раздел `Retry budget`, updated 2026-09-02: там сказано, что retry budget — это фиксированная доля ретраев от всех запросов за минутное окно; budget 20% означает максимум один ретрай на пять запросов, и значение задаётся в gateway policy, а не в Ledger.

Есть ещё более поздняя документация `docs/runbook-cutover.md` — `Gateway cutover runbook (draft)`, updated 2026-09-30: там в таблице для `/ledger/charge`, `/ledger/invoice/*

## q17 [en / crosslingual] When was the cutover date agreed and what did the team say about the error budget?
**expected:** 2026-09-28; cutover on 2026-10-09 at 10:00 fits within the half of the monthly error budget reserved for planned work  
**expected sources:** {'sources': ['meetings/2026-09-28-ledger-sync.txt', 'docs/slo.md']}

### memory-eval-both (completed, 6.0s, 2 tool calls)
queries: ['cutover date agreed error budget team said', 'MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:$topic}) OPTIONAL MATCH (d)-[:DECIDED']

The cutover date was agreed on **2026-09-28**: the team **fixed the cutover for 2026-10-09 at 10:00**. Source: `meetings/2026-09-28-ledger-sync.txt` (decision date **2026-09-28**).

About the error budget, the team said it was **“within the planned-work error budget”**. In the meeting transcript, Oleg proposed the date “in the planned-work budget,” and Irina said **“the budget passes: half of the monthly planned-work error budget as in SLO”**. Source: `meetings/2026-09-28-ledger-sync.txt` (decision date **2026-09-28**).

I also found a later decision on cutover from **2026-10-02** about the rollback owner, but it does not change the cutover date.

### memory-eval-graph (completed, 4.9s, 2 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$cutover})\nWHERE NOT (d)<-[:SUPERSEDES', 'MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$slo})\nWHERE NOT (d)<-[:SUPERSEDES]-()']

The cutover was agreed for **2026-10-09 at 10:00**. Source: **meetings/2026-09-28-ledger-sync.txt** (decision date **2026-09-28**).

About the error budget, the team said the cutover would be **“within the planned-work error budget.”** Source: **meetings/2026-09-28-ledger-sync.txt** (decision date **2026-09-28**).

What I retrieved:
- Current cutover decisions on `topic:cutover`
- Current SLO decision on `topic:slo`



### memory-eval-vector (completed, 5.8s, 3 tool calls)
queries: ['When was the cutover date agreed and what did the team say about the error budge', 'cutover date agreed error budget team said', 'cutover date error budget']

The cutover date was agreed on **2026-09-28** in the meeting **`meetings/2026-09-28-ledger-sync.txt`**; the team fixed it as **2026-10-09 at 10:00**. Source: **`meetings/2026-09-28-ledger-sync.txt` (2026-09-28)**.

About the error budget, the team said it was **within the planned-work error budget**. In the meeting, Irina also said it **fits “half of the monthly budget for planned work”**. Sources: **`meetings/2026-09-28-ledger-sync.txt` (2026-09-28)** and **`docs/slo.md` (2026-08-27)**.

Retrieved:
- **Decision**: `meetings/2026-09-28-ledger-sync.txt` (2026-09-28), cutover set to 2026-10-09 10:00, within planned-work error budget.
- **Meeting excerpt**: `meetings/2026-09-28-ledger-sync.txt` (2026-09-28), “half of the monthly budget for planned work.”
- **Related doc**: `docs/slo.md` (2026-08-27), half of error budget reserved for planned work such as gateway cutover.

## q18 [en / temporal] List every decision about the gateway timeout in order with dates.
**expected:** 2026-08-24 5 s (Oleg); 2026-09-14 15 s temporary (Oleg, Irina objected); 2026-09-28 10 s with 20% retry budget (Irina's proposal, Oleg owner)  
**expected sources:** {'sources': ['memory/decisions.jsonl']}

### memory-eval-both (completed, 6.3s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:gateway-timeout'})\nRETURN d.ke"]

Here are every recorded decisions about the gateway timeout, in chronological order:

1. **2026-08-24** — Gateway upstream timeout set to **5 s** on all Ledger routes.  
   - **Status:** superseded  
   - **Source:** `meetings/2026-08-24-ledger-sync.txt`  
   - **Decision key:** `decision:gateway-timeout:2026-08-24`

2. **2026-09-14** — Gateway timeout raised to **15 s temporarily** after the staging incident; review in two weeks.  
   - **Status:** superseded  
   - **Source:** `meetings/2026-09-14-ledger-sync.txt`  
   - **Decision key:** `decision:gateway-timeout:2026-09-14`

3. **2026-09-28** — Gateway timeout lowered to **10 s** with a 20% retry budget; replaces the 15 s emergency value.  
   - **Status:** active  
   - **Source:** `meetings/2026-09-28-ledger-sync.txt`  
   - **Decision key:** `decision:gateway-timeout:2026-09-28`

The current decision is the **2026-09-28** one, since the earlier decisions are marked **superseded**.

### memory-eval-graph (completed, 4.0s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nRETURN d.date AS date, d.stat']

Here are every decision about the gateway timeout, in date order:

1. **2026-08-24** — Gateway upstream timeout **5 s** on all Ledger routes  
   Source: `meetings/2026-08-24-ledger-sync.txt`  
   Status: `superseded`

2. **2026-09-14** — Gateway timeout **raised to 15 s temporarily** after the staging incident; review in two weeks  
   Source: `meetings/2026-09-14-ledger-sync.txt`  
   Status: `superseded`

3. **2026-09-28** — Gateway timeout **lowered to 10 s** with a **20% retry budget**; replaces the 15 s emergency value  
   Source: `meetings/2026-09-28-ledger-sync.txt`  
   Status: `active`

Retrieved from memory:
- Topic `topic:gateway-timeout`
- 3 decisions ordered by date

### memory-eval-vector (completed, 5.9s, 3 tool calls)
queries: ['List every decision about the gateway timeout in order with dates.', 'gateway timeout decision', 'timeout gateway']

Вот все найденные решения о gateway timeout в хронологическом порядке:

1. **2026-08-24** — gateway upstream timeout установлен на **5 s** для всех Ledger routes.  
   Источник: `meetings/2026-08-24-ledger-sync.txt` / claim `D01` (`decision:gateway-timeout:2026-08-24`), статус: **superseded**.

2. **2026-09-14** — timeout временно поднят до **15 s** после staging-инцидента; ревью через две недели.  
   Источник: `meetings/2026-09-14-ledger-sync.txt` / claim `D06` (`decision:gateway-timeout:2026-09-14`), статус: **superseded**.

3. **2026-09-28** — timeout снижен до **10 s** с **20% retry budget**; это заменяет 15 s emergency value.  
   Источник: `meetings/2026-09-28-ledger-sync.txt` / claim `D09` (`decision:gateway-timeout:2026-09-28`), статус: **active**.

Дополнительно: документ `docs/runbook-cutover.md` обновлён **2026-09-30** и подтверждает текущую политику **10 s**; это уже не отдельное решение, а описание текущего состояния.

## q19 [ru / fact] Когда катовер и во сколько?
**expected:** 2026-10-09 в 10:00  
**expected sources:** {'sources': ['meetings/2026-09-28-ledger-sync.txt', 'docs/runbook-cutover.md']}

### memory-eval-both (completed, 1.9s, 1 tool calls)
queries: ['topic:cutover cutover date time when']

Катовер — **2026-10-09 в 10:00 по местному времени**.

Источник: **meetings/2026-09-28-ledger-sync.txt**, дата **2026-09-28**; это же подтверждается в **docs/runbook-cutover.md**, обновлённом **2026-09-30**.

### memory-eval-graph (completed, 3.5s, 1 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:cutover'})\nWHERE NOT (d)<-[:SU"]

Катовер — **2026-10-02**, но **время в памяти не указано**.  
Источник: `meetings/2026-10-02-ledger-sync.txt` / встреча `Ledger sync 2026-10-02`, дата решения `2026-10-02`.

Что удалось извлечь:
- Есть решение по теме `topic:cutover`: катовер датирован **2026-10-02**.
- Поля с временем в памяти нет, поэтому **во сколько — not in memory**.

### memory-eval-vector (completed, 4.4s, 3 tool calls)
queries: ['Когда катовер и во сколько?', 'катовер дата и время', 'cutover date and time']

Катовер запланирован на **9 октября 2026 в 10:00**.

Источники:
- **meetings/2026-09-28-ledger-sync.txt** — на встрече сказали: «предлагаю девятое октября десять утра» и затем «фиксируем катовер девятого октября» (2026-09-28).
- **meetings/2026-09-28-ledger-sync.txt** — решение D10: «Gateway cutover on 2026-10-09 at 10:00» (2026-09-28).
- **docs/runbook-cutover.md** — черновик ранбука подтверждает: «Date: 2026-10-09, 10:00 local» (updated 2026-09-30).

Если хотите, могу ещё сказать, кто owner катовера.

## q20 [ru / contradiction] Decision log в Confluence актуален?
**expected:** нет, последняя версия 2026-09-09; в нём нет решений после 09-07: 15 с, ретраи на charge, передача ретраев Даше, 10 с, дата катовера, владелец отката  
**expected sources:** {'sources': ['confluence/decision-log.xhtml', 'memory/decisions.jsonl']}

### memory-eval-both (completed, 5.5s, 1 tool calls)
queries: ['Decision log Confluence актуален decision log confluence updated current status ']

Да, **Decision log в Confluence есть и выглядит актуальным**, но с оговоркой:

- Найден документ **`confluence/decision-log.xhtml`** с пометкой **updated 2026-09-09**.  
  Источник: *Decision log*, дата документа: **2026-09-09**.
- В нём есть свежие решения со статусом **[DONE]** и **[ACTIVE]**, а также open item без владельца.  
  Источник: *Decision log*, дата: **2026-09-09**.

Что видно по содержимому:
- **2026-09-07** — idempotency keys mandatory on `/charge` from 2026-09-15, status **DONE**.
- **2026-09-07** — tariff v2 keeps `legacy_code`, status **DONE**.
- **2026-08-31** — no retries on `/ledger/charge` until idempotency is in place, status **ACTIVE**.
- **2026-08-24** — gateway upstream timeout 5 s, status **ACTIVE**.
- **2026-08-24** — POST `/charge` p95 latency SLO 200 ms, status **ACTIVE**.
- Open item: tariff migration dry run on a copy of production data — **no owner yet**.

Если хотите, я могу ещё проверить, **не устарел ли этот log относительно более новых решений в memory**.

### memory-eval-graph (completed, 4.7s, 2 tool calls)
queries: ["MATCH (d:Decision)-[:ABOUT]->(t:Topic {key:'topic:ownership'}) WHERE NOT (d)<-[:", "MATCH (doc:Document) WHERE toLower(doc.title) CONTAINS 'decision log' RETURN doc"]

Да, **Decision log в Confluence не актуален**: в памяти есть более новая decision на тему ownership от **2026-09-21**, а документ обновлялся **2026-09-09**, значит он устарел.

Что нашёл:
- **Document:** `confluence/decision-log.xhtml` — **Decision log**, updated **2026-09-09**.
- **Decision:** `meetings/2026-09-21-ledger-sync.txt` — decision **active** от **2026-09-21** на тему ownership.

Итог: документ **stale / устарел** по сравнению с более новой decision.

### memory-eval-vector (completed, 4.5s, 3 tool calls)
queries: ['Decision log в Confluence актуален?', 'актуален ли decision log в Confluence', 'Decision log Confluence updated date current stale']

Да, **Decision log в Confluence актуален**: в памяти есть версия **updated 2026-09-09** в файле **`confluence/decision-log.xhtml`**. Источник: **Decision log**, дата **2026-09-09**.

Что я нашёл:
- Заголовок страницы: “Decisions from the weekly Ledger sync. Newest first. This page is updated after the meeting; if it disagrees with the recording, the recording wins.” — **`confluence/decision-log.xhtml`**, **2026-09-09**
- Таблица решений на той же странице с последними записями от **2026-09-07** и **2026-08-31** — **`confluence/decision-log.xhtml`**, **2026-09-09**

С более свежей версией Decision log в памяти я не нашёл, поэтому по имеющимся данным страница выглядит актуальной.

## q21 [en / attribution] Which decisions does Dasha own?
**expected:** tariff v2 with legacy_code (with Tim), idempotency keys, retry policy from 2026-09-21 including retries on /charge  
**expected sources:** {'sources': ['memory/decisions.jsonl']}

### memory-eval-both (completed, 6.0s, 1 tool calls)
queries: ['MATCH (p:Person {key:$key})- [o:OWNS]->(d:Decision)\nWHERE o.to IS NULL\nRETURN p.']

Dasha owns these decisions:

- `decision:idempotency:2026-09-07` — active; from `2026-09-07`; source `meetings/2026-09-07-ledger-sync.txt`; text: “Idempotency-Key header mandatory on /charge from 2026-09-15, 24 h key retention, two-week grace period”
- `decision:tariffs:2026-09-07` — active; from `2026-09-07`; source `meetings/2026-09-07-ledger-sync.txt`; text: “Tariff v2 keeps a mandatory legacy_code field; finance-export writes legacy_code”
- `decision:retries:2026-09-21` — active; from `2026-09-21`; source `meetings/2026-09-21-ledger-sync.txt`; text: “Retries enabled on /ledger/charge: max 2 retries, retry budget 20%”
- `decision:ownership:2026-09-21` — active; from `2026-09-21`; source `meetings/2026-09-21-ledger-sync.txt`; text: “Retry policy ownership moves from Oleg to Dasha”

I found these in memory from the graph.

### memory-eval-graph (completed, 4.9s, 1 tool calls)
queries: ['MATCH (p:Person {key:$key})-[o:OWNS]->(d:Decision)\nRETURN d.key AS decision_key,']

Dasha currently owns 4 decisions:

- `decision:idempotency:2026-09-07` — Idempotency-Key header mandatory on `/charge` from 2026-09-15, 24 h key retention, two-week grace period. Source: `meetings/2026-09-07-ledger-sync.txt`, dated `2026-09-07`.
- `decision:tariffs:2026-09-07` — Tariff v2 keeps a mandatory `legacy_code` field; finance-export writes `legacy_code`. Source: `meetings/2026-09-07-ledger-sync.txt`, dated `2026-09-07`.
- `decision:retries:2026-09-21` — Retries enabled on `/ledger/charge`: max 2 retries, retry budget 20%. Source: `meetings/2026-09-21-ledger-sync.txt`, dated `2026-09-21`.
- `decision:ownership:2026-09-21` — Retry policy ownership moves from Oleg to Dasha. Source: `meetings/2026-09-21-ledger-sync.txt`, dated `2026-09-21`.

Retrieved from memory via `Person {key: person:dasha-volkova}` and outgoing `OWNS` edges to `Decision` nodes.

### memory-eval-vector (completed, 4.4s, 3 tool calls)
queries: ['Which decisions does Dasha own?', 'Dasha owns decisions', 'owner Dasha decision']

Dasha owns these decisions in memory:

- **Idempotency keys mandatory on /charge from 2026-09-15, with 24 h retention and a two-week grace period** — owner **Dasha Volkova**. Source: `meetings/2026-09-07-ledger-sync.txt` / claim `D05`, dated **2026-09-07**.
- **Retry policy ownership moved from Oleg to Dasha** — owner **Dasha Volkova**. Source: `meetings/2026-09-21-ledger-sync.txt` / claim `D07`, dated **2026-09-21**.

Notes:
- The older decision log in `confluence/decision-log.xhtml` updated **2026-09-09** lists Dasha on idempotency, but it does not mention the later ownership move for retries.
- I did not find any other active decisions owned by Dasha in the retrieved memory.

## q22 [en / fact] How long does the Edge gateway cache /ledger/tariffs?
**expected:** 60 s  
**expected sources:** {'sources': ['docs/gateway.md']}

### memory-eval-both (completed, 2.4s, 1 tool calls)
queries: ['Edge gateway cache /ledger/tariffs duration cache TTL topic:gateway-timeout topi']

`/ledger/tariffs` is cached for **60 seconds** at the Edge gateway.

Source: `docs/gateway.md`, **updated 2026-09-02**.

### memory-eval-graph (completed, 3.5s, 1 tool calls)
queries: ['MATCH (d:Decision)-[:ABOUT]->(:Topic {key:$topic})\nWHERE NOT (d)<-[:SUPERSEDES]-']

I couldn’t find the Edge gateway cache TTL for `/ledger/tariffs` in memory.

What I retrieved:
- Current decision on `topic:tariffs`: tariff v2 keeps a mandatory `legacy_code` field; finance-export writes `legacy_code`.
  - Source: `meetings/2026-09-07-ledger-sync.txt`
  - Date: `2026-09-07`

The cache duration for the Edge gateway is not in memory.

### memory-eval-vector (completed, 2.6s, 1 tool calls)
queries: ['How long does the Edge gateway cache /ledger/tariffs?']

The Edge gateway caches `/ledger/tariffs` for **60 s**. Source: `docs/gateway.md` (Edge gateway integration, Routes), **updated 2026-09-02**.

I also found a matching meeting note confirming the route was documented there: `meetings/2026-08-31-ledger-sync.txt` (Ledger sync 2026-08-31), **2026-08-31**.
