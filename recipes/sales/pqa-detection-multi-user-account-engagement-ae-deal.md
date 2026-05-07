---
name: Pqa Detection Multi User Account Engagement Ae Deal
description: Surface product-qualified accounts — where multiple users from the same company engage meaningfully in a short
  window — as real AE opportunities.
intempt:
  id: pqa-detection-multi-user-account-engagement-ae-deal
  version: 1.0.0
  slashCommand: /pqa-detection-multi-user-account-engagement-ae-deal
  shortDescription: Surface product-qualified accounts — where multiple users from the same company engage meaningfully in
    a short window — as real AE opportunities.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: revops-automator
    mode:
    - b2b
    complexity: advanced
    executionMode: live
    tags:
    - sales-automation
    - pqa
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
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: compute-qualification-score
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: PQA detection
      — multi-user account engagement → AE deal +.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: PQA detection — multi-user account engagement → AE deal +.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: PQA detection — multi-user
      account engagement → AE deal +.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: PQA detection — multi-user account engagement → AE deal +.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Pqa Detection Multi User Account Engagement Ae Deal

Surface product-qualified accounts — where multiple users from the same company engage meaningfully in a short window — as real AE opportunities.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: PQA detection — multi-user account engagement → AE deal +.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: PQA detection — multi-user account engagement → AE deal +.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: PQA detection — multi-user account engagement → AE deal +.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: PQA detection — multi-user account engagement → AE deal +.)

## Prerequisites

- Integration: **slack** (blocking)
