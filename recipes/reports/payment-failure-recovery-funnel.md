---
name: Payment Failure Recovery Funnel
description: Dunning recovery funnel using canonical billing events with per-attempt success rate and revenue-at-risk.
intempt:
  id: payment-failure-recovery-funnel
  version: 1.0.0
  slashCommand: /payment-failure-recovery-funnel
  shortDescription: Dunning recovery funnel using canonical billing events with per-attempt success rate and revenue-at-risk.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - saas
    complexity: quick
    executionMode: live
    tags:
    - funnel
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-funnel-report
    describe: Configure and materialize the report described below.
    produces: report
---

# Payment Failure Recovery Funnel

Dunning recovery funnel using canonical billing events with per-attempt success rate and revenue-at-risk.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
