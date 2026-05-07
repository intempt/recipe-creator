---
name: Sales Activity Coaching Dashboard
description: 'Sales Manager view: rep activity (calls/emails/meetings), revenue-per-call efficiency, win-loss patterns — the
  canonical coaching artifact.'
intempt:
  id: sales-activity-coaching-dashboard
  version: 1.0.0
  slashCommand: /sales-activity-coaching-dashboard
  shortDescription: 'Sales Manager view: rep activity (calls/emails/meetings), revenue-per-call efficiency, win-loss patterns
    — the canonical coaching artifact.'
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - b2b
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

# Sales Activity Coaching Dashboard

Sales Manager view: rep activity (calls/emails/meetings), revenue-per-call efficiency, win-loss patterns — the canonical coaching artifact.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
