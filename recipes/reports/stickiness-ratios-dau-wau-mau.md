---
name: Stickiness Ratios Dau Wau Mau
description: DAU, WAU, MAU with stickiness ratios (DAU/WAU and DAU/MAU) — the standard PLG engagement metric.
intempt:
  id: stickiness-ratios-dau-wau-mau
  version: 1.0.0
  slashCommand: /stickiness-ratios-dau-wau-mau
  shortDescription: DAU, WAU, MAU with stickiness ratios (DAU/WAU and DAU/MAU) — the standard PLG engagement metric.
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

# Stickiness Ratios Dau Wau Mau

DAU, WAU, MAU with stickiness ratios (DAU/WAU and DAU/MAU) — the standard PLG engagement metric.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
