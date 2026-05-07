---
name: Trial Activation Funnel
description: Trial milestone funnel using subscription_created (trial), session_start, and journey-goal events.
intempt:
  id: trial-activation-funnel
  version: 1.0.0
  slashCommand: /trial-activation-funnel
  shortDescription: Trial milestone funnel using subscription_created (trial), session_start, and journey-goal events.
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

# Trial Activation Funnel

Trial milestone funnel using subscription_created (trial), session_start, and journey-goal events.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
