---
name: Post Purchase Second Order Velocity
description: Histogram of days from 1st to 2nd order_created — informs the right delay for replenishment journey triggers.
intempt:
  id: post-purchase-second-order-velocity
  version: 1.0.0
  slashCommand: /post-purchase-second-order-velocity
  shortDescription: Histogram of days from 1st to 2nd order_created — informs the right delay for replenishment journey triggers.
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

# Post Purchase Second Order Velocity

Histogram of days from 1st to 2nd order_created — informs the right delay for replenishment journey triggers.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
