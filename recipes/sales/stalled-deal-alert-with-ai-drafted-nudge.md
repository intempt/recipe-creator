---
name: Stalled Deal Alert With Ai Drafted Nudge
description: Rescue quiet deals by giving the AE an AI-drafted nudge ready to send.
intempt:
  id: stalled-deal-alert-with-ai-drafted-nudge
  version: 1.0.0
  slashCommand: /stalled-deal-alert-with-ai-drafted-nudge
  shortDescription: Rescue quiet deals by giving the AE an AI-drafted nudge ready to send.
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
    - stalled
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Stalled
      deal alert with AI-drafted nudge.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Stalled deal alert with AI-drafted nudge.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Stalled deal alert
      with AI-drafted nudge.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Stalled deal alert with AI-drafted nudge.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Stalled Deal Alert With Ai Drafted Nudge

Rescue quiet deals by giving the AE an AI-drafted nudge ready to send.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Stalled deal alert with AI-drafted nudge.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Stalled deal alert with AI-drafted nudge.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Stalled deal alert with AI-drafted nudge.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Stalled deal alert with AI-drafted nudge.)

## Prerequisites

- Integration: **slack** (blocking)
