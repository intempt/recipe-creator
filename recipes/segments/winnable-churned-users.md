---
name: Winnable Churned Users
description: Recently churned users who showed engagement before churn — best win-back candidates.
intempt:
  id: winnable-churned-users
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Recently churned users who showed engagement before churn — best win-back candidates.
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

# Winnable Churned Users

Recently churned users who showed engagement before churn — best win-back candidates.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
