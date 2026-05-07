---
name: Time To Ship Distribution
description: Histogram of fulfillment time per order with median/p75/p95 callouts and per-bin operational benchmarks.
intempt:
  id: time-to-ship-distribution
  version: 1.0.0
  slashCommand: /time-to-ship-distribution
  shortDescription: Histogram of fulfillment time per order with median/p75/p95 callouts and per-bin operational benchmarks.
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

# Time To Ship Distribution

Histogram of fulfillment time per order with median/p75/p95 callouts and per-bin operational benchmarks.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
