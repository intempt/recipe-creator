---
name: Engaged Non Buyer First Purchase Push
description: Aggressive conversion sequence for subscribers who engage heavily (opens, clicks, browse) but have never purchased.
  Time-bound incentive and FAQ-based objection handling.
intempt:
  id: engaged-non-buyer-first-purchase-push
  version: 1.0.0
  slashCommand: /engaged-non-buyer-first-purchase-push
  shortDescription: Aggressive conversion sequence for subscribers who engage heavily (opens, clicks, browse) but have never
    purchased. Time-bound incentive and FAQ-based objection handling.
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
    - win-back-and-re-engagement
    - engaged
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
      for deep-lapsed. (Tailored for: Engaged non-buyer → first purchase push.)'
    produces: content
  - id: build-journey
    describe: 'Build a multi-arm journey routing each tier through appropriate touches with escalating incentives. (Tailored
      for: Engaged non-buyer → first purchase push.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey. (Tailored
      for: Engaged non-buyer → first purchase push.)'
    produces: report
  - id: build-experiment
    describe: 'Add A/B variants on incentive type (discount vs free gift vs value-only). (Tailored for: Engaged non-buyer
      → first purchase push.)'
    produces: experiment
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Engaged Non Buyer First Purchase Push

Aggressive conversion sequence for subscribers who engage heavily (opens, clicks, browse) but have never purchased. Time-bound incentive and FAQ-based objection handling.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.

## Steps

1. Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive offer for deep-lapsed. (Tailored for: Engaged non-buyer → first purchase push.)
2. Build a multi-arm journey routing each tier through appropriate touches with escalating incentives. (Tailored for: Engaged non-buyer → first purchase push.)
3. Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey. (Tailored for: Engaged non-buyer → first purchase push.)
4. Add A/B variants on incentive type (discount vs free gift vs value-only). (Tailored for: Engaged non-buyer → first purchase push.)

## Prerequisites

- Integration: **shopify** (blocking)
