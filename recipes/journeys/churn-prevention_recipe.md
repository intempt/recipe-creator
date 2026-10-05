---
name: churn-prevention
description: |
  Use when a user mentions "churn prevention", or asks for related help. AI-derived risk scoring, CSM alerts, automated re-engagement, and retention measurement.
arguments: []
intempt:
  id: churn-prevention
  version: 1.0.0
  slashCommand: /churn-prevention
  group: Journeys
  shortDescription: "Create a churn_risk_score attribute from engagement, support sentiment, and feature usage, then segment high-risk users for CSM alerts."
  availability: coming-soon
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
      title: "Compute Churn Risk"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals."
      prompt: "Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals."
    - step: 2
      title: "Segment At Risk"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: [attribute]
      description: "Segment users into low/medium/high churn-risk buckets."
      prompt: "Segment users into low/medium/high churn-risk buckets."
    - step: 3
      title: "Build Csm Workflow"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, segment]
      description: "Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack."
      prompt: "Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack."
    - step: 4
      title: "Build Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute, segment, workflow]
      description: "Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails."
      prompt: "Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails."
    - step: 5
      title: "Build Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, segment, workflow, asset]
      description: "Build a journey for medium-risk users with auto-engagement before CSM intervention is needed."
      prompt: "Build a journey for medium-risk users with auto-engagement before CSM intervention is needed."
    - step: 6
      title: "Build Retention Report"
      command: build_retention_report
      produces: report
      bindsAs: report
      dependsOn: [attribute, segment, workflow, asset, journey]
      description: "Compose a retention report tracking churn rate by risk tier and intervention type."
      prompt: "Compose a retention report tracking churn rate by risk tier and intervention type."
    - step: 7
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, segment, workflow, asset, journey, report]
      description: "Compose a dashboard showing risk distribution, intervention success rate, and net retention impact."
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

# Churn Prevention

## Procedure

1. **Compute Churn Risk** [`create_ai_attribute`] — Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals. → produces: attribute
2. **Segment At Risk** [`create_segment`] — Segment users into low/medium/high churn-risk buckets. → produces: segment
3. **Build Csm Workflow** [`create_workflow`] — Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. → produces: workflow
4. **Build Content** [`create_email_content`] — Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. → produces: asset
5. **Build Journey** [`create_journey`] — Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. → produces: journey
6. **Build Retention Report** [`build_retention_report`] — Compose a retention report tracking churn rate by risk tier and intervention type. → produces: report
7. **Build Dashboard** [`create_dashboard`] — Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. → produces: dashboard
