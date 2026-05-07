---
name: Expansion Revenue Trend
description: Expansion revenue derived from subscription_updated change-events with quality-of-MRR-growth surfacing.
intempt:
  id: expansion-revenue-trend
  version: 1.0.0
  slashCommand: /expansion-revenue-trend
  shortDescription: Expansion revenue derived from subscription_updated change-events with quality-of-MRR-growth surfacing.
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

# Expansion Revenue Trend

Expansion revenue derived from subscription_updated change-events with quality-of-MRR-growth surfacing.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
