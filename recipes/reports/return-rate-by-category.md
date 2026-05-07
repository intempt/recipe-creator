---
name: Return Rate By Category
description: Return rate by product category with previous-period comparison and rising-rate flagging.
intempt:
  id: return-rate-by-category
  version: 1.0.0
  slashCommand: /return-rate-by-category
  shortDescription: Return rate by product category with previous-period comparison and rising-rate flagging.
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

# Return Rate By Category

Return rate by product category with previous-period comparison and rising-rate flagging.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
