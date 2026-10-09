---
name: cart-recovery
description: |
  Use when a user mentions "cart recovery", "abandoned cart", "cart recovery", or asks for related help. Recover abandoned carts with a 3-touch sequence: segment, content, journey, A/B variants, dashboard, alert workflow.
arguments: []
intempt:
  id: cart-recovery
  title: "Abandoned cart recovery"
  version: 1.0.0
  slashCommand: /cart-recovery
  group: Journeys
  shortDescription: "Emails shoppers who left items behind, three times over three days, and measures how much revenue comes back."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [ecommerce]
    complexity: advanced
    executionMode: live
    tags: [cart-recovery]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_experiment
    - create_dashboard
    - create_workflow
  procedure:
    - step: 1
      title: "Find who abandoned a cart"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Anyone who abandoned a cart in the last 30 days and never placed that order."
      prompt: "Identify users who abandoned a cart in the last 30 days but have not placed an order for that cart."
    - step: 2
      title: "Write the three emails"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "A reminder, then urgency with social proof, then a final notice with an optional discount, all in your brand voice."
      prompt: "Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency + social proof. Touch 3: final reminder optionally with discount."
    - step: 3
      title: "Schedule the sequence"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "The three emails go out 1 hour, 24 hours and 72 hours after the cart was abandoned."
      prompt: "Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr, and 72hr after abandonment."
    - step: 4
      title: "Test subject lines and offers"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey]
      description: "A/B variants on the subject lines and on how big an incentive the last email carries."
      prompt: "Add A/B variants on subject lines and incentive levels for the recovery journey."
    - step: 5
      title: "Track recovered revenue"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, experiment]
      description: "Recovery rate, revenue recovered, and how long people take to come back."
      prompt: "Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey."
    - step: 6
      title: "Alert when it stops working"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [segment, asset, journey, experiment, dashboard]
      description: "The team is told if the recovery rate falls below 15% over any 7 day window."
      prompt: "Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Abandoned cart recovery

Emails shoppers who left items behind, three times over three days, and measures how much revenue comes back.

## What it does

1. **Find who abandoned a cart** (`create_segment`)

   Anyone who abandoned a cart in the last 30 days and never placed that order.

2. **Write the three emails** (`create_email_content`)

   A reminder, then urgency with social proof, then a final notice with an optional discount, all in your brand voice.

3. **Schedule the sequence** (`create_journey`)

   The three emails go out 1 hour, 24 hours and 72 hours after the cart was abandoned.

4. **Test subject lines and offers** (`create_experiment`)

   A/B variants on the subject lines and on how big an incentive the last email carries.

5. **Track recovered revenue** (`create_dashboard`)

   Recovery rate, revenue recovered, and how long people take to come back.

6. **Alert when it stops working** (`create_workflow`)

   The team is told if the recovery rate falls below 15% over any 7 day window.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
