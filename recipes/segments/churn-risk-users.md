---
name: Churn Risk Users
description: Previously active paid users who have gone silent in the last month.
intempt:
  id: churn-risk-users
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Previously active paid users who have gone silent in the last month.
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

# Churn Risk Users

Previously active paid users who have gone silent in the last month.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
