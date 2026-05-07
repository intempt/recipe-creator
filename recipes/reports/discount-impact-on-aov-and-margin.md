---
name: Discount Impact On Aov And Margin
description: How discount usage affects AOV — surfaces whether discounts grow the basket or just shift demand to discounted
  moments.
intempt:
  id: discount-impact-on-aov-and-margin
  version: 1.0.0
  slashCommand: /discount-impact-on-aov-and-margin
  shortDescription: How discount usage affects AOV — surfaces whether discounts grow the basket or just shift demand to discounted
    moments.
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

# Discount Impact On Aov And Margin

How discount usage affects AOV — surfaces whether discounts grow the basket or just shift demand to discounted moments.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
