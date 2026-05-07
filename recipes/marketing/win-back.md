---
name: Win Back
description: Tiered re-engagement for lapsed users — segment by recency, content per tier, journey, retention measurement.
intempt:
  id: win-back
  version: 1.0.0
  slashCommand: /win-back
  shortDescription: Tiered re-engagement for lapsed users — segment by recency, content per tier, journey, retention measurement.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - all
    complexity: advanced
    executionMode: live
    tags:
    - win-back
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
      for deep-lapsed.'
    produces: content
  - id: build-journey
    describe: Build a multi-arm journey routing each tier through appropriate touches with escalating incentives.
    produces: journey
  - id: build-retention-report
    describe: Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey.
    produces: report
  - id: build-experiment
    describe: Add A/B variants on incentive type (discount vs free gift vs value-only).
    produces: experiment
---

# Win Back

Tiered re-engagement for lapsed users — segment by recency, content per tier, journey, retention measurement.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.

## Steps

1. Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive offer for deep-lapsed.
2. Build a multi-arm journey routing each tier through appropriate touches with escalating incentives.
3. Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey.
4. Add A/B variants on incentive type (discount vs free gift vs value-only).
