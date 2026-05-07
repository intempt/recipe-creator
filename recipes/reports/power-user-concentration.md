---
name: Power User Concentration
description: Pareto chart of top 1% / 5% / 10% of users by event volume vs share of total events.
intempt:
  id: power-user-concentration
  version: 1.0.0
  slashCommand: /power-user-concentration
  shortDescription: Pareto chart of top 1% / 5% / 10% of users by event volume vs share of total events.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - saas
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

# Power User Concentration

Pareto chart of top 1% / 5% / 10% of users by event volume vs share of total events.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
