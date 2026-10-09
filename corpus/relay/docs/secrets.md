---
title: Secrets handling
updated: 2026-09-10
owner: Yulia Tarasova
---

# Secrets handling

Decided at the security review of 2026-09-07 (ADR-008).

## Rule

Secrets (per-endpoint signing keys, DynamoDB is IAM, DocumentDB credentials during dual write) are read from SSM Parameter Store at function startup and cached in the instance. Nothing secret appears in Lambda environment variables or CloudFormation parameters.

## Parameters

| Parameter | Type | Rotation |
|---|---|---|
| `/relay/prod/signing/<endpoint_id>` | SecureString | on customer request |
| `/relay/prod/docdb/credentials` | SecureString | **overdue**: last rotated January 2026; must be rotated before DocumentDB decommission |

## Cost of the rule

About 100 ms on a cold start, hidden by provisioned concurrency on `relay-deliver`. Rotation is a parameter update followed by a redeploy.

## Access

Functions get `ssm:GetParameter` on their own prefix only. `describe` on the stack no longer reveals anything.
