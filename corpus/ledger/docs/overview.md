---
title: Ledger service overview
updated: 2026-08-20
owner: Dasha Volkova
---

# Ledger service overview

Ledger is the internal billing service. It records charges against customer
accounts, produces monthly invoices and owns the tariff catalogue. Every other
service that needs to bill a customer calls Ledger; nothing else writes to the
billing tables.

## Components

| Component | Language | Role |
|---|---|---|
| `ledger-api` | Go | HTTP API: `/charge`, `/invoice`, `/tariffs` |
| `ledger-worker` | Go | nightly invoice generation, tariff recalculation |
| `ledger-db` | PostgreSQL 16 | charges, invoices, tariffs |
| `finance-export` | Python | daily CSV export to the finance warehouse |

## Endpoints

- `POST /charge` records one charge. Body: `account_id`, `amount`, `currency`,
  `tariff_code`. Returns the charge id. This is the hot path; see
  [slo.md](slo.md) for the latency target.
- `GET /invoice/{account_id}/{period}` returns a rendered invoice.
- `GET /tariffs` returns the active tariff catalogue.

## Current programme of work (Q3 2026)

1. Move `ledger-api` behind the Edge gateway instead of the old nginx front.
   See [gateway.md](gateway.md). Platform owner: Oleg Prikhodko.
2. Replace the tariff schema with v2. See [tariffs-v2.md](tariffs-v2.md).
   Backend owner: Dasha Volkova.
3. Formal SLOs and an error budget. See [slo.md](slo.md). SRE owner: Irina
   Belova.

Product owner for the whole programme: Marat Yusupov.
