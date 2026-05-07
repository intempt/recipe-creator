---
name: Event Registration Confirmation Pre Event Warm Up
description: Registration confirmation + pre-event warm-up content to maximize attendance rate. Solves the 50%+ no-show problem
  that kills event ROI.
intempt:
  id: event-registration-confirmation-pre-event-warm-up
  version: 1.0.0
  slashCommand: /event-registration-confirmation-pre-event-warm-up
  shortDescription: Registration confirmation + pre-event warm-up content to maximize attendance rate. Solves the 50%+ no-show
    problem that kills event ROI.
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
    - lead-qualification-and-outbound
    - event
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Event registration
      confirmation + pre-event warm-up.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Event registration confirmation + pre-event warm-up.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Event registration
      confirmation + pre-event warm-up.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Event registration confirmation + pre-event warm-up.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
---

# Event Registration Confirmation Pre Event Warm Up

Registration confirmation + pre-event warm-up content to maximize attendance rate. Solves the 50%+ no-show problem that kills event ROI.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Event registration confirmation + pre-event warm-up.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Event registration confirmation + pre-event warm-up.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Event registration confirmation + pre-event warm-up.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Event registration confirmation + pre-event warm-up.)

## Prerequisites

- Integration: **hubspot** (blocking)
