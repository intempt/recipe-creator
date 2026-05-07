---
name: Signup Activation Funnel
description: Signup-to-activation funnel using user_created and goal_completed_in_journey with per-step time-to-convert.
intempt:
  id: signup-activation-funnel
  version: 1.0.0
  slashCommand: /signup-activation-funnel
  shortDescription: Signup-to-activation funnel using user_created and goal_completed_in_journey with per-step time-to-convert.
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

# Signup Activation Funnel

Signup-to-activation funnel using user_created and goal_completed_in_journey with per-step time-to-convert.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
