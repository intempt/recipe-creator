---
name: Trial Activation First Key Action
description: 7-day activation push for new trial signups — drives toward the first key in-product action that correlates with
  conversion. Branches on whether activation happens.
intempt:
  id: trial-activation-first-key-action
  version: 1.0.0
  slashCommand: /trial-activation-first-key-action
  shortDescription: 7-day activation push for new trial signups — drives toward the first key in-product action that correlates
    with conversion. Branches on whether activation happens.
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
    - trial
    - trial-and-activation
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
      invites, data uploaded). (Tailored for: Trial activation — first key action.)'
    produces: attribute
  - id: build-content
    describe: 'Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored
      for: Trial activation — first key action.)'
    produces: content
  - id: build-journey
    describe: 'Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored
      for: Trial activation — first key action.)'
    produces: journey
  - id: build-funnel-report
    describe: 'Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention
      overlay. (Tailored for: Trial activation — first key action.)'
    produces: report
  prerequisites:
    integrations:
    - value: segment
      severity: blocking
    - value: stripe
      severity: blocking
---

# Trial Activation First Key Action

7-day activation push for new trial signups — drives toward the first key in-product action that correlates with conversion. Branches on whether activation happens.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded). (Tailored for: Trial activation — first key action.)
2. Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored for: Trial activation — first key action.)
3. Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored for: Trial activation — first key action.)
4. Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay. (Tailored for: Trial activation — first key action.)

## Prerequisites

- Integration: **segment** (blocking)
- Integration: **stripe** (blocking)
