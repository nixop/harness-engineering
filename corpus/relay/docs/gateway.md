---
title: API gateway integration
updated: 2026-03-18
owner: Pavel Grishin
---

# API gateway integration

Relay is fronted by the account's API gateway per ADR-002 (2026-03-04). Routes, timeouts and retry policies live in the `gateway` nested stack.

## Routes

| Route | Backend | Policy |
|---|---|---|
| `POST /relay/deliver` | `relay-api:8080/deliver` | auth, timeout, **no retries** |
| `GET /relay/deliveries/*` | `relay-api:8080/deliveries/*` | auth, timeout, retries up to 2 |
| `GET /relay/endpoints` | `relay-api:8080/endpoints` | auth, timeout, cache 30 s |

Callers switch from `relay.internal` to the gateway hostname; authentication is described in [gateway-auth.md](gateway-auth.md).

## Timeouts

The integration timeout on every Relay route is **10 seconds** (decided 2026-03-16). It is a round number above the p99 of `POST /deliver` at intake, 1.8 s. The synchronous `wait=true` mode can exceed it; that mode is being removed and the timeout is not sized for it.

## Retries

Retries on `POST /deliver` are **disabled** (decided 2026-03-30): a delivery is not idempotent yet, and a retried request can reach the customer twice. Read routes retry up to two times.

### Retry budget

When retries are enabled on a route they are capped by a retry budget: the share of retried requests among all requests to the route over a one-minute window. Above the budget the gateway stops retrying until the window clears. The value is set per route in the gateway policy, not in Relay.

## Observability

The gateway emits per-route latency, 4xx/5xx and integration timeouts to CloudWatch; the SLO dashboard reads delivery latency from these metrics since 2026-03-18.
