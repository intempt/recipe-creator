---
name: Revenue Operations Dashboard
description: 'RevOps / CRO strategic view: trailing GTM health, funnel attribution by source, win-loss patterns, and NRR trends.'
intempt:
  id: revenue-operations-dashboard
  version: 1.0.0
  slashCommand: /revenue-operations-dashboard
  shortDescription: 'RevOps / CRO strategic view: trailing GTM health, funnel attribution by source, win-loss patterns, and
    NRR trends.'
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

# Revenue Operations Dashboard

RevOps / CRO strategic view: trailing GTM health, funnel attribution by source, win-loss patterns, and NRR trends.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
