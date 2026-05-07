---
name: R 1St 2Nd Purchase 30 Day Activation
description: 'Converts one-time buyers to repeat customers within 30 days. Industry data: only ~27% of first-time buyers buy
  again. This sequence targets that gap with cross-category recommendations and timing...'
intempt:
  id: r-1st-2nd-purchase-30-day-activation
  version: 1.0.0
  slashCommand: /r-1st-2nd-purchase-30-day-activation
  shortDescription: 'Converts one-time buyers to repeat customers within 30 days. Industry data: only ~27% of first-time buyers
    buy again. This sequence targets that gap with cross-category recommendations and timing...'
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
    - post-purchase-and-retention
    - r
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: attribute
    type: attribute
    description: Attribute produced by this recipe.
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: compute-trial-health
    describe: 'Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team
      invites, data uploaded). (Tailored for: 1st → 2nd purchase 30-day activation.)'
    produces: attribute
  - id: build-content
    describe: 'Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored
      for: 1st → 2nd purchase 30-day activation.)'
    produces: content
  - id: build-journey
    describe: 'Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored
      for: 1st → 2nd purchase 30-day activation.)'
    produces: journey
  - id: build-funnel-report
    describe: 'Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention
      overlay. (Tailored for: 1st → 2nd purchase 30-day activation.)'
    produces: report
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# R 1St 2Nd Purchase 30 Day Activation

Converts one-time buyers to repeat customers within 30 days. Industry data: only ~27% of first-time buyers buy again. This sequence targets that gap with cross-category recommendations and timing...

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded). (Tailored for: 1st → 2nd purchase 30-day activation.)
2. Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored for: 1st → 2nd purchase 30-day activation.)
3. Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored for: 1st → 2nd purchase 30-day activation.)
4. Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay. (Tailored for: 1st → 2nd purchase 30-day activation.)

## Prerequisites

- Integration: **shopify** (blocking)
