---
name: High Intent Icp Prospects
description: ICP-matching accounts with active intent signals (pricing + docs visited recently).
intempt:
  id: high-intent-icp-prospects
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: ICP-matching accounts with active intent signals (pricing + docs visited recently).
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
    - accounts-segment
    object: accounts
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

# High Intent Icp Prospects

ICP-matching accounts with active intent signals (pricing + docs visited recently).

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
