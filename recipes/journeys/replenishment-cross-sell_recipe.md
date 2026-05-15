---
name: replenishment-cross-sell
description: |
  Use when a user mentions "replenishment & cross-sell", or asks for related help. Reorder reminders for consumable products + cross-sell complementary items + referral nudges.
arguments: []
intempt:
  id: replenishment-cross-sell
  version: 1.0.0
  slashCommand: /replenishment-cross-sell
  group: Journeys
  shortDescription: "Reorder reminders for consumable products + cross-sell complementary items + referral nudges."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [ecommerce]
    complexity: advanced
    executionMode: live
    tags: [replenishment-cross-sell]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_recommendation
    - create_experiment
    - create_dashboard
  procedure:
    - step: 1
      title: "Identify Replenishment Window"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Identify users approaching their typical reorder window for consumable products based on purchase history."
      prompt: "Identify users approaching their typical reorder window for consumable products based on purchase history."
    - step: 2
      title: "Build Reorder Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "Generate reorder-reminder emails timed to the user's consumption pattern, with one-click reorder link."
      prompt: "Generate reorder-reminder emails timed to the user's consumption pattern, with one-click reorder link."
    - step: 3
      title: "Build Reorder Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Build a journey sending reorder reminders at appropriate intervals before depletion."
      prompt: "Build a journey sending reorder reminders at appropriate intervals before depletion."
    - step: 4
      title: "Build Cross Sell Recommendations"
      command: create_recommendation
      produces: recommendation
      bindsAs: recommendation
      dependsOn: [segment, asset, journey]
      description: "Generate cross-sell recommendations for complementary products based on the customer's purchase history."
      prompt: "Generate cross-sell recommendations for complementary products based on the customer's purchase history."
    - step: 5
      title: "Build Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey, recommendation]
      description: "Add A/B variants on cross-sell timing (with-reorder vs separate-touch)."
      prompt: "Add A/B variants on cross-sell timing (with-reorder vs separate-touch)."
    - step: 6
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, recommendation, experiment]
      description: "Compose a dashboard tracking reorder rate, cross-sell attach rate, and 12-month repeat-purchase value."
      prompt: "Compose a dashboard tracking reorder rate, cross-sell attach rate, and 12-month repeat-purchase value."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Replenishment & Cross-Sell

## Procedure

1. **Identify Replenishment Window** [`create_segment`] — Identify users approaching their typical reorder window for consumable products based on purchase history. → produces: segment
2. **Build Reorder Content** [`create_email_content`] — Generate reorder-reminder emails timed to the user's consumption pattern, with one-click reorder link. → produces: asset
3. **Build Reorder Journey** [`create_journey`] — Build a journey sending reorder reminders at appropriate intervals before depletion. → produces: journey
4. **Build Cross Sell Recommendations** [`create_recommendation`] — Generate cross-sell recommendations for complementary products based on the customer's purchase history. → produces: recommendation
5. **Build Experiment** [`create_experiment`] — Add A/B variants on cross-sell timing (with-reorder vs separate-touch). → produces: experiment
6. **Build Dashboard** [`create_dashboard`] — Compose a dashboard tracking reorder rate, cross-sell attach rate, and 12-month repeat-purchase value. → produces: dashboard
