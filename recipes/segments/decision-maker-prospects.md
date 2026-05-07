---
name: Decision Maker Prospects
description: Senior-title users (C-level, VP, Director) showing intent — priority routing for AE outreach.
intempt:
  id: decision-maker-prospects
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Senior-title users (C-level, VP, Director) showing intent — priority routing for AE outreach.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - segments
    agent: segment-architect
    mode:
    - b2b
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

# Decision Maker Prospects

Senior-title users (C-level, VP, Director) showing intent — priority routing for AE outreach.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
