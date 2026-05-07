---
name: Trial Expiring High Likelihood Ae Outreach Task
description: Capture high-intent trial users in their last 72 hours before conversion closes.
intempt:
  id: trial-expiring-high-likelihood-ae-outreach-task
  version: 1.0.0
  slashCommand: /trial-expiring-high-likelihood-ae-outreach-task
  shortDescription: Capture high-intent trial users in their last 72 hours before conversion closes.
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
    - sales-automation
    - trial
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: attribute
    type: attribute
    description: Attribute produced by this recipe.
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: compute-trial-health
    describe: 'Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team
      invites, data uploaded). (Tailored for: Trial expiring + high likelihood → AE outreach task.)'
    produces: attribute
  - id: build-content
    describe: 'Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored
      for: Trial expiring + high likelihood → AE outreach task.)'
    produces: content
  - id: build-journey
    describe: 'Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored
      for: Trial expiring + high likelihood → AE outreach task.)'
    produces: journey
  - id: build-funnel-report
    describe: 'Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention
      overlay. (Tailored for: Trial expiring + high likelihood → AE outreach task.)'
    produces: report
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Trial Expiring High Likelihood Ae Outreach Task

Capture high-intent trial users in their last 72 hours before conversion closes.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded). (Tailored for: Trial expiring + high likelihood → AE outreach task.)
2. Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored for: Trial expiring + high likelihood → AE outreach task.)
3. Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored for: Trial expiring + high likelihood → AE outreach task.)
4. Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay. (Tailored for: Trial expiring + high likelihood → AE outreach task.)

## Prerequisites

- Integration: **slack** (blocking)
