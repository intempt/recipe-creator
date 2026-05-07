---
name: Renewal Window 90 Day
description: Subscriptions ending in next 90 days — foundation for renewal-flow journeys and NRR plays.
intempt:
  id: renewal-window-90-day
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Subscriptions ending in next 90 days — foundation for renewal-flow journeys and NRR plays.
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

# Renewal Window 90 Day

Subscriptions ending in next 90 days — foundation for renewal-flow journeys and NRR plays.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
