---
name: Demo Request Instant Ae Task Account Enrichment
description: Turn demo hand-raisers into booked meetings in under an hour.
intempt:
  id: demo-request-instant-ae-task-account-enrichment
  version: 1.0.0
  slashCommand: /demo-request-instant-ae-task-account-enrichment
  shortDescription: Turn demo hand-raisers into booked meetings in under an hour.
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
    - demo
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Demo request
      → instant AE task + account enrichment +.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Demo request → instant AE task + account enrichment +.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Demo request → instant
      AE task + account enrichment +.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Demo request → instant AE task + account enrichment +.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Demo Request Instant Ae Task Account Enrichment

Turn demo hand-raisers into booked meetings in under an hour.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Demo request → instant AE task + account enrichment +.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Demo request → instant AE task + account enrichment +.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Demo request → instant AE task + account enrichment +.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Demo request → instant AE task + account enrichment +.)

## Prerequisites

- Integration: **slack** (blocking)
