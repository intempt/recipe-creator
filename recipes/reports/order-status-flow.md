---
name: Order Status Flow
description: Order distribution across created/fulfilled/refunded/cancelled states over time — the operational pulse of order
  flow.
intempt:
  id: order-status-flow
  version: 1.0.0
  slashCommand: /order-status-flow
  shortDescription: Order distribution across created/fulfilled/refunded/cancelled states over time — the operational pulse
    of order flow.
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

# Order Status Flow

Order distribution across created/fulfilled/refunded/cancelled states over time — the operational pulse of order flow.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
