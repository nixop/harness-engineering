---
title: Idempotency keys for /charge
updated: 2026-09-12
owner: Dasha Volkova
---

# Idempotency keys for `/charge`

To make `POST /charge` safe to retry, callers send an `Idempotency-Key`
header: a UUID chosen by the caller per logical charge. Ledger stores the key
with the charge for 24 hours. A second request with the same key returns the
original charge id and does not bill again.

Rules:

- The key is required from 2026-09-15. Requests without it are rejected with
  400 after a two-week grace period during which they are only logged.
- Keys are scoped per caller (`X-Caller`), so two services can use the same
  UUID without colliding.
- A request with a known key but a different body returns 409.

Once every caller sends keys, the gateway can enable retries on
`/ledger/charge`; see the gateway policy for the retry limit and budget.
