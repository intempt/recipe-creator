---
name: One Time Buyers At Risk
description: Customers who made one purchase but have not returned in 60+ days.
intempt:
  id: one-time-buyers-at-risk
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Customers who made one purchase but have not returned in 60+ days.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - segments
    agent: segment-architect
    mode:
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

# One Time Buyers At Risk

Customers who made one purchase but have not returned in 60+ days.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
