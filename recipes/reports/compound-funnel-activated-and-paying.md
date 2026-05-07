---
name: Compound Funnel Activated And Paying
description: PLG funnel where success = activated AND paying, separating real activation from vanity activation.
intempt:
  id: compound-funnel-activated-and-paying
  version: 1.0.0
  slashCommand: /compound-funnel-activated-and-paying
  shortDescription: PLG funnel where success = activated AND paying, separating real activation from vanity activation.
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

# Compound Funnel Activated And Paying

PLG funnel where success = activated AND paying, separating real activation from vanity activation.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
