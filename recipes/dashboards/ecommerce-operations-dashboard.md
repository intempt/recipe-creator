---
name: Ecommerce Operations Dashboard
description: 'Ops / fulfillment view: order flow, fulfillment rate, returns, refunds, and quality issues by product.'
intempt:
  id: ecommerce-operations-dashboard
  version: 1.0.0
  slashCommand: /ecommerce-operations-dashboard
  shortDescription: 'Ops / fulfillment view: order flow, fulfillment rate, returns, refunds, and quality issues by product.'
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

# Ecommerce Operations Dashboard

Ops / fulfillment view: order flow, fulfillment rate, returns, refunds, and quality issues by product.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
