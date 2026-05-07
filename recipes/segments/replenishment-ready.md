---
name: Replenishment Ready
description: Customers approaching their typical re-order cycle. 8-15% conversion on replenishment reminders vs 1-3% on general
  promos.
intempt:
  id: replenishment-ready
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Customers approaching their typical re-order cycle. 8-15% conversion on replenishment reminders vs 1-3%
    on general promos.
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

# Replenishment Ready

Customers approaching their typical re-order cycle. 8-15% conversion on replenishment reminders vs 1-3% on general promos.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
