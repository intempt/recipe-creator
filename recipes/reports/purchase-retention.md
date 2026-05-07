---
name: Purchase Retention
description: Repeat-purchase retention with cohort-level second-purchase rates and time-to-2nd-purchase distribution.
intempt:
  id: purchase-retention
  version: 1.0.0
  slashCommand: /purchase-retention
  shortDescription: Repeat-purchase retention with cohort-level second-purchase rates and time-to-2nd-purchase distribution.
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

# Purchase Retention

Repeat-purchase retention with cohort-level second-purchase rates and time-to-2nd-purchase distribution.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
