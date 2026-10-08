---
title: Edge gateway integration
updated: 2026-09-02
owner: Oleg Prikhodko
---

# Edge gateway integration

`ledger-api` is being moved behind the Edge gateway. The gateway terminates
TLS, authenticates callers with service tokens and applies per-route policies.
Callers switch from `ledger.internal` to `edge.internal/ledger`.

## Routes

| External path | Backend | Policy |
|---|---|---|
| `/ledger/charge` | `ledger-api:8080/charge` | auth: service token, timeout, no retries |
| `/ledger/invoice/*` | `ledger-api:8080/invoice/*` | auth: service token, timeout, retries allowed |
| `/ledger/tariffs` | `ledger-api:8080/tariffs` | auth: service token, cache 60 s |

## Timeouts

The upstream timeout for every Ledger route is **5 seconds**. It was chosen as
a round number above the p99 of `/charge` measured on the old nginx front
(1.8 s). Anything slower than that is a problem in Ledger, not something the
gateway should wait for.

## Retries

Retries are **disabled on `/ledger/charge`**. A charge is not idempotent today:
a retried request can bill the customer twice. Retries on the read-only
routes are allowed, up to 2 attempts.

### Retry budget

When retries are enabled on a route they are governed by a *retry budget*: the
gateway allows retries only while retried requests are below a fixed share of
all requests to that route over a one-minute window. The share is the budget.
A budget of 20% means at most one in five requests may be a retry; above that
the gateway stops retrying until the window clears. The budget protects Ledger
from a retry storm during an incident. The value per route is set in the
gateway policy, not in Ledger.

## Authentication

Callers present a service token in `Authorization: Bearer`. The gateway
validates it and forwards the caller identity in `X-Caller`. Ledger trusts
`X-Caller` only from the gateway's network.
