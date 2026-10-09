---
title: "PoC-2 report: Relay on EKS"
updated: 2026-07-24
owner: Timur Aliev
---

# PoC-2 report: Relay on EKS with autoscaling

Period 2026-06-22 to 2026-07-24, per ADR-005. A dedicated EKS cluster with Karpenter, Relay API and workers as deployments with HPA on queue depth.

## Results

| Metric | Value |
|---|---|
| Delivery latency p95 | **0.4 s** |
| Delivery latency p99 | 0.9 s |
| Monthly cost at current volume | **$6,100** |
| Scale-out to 3x volume | 90 s |
| Operations | a second cluster: upgrades, node images, Karpenter, 24/7 on-call |

## Assessment

Latency is excellent and headroom is large. The cost is the cost of a cluster plus the cost of a team that does not exist: the platform team does not want to operate Kubernetes for one service.

Recommendation from the PoC owner: keep EKS with autoscaling (written up as ADR-007).
