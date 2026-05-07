---
name: Lead To Mql To Sql Funnel
description: Qualification funnel built on lead_stage_changed transitions with per-stage velocity.
intempt:
  id: lead-to-mql-to-sql-funnel
  version: 1.0.0
  slashCommand: /lead-to-mql-to-sql-funnel
  shortDescription: Qualification funnel built on lead_stage_changed transitions with per-stage velocity.
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

# Lead To Mql To Sql Funnel

Qualification funnel built on lead_stage_changed transitions with per-stage velocity.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
