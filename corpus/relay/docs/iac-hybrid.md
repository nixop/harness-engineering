---
title: Hybrid IaC layout
updated: 2026-04-24
owner: Sergey Belov
---

# Hybrid IaC layout

Per ADR-004 (2026-04-22), which supersedes ADR-001: networking stays in Terraform, application stacks are CloudFormation. This page is the boundary.

## Terraform (network team's repository, `net-core/`)

- VPC and subnets for `relay-prod`, `relay-staging`
- Cross-account peering to the billing and audit accounts
- Route 53 delegation for `relay.internal`
- The VPC link used by the API gateway

Drift: `terraform plan` nightly in the network team's pipeline; non-empty plans page the network on-call.

## CloudFormation (`infra/cfn/`)

- `relay-<env>` root stack with nested `data`, `compute`, `gateway`
- The former `network` nested stack is removed; its outputs (VPC id, subnet ids, VPC link id) are read from SSM parameters that Terraform writes

Drift: `DetectStackDrift` nightly, alerts to Relay on-call (since 2026-03-02).

## Hand-off between the two

Terraform exports `/relay/<env>/network/vpc-id`, `/relay/<env>/network/private-subnets`, `/relay/<env>/network/vpc-link-id` to SSM Parameter Store. CloudFormation stacks reference them with dynamic references. Changing a network output requires a Terraform apply and then a CloudFormation deploy; there is no automatic trigger.

## What moved back

Nothing was recreated. The `network` nested stack created in February was deleted with `DeletionPolicy: Retain` on every resource and the resources were imported back into Terraform state on 2026-04-28.
