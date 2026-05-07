---
name: Mrr Trend
description: MRR over time by plan with month-over-month growth rate and net-new MRR overlay.
intempt:
  id: mrr-trend
  version: 1.0.0
  slashCommand: /mrr-trend
  shortDescription: MRR over time by plan with month-over-month growth rate and net-new MRR overlay.
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

# Mrr Trend

MRR over time by plan with month-over-month growth rate and net-new MRR overlay.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
