---
name: Lapsed Customer Win Back
description: 4-email win-back sequence for customers who haven't purchased in 90+ days. Progresses from 'we miss you' check-in
  to incentive to final sunset message.
intempt:
  id: lapsed-customer-win-back
  version: 1.0.0
  slashCommand: /lapsed-customer-win-back
  shortDescription: 4-email win-back sequence for customers who haven't purchased in 90+ days. Progresses from 'we miss you'
    check-in to incentive to final sunset message.
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
    - lapsed
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
      for deep-lapsed. (Tailored for: Lapsed customer win-back.)'
    produces: content
  - id: build-journey
    describe: 'Build a multi-arm journey routing each tier through appropriate touches with escalating incentives. (Tailored
      for: Lapsed customer win-back.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey. (Tailored
      for: Lapsed customer win-back.)'
    produces: report
  - id: build-experiment
    describe: 'Add A/B variants on incentive type (discount vs free gift vs value-only). (Tailored for: Lapsed customer win-back.)'
    produces: experiment
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Lapsed Customer Win Back

4-email win-back sequence for customers who haven't purchased in 90+ days. Progresses from 'we miss you' check-in to incentive to final sunset message.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.

## Steps

1. Generate tier-appropriate win-back content: gentle for early-lapsed, value-reminder for mid, exclusive offer for deep-lapsed. (Tailored for: Lapsed customer win-back.)
2. Build a multi-arm journey routing each tier through appropriate touches with escalating incentives. (Tailored for: Lapsed customer win-back.)
3. Compose a retention report measuring re-engagement rates per tier over a 90-day window post-journey. (Tailored for: Lapsed customer win-back.)
4. Add A/B variants on incentive type (discount vs free gift vs value-only). (Tailored for: Lapsed customer win-back.)

## Prerequisites

- Integration: **shopify** (blocking)
