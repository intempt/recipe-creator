---
name: Annual Renewal Reminder Sequence
description: 90/60/30/7 day renewal reminder cadence for annual subscriptions. Builds renewal confidence with usage recaps
  and value reinforcement before the charge lands.
intempt:
  id: annual-renewal-reminder-sequence
  version: 1.0.0
  slashCommand: /annual-renewal-reminder-sequence
  shortDescription: 90/60/30/7 day renewal reminder cadence for annual subscriptions. Builds renewal confidence with usage
    recaps and value reinforcement before the charge lands.
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
    - billing-and-subscription-lifecycle
    - annual
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
      signals. (Tailored for: Annual renewal reminder sequence.)'
    produces: attribute
  - id: build-csm-workflow
    describe: 'Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored
      for: Annual renewal reminder sequence.)'
    produces: workflow
  - id: build-content
    describe: 'Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored
      for: Annual renewal reminder sequence.)'
    produces: content
  - id: build-journey
    describe: 'Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for:
      Annual renewal reminder sequence.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Annual renewal
      reminder sequence.)'
    produces: report
  - id: build-dashboard
    describe: 'Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored
      for: Annual renewal reminder sequence.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: stripe
      severity: blocking
---

# Annual Renewal Reminder Sequence

90/60/30/7 day renewal reminder cadence for annual subscriptions. Builds renewal confidence with usage recaps and value reinforcement before the charge lands.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals. (Tailored for: Annual renewal reminder sequence.)
2. Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored for: Annual renewal reminder sequence.)
3. Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored for: Annual renewal reminder sequence.)
4. Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for: Annual renewal reminder sequence.)
5. Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Annual renewal reminder sequence.)
6. Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored for: Annual renewal reminder sequence.)

## Prerequisites

- Integration: **stripe** (blocking)
