---
name: Customer 360 Dashboard
description: 'CRM / Lifecycle view: lifecycle stage distribution, repeat-purchase mechanics, LTV by acquisition cohort.'
intempt:
  id: customer-360-dashboard
  version: 1.0.0
  slashCommand: /customer-360-dashboard
  shortDescription: 'CRM / Lifecycle view: lifecycle stage distribution, repeat-purchase mechanics, LTV by acquisition cohort.'
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

# Customer 360 Dashboard

CRM / Lifecycle view: lifecycle stage distribution, repeat-purchase mechanics, LTV by acquisition cohort.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
