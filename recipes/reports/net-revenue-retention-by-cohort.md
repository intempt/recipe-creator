---
name: Net Revenue Retention By Cohort
description: 'Proper NRR per cohort: starting MRR + expansion + reactivation − contraction − churn. Requires subscription_updated
  delta-computation.'
intempt:
  id: net-revenue-retention-by-cohort
  version: 1.0.0
  slashCommand: /net-revenue-retention-by-cohort
  shortDescription: 'Proper NRR per cohort: starting MRR + expansion + reactivation − contraction − churn. Requires subscription_updated
    delta-computation.'
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

# Net Revenue Retention By Cohort

Proper NRR per cohort: starting MRR + expansion + reactivation − contraction − churn. Requires subscription_updated delta-computation.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
