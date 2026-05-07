---
name: Active Research Surge Accounts
description: Accounts with 3+ pricing-page visits in last 7 days — active buying-cycle signal.
intempt:
  id: active-research-surge-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Accounts with 3+ pricing-page visits in last 7 days — active buying-cycle signal.
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

# Active Research Surge Accounts

Accounts with 3+ pricing-page visits in last 7 days — active buying-cycle signal.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
