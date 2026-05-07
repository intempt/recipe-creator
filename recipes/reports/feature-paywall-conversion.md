---
name: Feature Paywall Conversion
description: 'Per-feature: % of free users who interact with it and subsequently view pricing AND subscribe — informs feature-gating
  strategy.'
intempt:
  id: feature-paywall-conversion
  version: 1.0.0
  slashCommand: /feature-paywall-conversion
  shortDescription: 'Per-feature: % of free users who interact with it and subsequently view pricing AND subscribe — informs
    feature-gating strategy.'
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - saas
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

# Feature Paywall Conversion

Per-feature: % of free users who interact with it and subsequently view pricing AND subscribe — informs feature-gating strategy.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
