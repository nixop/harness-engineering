---
title: Serverless cutover runbook
updated: 2026-09-29
owner: Ivan Melnik
---

# Serverless cutover runbook

Cutover of Relay from the EKS deployment to Lambda.

**Date:** not scheduled.

## Preconditions

- Staging on Lambda one week without incidents (done 2026-09-28).
- Provisioned concurrency on `relay-deliver`: 4 instances (sized after the 3x load test).
- Load test at 10x: **not done**.
- DynamoDB cutover first; the two must be a week apart.

## Steps

1. Freeze endpoint changes 24 h before.
2. Switch the gateway integration for `POST /relay/deliver` and `GET /relay/*` from the VPC link to the Lambda integrations.
3. Scale EKS deployments to 0 replicas but keep the cluster for 7 days.
4. Watch delivery p95, DLQ depth and intake 5xx for 30 minutes.

## Rollback

Switch the gateway integrations back to the VPC link and scale EKS deployments up. **Rollback owner: TBD.** See [runbook-rollback.md](runbook-rollback.md).
