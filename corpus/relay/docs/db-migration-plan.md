---
title: DocumentDB to DynamoDB migration plan
updated: 2026-05-26
owner: Denis Orlov
---

# DocumentDB to DynamoDB migration plan

## Phases

| Phase | What | Owner | Target |
|---|---|---|---|
| 0 | Dry run of the backfill script on a production snapshot; compare counts and sums per customer | **TBD** | before phase 1 |
| 1 | Create the table and GSIs; backfill deliveries from the last 90 days | Denis | 2026-06-30 |
| 2 | Dual write from `relay-api` and `relay-worker` | Denis | from 2026-07-01, at least 3 weeks |
| 3 | Switch reads to DynamoDB | Denis | after the compute decision |
| 4 | Stop dual write; decommission DocumentDB | Denis | not scheduled |

Phase 0 has had no owner since it was raised on 2026-05-04. Phase 1 is blocked on it.

## Cutover

Not dated. It must not coincide with the compute cutover week.

## Decommission

DocumentDB decommission has no date. Credentials must be rotated before decommission (security review item).
