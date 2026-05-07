---
name: Customer Success Dashboard
description: 'CS Lead / CSM view: account health, expansion signals, NRR, NPS, and at-risk account intelligence.'
intempt:
  id: customer-success-dashboard
  version: 1.0.0
  slashCommand: /customer-success-dashboard
  shortDescription: 'CS Lead / CSM view: account health, expansion signals, NRR, NPS, and at-risk account intelligence.'
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

# Customer Success Dashboard

CS Lead / CSM view: account health, expansion signals, NRR, NPS, and at-risk account intelligence.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
