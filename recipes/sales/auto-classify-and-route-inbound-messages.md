---
name: Auto Classify And Route Inbound Messages
description: Automatically classify inbound messages by intent and route to the right team or queue.
intempt:
  id: auto-classify-and-route-inbound-messages
  version: 1.0.0
  slashCommand: /auto-classify-and-route-inbound-messages
  shortDescription: Automatically classify inbound messages by intent and route to the right team or queue.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: revops-automator
    mode:
    - saas
    complexity: advanced
    executionMode: live
    tags:
    - auto
    - inbox-and-reply-automation
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Auto-classify
      and route inbound messages.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Auto-classify and route inbound messages.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Auto-classify and route
      inbound messages.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Auto-classify and route inbound messages.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Auto Classify And Route Inbound Messages

Automatically classify inbound messages by intent and route to the right team or queue.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Auto-classify and route inbound messages.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Auto-classify and route inbound messages.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Auto-classify and route inbound messages.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Auto-classify and route inbound messages.)

## Prerequisites

- Integration: **slack** (blocking)
