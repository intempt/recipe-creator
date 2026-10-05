---
name: business-review
description: |
  Use when a user mentions "business review package", or asks for related help. Headline metrics, week-over-week deltas, wins, concerns, recommended actions, scheduled Slack digest.
arguments: []
intempt:
  id: business-review
  version: 1.0.0
  slashCommand: /business-review
  group: Dashboards
  shortDescription: "Produces a business review dashboard with headline KPIs and WoW deltas, a narrative report, and a scheduled Slack digest workflow."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [all]
    complexity: standard
    executionMode: live
    tags: [business-review]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_dashboard
    - create_report
    - create_workflow
  procedure:
    - step: 1
      title: "Compose Br Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      description: "Compose a business review dashboard with headline KPIs, WoW deltas, top wins, and top concerns."
      prompt: "Compose a business review dashboard with headline KPIs, WoW deltas, top wins, and top concerns."
    - step: 2
      title: "Generate Narrative Report"
      command: create_report
      produces: report
      bindsAs: report
      dependsOn: [dashboard]
      description: "Generate a narrative report summarizing the period: what changed, why, and recommended actions."
      prompt: "Generate a narrative report summarizing the period: what changed, why, and recommended actions."
    - step: 3
      title: "Schedule Digest Workflow"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [dashboard, report]
      description: "Create a workflow that delivers the dashboard and narrative as a scheduled Slack digest at the chosen cadence."
      prompt: "Create a workflow that delivers the dashboard and narrative as a scheduled Slack digest at the chosen cadence."
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---

# Business Review Package

## Procedure

1. **Compose Br Dashboard** [`create_dashboard`] — Compose a business review dashboard with headline KPIs, WoW deltas, top wins, and top concerns. → produces: dashboard
2. **Generate Narrative Report** [`create_report`] — Generate a narrative report summarizing the period: what changed, why, and recommended actions. → produces: report
3. **Schedule Digest Workflow** [`create_workflow`] — Create a workflow that delivers the dashboard and narrative as a scheduled Slack digest at the chosen cadence. → produces: workflow
