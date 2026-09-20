---
name: lead-qualification
description: |
  Use when a user mentions "lead qualification & routing", "lead routing", "lead qualification", or asks for related help. Score leads, segment, route hot leads to sales, nurture the rest.
arguments: []
intempt:
  id: lead-qualification
  title: "Lead qualification and handoff"
  version: 1.0.0
  slashCommand: /lead-qualification
  group: Journeys
  shortDescription: "Scores inbound leads, sends the sales ready ones round robin to a rep with the context attached, and puts the rest into nurture."
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
      title: "Score every lead"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "A qualification score weighing company fit, intent and engagement."
      prompt: "Define a Qualification attribute weighting firmographic fit, intent, and engagement."
    - step: 2
      title: "Split into hot, warm and cold"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [attribute]
      description: "Three tiers off that score."
      prompt: "Segment leads into hot/warm/cold tiers based on qualification score."
    - step: 3
      title: "Route hot leads round robin"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, segment]
      description: "Hot leads are handed round robin to a rep on the team, with a task created that carries the context."
      prompt: "Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context."
    - step: 4
      title: "Nurture warm and cold leads"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, segment, workflow]
      description: "A journey for each of the other two tiers, at a cadence that suits how far off they are."
      prompt: "Build nurture journeys for warm and cold leads with appropriate cadence."
    - step: 5
      title: "Track handoff to opportunity"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, segment, workflow, journey]
      description: "Lead volume, score distribution, how many reach a rep, and how many turn into opportunities."
      prompt: "Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity."
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Lead qualification and handoff

Scores inbound leads, sends the sales ready ones round robin to a rep with the context attached, and puts the rest into nurture.

## What it does

1. **Score every lead** (`create_ai_attribute`)

   A qualification score weighing company fit, intent and engagement.

2. **Split into hot, warm and cold** (`create_segment`)

   Three tiers off that score.

3. **Route hot leads round robin** (`create_workflow`)

   Hot leads are handed round robin to a rep on the team, with a task created that carries the context.

4. **Nurture warm and cold leads** (`create_journey`)

   A journey for each of the other two tiers, at a cadence that suits how far off they are.

5. **Track handoff to opportunity** (`create_dashboard`)

   Lead volume, score distribution, how many reach a rep, and how many turn into opportunities.

## What you end up with

- **attribute** (attribute): Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
