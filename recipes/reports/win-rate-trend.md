---
name: Win Rate Trend
description: Win rate over time as a single tracking metric — surfaces GTM health trajectory without the breakdown overhead
  of win-loss-analysis.
intempt:
  id: win-rate-trend
  version: 1.0.0
  slashCommand: /win-rate-trend
  shortDescription: Win rate over time as a single tracking metric — surfaces GTM health trajectory without the breakdown
    overhead of win-loss-analysis.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - b2b
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

# Win Rate Trend

Win rate over time as a single tracking metric — surfaces GTM health trajectory without the breakdown overhead of win-loss-analysis.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
