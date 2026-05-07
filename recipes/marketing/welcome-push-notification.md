---
name: Welcome Push Notification
description: First-push onboarding for new mobile app users — confirms notification permission value, introduces the app,
  and drives to first-purchase or first-key-action.
intempt:
  id: welcome-push-notification
  version: 1.0.0
  slashCommand: /welcome-push-notification
  shortDescription: First-push onboarding for new mobile app users — confirms notification permission value, introduces the
    app, and drives to first-purchase or first-key-action.
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
    - welcome
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
  steps:
  - id: build-content
    describe: 'Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. (Tailored
      for: Welcome push notification.)'
    produces: content
  - id: build-journey
    describe: 'Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored
      for: Welcome push notification.)'
    produces: journey
  - id: build-experiment
    describe: 'Add A/B variants on subject lines and welcome offer presence. (Tailored for: Welcome push notification.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the
      welcome journey. (Tailored for: Welcome push notification.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: firebase
      severity: blocking
---

# Welcome Push Notification

First-push onboarding for new mobile app users — confirms notification permission value, introduces the app, and drives to first-purchase or first-key-action.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. (Tailored for: Welcome push notification.)
2. Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored for: Welcome push notification.)
3. Add A/B variants on subject lines and welcome offer presence. (Tailored for: Welcome push notification.)
4. Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey. (Tailored for: Welcome push notification.)

## Prerequisites

- Integration: **firebase** (blocking)
