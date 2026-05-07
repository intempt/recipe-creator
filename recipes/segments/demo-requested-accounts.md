---
name: Demo Requested Accounts
description: Accounts where any user submitted a demo form in last 30 days — top SDR-routing priority.
intempt:
  id: demo-requested-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Accounts where any user submitted a demo form in last 30 days — top SDR-routing priority.
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

# Demo Requested Accounts

Accounts where any user submitted a demo form in last 30 days — top SDR-routing priority.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
