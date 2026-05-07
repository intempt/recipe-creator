---
name: Customer Lifecycle Distribution
description: Distribution of customers across the canonical lifecycle stages (At risk, Needs attention, New customers, Promising,
  Regulars, Champions) with month-over-month migration tracking.
intempt:
  id: customer-lifecycle-distribution
  version: 1.0.0
  slashCommand: /customer-lifecycle-distribution
  shortDescription: Distribution of customers across the canonical lifecycle stages (At risk, Needs attention, New customers,
    Promising, Regulars, Champions) with month-over-month migration tracking.
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

# Customer Lifecycle Distribution

Distribution of customers across the canonical lifecycle stages (At risk, Needs attention, New customers, Promising, Regulars, Champions) with month-over-month migration tracking.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
