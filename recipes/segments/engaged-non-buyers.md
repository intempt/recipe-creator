---
name: Engaged Non Buyers
description: Highly engaged visitors who have never made a purchase — first-purchase targeting cohort.
intempt:
  id: engaged-non-buyers
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Highly engaged visitors who have never made a purchase — first-purchase targeting cohort.
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

# Engaged Non Buyers

Highly engaged visitors who have never made a purchase — first-purchase targeting cohort.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
