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
  title: "Weekly business review pack"
  shortDescription: "Builds the weekly scorecard, writes the narrative on what moved and why, and posts both to Slack on the cadence you pick."
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
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
  invokesCommands:
    - create_dashboard
    - create_report
    - create_workflow
  procedure:
    - step: 1
      title: "Build the headline scorecard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      description: "Headline KPIs with week-over-week change, the top wins and the top concerns."
      prompt: "Compose a business review dashboard with headline KPIs, WoW deltas, top wins, and top concerns."
    - step: 2
      title: "Write the period narrative"
      command: create_report
      produces: report
      bindsAs: report
      dependsOn: [dashboard]
      description: "A written summary of what changed over the period, why it changed, and what to do next."
      prompt: "Generate a narrative report summarizing the period: what changed, why, and recommended actions."
    - step: 3
      title: "Send it to Slack on a cadence"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [dashboard, report]
      description: "Delivers the dashboard and the narrative to Slack on the schedule you choose."
      prompt: "Create a workflow that delivers the dashboard and narrative as a scheduled Slack digest at the chosen cadence."
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Weekly business review pack

Builds the weekly scorecard, writes the narrative on what moved and why, and posts both to Slack on the cadence you pick.

## Before you run it

- Connect slack

## What it does

1. **Build the headline scorecard** (`create_dashboard`)

   Headline KPIs with week-over-week change, the top wins and the top concerns.

2. **Write the period narrative** (`create_report`)

   A written summary of what changed over the period, why it changed, and what to do next.

3. **Send it to Slack on a cadence** (`create_workflow`)

   Delivers the dashboard and the narrative to Slack on the schedule you choose.

## What you end up with

- **dashboard** (dashboard): Dashboard produced by this recipe.
- **report** (report): Report produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
