---
title: Rollback runbook
updated: 2026-09-24
owner: Lena Kim
---

# Rollback runbook

Written for the serverless cutover; covers the database cutover as well.

## Compute rollback (Lambda to EKS)

1. In the `gateway` nested stack, point the `deliver` and `query` integrations back to the VPC link; deploy. Effective within 2 minutes.
2. `kubectl scale deploy relay-api relay-worker --replicas=3/6`.
3. Drain `relay-deliveries`: leave `relay-deliver` running until the queue is empty, then disable the trigger.
4. Confirm p95 and success rate on the SLO dashboard.

## Database rollback (DynamoDB to DocumentDB)

Only possible while dual write is on. Switch the read flag back to DocumentDB; deliveries written only to DynamoDB in the window are replayed by the backfill script in reverse.

## Owner

The rollback owner is named in the cutover decision. This runbook is maintained by SRE.
