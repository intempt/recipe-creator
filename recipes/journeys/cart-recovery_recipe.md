---
name: cart-recovery
description: |
  Use when a user mentions "cart recovery", "abandoned cart", "cart recovery", or asks for related help. Recover abandoned carts with a 3-touch sequence — segment, content, journey, A/B variants, dashboard, alert workflow.
arguments: []
intempt:
  id: cart-recovery
  version: 1.0.0
  slashCommand: /cart-recovery
  group: Journeys
  shortDescription: "Create a cart-abandoners segment, 3 cart-recovery emails, and a 3-touch journey at 1h, 24h, and 72h after abandonment."
  availability: coming-soon
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
      title: "Identify Audience"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Identify users with cart_abandoned event in last 30 days who have NOT placed an order for that cart."
      prompt: "Identify users with cart_abandoned event in last 30 days who have NOT placed an order for that cart."
    - step: 2
      title: "Build Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency + social proof. Touch 3: final reminder optionally with discount."
      prompt: "Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency + social proof. Touch 3: final reminder optionally with discount."
    - step: 3
      title: "Build Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr, and 72hr after abandonment."
      prompt: "Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr, and 72hr after abandonment."
    - step: 4
      title: "Build Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey]
      description: "Add A/B variants on subject lines and incentive levels for the recovery journey."
      prompt: "Add A/B variants on subject lines and incentive levels for the recovery journey."
    - step: 5
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, experiment]
      description: "Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey."
      prompt: "Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey."
    - step: 6
      title: "Build Alert Workflow"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [segment, asset, journey, experiment, dashboard]
      description: "Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window."
      prompt: "Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---

# Cart Recovery

## Procedure

1. **Identify Audience** [`create_segment`] — Identify users with cart_abandoned event in last 30 days who have NOT placed an order for that cart. → produces: segment
2. **Build Content** [`create_email_content`] — Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency + social proof. Touch 3: final reminder optionally with discount. → produces: asset
3. **Build Journey** [`create_journey`] — Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr, and 72hr after abandonment. → produces: journey
4. **Build Experiment** [`create_experiment`] — Add A/B variants on subject lines and incentive levels for the recovery journey. → produces: experiment
5. **Build Dashboard** [`create_dashboard`] — Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey. → produces: dashboard
6. **Build Alert Workflow** [`create_workflow`] — Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window. → produces: workflow
