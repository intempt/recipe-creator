---
name: Failed Payment Accounts
description: Users with payment failure in last 14 days — dunning/recovery cohort.
intempt:
  id: failed-payment-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Users with payment failure in last 14 days — dunning/recovery cohort.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - segments
    agent: segment-architect
    mode:
    - saas
    - ecommerce
    complexity: standard
    executionMode: live
    tags:
    - users-segment
    object: users
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: segment
    type: segment
    description: Segment created on /segments.
  steps:
  - id: configure-segment-rule
    describe: Open the segment authoring surface, name the segment, and apply the rule below.
    produces: segment
---

# Failed Payment Accounts

Users with payment failure in last 14 days — dunning/recovery cohort.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
