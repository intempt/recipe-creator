---
name: Refund Rate By Product And Category
description: Refund rate by product (from order line items) with previous-period comparison and quality-issue flagging.
intempt:
  id: refund-rate-by-product-and-category
  version: 1.0.0
  slashCommand: /refund-rate-by-product-and-category
  shortDescription: Refund rate by product (from order line items) with previous-period comparison and quality-issue flagging.
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

# Refund Rate By Product And Category

Refund rate by product (from order line items) with previous-period comparison and quality-issue flagging.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
