---
name: Replenishment Cross Sell
description: Reorder reminders for consumable products + cross-sell complementary items + referral nudges.
intempt:
  id: replenishment-cross-sell
  version: 1.0.0
  slashCommand: /replenishment-cross-sell
  shortDescription: Reorder reminders for consumable products + cross-sell complementary items + referral nudges.
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
    - replenishment-cross-sell
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
    describe: Generate reorder-reminder emails timed to the user's consumption pattern, with one-click reorder link.
    produces: content
  - id: build-reorder-journey
    describe: Build a journey sending reorder reminders at appropriate intervals before depletion.
    produces: journey
  - id: build-cross-sell-recommendations
    describe: Generate cross-sell recommendations for complementary products based on the customer's purchase history.
    produces: recommendation
  - id: build-experiment
    describe: Add A/B variants on cross-sell timing (with-reorder vs separate-touch).
    produces: experiment
  - id: build-dashboard
    describe: Compose a dashboard tracking reorder rate, cross-sell attach rate, and 12-month repeat-purchase value.
    produces: dashboard
---

# Replenishment Cross Sell

Reorder reminders for consumable products + cross-sell complementary items + referral nudges.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate reorder-reminder emails timed to the user's consumption pattern, with one-click reorder link.
2. Build a journey sending reorder reminders at appropriate intervals before depletion.
3. Generate cross-sell recommendations for complementary products based on the customer's purchase history.
4. Add A/B variants on cross-sell timing (with-reorder vs separate-touch).
5. Compose a dashboard tracking reorder rate, cross-sell attach rate, and 12-month repeat-purchase value.
