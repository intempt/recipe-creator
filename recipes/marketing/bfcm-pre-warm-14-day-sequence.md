---
name: Bfcm Pre Warm 14 Day Sequence
description: 14-day pre-Black-Friday sequence that warms inboxes (protects deliverability), builds wishlists, and captures
  early-intent shoppers with teasers leading into launch.
intempt:
  id: bfcm-pre-warm-14-day-sequence
  version: 1.0.0
  slashCommand: /bfcm-pre-warm-14-day-sequence
  shortDescription: 14-day pre-Black-Friday sequence that warms inboxes (protects deliverability), builds wishlists, and captures
    early-intent shoppers with teasers leading into launch.
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
    - seasonal-and-campaign-driven
    - bfcm
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
      + social proof. Touch 3: final reminder optionally with discount. (Tailored for: BFCM pre-warm 14-day sequence.)'
    produces: content
  - id: build-journey
    describe: 'Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr,
      and 72hr after abandonment. (Tailored for: BFCM pre-warm 14-day sequence.)'
    produces: journey
  - id: build-experiment
    describe: 'Add A/B variants on subject lines and incentive levels for the recovery journey. (Tailored for: BFCM pre-warm
      14-day sequence.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey.
      (Tailored for: BFCM pre-warm 14-day sequence.)'
    produces: dashboard
  - id: build-alert-workflow
    describe: 'Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window. (Tailored for:
      BFCM pre-warm 14-day sequence.)'
    produces: workflow
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Bfcm Pre Warm 14 Day Sequence

14-day pre-Black-Friday sequence that warms inboxes (protects deliverability), builds wishlists, and captures early-intent shoppers with teasers leading into launch.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency + social proof. Touch 3: final reminder optionally with discount. (Tailored for: BFCM pre-warm 14-day sequence.)
2. Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr, and 72hr after abandonment. (Tailored for: BFCM pre-warm 14-day sequence.)
3. Add A/B variants on subject lines and incentive levels for the recovery journey. (Tailored for: BFCM pre-warm 14-day sequence.)
4. Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey. (Tailored for: BFCM pre-warm 14-day sequence.)
5. Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window. (Tailored for: BFCM pre-warm 14-day sequence.)

## Prerequisites

- Integration: **shopify** (blocking)
