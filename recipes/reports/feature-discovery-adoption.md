---
name: Feature Discovery Adoption
description: 4-step funnel from first feature exposure to repeated use, using canonical click_on patterns.
intempt:
  id: feature-discovery-adoption
  version: 1.0.0
  slashCommand: /feature-discovery-adoption
  shortDescription: 4-step funnel from first feature exposure to repeated use, using canonical click_on patterns.
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
    - funnel
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-funnel-report
    describe: Configure and materialize the report described below.
    produces: report
---

# Feature Discovery Adoption

4-step funnel from first feature exposure to repeated use, using canonical click_on patterns.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
