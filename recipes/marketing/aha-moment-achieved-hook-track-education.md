---
name: Aha Moment Achieved Hook Track Education
description: Track 2 successor to trial activation — fires when the user hits the aha-moment. Deepens feature usage with repeated
  value loops (per ProductLed's hook framework). Increases likelihood of paid...
intempt:
  id: aha-moment-achieved-hook-track-education
  version: 1.0.0
  slashCommand: /aha-moment-achieved-hook-track-education
  shortDescription: Track 2 successor to trial activation — fires when the user hits the aha-moment. Deepens feature usage
    with repeated value loops (per ProductLed's hook framework). Increases likelihood of paid...
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
    - aha
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
      invites, data uploaded). (Tailored for: Aha-moment achieved → hook-track education.)'
    produces: attribute
  - id: build-content
    describe: 'Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored
      for: Aha-moment achieved → hook-track education.)'
    produces: content
  - id: build-journey
    describe: 'Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored
      for: Aha-moment achieved → hook-track education.)'
    produces: journey
  - id: build-funnel-report
    describe: 'Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention
      overlay. (Tailored for: Aha-moment achieved → hook-track education.)'
    produces: report
  prerequisites:
    integrations:
    - value: segment
      severity: blocking
---

# Aha Moment Achieved Hook Track Education

Track 2 successor to trial activation — fires when the user hits the aha-moment. Deepens feature usage with repeated value loops (per ProductLed's hook framework). Increases likelihood of paid...

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded). (Tailored for: Aha-moment achieved → hook-track education.)
2. Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored for: Aha-moment achieved → hook-track education.)
3. Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored for: Aha-moment achieved → hook-track education.)
4. Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay. (Tailored for: Aha-moment achieved → hook-track education.)

## Prerequisites

- Integration: **segment** (blocking)
