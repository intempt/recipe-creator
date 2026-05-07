---
name: First Purchase Cohort Ltv Curve
description: Cumulative revenue per cohort member by cohort age — the textbook DTC LTV view.
intempt:
  id: first-purchase-cohort-ltv-curve
  version: 1.0.0
  slashCommand: /first-purchase-cohort-ltv-curve
  shortDescription: Cumulative revenue per cohort member by cohort age — the textbook DTC LTV view.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - ecommerce
    complexity: quick
    executionMode: live
    tags:
    - insights
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-insights-report
    describe: Configure and materialize the report described below.
    produces: report
---

# First Purchase Cohort Ltv Curve

Cumulative revenue per cohort member by cohort age — the textbook DTC LTV view.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
