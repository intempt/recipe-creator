---
name: Campaign Performance Leaderboard
description: 'Per-campaign email/SMS performance: sent, opened, clicked, converted, revenue, revenue-per-send — the canonical
  Klaviyo-style view.'
intempt:
  id: campaign-performance-leaderboard
  version: 1.0.0
  slashCommand: /campaign-performance-leaderboard
  shortDescription: 'Per-campaign email/SMS performance: sent, opened, clicked, converted, revenue, revenue-per-send — the
    canonical Klaviyo-style view.'
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - ecommerce
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

# Campaign Performance Leaderboard

Per-campaign email/SMS performance: sent, opened, clicked, converted, revenue, revenue-per-send — the canonical Klaviyo-style view.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
