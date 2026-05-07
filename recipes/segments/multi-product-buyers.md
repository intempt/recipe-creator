---
name: Multi Product Buyers
description: Customers who have purchased across multiple distinct products — cross-sell-ready cohort.
intempt:
  id: multi-product-buyers
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Customers who have purchased across multiple distinct products — cross-sell-ready cohort.
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

# Multi Product Buyers

Customers who have purchased across multiple distinct products — cross-sell-ready cohort.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
