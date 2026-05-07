---
name: Feature Usage Heatmap By Cohort
description: Feature usage by signup cohort with sticky-feature identification and cohort-onboarding regression detection.
intempt:
  id: feature-usage-heatmap-by-cohort
  version: 1.0.0
  slashCommand: /feature-usage-heatmap-by-cohort
  shortDescription: Feature usage by signup cohort with sticky-feature identification and cohort-onboarding regression detection.
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

# Feature Usage Heatmap By Cohort

Feature usage by signup cohort with sticky-feature identification and cohort-onboarding regression detection.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
