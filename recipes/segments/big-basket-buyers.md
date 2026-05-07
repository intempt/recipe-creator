---
name: Big Basket Buyers
description: Customers with high average order value — premium-bundle and upsell-targeting cohort.
intempt:
  id: big-basket-buyers
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Customers with high average order value — premium-bundle and upsell-targeting cohort.
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

# Big Basket Buyers

Customers with high average order value — premium-bundle and upsell-targeting cohort.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
