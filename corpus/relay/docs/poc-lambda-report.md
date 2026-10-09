---
title: "PoC-3 report: Relay on Lambda"
updated: 2026-07-24
owner: Ivan Melnik
---

# PoC-3 report: Relay on Lambda

Period 2026-06-22 to 2026-07-24, per ADR-005. Ownership moved from Sergey Belov to Ivan Melnik on 2026-07-13. Intake handler behind the API gateway, SQS between intake and delivery, delivery handler with provisioned concurrency.

## Results

| Metric | Value |
|---|---|
| Delivery latency p95, provisioned concurrency on `/deliver` | **1.9 s** |
| Delivery latency p95, no provisioned concurrency | 3.4 s |
| Cold start | 1.2 s |
| Monthly cost at current volume | **$3,600 (-41% vs EKS)** |
| Scale-out to 3x volume | immediate |
| Operations | no cluster; Lambda, SQS and the gateway are managed |

## Assessment

Within the 2 s SLO only with provisioned concurrency; without it the SLO is missed. Retries and timeouts need to be redone for an asynchronous intake (gateway retries would double-enqueue). A load test at 10x current volume was not done in the PoC.

Reviewed 2026-07-27; decided at the architecture committee on 2026-08-03 (ADR-006).
