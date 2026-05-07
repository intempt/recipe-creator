---
name: Cohort Acquisition Ltv Dashboard
description: 'Performance Marketer / DTC Founder view: cohort LTV curves by acquisition channel, repeat-purchase mechanics,
  second-order velocity — the #1 dashboard for $20M+ DTC brands.'
intempt:
  id: cohort-acquisition-ltv-dashboard
  version: 1.0.0
  slashCommand: /cohort-acquisition-ltv-dashboard
  shortDescription: 'Performance Marketer / DTC Founder view: cohort LTV curves by acquisition channel, repeat-purchase mechanics,
    second-order velocity — the #1 dashboard for $20M+ DTC brands.'
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - ecommerce
    complexity: standard
    executionMode: live
    tags:
    - dashboard
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: dashboard
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
  steps:
  - id: build-dashboard
    describe: Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes
      per the spec below.
    produces: dashboard
---

# Cohort Acquisition Ltv Dashboard

Performance Marketer / DTC Founder view: cohort LTV curves by acquisition channel, repeat-purchase mechanics, second-order velocity — the #1 dashboard for $20M+ DTC brands.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
