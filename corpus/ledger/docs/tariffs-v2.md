---
title: Tariff schema v2
updated: 2026-09-10
owner: Dasha Volkova
---

# Tariff schema v2

The v1 tariff table mixed pricing with product metadata and could not express
tiered pricing. v2 separates the two and adds tiers.

## Schema

```sql
CREATE TABLE tariff_v2 (
  code         text PRIMARY KEY,      -- e.g. "api-standard"
  legacy_code  text NOT NULL,         -- the v1 code, kept for finance export
  product      text NOT NULL,
  currency     char(3) NOT NULL,
  valid_from   date NOT NULL,
  valid_to     date
);

CREATE TABLE tariff_tier_v2 (
  code       text REFERENCES tariff_v2(code),
  from_units bigint NOT NULL,
  unit_price numeric(12,4) NOT NULL,
  PRIMARY KEY (code, from_units)
);
```

## `legacy_code`

Finance systems reconcile charges by the v1 tariff code. Until the finance
warehouse is migrated, every v2 tariff carries its v1 code in `legacy_code`,
and `finance-export` writes `legacy_code`, not `code`, into the CSV. This field
was added after the finance review on 2026-09-07 and is mandatory.

## Migration

1. Create the v2 tables alongside v1.
2. Backfill v2 from v1 with a script; tiers are generated from the single v1
   price as one tier starting at 0 units.
3. Dual-write for two weeks.
4. Switch reads to v2; drop v1 after one billing cycle.

A dry run of the backfill against a copy of production data is required before
step 2. The dry run has not been scheduled yet.
