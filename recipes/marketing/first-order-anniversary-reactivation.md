---
name: First Order Anniversary Reactivation
description: Annual reactivation triggered on the 1-year anniversary of a customer's first purchase. Especially strong for
  seasonal or annual-purchase cycles (holiday gifts, annual supplies, birthday gifting).
intempt:
  id: first-order-anniversary-reactivation
  version: 1.0.0
  slashCommand: /first-order-anniversary-reactivation
  shortDescription: Annual reactivation triggered on the 1-year anniversary of a customer's first purchase. Especially strong
    for seasonal or annual-purchase cycles (holiday gifts, annual supplies, birthday gifting).
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - ecommerce
    complexity: advanced
    executionMode: live
    tags:
    - first
    - post-purchase-and-retention
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
      invites, data uploaded). (Tailored for: First-order anniversary reactivation.)'
    produces: attribute
  - id: build-content
    describe: 'Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored
      for: First-order anniversary reactivation.)'
    produces: content
  - id: build-journey
    describe: 'Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored
      for: First-order anniversary reactivation.)'
    produces: journey
  - id: build-funnel-report
    describe: 'Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention
      overlay. (Tailored for: First-order anniversary reactivation.)'
    produces: report
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# First Order Anniversary Reactivation

Annual reactivation triggered on the 1-year anniversary of a customer's first purchase. Especially strong for seasonal or annual-purchase cycles (holiday gifts, annual supplies, birthday gifting).

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Steps

1. Define an AI-derived trial_health_score attribute computed from event signals (logins, key feature usage, team invites, data uploaded). (Tailored for: First-order anniversary reactivation.)
2. Generate tier-specific onboarding email content emphasizing relevant aha-moment features per tier. (Tailored for: First-order anniversary reactivation.)
3. Build a tiered onboarding journey routing each tier through appropriate education and conversion touches. (Tailored for: First-order anniversary reactivation.)
4. Compose a funnel report tracking trial-signup → key-event-1 → key-event-2 → paid-conversion with retention overlay. (Tailored for: First-order anniversary reactivation.)

## Prerequisites

- Integration: **shopify** (blocking)
