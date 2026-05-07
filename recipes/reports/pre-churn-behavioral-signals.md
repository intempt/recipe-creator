---
name: Pre Churn Behavioral Signals
description: Path to subscription_cancelled with precursor-event ranking by lift over baseline.
intempt:
  id: pre-churn-behavioral-signals
  version: 1.0.0
  slashCommand: /pre-churn-behavioral-signals
  shortDescription: Path to subscription_cancelled with precursor-event ranking by lift over baseline.
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

# Pre Churn Behavioral Signals

Path to subscription_cancelled with precursor-event ranking by lift over baseline.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
