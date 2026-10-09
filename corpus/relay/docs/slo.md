---
title: Relay SLOs
updated: 2026-01-28
owner: Lena Kim
---

# Relay SLOs

Decided 2026-01-26.

| Indicator | Objective | Window |
|---|---|---|
| Delivery latency, p95: from `POST /deliver` accepted to the first delivery attempt sent | **2 s** | 5 minutes |
| Delivery success rate: deliveries that reach the customer endpoint after all attempts | **99.5%** | calendar month |
| `GET /deliveries/*` latency, p95 | 500 ms | 5 minutes |

The latency SLO measures Relay, not the customer: it ends when the first attempt is sent, not when the customer answers.

## Error budget

99.5% success leaves 0.5% of deliveries per month. Half of the downtime budget implied by that is reserved for planned work such as the gateway cutover and the compute migration; the other half is operational. If the operational half is spent, feature work on Relay stops for the rest of the month.

## What counts

Gateway timeouts and 5xx from Relay count against success. Customer endpoints returning 4xx after all attempts count as delivered-but-rejected and do not count against the SLO.
