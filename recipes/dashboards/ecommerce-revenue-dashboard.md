---
name: Ecommerce Revenue Dashboard
description: 'Founder / CMO revenue overview: top-line revenue, AOV, channel, conversion, and category performance.'
intempt:
  id: ecommerce-revenue-dashboard
  version: 1.0.0
  slashCommand: /ecommerce-revenue-dashboard
  shortDescription: 'Founder / CMO revenue overview: top-line revenue, AOV, channel, conversion, and category performance.'
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

# Ecommerce Revenue Dashboard

Founder / CMO revenue overview: top-line revenue, AOV, channel, conversion, and category performance.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
