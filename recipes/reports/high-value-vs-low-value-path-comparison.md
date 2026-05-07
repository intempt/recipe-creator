---
name: High Value Vs Low Value Path Comparison
description: 'Two Path reports side-by-side: paths taken by users who placed >$X orders vs <$X or non-converters.'
intempt:
  id: high-value-vs-low-value-path-comparison
  version: 1.0.0
  slashCommand: /high-value-vs-low-value-path-comparison
  shortDescription: 'Two Path reports side-by-side: paths taken by users who placed >$X orders vs <$X or non-converters.'
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
    - path
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-path-report
    describe: Configure and materialize the report described below.
    produces: report
---

# High Value Vs Low Value Path Comparison

Two Path reports side-by-side: paths taken by users who placed >$X orders vs <$X or non-converters.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
