---
name: Marketing Attribution Dashboard
description: 'Marketing Lead view: revenue by channel, email-driven revenue, search-driven revenue, and category-level marketing
  performance. Note: ROAS/CAC require ad-spend integration not in canonical taxonomy.'
intempt:
  id: marketing-attribution-dashboard
  version: 1.0.0
  slashCommand: /marketing-attribution-dashboard
  shortDescription: 'Marketing Lead view: revenue by channel, email-driven revenue, search-driven revenue, and category-level
    marketing performance. Note: ROAS/CAC require ad-spend integration not in canonical taxonomy.'
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

# Marketing Attribution Dashboard

Marketing Lead view: revenue by channel, email-driven revenue, search-driven revenue, and category-level marketing performance. Note: ROAS/CAC require ad-spend integration not in canonical taxonomy.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
