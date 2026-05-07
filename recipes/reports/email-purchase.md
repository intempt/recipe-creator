---
name: Email Purchase
description: Email-to-purchase funnel using canonical email events with campaign comparison and revenue-per-email.
intempt:
  id: email-purchase
  version: 1.0.0
  slashCommand: /email-purchase
  shortDescription: Email-to-purchase funnel using canonical email events with campaign comparison and revenue-per-email.
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

# Email Purchase

Email-to-purchase funnel using canonical email events with campaign comparison and revenue-per-email.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
