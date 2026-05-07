---
name: Subscription Health Dashboard
description: 'Finance / RevOps view: MRR movement, churn cohorts, payment recovery, NRR — the monthly board-review subscription
  metrics.'
intempt:
  id: subscription-health-dashboard
  version: 1.0.0
  slashCommand: /subscription-health-dashboard
  shortDescription: 'Finance / RevOps view: MRR movement, churn cohorts, payment recovery, NRR — the monthly board-review
    subscription metrics.'
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - saas
    complexity: standard
    executionMode: live
    tags:
    - dashboard
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: dashboard
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
  steps:
  - id: build-dashboard
    describe: Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes
      per the spec below.
    produces: dashboard
---

# Subscription Health Dashboard

Finance / RevOps view: MRR movement, churn cohorts, payment recovery, NRR — the monthly board-review subscription metrics.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
