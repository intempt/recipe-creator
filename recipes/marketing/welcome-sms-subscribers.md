---
name: Welcome Sms Subscribers
description: Single-channel SMS-only welcome for subscribers who opted in to SMS but didn't provide email — quick brand intro
  and incentive delivery under SMS character constraints.
intempt:
  id: welcome-sms-subscribers
  version: 1.0.0
  slashCommand: /welcome-sms-subscribers
  shortDescription: Single-channel SMS-only welcome for subscribers who opted in to SMS but didn't provide email — quick brand
    intro and incentive delivery under SMS character constraints.
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
      for: Welcome SMS subscribers.)'
    produces: content
  - id: build-journey
    describe: 'Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored
      for: Welcome SMS subscribers.)'
    produces: journey
  - id: build-experiment
    describe: 'Add A/B variants on subject lines and welcome offer presence. (Tailored for: Welcome SMS subscribers.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the
      welcome journey. (Tailored for: Welcome SMS subscribers.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: twilio
      severity: blocking
---

# Welcome Sms Subscribers

Single-channel SMS-only welcome for subscribers who opted in to SMS but didn't provide email — quick brand intro and incentive delivery under SMS character constraints.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. (Tailored for: Welcome SMS subscribers.)
2. Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored for: Welcome SMS subscribers.)
3. Add A/B variants on subject lines and welcome offer presence. (Tailored for: Welcome SMS subscribers.)
4. Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey. (Tailored for: Welcome SMS subscribers.)

## Prerequisites

- Integration: **twilio** (blocking)
