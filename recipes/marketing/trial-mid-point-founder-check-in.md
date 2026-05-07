---
name: Trial Mid Point Founder Check In
description: 'Plain-text founder-voice email delivered at trial midpoint. Gartner: trial users who receive a sales touch at
  the right moment convert 41% more often than fixed-schedule outreach.'
intempt:
  id: trial-mid-point-founder-check-in
  version: 1.0.0
  slashCommand: /trial-mid-point-founder-check-in
  shortDescription: 'Plain-text founder-voice email delivered at trial midpoint. Gartner: trial users who receive a sales
    touch at the right moment convert 41% more often than fixed-schedule outreach.'
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
      invites, data uploaded). (Tailored for: Trial mid-point founder check-in.)'
    produces: attribute
  - id: build-content
    describe: 'Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored
      for: Trial mid-point founder check-in.)'
    produces: content
  - id: build-journey
    describe: 'Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored
      for: Trial mid-point founder check-in.)'
    produces: journey
  - id: build-funnel-report
    describe: 'Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention
      overlay. (Tailored for: Trial mid-point founder check-in.)'
    produces: report
  prerequisites:
    integrations:
    - value: stripe
      severity: blocking
---

# Trial Mid Point Founder Check In

Plain-text founder-voice email delivered at trial midpoint. Gartner: trial users who receive a sales touch at the right moment convert 41% more often than fixed-schedule outreach.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded). (Tailored for: Trial mid-point founder check-in.)
2. Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored for: Trial mid-point founder check-in.)
3. Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored for: Trial mid-point founder check-in.)
4. Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay. (Tailored for: Trial mid-point founder check-in.)

## Prerequisites

- Integration: **stripe** (blocking)
