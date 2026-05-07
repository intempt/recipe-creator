---
name: Forecast Vs Actual Quota
description: Period-level revenue forecast vs. actual closed-won vs. quota target with pipeline coverage ratio and projected
  close.
intempt:
  id: forecast-vs-actual-quota
  version: 1.0.0
  slashCommand: /forecast-vs-actual-quota
  shortDescription: Period-level revenue forecast vs. actual closed-won vs. quota target with pipeline coverage ratio and
    projected close.
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

# Forecast Vs Actual Quota

Period-level revenue forecast vs. actual closed-won vs. quota target with pipeline coverage ratio and projected close.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
