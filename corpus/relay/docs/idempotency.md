---
title: Idempotency keys on /deliver
updated: 2026-05-20
owner: Nikita Frolov
---

# Idempotency keys on `/deliver`

Decided 2026-05-18. To make `POST /deliver` safe to retry, callers send an `Idempotency-Key` header, a UUID chosen per logical delivery. Relay stores the key with the delivery for 24 hours; a second request with the same key returns the original delivery id and does not deliver again.

## Rollout

- From **2026-06-01** the header is mandatory. For two weeks requests without it are accepted and logged; after 2026-06-15 they are rejected with 400.
- Keys are scoped per caller (`X-Caller-Arn`), so two services may reuse a UUID.
- Same key, different body: 409.

## Why

Gateway retries on `/deliver` were disabled on 2026-03-30 because a retried delivery could reach a customer twice. Once every caller sends keys, retries can be enabled at the gateway with a limit and a budget set in the gateway policy.

## Storage

Keys live in the deliveries table with a TTL of 24 hours. In the DynamoDB design the key is the sort key of the `IDEMPOTENCY#` item under the caller's partition.
