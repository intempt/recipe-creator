---
name: Trial Users High Engagement
description: Trial users with strong usage signals who are likely to convert. Engagement scored as low/medium/high.
intempt:
  id: trial-users-high-engagement
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Trial users with strong usage signals who are likely to convert. Engagement scored as low/medium/high.
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

# Trial Users High Engagement

Trial users with strong usage signals who are likely to convert. Engagement scored as low/medium/high.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
