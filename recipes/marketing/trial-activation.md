---
name: Trial Activation
description: Drive trial users to paid conversion via scoring, segmentation, onboarding journey, and funnel measurement.
intempt:
  id: trial-activation
  version: 1.0.0
  slashCommand: /trial-activation
  shortDescription: Drive trial users to paid conversion via scoring, segmentation, onboarding journey, and funnel measurement.
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
    - trial-activation
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
    describe: Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team
      invites, data uploaded).
    produces: attribute
  - id: build-content
    describe: Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier.
    produces: content
  - id: build-journey
    describe: Build a tiered onboarding journey routing each tier through appropriate education and conversion touches.
    produces: journey
  - id: build-funnel-report
    describe: Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay.
    produces: report
---

# Trial Activation

Drive trial users to paid conversion via scoring, segmentation, onboarding journey, and funnel measurement.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded).
2. Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier.
3. Build a tiered onboarding journey routing each tier through appropriate education and conversion touches.
4. Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay.
