---
name: Pre Cancellation Save
description: Triggered when user initiates cancellation — offers alternatives (pause, downgrade, discount) before the cancel
  completes. Captures reason via exit survey.
intempt:
  id: pre-cancellation-save
  version: 1.0.0
  slashCommand: /pre-cancellation-save
  shortDescription: Triggered when user initiates cancellation — offers alternatives (pause, downgrade, discount) before the
    cancel completes. Captures reason via exit survey.
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
    - pre
    - billing-and-subscription-lifecycle
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
      signals. (Tailored for: Pre-cancellation save.)'
    produces: attribute
  - id: build-csm-workflow
    describe: 'Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored
      for: Pre-cancellation save.)'
    produces: workflow
  - id: build-content
    describe: 'Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored
      for: Pre-cancellation save.)'
    produces: content
  - id: build-journey
    describe: 'Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for:
      Pre-cancellation save.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Pre-cancellation
      save.)'
    produces: report
  - id: build-dashboard
    describe: 'Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored
      for: Pre-cancellation save.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: stripe
      severity: blocking
---

# Pre Cancellation Save

Triggered when user initiates cancellation — offers alternatives (pause, downgrade, discount) before the cancel completes. Captures reason via exit survey.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals. (Tailored for: Pre-cancellation save.)
2. Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored for: Pre-cancellation save.)
3. Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored for: Pre-cancellation save.)
4. Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for: Pre-cancellation save.)
5. Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Pre-cancellation save.)
6. Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored for: Pre-cancellation save.)

## Prerequisites

- Integration: **stripe** (blocking)
