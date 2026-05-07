---
name: Mrr Movement Decomposition
description: The canonical SaaS MRR waterfall — new, expansion, contraction, churn, reactivation per month. Requires subscription_updated
  delta-computation.
intempt:
  id: mrr-movement-decomposition
  version: 1.0.0
  slashCommand: /mrr-movement-decomposition
  shortDescription: The canonical SaaS MRR waterfall — new, expansion, contraction, churn, reactivation per month. Requires
    subscription_updated delta-computation.
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

# Mrr Movement Decomposition

The canonical SaaS MRR waterfall — new, expansion, contraction, churn, reactivation per month. Requires subscription_updated delta-computation.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
