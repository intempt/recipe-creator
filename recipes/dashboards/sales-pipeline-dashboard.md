---
name: Sales Pipeline Dashboard
description: 'AE / Sales Manager operational view: open pipeline, deal velocity, multi-threading risk, and account engagement
  on active deals.'
intempt:
  id: sales-pipeline-dashboard
  version: 1.0.0
  slashCommand: /sales-pipeline-dashboard
  shortDescription: 'AE / Sales Manager operational view: open pipeline, deal velocity, multi-threading risk, and account
    engagement on active deals.'
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

# Sales Pipeline Dashboard

AE / Sales Manager operational view: open pipeline, deal velocity, multi-threading risk, and account engagement on active deals.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
