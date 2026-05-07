---
name: At Risk Vips
description: High-lifetime-value customers showing recency decay — Klaviyo's Needs Attention cohort. Distinct from generic
  churn risk.
intempt:
  id: at-risk-vips
  version: 1.0.0
  slashCommand: /segment-recipe
  shortDescription: High-lifetime-value customers showing recency decay — Klaviyo's Needs Attention cohort. Distinct from
    generic churn risk.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - segments
    agent: segment-architect
    mode:
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

# At Risk Vips

High-lifetime-value customers showing recency decay — Klaviyo's Needs Attention cohort. Distinct from generic churn risk.

## Outputs

- **segment** (segment): Segment created on /segments.

## Steps

1. Open the segment authoring surface, name the segment, and apply the rule below.
