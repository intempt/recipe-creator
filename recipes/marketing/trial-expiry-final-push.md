---
name: Trial Expiry Final Push
description: 3-email trial expiry push — 7, 3, and 1 day before trial ends. Branches on activation status — activated users
  get a confident upgrade push, non-activated users get a more urgent value justification.
intempt:
  id: trial-expiry-final-push
  version: 1.0.0
  slashCommand: /trial-expiry-final-push
  shortDescription: 3-email trial expiry push — 7, 3, and 1 day before trial ends. Branches on activation status — activated
    users get a confident upgrade push, non-activated users get a more urgent value justification.
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
      invites, data uploaded). (Tailored for: Trial expiry — final push.)'
    produces: attribute
  - id: build-content
    describe: 'Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored
      for: Trial expiry — final push.)'
    produces: content
  - id: build-journey
    describe: 'Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored
      for: Trial expiry — final push.)'
    produces: journey
  - id: build-funnel-report
    describe: 'Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention
      overlay. (Tailored for: Trial expiry — final push.)'
    produces: report
  prerequisites:
    integrations:
    - value: stripe
      severity: blocking
---

# Trial Expiry Final Push

3-email trial expiry push — 7, 3, and 1 day before trial ends. Branches on activation status — activated users get a confident upgrade push, non-activated users get a more urgent value justification.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded). (Tailored for: Trial expiry — final push.)
2. Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored for: Trial expiry — final push.)
3. Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored for: Trial expiry — final push.)
4. Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay. (Tailored for: Trial expiry — final push.)

## Prerequisites

- Integration: **stripe** (blocking)
