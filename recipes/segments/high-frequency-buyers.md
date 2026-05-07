---
name: High Frequency Buyers
description: Customers who purchase 4+ times per quarter — most loyal cohort.
intempt:
  id: high-frequency-buyers
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Customers who purchase 4+ times per quarter — most loyal cohort.
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

# High Frequency Buyers

Customers who purchase 4+ times per quarter — most loyal cohort.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
