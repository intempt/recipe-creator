---
name: Browse Purchase Funnel
description: Browse-to-purchase funnel using canonical page_viewed/cart/order events with device-comparison conversion.
intempt:
  id: browse-purchase-funnel
  version: 1.0.0
  slashCommand: /browse-purchase-funnel
  shortDescription: Browse-to-purchase funnel using canonical page_viewed/cart/order events with device-comparison conversion.
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
    - funnel
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-funnel-report
    describe: Configure and materialize the report described below.
    produces: report
---

# Browse Purchase Funnel

Browse-to-purchase funnel using canonical page_viewed/cart/order events with device-comparison conversion.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
