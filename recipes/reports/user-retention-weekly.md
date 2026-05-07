---
name: User Retention Weekly
description: Weekly cohort retention with W1/W4/W12 benchmarks and acquisition-source comparison.
intempt:
  id: user-retention-weekly
  version: 1.0.0
  slashCommand: /user-retention-weekly
  shortDescription: Weekly cohort retention with W1/W4/W12 benchmarks and acquisition-source comparison.
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

# User Retention Weekly

Weekly cohort retention with W1/W4/W12 benchmarks and acquisition-source comparison.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
