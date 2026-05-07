---
name: Plg Sales Handoff Dashboard
description: 'PLG sales view: PQL leaderboard, account-level PQA signals, paywall conversion, and free-to-paid funnel.'
intempt:
  id: plg-sales-handoff-dashboard
  version: 1.0.0
  slashCommand: /plg-sales-handoff-dashboard
  shortDescription: 'PLG sales view: PQL leaderboard, account-level PQA signals, paywall conversion, and free-to-paid funnel.'
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

# Plg Sales Handoff Dashboard

PLG sales view: PQL leaderboard, account-level PQA signals, paywall conversion, and free-to-paid funnel.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
