---
name: Browse To Buy Retention
description: First-visit-to-purchase retention with W1/W4/W12 benchmarks and channel-source comparison.
intempt:
  id: browse-to-buy-retention
  version: 1.0.0
  slashCommand: /browse-to-buy-retention
  shortDescription: First-visit-to-purchase retention with W1/W4/W12 benchmarks and channel-source comparison.
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

# Browse To Buy Retention

First-visit-to-purchase retention with W1/W4/W12 benchmarks and channel-source comparison.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
