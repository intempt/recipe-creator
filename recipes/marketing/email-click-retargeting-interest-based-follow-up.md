---
name: Email Click Retargeting Interest Based Follow Up
description: When a subscriber clicks a specific link in a campaign email, branches on clicked URL to send targeted follow-up
  tied to the interest they just expressed. Surgical — not bulk retargeting.
intempt:
  id: email-click-retargeting-interest-based-follow-up
  version: 1.0.0
  slashCommand: /email-click-retargeting-interest-based-follow-up
  shortDescription: When a subscriber clicks a specific link in a campaign email, branches on clicked URL to send targeted
    follow-up tied to the interest they just expressed. Surgical — not bulk retargeting.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - ecommerce
    complexity: advanced
    executionMode: live
    tags:
    - email
    - win-back-and-re-engagement
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: report
    type: report
    description: Report produced by this recipe.
  - name: experiment
    type: experiment
    description: Experiment produced by this recipe.
  steps:
  - id: build-content
    describe: 'Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive offer
      for deep-lapsed. (Tailored for: Email click retargeting — interest-based follow-up.)'
    produces: content
  - id: build-journey
    describe: 'Build a multi-arm journey routing each tier through appropriate touches with escalating incentives. (Tailored
      for: Email click retargeting — interest-based follow-up.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey. (Tailored
      for: Email click retargeting — interest-based follow-up.)'
    produces: report
  - id: build-experiment
    describe: 'Add A/B variants on incentive type (discount vs free gift vs value-only). (Tailored for: Email click retargeting
      — interest-based follow-up.)'
    produces: experiment
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Email Click Retargeting Interest Based Follow Up

When a subscriber clicks a specific link in a campaign email, branches on clicked URL to send targeted follow-up tied to the interest they just expressed. Surgical — not bulk retargeting.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.

## Steps

1. Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive offer for deep-lapsed. (Tailored for: Email click retargeting — interest-based follow-up.)
2. Build a multi-arm journey routing each tier through appropriate touches with escalating incentives. (Tailored for: Email click retargeting — interest-based follow-up.)
3. Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey. (Tailored for: Email click retargeting — interest-based follow-up.)
4. Add A/B variants on incentive type (discount vs free gift vs value-only). (Tailored for: Email click retargeting — interest-based follow-up.)

## Prerequisites

- Integration: **shopify** (blocking)
