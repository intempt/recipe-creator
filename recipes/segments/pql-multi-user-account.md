---
name: Pql Multi User Account
description: Free/trial accounts with 2+ engaged users from same company — enterprise PQL signal.
intempt:
  id: pql-multi-user-account
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Free/trial accounts with 2+ engaged users from same company — enterprise PQL signal.
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

# Pql Multi User Account

Free/trial accounts with 2+ engaged users from same company — enterprise PQL signal.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
