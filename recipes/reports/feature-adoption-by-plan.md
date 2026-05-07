---
name: Feature Adoption By Plan
description: Feature adoption by plan tier with adoption-rate trend and tier-specific feature affinity.
intempt:
  id: feature-adoption-by-plan
  version: 1.0.0
  slashCommand: /feature-adoption-by-plan
  shortDescription: Feature adoption by plan tier with adoption-rate trend and tier-specific feature affinity.
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

# Feature Adoption By Plan

Feature adoption by plan tier with adoption-rate trend and tier-specific feature affinity.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
