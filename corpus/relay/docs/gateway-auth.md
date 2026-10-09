---
title: Gateway authentication
updated: 2026-03-25
owner: Yulia Tarasova
---

# Gateway authentication

Decided 2026-03-23. Callers authenticate to the API gateway with IAM-signed requests (SigV4); the shared API key that used to live in three repositories is retired on 2026-04-30.

## Caller setup

Each calling service gets an IAM role with `execute-api:Invoke` on its own routes only:

| Service | Routes |
|---|---|
| orders | `POST /relay/deliver`, `GET /relay/deliveries/*` |
| billing | `POST /relay/deliver` |
| notifications | `POST /relay/deliver`, `GET /relay/endpoints` |
| support-console | `GET /relay/deliveries/*`, `GET /relay/endpoints` |

Clients use the internal `sigv4-client` library; migration is about a day per service.

## Inside Relay

The gateway forwards the caller's role in `X-Caller-Arn`. Relay trusts the header only from the gateway's VPC link.

## Retirement of the shared key

- 2026-04-06: key rejected on staging.
- 2026-04-27: all four services confirmed on SigV4.
- 2026-04-30: key deleted.
