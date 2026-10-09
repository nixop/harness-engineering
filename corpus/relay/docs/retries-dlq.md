---
title: Delivery retries through SQS and the DLQ
updated: 2026-08-27
owner: Ivan Melnik
---

# Delivery retries through SQS and the dead-letter queue

Decided 2026-08-24 (ADR-009). Retries are no longer a gateway policy.

## Mechanism

- `relay-intake` writes the delivery and sends one message to `relay-deliveries`.
- `relay-deliver` posts to the customer. On failure or timeout it throws; SQS redrives with exponential backoff: 30 s, 2 min, 10 min, 30 min, 2 h.
- After **5 attempts** the message goes to `relay-deliveries-dlq`; an alert fires and the delivery is marked `failed`.
- Gateway retries on `POST /relay/deliver` are **off**; a gateway retry would enqueue twice.

## Retry budget

Not needed: the queue bounds retries per message and visibility timeouts bound concurrency. The retry budget concept from the gateway era does not apply.

## Ownership

Retries are owned by the Relay core lead until the serverless cutover, then by the owner of the SQS pipeline.

## Dashboards

`relay-deliveries` age of oldest message, redrive count, DLQ depth.
