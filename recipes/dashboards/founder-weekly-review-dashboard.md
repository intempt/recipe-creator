---
name: Founder Weekly Review Dashboard
description: The single scorecard a founder/operator wants every Monday — new customers, churn, revenue, retention, engagement,
  with WoW and YoY comparison.
intempt:
  id: founder-weekly-review-dashboard
  version: 1.0.0
  slashCommand: /founder-weekly-review-dashboard
  shortDescription: The single scorecard a founder/operator wants every Monday — new customers, churn, revenue, retention,
    engagement, with WoW and YoY comparison.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - all
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

# Founder Weekly Review Dashboard

The single scorecard a founder/operator wants every Monday — new customers, churn, revenue, retention, engagement, with WoW and YoY comparison.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
