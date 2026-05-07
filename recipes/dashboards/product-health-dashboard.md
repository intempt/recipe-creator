---
name: Product Health Dashboard
description: 'PM view: stickiness, feature adoption depth, retention by feature, NPS, and the active vs. passive user split.'
intempt:
  id: product-health-dashboard
  version: 1.0.0
  slashCommand: /product-health-dashboard
  shortDescription: 'PM view: stickiness, feature adoption depth, retention by feature, NPS, and the active vs. passive user
    split.'
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

# Product Health Dashboard

PM view: stickiness, feature adoption depth, retention by feature, NPS, and the active vs. passive user split.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
