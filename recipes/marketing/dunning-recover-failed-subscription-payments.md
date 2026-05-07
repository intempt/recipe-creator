---
name: Dunning Recover Failed Subscription Payments
description: Recover revenue from failed recurring payments with a structured retry and CSM escalation flow.
intempt:
  id: dunning-recover-failed-subscription-payments
  version: 1.0.0
  slashCommand: /dunning-recover-failed-subscription-payments
  shortDescription: Recover revenue from failed recurring payments with a structured retry and CSM escalation flow.
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
    - revenue-operations
    - dunning
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
      signals. (Tailored for: Dunning — recover failed subscription payments.)'
    produces: attribute
  - id: build-csm-workflow
    describe: 'Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored
      for: Dunning — recover failed subscription payments.)'
    produces: workflow
  - id: build-content
    describe: 'Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored
      for: Dunning — recover failed subscription payments.)'
    produces: content
  - id: build-journey
    describe: 'Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for:
      Dunning — recover failed subscription payments.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Dunning —
      recover failed subscription payments.)'
    produces: report
  - id: build-dashboard
    describe: 'Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored
      for: Dunning — recover failed subscription payments.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: stripe
      severity: blocking
    - value: slack
      severity: blocking
---

# Dunning Recover Failed Subscription Payments

Recover revenue from failed recurring payments with a structured retry and CSM escalation flow.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals. (Tailored for: Dunning — recover failed subscription payments.)
2. Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored for: Dunning — recover failed subscription payments.)
3. Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored for: Dunning — recover failed subscription payments.)
4. Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for: Dunning — recover failed subscription payments.)
5. Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Dunning — recover failed subscription payments.)
6. Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored for: Dunning — recover failed subscription payments.)

## Prerequisites

- Integration: **stripe** (blocking)
- Integration: **slack** (blocking)
