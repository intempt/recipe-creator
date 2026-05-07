---
name: Monthly Logo Retention Trend
description: Single trailing logo-retention rate over time — the headline number that pairs with NRR but answers a simpler
  question.
intempt:
  id: monthly-logo-retention-trend
  version: 1.0.0
  slashCommand: /monthly-logo-retention-trend
  shortDescription: Single trailing logo-retention rate over time — the headline number that pairs with NRR but answers a
    simpler question.
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

# Monthly Logo Retention Trend

Single trailing logo-retention rate over time — the headline number that pairs with NRR but answers a simpler question.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
