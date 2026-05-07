---
name: Rep Activity Leaderboard
description: Per-rep sales activity (calls, emails, meetings, tasks) with revenue-correlation and quota-attainment overlay.
intempt:
  id: rep-activity-leaderboard
  version: 1.0.0
  slashCommand: /rep-activity-leaderboard
  shortDescription: Per-rep sales activity (calls, emails, meetings, tasks) with revenue-correlation and quota-attainment
    overlay.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - b2b
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

# Rep Activity Leaderboard

Per-rep sales activity (calls, emails, meetings, tasks) with revenue-correlation and quota-attainment overlay.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
