---
name: Weekly Business Review Summary
description: Single dashboard with the 6 KPIs every founder/exec wants every Monday — new customers, churn, revenue, MRR/ARR,
  retention, top engagement.
intempt:
  id: weekly-business-review-summary
  version: 1.0.0
  slashCommand: /weekly-business-review-summary
  shortDescription: Single dashboard with the 6 KPIs every founder/exec wants every Monday — new customers, churn, revenue,
    MRR/ARR, retention, top engagement.
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

# Weekly Business Review Summary

Single dashboard with the 6 KPIs every founder/exec wants every Monday — new customers, churn, revenue, MRR/ARR, retention, top engagement.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
