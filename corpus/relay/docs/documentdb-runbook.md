---
title: DocumentDB operations runbook
updated: 2026-02-02
owner: Denis Orlov
---

# DocumentDB operations runbook

DocumentDB is the system of record for Relay: deliveries, endpoints and outcomes. Cluster `relay-prod-docdb`, DocumentDB 5.0, one writer and two readers.

## Health

- Read p99 at peak is 9 ms (January 2026) and rising about 1 ms per month with volume.
- Writer CPU above 70% for 10 minutes pages the data on-call.

## Backups

Automated snapshots daily at 03:00, retained 14 days. Manual snapshot before any schema change.

## Failover

`aws docdb failover-db-cluster --db-cluster-identifier relay-prod-docdb`. Writes pause for about 30 s; Relay workers retry writes for up to 2 minutes.

## Credentials

Application credentials are in Secrets Manager under `relay/prod/docdb`. They were last rotated in January 2026.

## Known issues

- Index build on the `deliveries` collection locks writes for the duration; schedule in the 02:00 window.
- Connection count spikes when workers restart; the connection pool is capped at 50 per worker.
