---
name: First Session Paths After Signup
description: Forward path from user_created showing what new users actually do in their first session vs. the intended onboarding
  flow.
intempt:
  id: first-session-paths-after-signup
  version: 1.0.0
  slashCommand: /first-session-paths-after-signup
  shortDescription: Forward path from user_created showing what new users actually do in their first session vs. the intended
    onboarding flow.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - saas
    - ecommerce
    complexity: quick
    executionMode: live
    tags:
    - path
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-path-report
    describe: Configure and materialize the report described below.
    produces: report
---

# First Session Paths After Signup

Forward path from user_created showing what new users actually do in their first session vs. the intended onboarding flow.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
