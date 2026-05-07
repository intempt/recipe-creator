---
name: Accounts At Churn Risk
description: Active accounts showing health deterioration — CSM intervention needed.
intempt:
  id: accounts-at-churn-risk
  version: 1.0.1
  slashCommand: /segment-recipe
  shortDescription: Active accounts showing health deterioration — CSM intervention needed.
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

# Accounts At Churn Risk

Active accounts showing health deterioration — CSM intervention needed.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
