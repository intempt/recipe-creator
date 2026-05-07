---
name: Checkout Form Friction
description: Checkout-stage drop-off with page-level friction surfacing — reveals form fields, payment methods, and steps
  that cause abandonment.
intempt:
  id: checkout-form-friction
  version: 1.0.0
  slashCommand: /checkout-form-friction
  shortDescription: Checkout-stage drop-off with page-level friction surfacing — reveals form fields, payment methods, and
    steps that cause abandonment.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - ecommerce
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

# Checkout Form Friction

Checkout-stage drop-off with page-level friction surfacing — reveals form fields, payment methods, and steps that cause abandonment.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
