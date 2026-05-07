---
name: Renewal Readiness 90 60 30 Day Tiered Csm Tasks
description: Keep renewals on track with a structured 90/60/30 cadence.
intempt:
  id: renewal-readiness-90-60-30-day-tiered-csm-tasks
  version: 1.0.0
  slashCommand: /renewal-readiness-90-60-30-day-tiered-csm-tasks
  shortDescription: Keep renewals on track with a structured 90/60/30 cadence.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - b2b
    complexity: advanced
    executionMode: live
    tags:
    - revenue-operations
    - renewal
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
      signals. (Tailored for: Renewal readiness — 90/60/30 day tiered CSM tasks.)'
    produces: attribute
  - id: build-csm-workflow
    describe: 'Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored
      for: Renewal readiness — 90/60/30 day tiered CSM tasks.)'
    produces: workflow
  - id: build-content
    describe: 'Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored
      for: Renewal readiness — 90/60/30 day tiered CSM tasks.)'
    produces: content
  - id: build-journey
    describe: 'Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for:
      Renewal readiness — 90/60/30 day tiered CSM tasks.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Renewal readiness
      — 90/60/30 day tiered CSM tasks.)'
    produces: report
  - id: build-dashboard
    describe: 'Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored
      for: Renewal readiness — 90/60/30 day tiered CSM tasks.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Renewal Readiness 90 60 30 Day Tiered Csm Tasks

Keep renewals on track with a structured 90/60/30 cadence.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals. (Tailored for: Renewal readiness — 90/60/30 day tiered CSM tasks.)
2. Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored for: Renewal readiness — 90/60/30 day tiered CSM tasks.)
3. Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored for: Renewal readiness — 90/60/30 day tiered CSM tasks.)
4. Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for: Renewal readiness — 90/60/30 day tiered CSM tasks.)
5. Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Renewal readiness — 90/60/30 day tiered CSM tasks.)
6. Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored for: Renewal readiness — 90/60/30 day tiered CSM tasks.)

## Prerequisites

- Integration: **slack** (blocking)
