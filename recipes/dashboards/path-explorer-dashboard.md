---
name: Path Explorer Dashboard
description: 'UX / PM research view: the full set of behavioral path analyses on one canvas — first-session, feature paths,
  support deflection, pre-churn.'
intempt:
  id: path-explorer-dashboard
  version: 1.0.0
  slashCommand: /path-explorer-dashboard
  shortDescription: 'UX / PM research view: the full set of behavioral path analyses on one canvas — first-session, feature
    paths, support deflection, pre-churn.'
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

# Path Explorer Dashboard

UX / PM research view: the full set of behavioral path analyses on one canvas — first-session, feature paths, support deflection, pre-churn.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
