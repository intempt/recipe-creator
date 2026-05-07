---
name: Demo No Show Re Engagement
description: Fires when a scheduled demo is missed. 3-email recovery cadence that assumes scheduling conflict (not disinterest)
  and offers easy rescheduling.
intempt:
  id: demo-no-show-re-engagement
  version: 1.0.0
  slashCommand: /demo-no-show-re-engagement
  shortDescription: Fires when a scheduled demo is missed. 3-email recovery cadence that assumes scheduling conflict (not
    disinterest) and offers easy rescheduling.
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Demo no-show
      re-engagement.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Demo no-show re-engagement.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Demo no-show re-engagement.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Demo no-show re-engagement.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
---

# Demo No Show Re Engagement

Fires when a scheduled demo is missed. 3-email recovery cadence that assumes scheduling conflict (not disinterest) and offers easy rescheduling.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Demo no-show re-engagement.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Demo no-show re-engagement.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Demo no-show re-engagement.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Demo no-show re-engagement.)

## Prerequisites

- Integration: **hubspot** (blocking)
