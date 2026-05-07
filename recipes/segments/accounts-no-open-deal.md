---
name: Accounts No Open Deal
description: Healthy customer accounts with no current open deal — whitespace expansion opportunity.
intempt:
  id: accounts-no-open-deal
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Healthy customer accounts with no current open deal — whitespace expansion opportunity.
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

# Accounts No Open Deal

Healthy customer accounts with no current open deal — whitespace expansion opportunity.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
