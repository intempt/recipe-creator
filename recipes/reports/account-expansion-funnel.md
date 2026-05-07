---
name: Account Expansion Funnel
description: Plan-limit-to-upgrade funnel built from real subscription state-change events with per-step time-to-convert.
intempt:
  id: account-expansion-funnel
  version: 1.0.0
  slashCommand: /account-expansion-funnel
  shortDescription: Plan-limit-to-upgrade funnel built from real subscription state-change events with per-step time-to-convert.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - b2b
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

# Account Expansion Funnel

Plan-limit-to-upgrade funnel built from real subscription state-change events with per-step time-to-convert.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
