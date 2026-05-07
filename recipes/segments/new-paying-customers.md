---
name: New Paying Customers
description: First 30 days post-subscription — paid-onboarding cohort distinct from generic recently-signed-up.
intempt:
  id: new-paying-customers
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: First 30 days post-subscription — paid-onboarding cohort distinct from generic recently-signed-up.
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

# New Paying Customers

First 30 days post-subscription — paid-onboarding cohort distinct from generic recently-signed-up.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
