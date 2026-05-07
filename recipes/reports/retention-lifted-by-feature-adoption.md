---
name: Retention Lifted By Feature Adoption
description: Side-by-side cohort retention curves for users who adopted a target feature in week 1 vs those who didn't.
intempt:
  id: retention-lifted-by-feature-adoption
  version: 1.0.0
  slashCommand: /retention-lifted-by-feature-adoption
  shortDescription: Side-by-side cohort retention curves for users who adopted a target feature in week 1 vs those who didn't.
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
    - retention
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-retention-report
    describe: Configure and materialize the report described below.
    produces: report
---

# Retention Lifted By Feature Adoption

Side-by-side cohort retention curves for users who adopted a target feature in week 1 vs those who didn't.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
