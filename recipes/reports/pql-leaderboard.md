---
name: Pql Leaderboard
description: Sortable list of free users hitting configurable PQL thresholds — the canonical PLG sales-handoff report.
intempt:
  id: pql-leaderboard
  version: 1.0.0
  slashCommand: /pql-leaderboard
  shortDescription: Sortable list of free users hitting configurable PQL thresholds — the canonical PLG sales-handoff report.
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

# Pql Leaderboard

Sortable list of free users hitting configurable PQL thresholds — the canonical PLG sales-handoff report.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
