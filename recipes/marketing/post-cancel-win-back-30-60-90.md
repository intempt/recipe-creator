---
name: Post Cancel Win Back 30 60 90
description: 3-email win-back cadence delivered 30, 60, and 90 days after cancellation. Distinct from pre-cancel save — this
  is post-departure with product updates and come-back offers.
intempt:
  id: post-cancel-win-back-30-60-90
  version: 1.0.0
  slashCommand: /post-cancel-win-back-30-60-90
  shortDescription: 3-email win-back cadence delivered 30, 60, and 90 days after cancellation. Distinct from pre-cancel save
    — this is post-departure with product updates and come-back offers.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - saas
    complexity: advanced
    executionMode: live
    tags:
    - post
    - retention-and-churn-prevention
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
      for deep-lapsed. (Tailored for: Post-cancel win-back (30/60/90).)'
    produces: content
  - id: build-journey
    describe: 'Build a multi-arm journey routing each tier through appropriate touches with escalating incentives. (Tailored
      for: Post-cancel win-back (30/60/90).)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey. (Tailored
      for: Post-cancel win-back (30/60/90).)'
    produces: report
  - id: build-experiment
    describe: 'Add A/B variants on incentive type (discount vs free gift vs value-only). (Tailored for: Post-cancel win-back
      (30/60/90).)'
    produces: experiment
  prerequisites:
    integrations:
    - value: stripe
      severity: blocking
---

# Post Cancel Win Back 30 60 90

3-email win-back cadence delivered 30, 60, and 90 days after cancellation. Distinct from pre-cancel save — this is post-departure with product updates and come-back offers.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.

## Steps

1. Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive offer for deep-lapsed. (Tailored for: Post-cancel win-back (30/60/90).)
2. Build a multi-arm journey routing each tier through appropriate touches with escalating incentives. (Tailored for: Post-cancel win-back (30/60/90).)
3. Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey. (Tailored for: Post-cancel win-back (30/60/90).)
4. Add A/B variants on incentive type (discount vs free gift vs value-only). (Tailored for: Post-cancel win-back (30/60/90).)

## Prerequisites

- Integration: **stripe** (blocking)
