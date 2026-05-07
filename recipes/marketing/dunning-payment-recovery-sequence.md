---
name: Dunning Payment Recovery Sequence
description: Multi-touch failed-payment recovery. Speed is critical — an email sent 4 hours after failure recovers more than
  one sent 4 days later. Branches on retry attempts and failure reason.
intempt:
  id: dunning-payment-recovery-sequence
  version: 1.0.0
  slashCommand: /dunning-payment-recovery-sequence
  shortDescription: Multi-touch failed-payment recovery. Speed is critical — an email sent 4 hours after failure recovers
    more than one sent 4 days later. Branches on retry attempts and failure reason.
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
    - dunning
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
      signals. (Tailored for: Dunning — payment recovery sequence.)'
    produces: attribute
  - id: build-csm-workflow
    describe: 'Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored
      for: Dunning — payment recovery sequence.)'
    produces: workflow
  - id: build-content
    describe: 'Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored
      for: Dunning — payment recovery sequence.)'
    produces: content
  - id: build-journey
    describe: 'Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for:
      Dunning — payment recovery sequence.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Dunning —
      payment recovery sequence.)'
    produces: report
  - id: build-dashboard
    describe: 'Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored
      for: Dunning — payment recovery sequence.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: stripe
      severity: blocking
---

# Dunning Payment Recovery Sequence

Multi-touch failed-payment recovery. Speed is critical — an email sent 4 hours after failure recovers more than one sent 4 days later. Branches on retry attempts and failure reason.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals. (Tailored for: Dunning — payment recovery sequence.)
2. Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored for: Dunning — payment recovery sequence.)
3. Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored for: Dunning — payment recovery sequence.)
4. Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for: Dunning — payment recovery sequence.)
5. Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Dunning — payment recovery sequence.)
6. Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored for: Dunning — payment recovery sequence.)

## Prerequisites

- Integration: **stripe** (blocking)
