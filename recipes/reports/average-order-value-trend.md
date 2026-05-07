---
name: Average Order Value Trend
description: AOV over time with units-per-order vs price-per-unit decomposition and new-vs-returning comparison.
intempt:
  id: average-order-value-trend
  version: 1.0.0
  slashCommand: /average-order-value-trend
  shortDescription: AOV over time with units-per-order vs price-per-unit decomposition and new-vs-returning comparison.
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

# Average Order Value Trend

AOV over time with units-per-order vs price-per-unit decomposition and new-vs-returning comparison.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
