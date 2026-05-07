---
name: Feature Discovery For Paid Users
description: Weekly spotlight on features paid users aren't using yet. Increases stickiness and justifies the invoice — distinct
  from upgrade-to-higher-tier upsell.
intempt:
  id: feature-discovery-for-paid-users
  version: 1.0.0
  slashCommand: /feature-discovery-for-paid-users
  shortDescription: Weekly spotlight on features paid users aren't using yet. Increases stickiness and justifies the invoice
    — distinct from upgrade-to-higher-tier upsell.
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
    - feature
    - growth-and-expansion
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
      invites, data uploaded). (Tailored for: Feature discovery for paid users.)'
    produces: attribute
  - id: build-content
    describe: 'Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored
      for: Feature discovery for paid users.)'
    produces: content
  - id: build-journey
    describe: 'Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored
      for: Feature discovery for paid users.)'
    produces: journey
  - id: build-funnel-report
    describe: 'Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention
      overlay. (Tailored for: Feature discovery for paid users.)'
    produces: report
  prerequisites:
    integrations:
    - value: segment
      severity: blocking
---

# Feature Discovery For Paid Users

Weekly spotlight on features paid users aren't using yet. Increases stickiness and justifies the invoice — distinct from upgrade-to-higher-tier upsell.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded). (Tailored for: Feature discovery for paid users.)
2. Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored for: Feature discovery for paid users.)
3. Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored for: Feature discovery for paid users.)
4. Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay. (Tailored for: Feature discovery for paid users.)

## Prerequisites

- Integration: **segment** (blocking)
