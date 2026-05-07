---
name: Welcome Series 2
description: Multi-email welcome sequence that introduces the brand, sets expectations, delivers any sign-up incentive, and
  guides new subscribers toward their first purchase.
intempt:
  id: welcome-series-2
  version: 1.0.0
  slashCommand: /welcome-series-2
  shortDescription: Multi-email welcome sequence that introduces the brand, sets expectations, delivers any sign-up incentive,
    and guides new subscribers toward their first purchase.
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
      for: Welcome series.)'
    produces: content
  - id: build-journey
    describe: 'Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored
      for: Welcome series.)'
    produces: journey
  - id: build-experiment
    describe: 'Add A/B variants on subject lines and welcome offer presence. (Tailored for: Welcome series.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the
      welcome journey. (Tailored for: Welcome series.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Welcome Series 2

Multi-email welcome sequence that introduces the brand, sets expectations, delivers any sign-up incentive, and guides new subscribers toward their first purchase.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. (Tailored for: Welcome series.)
2. Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored for: Welcome series.)
3. Add A/B variants on subject lines and welcome offer presence. (Tailored for: Welcome series.)
4. Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey. (Tailored for: Welcome series.)

## Prerequisites

- Integration: **shopify** (blocking)
