---
title: Drift detection and change freeze
updated: 2026-02-25
owner: Lena Kim
---

# Drift detection and change freeze

Decided at the incident review of 2026-02-23 after a manual load balancer change was reverted by the nightly deploy and delivery stopped for 20 minutes.

## Rules

1. No manual changes in the AWS console for production resources that belong to a Relay stack. Staging may be changed by hand for a test, and the test must end with the stack redeployed.
2. Every Relay stack runs `DetectStackDrift` nightly at 01:00.
3. A stack in `DRIFTED` state blocks the pipeline until it is reconciled.

## Alerts

Drift results go to the `#relay-infra` channel. Routing to the on-call rotation is an open item from the review; until it is done, the platform lead checks the channel every morning.

## Reconciling

- Change was intended: put it in the template, deploy, confirm `IN_SYNC`.
- Change was not intended: redeploy the stack; the template wins.
