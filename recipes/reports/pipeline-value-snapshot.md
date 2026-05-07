---
name: Pipeline Value Snapshot
description: Current open-pipeline value with stage decomposition, weighted forecast, and concentration risk surfacing.
intempt:
  id: pipeline-value-snapshot
  version: 1.0.0
  slashCommand: /pipeline-value-snapshot
  shortDescription: Current open-pipeline value with stage decomposition, weighted forecast, and concentration risk surfacing.
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

# Pipeline Value Snapshot

Current open-pipeline value with stage decomposition, weighted forecast, and concentration risk surfacing.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
