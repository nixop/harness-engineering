---
title: Load testing guide
updated: 2026-07-15
owner: Lena Kim
---

# Load testing guide

Used by both compute PoCs so the numbers are comparable.

## Profile

Replay of one production day scaled by a factor: 1x, 3x, 10x. Mix: 92% `POST /deliver`, 8% reads. Customer endpoints are simulated with a mock that answers in 200 ms for 95% of calls and 20 s for 5%.

## Metrics

Delivery latency p95 and p99 as defined in the SLO page; intake 5xx; for Lambda, cold starts and provisioned-concurrency spillover; for EKS, scale-out time.

## Requirement before any cutover

A run at **10x** current volume with p95 inside the SLO. Each PoC ran at 1x and 3x; the 10x run is still owed.
