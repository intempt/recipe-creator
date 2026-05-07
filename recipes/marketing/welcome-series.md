---
name: Welcome Series
description: First-touch sequence for new subscribers — segment, content, journey, A/B variants, performance dashboard.
intempt:
  id: welcome-series
  version: 1.0.0
  slashCommand: /welcome-series
  shortDescription: First-touch sequence for new subscribers — segment, content, journey, A/B variants, performance dashboard.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - all
    complexity: advanced
    executionMode: live
    tags:
    - welcome-series
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
    describe: Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice.
    produces: content
  - id: build-journey
    describe: Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription.
    produces: journey
  - id: build-experiment
    describe: Add A/B variants on subject lines and welcome offer presence.
    produces: experiment
  - id: build-dashboard
    describe: Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome
      journey.
    produces: dashboard
---

# Welcome Series

First-touch sequence for new subscribers — segment, content, journey, A/B variants, performance dashboard.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice.
2. Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription.
3. Add A/B variants on subject lines and welcome offer presence.
4. Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey.
