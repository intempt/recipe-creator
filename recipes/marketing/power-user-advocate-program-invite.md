---
name: Power User Advocate Program Invite
description: Identifies power users (high usage, high NPS, long tenure) and invites them to a structured advocate program
  — case studies, referrals, community leadership.
intempt:
  id: power-user-advocate-program-invite
  version: 1.0.0
  slashCommand: /power-user-advocate-program-invite
  shortDescription: Identifies power users (high usage, high NPS, long tenure) and invites them to a structured advocate program
    — case studies, referrals, community leadership.
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
    - growth-and-expansion
    - power
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
      invites, data uploaded). (Tailored for: Power user → advocate program invite.)'
    produces: attribute
  - id: build-content
    describe: 'Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored
      for: Power user → advocate program invite.)'
    produces: content
  - id: build-journey
    describe: 'Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored
      for: Power user → advocate program invite.)'
    produces: journey
  - id: build-funnel-report
    describe: 'Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention
      overlay. (Tailored for: Power user → advocate program invite.)'
    produces: report
  prerequisites:
    integrations:
    - value: segment
      severity: blocking
---

# Power User Advocate Program Invite

Identifies power users (high usage, high NPS, long tenure) and invites them to a structured advocate program — case studies, referrals, community leadership.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded). (Tailored for: Power user → advocate program invite.)
2. Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored for: Power user → advocate program invite.)
3. Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored for: Power user → advocate program invite.)
4. Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay. (Tailored for: Power user → advocate program invite.)

## Prerequisites

- Integration: **segment** (blocking)
