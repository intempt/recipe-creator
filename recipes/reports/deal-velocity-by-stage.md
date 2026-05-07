---
name: Deal Velocity By Stage
description: Median time spent in each deal stage with bottleneck-stage identification and won/lost velocity comparison.
intempt:
  id: deal-velocity-by-stage
  version: 1.0.0
  slashCommand: /deal-velocity-by-stage
  shortDescription: Median time spent in each deal stage with bottleneck-stage identification and won/lost velocity comparison.
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

# Deal Velocity By Stage

Median time spent in each deal stage with bottleneck-stage identification and won/lost velocity comparison.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
