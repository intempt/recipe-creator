---
name: Newly Activated Users
description: Users who completed activation in the last 7 days — warm and ready to expand.
intempt:
  id: newly-activated-users
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Users who completed activation in the last 7 days — warm and ready to expand.
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

# Newly Activated Users

Users who completed activation in the last 7 days — warm and ready to expand.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
