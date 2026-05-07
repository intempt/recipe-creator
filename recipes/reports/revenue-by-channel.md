---
name: Revenue By Channel
description: Revenue by acquisition channel with share-of-revenue, period comparison, and channel mix shift.
intempt:
  id: revenue-by-channel
  version: 1.0.0
  slashCommand: /revenue-by-channel
  shortDescription: Revenue by acquisition channel with share-of-revenue, period comparison, and channel mix shift.
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

# Revenue By Channel

Revenue by acquisition channel with share-of-revenue, period comparison, and channel mix shift.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
