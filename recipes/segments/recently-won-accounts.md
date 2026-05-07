---
name: Recently Won Accounts
description: Accounts that closed a deal in last 90 days — onboarding cohort distinct from new-paying-customers.
intempt:
  id: recently-won-accounts
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Accounts that closed a deal in last 90 days — onboarding cohort distinct from new-paying-customers.
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

# Recently Won Accounts

Accounts that closed a deal in last 90 days — onboarding cohort distinct from new-paying-customers.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
