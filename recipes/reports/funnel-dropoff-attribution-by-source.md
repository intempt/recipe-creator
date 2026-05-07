---
name: Funnel Dropoff Attribution By Source
description: Same funnel run separately by Users.utm_source — surfaces which acquisition channels actually convert.
intempt:
  id: funnel-dropoff-attribution-by-source
  version: 1.0.0
  slashCommand: /funnel-dropoff-attribution-by-source
  shortDescription: Same funnel run separately by Users.utm_source — surfaces which acquisition channels actually convert.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - all
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

# Funnel Dropoff Attribution By Source

Same funnel run separately by Users.utm_source — surfaces which acquisition channels actually convert.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
