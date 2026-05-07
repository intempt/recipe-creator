---
name: Order Status Push Updates
description: Transactional push updates for order lifecycle — confirmation, shipped, out-for-delivery, delivered. Reduces
  'where is my order' support tickets.
intempt:
  id: order-status-push-updates
  version: 1.0.0
  slashCommand: /order-status-push-updates
  shortDescription: Transactional push updates for order lifecycle — confirmation, shipped, out-for-delivery, delivered. Reduces
    'where is my order' support tickets.
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
    - order
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
      for: Order status push updates.)'
    produces: content
  - id: build-journey
    describe: 'Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored
      for: Order status push updates.)'
    produces: journey
  - id: build-experiment
    describe: 'Add A/B variants on subject lines and welcome offer presence. (Tailored for: Order status push updates.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the
      welcome journey. (Tailored for: Order status push updates.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: firebase
      severity: blocking
    - value: shopify
      severity: blocking
---

# Order Status Push Updates

Transactional push updates for order lifecycle — confirmation, shipped, out-for-delivery, delivered. Reduces 'where is my order' support tickets.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate a 4-email welcome sequence introducing the brand, product, and value props using brand voice. (Tailored for: Order status push updates.)
2. Build a 4-touch welcome journey sending the emails at 0hr, 1day, 3day, and 7day after subscription. (Tailored for: Order status push updates.)
3. Add A/B variants on subject lines and welcome offer presence. (Tailored for: Order status push updates.)
4. Compose a dashboard tracking open rates, click rates, conversion rate, and time-to-first-purchase from the welcome journey. (Tailored for: Order status push updates.)

## Prerequisites

- Integration: **firebase** (blocking)
- Integration: **shopify** (blocking)
