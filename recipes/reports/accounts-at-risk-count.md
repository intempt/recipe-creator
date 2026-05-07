---
name: Accounts At Risk Count
description: Count and trend of accounts whose engagement has declined materially — the canonical CS early-warning headline
  metric.
intempt:
  id: accounts-at-risk-count
  version: 1.0.0
  slashCommand: /accounts-at-risk-count
  shortDescription: Count and trend of accounts whose engagement has declined materially — the canonical CS early-warning
    headline metric.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - b2b
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

# Accounts At Risk Count

Count and trend of accounts whose engagement has declined materially — the canonical CS early-warning headline metric.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
