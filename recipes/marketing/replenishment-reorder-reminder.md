---
name: Replenishment Reorder Reminder
description: Timed reminder to reorder consumable products based on typical replenishment cycle — triggers when a user is
  approaching their configurable run-out date. Preserves repeat-purchase rate without...
intempt:
  id: replenishment-reorder-reminder
  version: 1.0.0
  slashCommand: /replenishment-reorder-reminder
  shortDescription: Timed reminder to reorder consumable products based on typical replenishment cycle — triggers when a user
    is approaching their configurable run-out date. Preserves repeat-purchase rate without...
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
    - replenishment
    - post-purchase-and-retention
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
  - name: recommendation
    type: recommendation
    description: Recommendation produced by this recipe.
  - name: experiment
    type: experiment
    description: Experiment produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: build-reorder-content
    describe: 'Generate reorder-reminder emails timed to the user''s consumption pattern, with one-click reorder link. (Tailored
      for: Replenishment reorder reminder.)'
    produces: content
  - id: build-reorder-journey
    describe: 'Build a journey sending reorder reminders at appropriate intervals before depletion. (Tailored for: Replenishment
      reorder reminder.)'
    produces: journey
  - id: build-cross-sell-recommendations
    describe: 'Generate cross-sell recommendations for complementary products based on the customer''s purchase history. (Tailored
      for: Replenishment reorder reminder.)'
    produces: recommendation
  - id: build-experiment
    describe: 'Add A/B variants on cross-sell timing (with-reorder vs separate-touch). (Tailored for: Replenishment reorder
      reminder.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking reorder rate, cross-sell attach rate, and 12-month repeat-purchase value. (Tailored
      for: Replenishment reorder reminder.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Replenishment Reorder Reminder

Timed reminder to reorder consumable products based on typical replenishment cycle — triggers when a user is approaching their configurable run-out date. Preserves repeat-purchase rate without...

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate reorder-reminder emails timed to the user's consumption pattern, with one-click reorder link. (Tailored for: Replenishment reorder reminder.)
2. Build a journey sending reorder reminders at appropriate intervals before depletion. (Tailored for: Replenishment reorder reminder.)
3. Generate cross-sell recommendations for complementary products based on the customer's purchase history. (Tailored for: Replenishment reorder reminder.)
4. Add A/B variants on cross-sell timing (with-reorder vs separate-touch). (Tailored for: Replenishment reorder reminder.)
5. Compose a dashboard tracking reorder rate, cross-sell attach rate, and 12-month repeat-purchase value. (Tailored for: Replenishment reorder reminder.)

## Prerequisites

- Integration: **shopify** (blocking)
