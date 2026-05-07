---
name: Checkout Abandonment Recovery
description: Higher-intent-than-cart recovery — fires specifically when the shopper started checkout (entered email/address)
  but didn't complete. Stronger urgency justified because intent is proven.
intempt:
  id: checkout-abandonment-recovery
  version: 1.0.0
  slashCommand: /checkout-abandonment-recovery
  shortDescription: Higher-intent-than-cart recovery — fires specifically when the shopper started checkout (entered email/address)
    but didn't complete. Stronger urgency justified because intent is proven.
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
    - checkout
    - cart-and-checkout-recovery
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
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: build-content
    describe: 'Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency
      + social proof. Touch 3: final reminder optionally with discount. (Tailored for: Checkout abandonment recovery.)'
    produces: content
  - id: build-journey
    describe: 'Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr,
      and 72hr after abandonment. (Tailored for: Checkout abandonment recovery.)'
    produces: journey
  - id: build-experiment
    describe: 'Add A/B variants on subject lines and incentive levels for the recovery journey. (Tailored for: Checkout abandonment
      recovery.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey.
      (Tailored for: Checkout abandonment recovery.)'
    produces: dashboard
  - id: build-alert-workflow
    describe: 'Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window. (Tailored for:
      Checkout abandonment recovery.)'
    produces: workflow
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Checkout Abandonment Recovery

Higher-intent-than-cart recovery — fires specifically when the shopper started checkout (entered email/address) but didn't complete. Stronger urgency justified because intent is proven.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency + social proof. Touch 3: final reminder optionally with discount. (Tailored for: Checkout abandonment recovery.)
2. Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr, and 72hr after abandonment. (Tailored for: Checkout abandonment recovery.)
3. Add A/B variants on subject lines and incentive levels for the recovery journey. (Tailored for: Checkout abandonment recovery.)
4. Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey. (Tailored for: Checkout abandonment recovery.)
5. Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window. (Tailored for: Checkout abandonment recovery.)

## Prerequisites

- Integration: **shopify** (blocking)
