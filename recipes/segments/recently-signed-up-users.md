---
name: Recently Signed Up Users
description: Users who created an account in the last 30 days — onboarding cohort.
intempt:
  id: recently-signed-up-users
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Users who created an account in the last 30 days — onboarding cohort.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - segments
    agent: segment-architect
    mode:
    - saas
    - ecommerce
    complexity: standard
    executionMode: live
    tags:
    - users-segment
    object: users
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

# Recently Signed Up Users

Users who created an account in the last 30 days — onboarding cohort.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
