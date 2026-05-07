---
name: Whatsapp Abandoned Cart Recovery
description: WhatsApp-based cart recovery — higher open and reply rates than email in WhatsApp-primary markets (LATAM, India,
  SEA, parts of EMEA).
intempt:
  id: whatsapp-abandoned-cart-recovery
  version: 1.0.0
  slashCommand: /whatsapp-abandoned-cart-recovery
  shortDescription: WhatsApp-based cart recovery — higher open and reply rates than email in WhatsApp-primary markets (LATAM,
    India, SEA, parts of EMEA).
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
    - whatsapp
    - push-and-mobile
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
      + social proof. Touch 3: final reminder optionally with discount. (Tailored for: WhatsApp abandoned cart recovery.)'
    produces: content
  - id: build-journey
    describe: 'Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr,
      and 72hr after abandonment. (Tailored for: WhatsApp abandoned cart recovery.)'
    produces: journey
  - id: build-experiment
    describe: 'Add A/B variants on subject lines and incentive levels for the recovery journey. (Tailored for: WhatsApp abandoned
      cart recovery.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey.
      (Tailored for: WhatsApp abandoned cart recovery.)'
    produces: dashboard
  - id: build-alert-workflow
    describe: 'Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window. (Tailored for:
      WhatsApp abandoned cart recovery.)'
    produces: workflow
  prerequisites:
    integrations:
    - value: whatsapp
      severity: blocking
    - value: shopify
      severity: blocking
---

# Whatsapp Abandoned Cart Recovery

WhatsApp-based cart recovery — higher open and reply rates than email in WhatsApp-primary markets (LATAM, India, SEA, parts of EMEA).

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency + social proof. Touch 3: final reminder optionally with discount. (Tailored for: WhatsApp abandoned cart recovery.)
2. Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr, and 72hr after abandonment. (Tailored for: WhatsApp abandoned cart recovery.)
3. Add A/B variants on subject lines and incentive levels for the recovery journey. (Tailored for: WhatsApp abandoned cart recovery.)
4. Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey. (Tailored for: WhatsApp abandoned cart recovery.)
5. Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window. (Tailored for: WhatsApp abandoned cart recovery.)

## Prerequisites

- Integration: **whatsapp** (blocking)
- Integration: **shopify** (blocking)
