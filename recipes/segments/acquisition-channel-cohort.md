---
name: Acquisition Channel Cohort
description: Customers acquired through a specific channel (parameterized by utm_source/medium) — for channel-quality analysis.
intempt:
  id: acquisition-channel-cohort
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Customers acquired through a specific channel (parameterized by utm_source/medium) — for channel-quality
    analysis.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - segments
    agent: segment-architect
    mode:
    - ecommerce
    - saas
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

# Acquisition Channel Cohort

Customers acquired through a specific channel (parameterized by utm_source/medium) — for channel-quality analysis.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
