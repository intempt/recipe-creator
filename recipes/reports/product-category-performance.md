---
name: Product Category Performance
description: Revenue + units by category with period comparison and category-level momentum scoring.
intempt:
  id: product-category-performance
  version: 1.0.0
  slashCommand: /product-category-performance
  shortDescription: Revenue + units by category with period comparison and category-level momentum scoring.
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

# Product Category Performance

Revenue + units by category with period comparison and category-level momentum scoring.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
