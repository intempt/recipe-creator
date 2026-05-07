---
name: Smb Accounts
description: Small businesses (under 100 employees) — self-serve / low-touch routing.
intempt:
  id: smb-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Small businesses (under 100 employees) — self-serve / low-touch routing.
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

# Smb Accounts

Small businesses (under 100 employees) — self-serve / low-touch routing.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
