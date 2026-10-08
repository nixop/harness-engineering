---
title: Gateway cutover runbook (draft)
updated: 2026-09-30
owner: Oleg Prikhodko
---

# Gateway cutover runbook (draft)

Cutover of Ledger traffic from the nginx front to the Edge gateway.

**Date:** 2026-10-09, 10:00 local, within the planned-work error budget.

## Gateway policy at cutover

| Route | Timeout | Retries | Retry budget |
|---|---|---|---|
| `/ledger/charge` | 10 s | 2 | 20% |
| `/ledger/invoice/*` | 10 s | 2 | 20% |
| `/ledger/tariffs` | 10 s | 2 | 20% |

The 10-second timeout replaces the 15-second emergency value set after the
2026-09-14 incident; the retry budget is what makes the lower timeout safe.
Retries on `/ledger/charge` are allowed now that idempotency keys are
mandatory.

## Steps

1. Freeze tariff changes 24 h before.
2. Switch DNS for `ledger.internal` to the gateway VIP with a 60 s TTL.
3. Watch p95 latency and 5xx on the gateway dashboard for 30 minutes.
4. Lower the TTL back to 300 s if stable.

## Rollback

Point `ledger.internal` back at the nginx VIP. DNS TTL makes this effective
within a minute. **Rollback owner: TBD.**
