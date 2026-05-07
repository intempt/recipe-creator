---
name: Paid User Retention
description: Monthly paid retention with logo and revenue retention separately, plus plan-tier comparison.
intempt:
  id: paid-user-retention
  version: 1.0.0
  slashCommand: /paid-user-retention
  shortDescription: Monthly paid retention with logo and revenue retention separately, plus plan-tier comparison.
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
    - retention
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-retention-report
    describe: Configure and materialize the report described below.
    produces: report
---

# Paid User Retention

Monthly paid retention with logo and revenue retention separately, plus plan-tier comparison.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
