---
name: Sign Up Anniversary Celebration
description: Annual sign-up anniversary email with anniversary-specific incentive — a habit-building touchpoint that re-engages
  subscribers who may have gone dormant.
intempt:
  id: sign-up-anniversary-celebration
  version: 1.0.0
  slashCommand: /sign-up-anniversary-celebration
  shortDescription: Annual sign-up anniversary email with anniversary-specific incentive — a habit-building touchpoint that
    re-engages subscribers who may have gone dormant.
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
    - sign
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
      for: Sign-up anniversary celebration.)'
    produces: content
  - id: build-journey
    describe: 'Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored
      for: Sign-up anniversary celebration.)'
    produces: journey
  - id: build-experiment
    describe: 'Add A/B variants on subject lines and welcome offer presence. (Tailored for: Sign-up anniversary celebration.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the
      welcome journey. (Tailored for: Sign-up anniversary celebration.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Sign Up Anniversary Celebration

Annual sign-up anniversary email with anniversary-specific incentive — a habit-building touchpoint that re-engages subscribers who may have gone dormant.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. (Tailored for: Sign-up anniversary celebration.)
2. Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored for: Sign-up anniversary celebration.)
3. Add A/B variants on subject lines and welcome offer presence. (Tailored for: Sign-up anniversary celebration.)
4. Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey. (Tailored for: Sign-up anniversary celebration.)

## Prerequisites

- Integration: **shopify** (blocking)
