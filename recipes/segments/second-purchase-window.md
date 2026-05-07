---
name: Second Purchase Window
description: First-time buyers in the critical 1-30 day window after their first order. 50% of all repeat purchases happen
  here.
intempt:
  id: second-purchase-window
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: First-time buyers in the critical 1-30 day window after their first order. 50% of all repeat purchases
    happen here.
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

# Second Purchase Window

First-time buyers in the critical 1-30 day window after their first order. 50% of all repeat purchases happen here.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
