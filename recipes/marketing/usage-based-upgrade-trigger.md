---
name: Usage Based Upgrade Trigger
description: Fires when a user approaches or exceeds their plan's usage limit. Frames the upgrade as 'you're getting so much
  value, your team is bottlenecked' — not a pushy sell.
intempt:
  id: usage-based-upgrade-trigger
  version: 1.0.0
  slashCommand: /usage-based-upgrade-trigger
  shortDescription: Fires when a user approaches or exceeds their plan's usage limit. Frames the upgrade as 'you're getting
    so much value, your team is bottlenecked' — not a pushy sell.
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
    - usage
    - growth-and-expansion
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
      signals. (Tailored for: Usage-based upgrade trigger.)'
    produces: attribute
  - id: build-csm-workflow
    describe: 'Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored
      for: Usage-based upgrade trigger.)'
    produces: workflow
  - id: build-content
    describe: 'Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored
      for: Usage-based upgrade trigger.)'
    produces: content
  - id: build-journey
    describe: 'Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for:
      Usage-based upgrade trigger.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Usage-based
      upgrade trigger.)'
    produces: report
  - id: build-dashboard
    describe: 'Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored
      for: Usage-based upgrade trigger.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: stripe
      severity: blocking
    - value: segment
      severity: blocking
---

# Usage Based Upgrade Trigger

Fires when a user approaches or exceeds their plan's usage limit. Frames the upgrade as 'you're getting so much value, your team is bottlenecked' — not a pushy sell.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals. (Tailored for: Usage-based upgrade trigger.)
2. Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored for: Usage-based upgrade trigger.)
3. Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored for: Usage-based upgrade trigger.)
4. Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for: Usage-based upgrade trigger.)
5. Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Usage-based upgrade trigger.)
6. Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored for: Usage-based upgrade trigger.)

## Prerequisites

- Integration: **stripe** (blocking)
- Integration: **segment** (blocking)
