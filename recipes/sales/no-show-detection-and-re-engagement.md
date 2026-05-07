---
name: No Show Detection And Re Engagement
description: Detect when a booked meeting was not attended and automatically trigger re-engagement.
intempt:
  id: no-show-detection-and-re-engagement
  version: 1.0.0
  slashCommand: /no-show-detection-and-re-engagement
  shortDescription: Detect when a booked meeting was not attended and automatically trigger re-engagement.
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
    - booking-flow-automation
    - no-show
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: No-show
      detection and re-engagement.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: No-show detection and re-engagement.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: No-show detection and
      re-engagement.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: No-show detection and re-engagement.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# No Show Detection And Re Engagement

Detect when a booked meeting was not attended and automatically trigger re-engagement.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: No-show detection and re-engagement.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: No-show detection and re-engagement.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: No-show detection and re-engagement.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: No-show detection and re-engagement.)

## Prerequisites

- Integration: **slack** (blocking)
