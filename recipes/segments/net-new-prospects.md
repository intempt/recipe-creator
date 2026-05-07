---
name: Net New Prospects
description: Recently identified accounts with minimal engagement — SDR first-touch foundation.
intempt:
  id: net-new-prospects
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: Recently identified accounts with minimal engagement — SDR first-touch foundation.
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

# Net New Prospects

Recently identified accounts with minimal engagement — SDR first-touch foundation.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
