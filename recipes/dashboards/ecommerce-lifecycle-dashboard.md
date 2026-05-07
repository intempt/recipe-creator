---
name: Ecommerce Lifecycle Dashboard
description: 'CRM / retention view: lifecycle distribution + migration, replenishment timing, discount cannibalization, and
  post-purchase paths.'
intempt:
  id: ecommerce-lifecycle-dashboard
  version: 1.0.0
  slashCommand: /ecommerce-lifecycle-dashboard
  shortDescription: 'CRM / retention view: lifecycle distribution + migration, replenishment timing, discount cannibalization,
    and post-purchase paths.'
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

# Ecommerce Lifecycle Dashboard

CRM / retention view: lifecycle distribution + migration, replenishment timing, discount cannibalization, and post-purchase paths.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
