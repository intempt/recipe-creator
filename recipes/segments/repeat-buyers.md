---
name: Repeat Buyers
description: Customers who have made 3+ purchases in the last 90 days with meaningful spend.
intempt:
  id: repeat-buyers
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Customers who have made 3+ purchases in the last 90 days with meaningful spend.
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

# Repeat Buyers

Customers who have made 3+ purchases in the last 90 days with meaningful spend.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
