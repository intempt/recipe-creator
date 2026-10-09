---
name: churn-prevention
description: |
  Use when a user mentions "churn prevention", or asks for related help. AI-derived risk scoring, CSM alerts, automated re-engagement, and retention measurement.
arguments: []
intempt:
  id: churn-prevention
  title: "Churn prevention"
  version: 1.0.0
  slashCommand: /churn-prevention
  group: Journeys
  shortDescription: "Flags customers who are drifting away, reaches them automatically while it is still cheap to fix, and pulls in a CSM when it is not."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas]
    complexity: advanced
    executionMode: live
    tags: [churn-prevention]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_email_content
    - create_journey
    - build_retention_report
    - create_dashboard
  procedure:
    - step: 1
      title: "Score churn risk"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "A churn risk score built from falling engagement, the tone of support tickets, and which features have gone unused."
      prompt: "Define an AI-derived Churn risk score attribute using engagement decline, support ticket sentiment, and feature-usage signals."
    - step: 2
      title: "Split into low, medium and high"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [attribute]
      description: "Three risk buckets off that score."
      prompt: "Segment users into low/medium/high churn-risk buckets."
    - step: 3
      title: "Tell the CSM about high risk"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, segment]
      description: "When a user crosses the high risk threshold, their CSM gets a Slack message carrying the context behind the score."
      prompt: "Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack."
    - step: 4
      title: "Write the win back emails"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute, segment, workflow]
      description: "Emails that point to a feature they are missing, share a customer success story, and remind them what they are paying for."
      prompt: "Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails."
    - step: 5
      title: "Reach medium risk first"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, segment, workflow, asset]
      description: "Medium risk users get those emails automatically, before the account needs a CSM to step in."
      prompt: "Build a journey for medium-risk users with auto-engagement before CSM intervention is needed."
    - step: 6
      title: "Compare churn by risk tier"
      command: build_retention_report
      produces: report
      bindsAs: report
      dependsOn: [attribute, segment, workflow, asset, journey]
      description: "Churn rate by risk tier and by which intervention the user received."
      prompt: "Compose a retention report tracking churn rate by risk tier and intervention type."
    - step: 7
      title: "See if the saves are working"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, segment, workflow, asset, journey, report]
      description: "Risk distribution, how often an intervention works, and the net effect on retention."
      prompt: "Compose a dashboard showing risk distribution, intervention success rate, and net retention impact."
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Churn prevention

Flags customers who are drifting away, reaches them automatically while it is still cheap to fix, and pulls in a CSM when it is not.

## Before you run it

- Connect slack

## What it does

1. **Score churn risk** (`create_ai_attribute`)

   A churn risk score built from falling engagement, the tone of support tickets, and which features have gone unused.

2. **Split into low, medium and high** (`create_segment`)

   Three risk buckets off that score.

3. **Tell the CSM about high risk** (`create_workflow`)

   When a user crosses the high risk threshold, their CSM gets a Slack message carrying the context behind the score.

4. **Write the win back emails** (`create_email_content`)

   Emails that point to a feature they are missing, share a customer success story, and remind them what they are paying for.

5. **Reach medium risk first** (`create_journey`)

   Medium risk users get those emails automatically, before the account needs a CSM to step in.

6. **Compare churn by risk tier** (`build_retention_report`)

   Churn rate by risk tier and by which intervention the user received.

7. **See if the saves are working** (`create_dashboard`)

   Risk distribution, how often an intervention works, and the net effect on retention.

## What you end up with

- **attribute** (attribute): Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
