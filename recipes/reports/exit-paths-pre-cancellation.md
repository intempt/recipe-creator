---
name: Exit Paths Pre Cancellation
description: Forward path from a /cancel page visit — surfaces what saves vs. kills retention attempts in the cancellation
  moment.
intempt:
  id: exit-paths-pre-cancellation
  version: 1.0.0
  slashCommand: /exit-paths-pre-cancellation
  shortDescription: Forward path from a /cancel page visit — surfaces what saves vs. kills retention attempts in the cancellation
    moment.
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

# Exit Paths Pre Cancellation

Forward path from a /cancel page visit — surfaces what saves vs. kills retention attempts in the cancellation moment.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
