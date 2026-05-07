---
name: Activation Funnel With Velocity
description: Activation funnel with median + p75 step velocity — surfaces where users stall, not just where they drop.
intempt:
  id: activation-funnel-with-velocity
  version: 1.0.0
  slashCommand: /activation-funnel-with-velocity
  shortDescription: Activation funnel with median + p75 step velocity — surfaces where users stall, not just where they drop.
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

# Activation Funnel With Velocity

Activation funnel with median + p75 step velocity — surfaces where users stall, not just where they drop.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
