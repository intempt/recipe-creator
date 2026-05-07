---
name: Repeat Cart Abandoners
description: Users who have abandoned checkout 2+ times in the last 30 days without purchasing.
intempt:
  id: repeat-cart-abandoners
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Users who have abandoned checkout 2+ times in the last 30 days without purchasing.
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

# Repeat Cart Abandoners

Users who have abandoned checkout 2+ times in the last 30 days without purchasing.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
