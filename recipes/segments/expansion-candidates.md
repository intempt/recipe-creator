---
name: Expansion Candidates
description: Users approaching their plan limit who are ready for an upgrade conversation.
intempt:
  id: expansion-candidates
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Users approaching their plan limit who are ready for an upgrade conversation.
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

# Expansion Candidates

Users approaching their plan limit who are ready for an upgrade conversation.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
