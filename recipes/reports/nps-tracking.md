---
name: Nps Tracking
description: NPS score over time from feedback_submitted with promoter/passive/detractor decomposition and trend.
intempt:
  id: nps-tracking
  version: 1.0.0
  slashCommand: /nps-tracking
  shortDescription: NPS score over time from feedback_submitted with promoter/passive/detractor decomposition and trend.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - all
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

# Nps Tracking

NPS score over time from feedback_submitted with promoter/passive/detractor decomposition and trend.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
