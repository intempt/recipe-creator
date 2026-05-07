---
name: Free To Paid Upgrade Csm Kickoff Task
description: Hand new paid customers off to CSM with context the moment they upgrade.
intempt:
  id: free-to-paid-upgrade-csm-kickoff-task
  version: 1.0.0
  slashCommand: /free-to-paid-upgrade-csm-kickoff-task
  shortDescription: Hand new paid customers off to CSM with context the moment they upgrade.
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
    - free
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
      signals. (Tailored for: Free-to-paid upgrade → CSM kickoff task.)'
    produces: attribute
  - id: build-csm-workflow
    describe: 'Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored
      for: Free-to-paid upgrade → CSM kickoff task.)'
    produces: workflow
  - id: build-content
    describe: 'Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored
      for: Free-to-paid upgrade → CSM kickoff task.)'
    produces: content
  - id: build-journey
    describe: 'Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for:
      Free-to-paid upgrade → CSM kickoff task.)'
    produces: journey
  - id: build-retention-report
    describe: 'Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Free-to-paid
      upgrade → CSM kickoff task.)'
    produces: report
  - id: build-dashboard
    describe: 'Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored
      for: Free-to-paid upgrade → CSM kickoff task.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: stripe
      severity: blocking
    - value: slack
      severity: blocking
---

# Free To Paid Upgrade Csm Kickoff Task

Hand new paid customers off to CSM with context the moment they upgrade.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment, and feature-usage signals. (Tailored for: Free-to-paid upgrade → CSM kickoff task.)
2. Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to Slack. (Tailored for: Free-to-paid upgrade → CSM kickoff task.)
3. Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails. (Tailored for: Free-to-paid upgrade → CSM kickoff task.)
4. Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. (Tailored for: Free-to-paid upgrade → CSM kickoff task.)
5. Compose a retention report tracking churn rate by risk tier and intervention type. (Tailored for: Free-to-paid upgrade → CSM kickoff task.)
6. Compose a dashboard showing risk distribution, intervention success rate, and net retention impact. (Tailored for: Free-to-paid upgrade → CSM kickoff task.)

## Prerequisites

- Integration: **stripe** (blocking)
- Integration: **slack** (blocking)
