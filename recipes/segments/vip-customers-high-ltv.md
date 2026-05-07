---
name: Vip Customers High Ltv
description: Highest-value customers by lifetime spend. Concrete numeric threshold (no percentile placeholder).
intempt:
  id: vip-customers-high-ltv
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Highest-value customers by lifetime spend. Concrete numeric threshold (no percentile placeholder).
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

# Vip Customers High Ltv

Highest-value customers by lifetime spend. Concrete numeric threshold (no percentile placeholder).

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
