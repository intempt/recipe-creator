---
name: Recently Churned Users
description: Users who cancelled their subscription in the last 30 days — fast win-back cohort.
intempt:
  id: recently-churned-users
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Users who cancelled their subscription in the last 30 days — fast win-back cohort.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - segments
    agent: segment-architect
    mode:
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

# Recently Churned Users

Users who cancelled their subscription in the last 30 days — fast win-back cohort.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
