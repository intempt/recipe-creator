---
name: Account Engagement Score Trend
description: Account-level engagement (rolled up from all users on the account) tracked over time — identifies expansion vs.
  churn-risk accounts.
intempt:
  id: account-engagement-score-trend
  version: 1.0.0
  slashCommand: /account-engagement-score-trend
  shortDescription: Account-level engagement (rolled up from all users on the account) tracked over time — identifies expansion
    vs. churn-risk accounts.
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

# Account Engagement Score Trend

Account-level engagement (rolled up from all users on the account) tracked over time — identifies expansion vs. churn-risk accounts.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
