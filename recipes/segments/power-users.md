---
name: Power Users
description: Highly engaged users with frequent sessions and high activity score in the last 30 days.
intempt:
  id: power-users
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Highly engaged users with frequent sessions and high activity score in the last 30 days.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - segments
    agent: segment-architect
    mode:
    - all
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

# Power Users

Highly engaged users with frequent sessions and high activity score in the last 30 days.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
