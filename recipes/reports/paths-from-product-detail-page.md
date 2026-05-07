---
name: Paths From Product Detail Page
description: Forward path from PDP page_viewed surfacing whether users add to cart, browse similar, search again, or exit.
intempt:
  id: paths-from-product-detail-page
  version: 1.0.0
  slashCommand: /paths-from-product-detail-page
  shortDescription: Forward path from PDP page_viewed surfacing whether users add to cart, browse similar, search again, or
    exit.
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
    - path
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-path-report
    describe: Configure and materialize the report described below.
    produces: report
---

# Paths From Product Detail Page

Forward path from PDP page_viewed surfacing whether users add to cart, browse similar, search again, or exit.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
