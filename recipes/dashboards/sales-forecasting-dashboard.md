---
name: Sales Forecasting Dashboard
description: 'Sales VP / CRO forecasting view: pipeline coverage 3:1, weighted forecast, quota attainment, projected close,
  forecast accuracy.'
intempt:
  id: sales-forecasting-dashboard
  version: 1.0.0
  slashCommand: /sales-forecasting-dashboard
  shortDescription: 'Sales VP / CRO forecasting view: pipeline coverage 3:1, weighted forecast, quota attainment, projected
    close, forecast accuracy.'
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - b2b
    complexity: standard
    executionMode: live
    tags:
    - dashboard
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: dashboard
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
  steps:
  - id: build-dashboard
    describe: Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes
      per the spec below.
    produces: dashboard
---

# Sales Forecasting Dashboard

Sales VP / CRO forecasting view: pipeline coverage 3:1, weighted forecast, quota attainment, projected close, forecast accuracy.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
