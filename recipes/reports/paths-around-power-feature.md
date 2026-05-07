---
name: Paths Around Power Feature
description: Bidirectional path bracketing a high-value feature interaction — surfaces what leads to discovery and what users
  do after.
intempt:
  id: paths-around-power-feature
  version: 1.0.0
  slashCommand: /paths-around-power-feature
  shortDescription: Bidirectional path bracketing a high-value feature interaction — surfaces what leads to discovery and
    what users do after.
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

# Paths Around Power Feature

Bidirectional path bracketing a high-value feature interaction — surfaces what leads to discovery and what users do after.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
