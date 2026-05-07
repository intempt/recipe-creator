---
name: Vip Entry Cs Welcome Outreach Task
description: Give new VIP customers a human touch the moment they hit the tier.
intempt:
  id: vip-entry-cs-welcome-outreach-task
  version: 1.0.0
  slashCommand: /vip-entry-cs-welcome-outreach-task
  shortDescription: Give new VIP customers a human touch the moment they hit the tier.
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
    - revenue-operations
    - vip
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
      for: VIP entry → CS welcome outreach task.)'
    produces: content
  - id: build-journey
    describe: 'Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored
      for: VIP entry → CS welcome outreach task.)'
    produces: journey
  - id: build-experiment
    describe: 'Add A/B variants on subject lines and welcome offer presence. (Tailored for: VIP entry → CS welcome outreach
      task.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the
      welcome journey. (Tailored for: VIP entry → CS welcome outreach task.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
    - value: slack
      severity: blocking
---

# Vip Entry Cs Welcome Outreach Task

Give new VIP customers a human touch the moment they hit the tier.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. (Tailored for: VIP entry → CS welcome outreach task.)
2. Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored for: VIP entry → CS welcome outreach task.)
3. Add A/B variants on subject lines and welcome offer presence. (Tailored for: VIP entry → CS welcome outreach task.)
4. Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey. (Tailored for: VIP entry → CS welcome outreach task.)

## Prerequisites

- Integration: **shopify** (blocking)
- Integration: **slack** (blocking)
