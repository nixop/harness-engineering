---
title: CloudFormation migration guide
updated: 2026-02-11
owner: Pavel Grishin
---

# CloudFormation migration guide

How Relay's Terraform modules move to CloudFormation, per ADR-001 (2026-01-14). The goal is a single tool for the whole account: one pipeline, drift detection on every stack, IAM boundaries per stack.

## Scope

All of Relay's infrastructure moves, including networking: VPC, subnets, the cross-account peering to billing and the DNS delegation. Networking goes last because peering is the riskiest resource to touch.

## Stack layout (decided 2026-02-09)

One root stack per environment (`relay-dev`, `relay-staging`, `relay-prod`) with four nested stacks: `network`, `data`, `compute`, `gateway`. A failed nested stack rolls back the whole root, which is the intended blast radius for an environment.

## Procedure per module

1. Write the template; run `cfn-lint` (the tag rule from 2026-02-09 fails the build if `cost-center` or `env` is missing).
2. `aws cloudformation create-change-set --change-set-type IMPORT` with the resource identifiers from Terraform state.
3. Execute the import; verify `DetectStackDrift` reports `IN_SYNC`.
4. Remove the resources from Terraform state with `terraform state rm`; keep the Terraform code until the last module has moved.

## Order

| Module | Target | Status on 2026-02-11 |
|---|---|---|
| compute | 2026-02-02 | done |
| data | 2026-02-16 | in progress |
| gateway (new) | March | not started |
| network | end of March | not started |

## Rollback

An imported resource can be removed from the stack with `DeletionPolicy: Retain` and re-imported into Terraform. No resource is recreated at any step.
