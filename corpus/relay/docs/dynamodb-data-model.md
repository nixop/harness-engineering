---
title: DynamoDB single-table data model
updated: 2026-05-12
owner: Denis Orlov
---

# DynamoDB single-table data model

Per ADR-003 (accepted 2026-05-06): one table, `relay-deliveries`, composite keys.

## Keys

| Item | PK | SK |
|---|---|---|
| Delivery | `CUST#<customer_id>` | `DEL#<created_at>#<delivery_id>` |
| Attempt | `CUST#<customer_id>` | `DEL#<created_at>#<delivery_id>#ATT#<n>` |
| Endpoint | `CUST#<customer_id>` | `EP#<endpoint_id>` |
| Idempotency key | `CALLER#<caller_arn>` | `IDEM#<key>` (TTL 24 h) |

## Access patterns

1. Create delivery and first attempt: one transaction.
2. Deliveries for a customer in a time range: query PK with SK between.
3. Delivery by id: GSI `by-delivery-id`.
4. Pending deliveries for the worker: GSI `by-status` on `status#next_attempt_at`.
5. Endpoints for a customer: query PK with SK begins_with `EP#`.
6. Idempotency lookup: get item.

Six patterns, matching the six Relay has had for three years. A new pattern means a new GSI, which is the trade-off recorded in ADR-003.

## PoC-1 numbers

Read p99 4 ms single-table, 11 ms multi-table, 9 ms DocumentDB at the same load; cost at projected volume 38% below DocumentDB.
