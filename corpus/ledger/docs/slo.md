---
title: Ledger SLOs
updated: 2026-08-27
owner: Irina Belova
---

# Ledger SLOs

Service level objectives for `ledger-api`, measured at the gateway.

| Route | Indicator | Objective |
|---|---|---|
| `POST /charge` | latency, p95 over 5 minutes | **200 ms** |
| `POST /charge` | availability, monthly | 99.9% |
| `GET /invoice/*` | latency, p95 | 800 ms |
| `GET /tariffs` | latency, p95 | 100 ms |

## Error budget

Availability of 99.9% leaves 43 minutes of downtime per month. Half of that
budget is reserved for planned work such as the gateway cutover; the other half
is the operational budget. If the operational budget is spent, feature work on
Ledger stops until the next month.

## What counts as an error

HTTP 5xx from Ledger and gateway timeouts both count against availability.
Client errors (4xx) do not. A request that succeeds only after a retry counts
as one success and one error.
