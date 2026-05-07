---
name: Support Deflection Paths
description: Backward path from ticket_created — surfaces in-product paths that immediately precede support tickets.
intempt:
  id: support-deflection-paths
  version: 1.0.0
  slashCommand: /support-deflection-paths
  shortDescription: Backward path from ticket_created — surfaces in-product paths that immediately precede support tickets.
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

# Support Deflection Paths

Backward path from ticket_created — surfaces in-product paths that immediately precede support tickets.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
