---
name: b2b-nurture
description: |
  Use when a user mentions "b2b nurture & deal acceleration", "pipeline", "deal management", or asks for related help. Score leads, segment by readiness, route hot leads to sales, nurture the rest.
arguments: []
intempt:
  id: b2b-nurture
  title: "B2B lead nurture and routing"
  version: 1.0.0
  slashCommand: /b2b-nurture
  group: Journeys
  shortDescription: "Scores inbound leads, hands the sales ready ones to a rep with an owner and a task, and keeps the rest warm with content matched to how close they are."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [b2b]
    complexity: advanced
    executionMode: live
    tags: [b2b-nurture]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Score every lead"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "A qualification score built from company fit, intent signals and how deeply the person has engaged."
      prompt: "Define a Qualification scoring attribute weighting firmographic fit, intent signals, and engagement depth."
    - step: 2
      title: "Split into hot, warm and cold"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [attribute]
      description: "Three buckets off that score: hot means sales ready, warm goes to nurture, cold is a long cycle."
      prompt: "Segment leads into hot (sales-ready), warm (nurture), and cold (long-cycle) buckets based on score."
    - step: 3
      title: "Hand hot leads to a rep"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, segment]
      description: "Hot leads get an owner assigned and a task created. Warm and cold leads go into the nurture journeys instead."
      prompt: "Create a workflow routing hot leads to sales (assign owner, create task) and adding warm/cold leads to nurture journeys."
    - step: 4
      title: "Write content for each bucket"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute, segment, workflow]
      description: "A demo offer for hot leads, case studies and an ROI calculator for warm ones, and education for cold ones."
      prompt: "Generate nurture content tailored per segment: hot=demo offer, warm=case studies + ROI calc, cold=education content."
    - step: 5
      title: "Nurture at the right pace"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, segment, workflow, asset]
      description: "One journey per bucket, each with the cadence and content that fits how ready the lead is."
      prompt: "Build per-segment nurture journeys with appropriate cadence and content."
    - step: 6
      title: "Track handoffs and conversion"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, segment, workflow, asset, journey]
      description: "Score distribution, how many hot leads actually reach sales, and how many nurtured leads turn into MQLs."
      prompt: "Compose a dashboard tracking score distribution, hot-lead handoff rate, and nurture-to-MQL conversion."
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# B2B lead nurture and routing

Scores inbound leads, hands the sales ready ones to a rep with an owner and a task, and keeps the rest warm with content matched to how close they are.

## What it does

1. **Score every lead** (`create_ai_attribute`)

   A qualification score built from company fit, intent signals and how deeply the person has engaged.

2. **Split into hot, warm and cold** (`create_segment`)

   Three buckets off that score: hot means sales ready, warm goes to nurture, cold is a long cycle.

3. **Hand hot leads to a rep** (`create_workflow`)

   Hot leads get an owner assigned and a task created. Warm and cold leads go into the nurture journeys instead.

4. **Write content for each bucket** (`create_email_content`)

   A demo offer for hot leads, case studies and an ROI calculator for warm ones, and education for cold ones.

5. **Nurture at the right pace** (`create_journey`)

   One journey per bucket, each with the cadence and content that fits how ready the lead is.

6. **Track handoffs and conversion** (`create_dashboard`)

   Score distribution, how many hot leads actually reach sales, and how many nurtured leads turn into MQLs.

## What you end up with

- **attribute** (attribute): Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
