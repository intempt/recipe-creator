---
name: b2b-nurture
description: |
  Use when a user mentions "b2b nurture & deal acceleration", "pipeline", "deal management", or asks for related help. Score leads, segment by readiness, route hot leads to sales, nurture the rest.
arguments: []
intempt:
  id: b2b-nurture
  version: 1.0.0
  slashCommand: /b2b-nurture
  group: Journeys
  shortDescription: "Score leads, segment by readiness, route hot leads to sales, nurture the rest."
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
      title: "Compute Lead Score"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "Define a Qualification scoring attribute weighting firmographic fit, intent signals, and engagement depth."
      prompt: "Define a Qualification scoring attribute weighting firmographic fit, intent signals, and engagement depth."
    - step: 2
      title: "Segment By Readiness"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [attribute]
      description: "Segment leads into hot (sales-ready), warm (nurture), and cold (long-cycle) buckets based on score."
      prompt: "Segment leads into hot (sales-ready), warm (nurture), and cold (long-cycle) buckets based on score."
    - step: 3
      title: "Build Routing Workflow"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, segment]
      description: "Create a workflow routing hot leads to sales (assign owner, create task) and adding warm/cold leads to nurture journeys."
      prompt: "Create a workflow routing hot leads to sales (assign owner, create task) and adding warm/cold leads to nurture journeys."
    - step: 4
      title: "Build Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute, segment, workflow]
      description: "Generate nurture content tailored per segment: hot=demo offer, warm=case studies + ROI calc, cold=education content."
      prompt: "Generate nurture content tailored per segment: hot=demo offer, warm=case studies + ROI calc, cold=education content."
    - step: 5
      title: "Build Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, segment, workflow, asset]
      description: "Build per-segment nurture journeys with appropriate cadence and content."
      prompt: "Build per-segment nurture journeys with appropriate cadence and content."
    - step: 6
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, segment, workflow, asset, journey]
      description: "Compose a dashboard tracking score distribution, hot-lead handoff rate, and nurture-to-MQL conversion."
      prompt: "Compose a dashboard tracking score distribution, hot-lead handoff rate, and nurture-to-MQL conversion."
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# B2B Nurture & Deal Acceleration

## Procedure

1. **Compute Lead Score** [`create_ai_attribute`] — Define a Qualification scoring attribute weighting firmographic fit, intent signals, and engagement depth. → produces: attribute
2. **Segment By Readiness** [`create_segment`] — Segment leads into hot (sales-ready), warm (nurture), and cold (long-cycle) buckets based on score. → produces: segment
3. **Build Routing Workflow** [`create_workflow`] — Create a workflow routing hot leads to sales (assign owner, create task) and adding warm/cold leads to nurture journeys. → produces: workflow
4. **Build Content** [`create_email_content`] — Generate nurture content tailored per segment: hot=demo offer, warm=case studies + ROI calc, cold=education content. → produces: asset
5. **Build Journey** [`create_journey`] — Build per-segment nurture journeys with appropriate cadence and content. → produces: journey
6. **Build Dashboard** [`create_dashboard`] — Compose a dashboard tracking score distribution, hot-lead handoff rate, and nurture-to-MQL conversion. → produces: dashboard
