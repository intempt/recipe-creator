---
name: Discount Only Buyers
description: Customers who only purchase when a discount is applied — suppression cohort for full-price campaigns.
intempt:
  id: discount-only-buyers
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Customers who only purchase when a discount is applied — suppression cohort for full-price campaigns.
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

# Discount Only Buyers

Customers who only purchase when a discount is applied — suppression cohort for full-price campaigns.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
