---
name: Weekly Active Users Trend
description: WAU trend with WAU/MAU stickiness ratio — the standard PLG engagement view.
intempt:
  id: weekly-active-users-trend
  version: 1.0.0
  slashCommand: /weekly-active-users-trend
  shortDescription: WAU trend with WAU/MAU stickiness ratio — the standard PLG engagement view.
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

# Weekly Active Users Trend

WAU trend with WAU/MAU stickiness ratio — the standard PLG engagement view.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
