---
name: Quota Attainment By Rep
description: Per-rep quota attainment (% of target hit) with trend, coverage ratio, and ranking — the headline sales-manager
  metric.
intempt:
  id: quota-attainment-by-rep
  version: 1.0.0
  slashCommand: /quota-attainment-by-rep
  shortDescription: Per-rep quota attainment (% of target hit) with trend, coverage ratio, and ranking — the headline sales-manager
    metric.
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

# Quota Attainment By Rep

Per-rep quota attainment (% of target hit) with trend, coverage ratio, and ranking — the headline sales-manager metric.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
