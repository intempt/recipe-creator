---
name: Icp Match Accounts
description: Accounts matching ideal customer profile by company size, industry, and geography.
intempt:
  id: icp-match-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Accounts matching ideal customer profile by company size, industry, and geography.
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

# Icp Match Accounts

Accounts matching ideal customer profile by company size, industry, and geography.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
