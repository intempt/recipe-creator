---
name: High Cart Value Abandoners
description: Cart abandoners with high cart value — priority recovery cohort distinct from frequency-based abandoners.
intempt:
  id: high-cart-value-abandoners
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Cart abandoners with high cart value — priority recovery cohort distinct from frequency-based abandoners.
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

# High Cart Value Abandoners

Cart abandoners with high cart value — priority recovery cohort distinct from frequency-based abandoners.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
