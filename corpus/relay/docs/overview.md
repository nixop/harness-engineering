---
title: Relay service overview
updated: 2026-01-20
owner: Anna Sokolova
---

# Relay service overview

Relay is the internal webhook delivery service. Product services call it when a customer-visible event happens; Relay persists the delivery, signs the payload, posts it to the customer's endpoint and records the outcome. Nothing else talks to customer endpoints directly.

## Components (as of January 2026)

| Component | Runtime | Role |
|---|---|---|
| `relay-api` | Go on the shared EKS cluster, 3 replicas | `POST /deliver`, `GET /deliveries/{id}`, `GET /endpoints` |
| `relay-worker` | Go on EKS, 6 replicas | pulls pending deliveries, posts them, applies the in-service retry schedule |
| `relay-db` | DocumentDB 5.0, 3 instances | deliveries, endpoints, outcomes |
| `relay-signer` | library | HMAC signing of payloads with per-endpoint secrets |

Infrastructure is described in Terraform 0.12 modules under `infra/`; the rest of the AWS account uses CloudFormation. A programme to change that starts this quarter.

## API

- `POST /deliver` accepts `endpoint_id`, `event`, `payload`, returns a delivery id. This is the hot path. A synchronous mode (`wait=true`) makes the call block until the first delivery attempt completes; about 2% of traffic uses it and it is slated for removal.
- `GET /deliveries/{id}` returns status and attempts.
- `GET /endpoints` lists registered endpoints for a customer.

## 2026 programme

1. Infrastructure code: Terraform to CloudFormation (platform, Pavel Grishin).
2. Front Relay with the API gateway (platform, Pavel Grishin).
3. Replace DocumentDB (data, Denis Orlov).
4. Decide the compute platform for Relay (architecture, Timur Aliev).

Product owner: Marat Yusupov. SLOs: Lena Kim. Costs: Olga Petrova. Security: Yulia Tarasova.
