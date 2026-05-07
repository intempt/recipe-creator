---
name: Post Demo Nurture 30 60 90 Day Cadence
description: Structured 3-touch nurture for prospects who had a demo but didn't close within 14 days. Value-add → customer
  success story → decision-push door-closing email.
intempt:
  id: post-demo-nurture-30-60-90-day-cadence
  version: 1.0.0
  slashCommand: /post-demo-nurture-30-60-90-day-cadence
  shortDescription: Structured 3-touch nurture for prospects who had a demo but didn't close within 14 days. Value-add → customer
    success story → decision-push door-closing email.
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
    - deal-progression
    - post
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Post-demo
      nurture — 30/60/90 day cadence.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Post-demo nurture — 30/60/90 day cadence.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Post-demo nurture —
      30/60/90 day cadence.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Post-demo nurture — 30/60/90 day cadence.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: salesforce
      severity: blocking
---

# Post Demo Nurture 30 60 90 Day Cadence

Structured 3-touch nurture for prospects who had a demo but didn't close within 14 days. Value-add → customer success story → decision-push door-closing email.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Post-demo nurture — 30/60/90 day cadence.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Post-demo nurture — 30/60/90 day cadence.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Post-demo nurture — 30/60/90 day cadence.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Post-demo nurture — 30/60/90 day cadence.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **salesforce** (blocking)
