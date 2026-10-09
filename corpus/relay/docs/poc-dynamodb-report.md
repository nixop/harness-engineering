---
title: "PoC-1 report: DynamoDB designs"
updated: 2026-05-01
owner: Denis Orlov
---

# PoC-1 report: DynamoDB single-table vs multi-table

Period 2026-04-08 to 2026-04-30. Dataset: 90 days of production-shaped deliveries (14 M items). Load: the six Relay access patterns at 1x and 3x current volume.

## Results

| Design | Read p99 | Write p99 | Monthly cost at projected volume |
|---|---|---|---|
| DocumentDB (baseline, current) | 9 ms | 14 ms | $5,200 |
| DynamoDB multi-table (4 tables) | 11 ms | 9 ms | $5,100 |
| DynamoDB single-table | **4 ms** | 8 ms | **$3,200 (-38%)** |

Multi-table loses on reads because the delivery-by-customer pattern needs two queries and a join in the application. Single-table serves every pattern with one query or one GSI.

## Recommendation

Single-table. The cost is query flexibility: every pattern is designed up front and a new one requires a new GSI. Relay's patterns have not changed in three years.

Reviewed 2026-05-04; objection from the architect on flexibility recorded in ADR-003.
