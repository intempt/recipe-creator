---
name: replenishment-cross-sell
description: |
  Use when a user mentions "replenishment & cross-sell", or asks for related help. Reorder reminders for consumable products + cross-sell complementary items + referral nudges.
arguments: []
intempt:
  id: replenishment-cross-sell
  title: "Replenishment and cross sell"
  version: 1.0.0
  slashCommand: /replenishment-cross-sell
  group: Journeys
  shortDescription: "Reminds people to reorder before they run out, at the pace they actually get through it, and suggests what pairs with it."
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
      title: "Work out when they run out"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Shoppers coming up on their usual reorder window, worked out from what they have bought before."
      prompt: "Identify users approaching their typical reorder window for consumable products based on purchase history."
    - step: 2
      title: "Write the reorder reminder"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "An email timed to their own consumption pattern, with a one click reorder link."
      prompt: "Generate reorder-reminder emails timed to the user's consumption pattern, with one-click reorder link."
    - step: 3
      title: "Remind before they run dry"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Reminders sent at intervals ahead of the point they run out."
      prompt: "Build a journey sending reorder reminders at appropriate intervals before depletion."
    - step: 4
      title: "Pick what pairs with it"
      command: create_recommendation
      produces: recommendation
      bindsAs: recommendation
      dependsOn: [segment, asset, journey]
      description: "Cross sell recommendations built from what that customer has bought before."
      prompt: "Generate cross-sell recommendations for complementary products based on the customer's purchase history."
    - step: 5
      title: "Test when to cross sell"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey, recommendation]
      description: "A/B variants putting the cross sell inside the reorder email or in a separate one."
      prompt: "Add A/B variants on cross-sell timing (with-reorder vs separate-touch)."
    - step: 6
      title: "Track reorders and attach rate"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, recommendation, experiment]
      description: "How many people reorder, how often the cross sell attaches, and the 12 month value of repeat buyers."
      prompt: "Compose a dashboard tracking reorder rate, cross-sell attach rate, and 12-month repeat-purchase value."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Replenishment and cross sell

Reminds people to reorder before they run out, at the pace they actually get through it, and suggests what pairs with it.

## What it does

1. **Work out when they run out** (`create_segment`)

   Shoppers coming up on their usual reorder window, worked out from what they have bought before.

2. **Write the reorder reminder** (`create_email_content`)

   An email timed to their own consumption pattern, with a one click reorder link.

3. **Remind before they run dry** (`create_journey`)

   Reminders sent at intervals ahead of the point they run out.

4. **Pick what pairs with it** (`create_recommendation`)

   Cross sell recommendations built from what that customer has bought before.

5. **Test when to cross sell** (`create_experiment`)

   A/B variants putting the cross sell inside the reorder email or in a separate one.

6. **Track reorders and attach rate** (`create_dashboard`)

   How many people reorder, how often the cross sell attaches, and the 12 month value of repeat buyers.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
