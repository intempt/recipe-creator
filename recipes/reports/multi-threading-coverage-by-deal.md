---
name: Multi Threading Coverage By Deal
description: Number of distinct stakeholders engaged per deal — single-threaded deals close at materially lower rates per
  Gartner.
intempt:
  id: multi-threading-coverage-by-deal
  version: 1.0.0
  slashCommand: /multi-threading-coverage-by-deal
  shortDescription: Number of distinct stakeholders engaged per deal — single-threaded deals close at materially lower rates
    per Gartner.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - b2b
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

# Multi Threading Coverage By Deal

Number of distinct stakeholders engaged per deal — single-threaded deals close at materially lower rates per Gartner.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
