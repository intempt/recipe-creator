---
name: Nps Detractor Rescue
description: Immediate response to NPS detractor scores — routes to CS for human intervention and captures specific pain points.
  Detractors are highest churn risk; fast response matters.
intempt:
  id: nps-detractor-rescue
  version: 1.0.0
  slashCommand: /nps-detractor-rescue
  shortDescription: Immediate response to NPS detractor scores — routes to CS for human intervention and captures specific
    pain points. Detractors are highest churn risk; fast response matters.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - saas
    complexity: advanced
    executionMode: live
    tags:
    - retention-and-churn-prevention
    - nps
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: attribute
    type: attribute
    description: Attribute produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: report
    type: report
    description: Report produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: compute-churn-risk
    describe: 'Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage
      signals. (Tailored for: NPS detractor rescue.)'
    produces: attribute
  - id: build-csm-workflow
    describe: 'Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored
      for: NPS detractor rescue.)'
    produces: workflow
  - id: build-content
    describe: 'Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored
      for: NPS detractor rescue.)'
    produces: content
  - id: build-journey
    describe: 'Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for:
      NPS detractor rescue.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: NPS detractor
      rescue.)'
    produces: report
  - id: build-dashboard
    describe: 'Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored
      for: NPS detractor rescue.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: segment
      severity: blocking
---

# Nps Detractor Rescue

Immediate response to NPS detractor scores — routes to CS for human intervention and captures specific pain points. Detractors are highest churn risk; fast response matters.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals. (Tailored for: NPS detractor rescue.)
2. Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored for: NPS detractor rescue.)
3. Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored for: NPS detractor rescue.)
4. Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for: NPS detractor rescue.)
5. Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: NPS detractor rescue.)
6. Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored for: NPS detractor rescue.)

## Prerequisites

- Integration: **segment** (blocking)
