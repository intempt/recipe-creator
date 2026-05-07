---
name: Lead Customer Sales
description: Sales pipeline funnel using deal_stage_changed and meeting events with stage velocity and forecasted revenue.
intempt:
  id: lead-customer-sales
  version: 1.0.0
  slashCommand: /lead-customer-sales
  shortDescription: Sales pipeline funnel using deal_stage_changed and meeting events with stage velocity and forecasted revenue.
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

# Lead Customer Sales

Sales pipeline funnel using deal_stage_changed and meeting events with stage velocity and forecasted revenue.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
