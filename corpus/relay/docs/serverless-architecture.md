---
title: Serverless architecture
updated: 2026-08-12
owner: Ivan Melnik
---

# Serverless architecture

Per ADR-006 (2026-08-05). Relay runs on Lambda.

```
caller --SigV4--> API gateway --> intake Lambda --> SQS (deliveries)
                                                      |
                                        delivery Lambda (provisioned concurrency)
                                                      |
                                   customer endpoint   +--> DynamoDB (relay-deliveries)
                                                      +--> DLQ after 5 attempts
```

## Functions

| Function | Trigger | Memory | Notes |
|---|---|---|---|
| `relay-intake` | gateway `POST /relay/deliver` | 512 MB | validates, writes the delivery, enqueues; returns 202 |
| `relay-deliver` | SQS `relay-deliveries` | 1024 MB | signs and posts; provisioned concurrency (sizing open, owner Ivan) |
| `relay-query` | gateway `GET /relay/*` | 256 MB | reads |

## What changed from EKS

- Intake is asynchronous: `POST /deliver` returns 202 with a delivery id; the synchronous `wait=true` mode is gone.
- Retries move from the gateway to the queue (see [retries-dlq.md](retries-dlq.md)).
- The gateway integration timeout matters only for intake; it is being revisited for Lambda.
- Secrets handling is under security review.

## Infrastructure

Everything is in the `compute` and `gateway` nested stacks (SAM transform). Networking inputs still come from Terraform through SSM.
