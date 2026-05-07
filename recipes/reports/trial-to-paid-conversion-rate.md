---
name: Trial To Paid Conversion Rate
description: Weekly trial-to-paid conversion using subscription_created.trial_end semantics with 18% benchmark.
intempt:
  id: trial-to-paid-conversion-rate
  version: 1.0.0
  slashCommand: /trial-to-paid-conversion-rate
  shortDescription: Weekly trial-to-paid conversion using subscription_created.trial_end semantics with 18% benchmark.
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
    - insights
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-insights-report
    describe: Configure and materialize the report described below.
    produces: report
---

# Trial To Paid Conversion Rate

Weekly trial-to-paid conversion using subscription_created.trial_end semantics with 18% benchmark.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
