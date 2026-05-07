---
name: Single Threaded Accounts
description: Multi-user companies where only 1 user is engaged — multi-threading risk for enterprise SaaS.
intempt:
  id: single-threaded-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Multi-user companies where only 1 user is engaged — multi-threading risk for enterprise SaaS.
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

# Single Threaded Accounts

Multi-user companies where only 1 user is engaged — multi-threading risk for enterprise SaaS.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
