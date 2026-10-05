---
name: lead-qualification
description: |
  Use when a user mentions "lead qualification & routing", "lead routing", "lead qualification", or asks for related help. Score leads, segment, route hot leads to sales, nurture the rest.
arguments: []
intempt:
  id: lead-qualification
  version: 1.0.0
  slashCommand: /lead-qualification
  group: Journeys
  shortDescription: "Produce a lead qualification score attribute, hot/warm/cold segment, sales routing workflow with tasks, and nurture journey for warm/cold leads."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b]
    complexity: advanced
    executionMode: live
    tags: [lead-qualification]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Compute Qualification Score"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "Define a Qualification attribute weighting firmographic fit, intent, and engagement."
      prompt: "Define a Qualification attribute weighting firmographic fit, intent, and engagement."
    - step: 2
      title: "Segment By Tier"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [attribute]
      description: "Segment leads into hot/warm/cold tiers based on qualification score."
      prompt: "Segment leads into hot/warm/cold tiers based on qualification score."
    - step: 3
      title: "Build Routing Workflow"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, segment]
      description: "Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context."
      prompt: "Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context."
    - step: 4
      title: "Build Nurture Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, segment, workflow]
      description: "Build nurture journeys for warm and cold leads with appropriate cadence."
      prompt: "Build nurture journeys for warm and cold leads with appropriate cadence."
    - step: 5
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, segment, workflow, journey]
      description: "Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity."
      prompt: "Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity."
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Lead Qualification & Routing

## Procedure

1. **Compute Qualification Score** [`create_ai_attribute`] — Define a Qualification attribute weighting firmographic fit, intent, and engagement. → produces: attribute
2. **Segment By Tier** [`create_segment`] — Segment leads into hot/warm/cold tiers based on qualification score. → produces: segment
3. **Build Routing Workflow** [`create_workflow`] — Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. → produces: workflow
4. **Build Nurture Journey** [`create_journey`] — Build nurture journeys for warm and cold leads with appropriate cadence. → produces: journey
5. **Build Dashboard** [`create_dashboard`] — Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. → produces: dashboard
