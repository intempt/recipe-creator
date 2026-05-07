---
name: Support Tickets Vs Churn Correlation
description: Dual-axis support ticket volume vs subscription cancellations with priority decomposition and lead-lag.
intempt:
  id: support-tickets-vs-churn-correlation
  version: 1.0.0
  slashCommand: /support-tickets-vs-churn-correlation
  shortDescription: Dual-axis support ticket volume vs subscription cancellations with priority decomposition and lead-lag.
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

# Support Tickets Vs Churn Correlation

Dual-axis support ticket volume vs subscription cancellations with priority decomposition and lead-lag.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
