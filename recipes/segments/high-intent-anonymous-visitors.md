---
name: High Intent Anonymous Visitors
description: Unidentified visitors with strong engagement signals — ad retargeting cohort.
intempt:
  id: high-intent-anonymous-visitors
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Unidentified visitors with strong engagement signals — ad retargeting cohort.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - segments
    agent: segment-architect
    mode:
    - saas
    - b2b
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

# High Intent Anonymous Visitors

Unidentified visitors with strong engagement signals — ad retargeting cohort.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
