---
name: Welcome New Users With Sms And Email
description: Multi-channel welcome combining SMS and email — SMS carries the immediate incentive delivery and urgency, email
  carries the brand story and product education.
intempt:
  id: welcome-new-users-with-sms-and-email
  version: 1.0.0
  slashCommand: /welcome-new-users-with-sms-and-email
  shortDescription: Multi-channel welcome combining SMS and email — SMS carries the immediate incentive delivery and urgency,
    email carries the brand story and product education.
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
      for: Welcome new users with SMS and email.)'
    produces: content
  - id: build-journey
    describe: 'Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored
      for: Welcome new users with SMS and email.)'
    produces: journey
  - id: build-experiment
    describe: 'Add A/B variants on subject lines and welcome offer presence. (Tailored for: Welcome new users with SMS and
      email.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the
      welcome journey. (Tailored for: Welcome new users with SMS and email.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
    - value: twilio
      severity: blocking
---

# Welcome New Users With Sms And Email

Multi-channel welcome combining SMS and email — SMS carries the immediate incentive delivery and urgency, email carries the brand story and product education.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. (Tailored for: Welcome new users with SMS and email.)
2. Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored for: Welcome new users with SMS and email.)
3. Add A/B variants on subject lines and welcome offer presence. (Tailored for: Welcome new users with SMS and email.)
4. Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey. (Tailored for: Welcome new users with SMS and email.)

## Prerequisites

- Integration: **shopify** (blocking)
- Integration: **twilio** (blocking)
