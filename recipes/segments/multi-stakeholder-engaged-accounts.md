---
name: Multi Stakeholder Engaged Accounts
description: Accounts where 3+ users have been active in last 14 days — buying-committee signal for B2B.
intempt:
  id: multi-stakeholder-engaged-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Accounts where 3+ users have been active in last 14 days — buying-committee signal for B2B.
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

# Multi Stakeholder Engaged Accounts

Accounts where 3+ users have been active in last 14 days — buying-committee signal for B2B.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
