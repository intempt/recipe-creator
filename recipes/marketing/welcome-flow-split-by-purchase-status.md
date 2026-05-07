---
name: Welcome Flow Split By Purchase Status
description: Branching welcome that detects whether the new signup is already a customer — non-buyers get trust-building +
  incentive, existing buyers get gratitude + loyalty messaging. Per Klaviyo 2026 audits...
intempt:
  id: welcome-flow-split-by-purchase-status
  version: 1.0.0
  slashCommand: /welcome-flow-split-by-purchase-status
  shortDescription: Branching welcome that detects whether the new signup is already a customer — non-buyers get trust-building
    + incentive, existing buyers get gratitude + loyalty messaging. Per Klaviyo 2026 audits...
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
    - welcome-and-onboarding
    - welcome
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
  - name: experiment
    type: experiment
    description: Experiment produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: build-content
    describe: 'Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. (Tailored
      for: Welcome flow — split by purchase status.)'
    produces: content
  - id: build-journey
    describe: 'Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored
      for: Welcome flow — split by purchase status.)'
    produces: journey
  - id: build-experiment
    describe: 'Add A/B variants on subject lines and welcome offer presence. (Tailored for: Welcome flow — split by purchase
      status.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the
      welcome journey. (Tailored for: Welcome flow — split by purchase status.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
    - value: twilio
      severity: blocking
---

# Welcome Flow Split By Purchase Status

Branching welcome that detects whether the new signup is already a customer — non-buyers get trust-building + incentive, existing buyers get gratitude + loyalty messaging. Per Klaviyo 2026 audits...

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. (Tailored for: Welcome flow — split by purchase status.)
2. Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored for: Welcome flow — split by purchase status.)
3. Add A/B variants on subject lines and welcome offer presence. (Tailored for: Welcome flow — split by purchase status.)
4. Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey. (Tailored for: Welcome flow — split by purchase status.)

## Prerequisites

- Integration: **shopify** (blocking)
- Integration: **twilio** (blocking)
