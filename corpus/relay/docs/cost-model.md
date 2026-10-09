---
title: Relay cost model
updated: 2026-09-23
owner: Olga Petrova
---

# Relay cost model

## History

| Month | Cost | Notes |
|---|---|---|
| May 2026 | $6,100 | shared EKS cluster, Relay is the main consumer |
| July 2026 | $6,300 | EKS plus both PoCs |
| September 2026 (forecast after cutover) | $3,800 | Lambda, SQS, DynamoDB |

PoC-3 measured $3,600 at current volume; the forecast adds provisioned concurrency and the DLQ.

## Budget alert (decided 2026-09-21)

Monthly budget for Relay production: **$4,000**. At 80% a page goes to the finance partner and the platform lead.

## Tags

Every resource carries `cost-center=relay` and `env`; the CloudFormation lint fails without them (since 2026-02-09). Terraform-managed networking is tagged by the network team.

## Savings recorded

- DynamoDB single-table vs DocumentDB: -38% on the data line (PoC-1).
- Lambda vs EKS: -41% on compute (PoC-3), about $30,000 a year.
