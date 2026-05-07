---
name: Cart Abandonment Rate
description: Cart abandonment rate by device with previous-period comparison and a 70% benchmark line.
intempt:
  id: cart-abandonment-rate
  version: 1.0.0
  slashCommand: /cart-abandonment-rate
  shortDescription: Cart abandonment rate by device with previous-period comparison and a 70% benchmark line.
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

# Cart Abandonment Rate

Cart abandonment rate by device with previous-period comparison and a 70% benchmark line.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
