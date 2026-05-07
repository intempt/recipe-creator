---
name: Post Conversion Onboarding Paths
description: Forward path from first paid event (subscription or order) — what new paying customers do in their first session
  as customers.
intempt:
  id: post-conversion-onboarding-paths
  version: 1.0.0
  slashCommand: /post-conversion-onboarding-paths
  shortDescription: Forward path from first paid event (subscription or order) — what new paying customers do in their first
    session as customers.
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

# Post Conversion Onboarding Paths

Forward path from first paid event (subscription or order) — what new paying customers do in their first session as customers.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
