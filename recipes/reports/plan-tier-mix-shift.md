---
name: Plan Tier Mix Shift
description: '% of revenue and % of customers per plan over time, surfacing up-market vs down-market drift.'
intempt:
  id: plan-tier-mix-shift
  version: 1.0.0
  slashCommand: /plan-tier-mix-shift
  shortDescription: '% of revenue and % of customers per plan over time, surfacing up-market vs down-market drift.'
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

# Plan Tier Mix Shift

% of revenue and % of customers per plan over time, surfacing up-market vs down-market drift.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
