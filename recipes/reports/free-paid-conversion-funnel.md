---
name: Free Paid Conversion Funnel
description: Trial-to-paid funnel using subscription_created (trial mode), pricing page views, and checkout_created.
intempt:
  id: free-paid-conversion-funnel
  version: 1.0.0
  slashCommand: /free-paid-conversion-funnel
  shortDescription: Trial-to-paid funnel using subscription_created (trial mode), pricing page views, and checkout_created.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - saas
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

# Free Paid Conversion Funnel

Trial-to-paid funnel using subscription_created (trial mode), pricing page views, and checkout_created.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
