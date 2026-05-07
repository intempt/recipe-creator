---
name: Active Vs Passive Users
description: 'Three-way split: producers (frequent click_on), consumers (only page_viewed/session_start), and inactive — the
  hidden segment most teams miss.'
intempt:
  id: active-vs-passive-users
  version: 1.0.0
  slashCommand: /active-vs-passive-users
  shortDescription: 'Three-way split: producers (frequent click_on), consumers (only page_viewed/session_start), and inactive
    — the hidden segment most teams miss.'
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - saas
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

# Active Vs Passive Users

Three-way split: producers (frequent click_on), consumers (only page_viewed/session_start), and inactive — the hidden segment most teams miss.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
