---
name: Long Cycle Enterprise Nurture Value First Drip
description: 7-email enterprise nurture (insight → case study → competitor comparison → objection-handler → next step) for
  MQLs who haven't booked a meeting after 30 days. Built for 30-90+ day sales cycles.
intempt:
  id: long-cycle-enterprise-nurture-value-first-drip
  version: 1.0.0
  slashCommand: /long-cycle-enterprise-nurture-value-first-drip
  shortDescription: 7-email enterprise nurture (insight → case study → competitor comparison → objection-handler → next step)
    for MQLs who haven't booked a meeting after 30 days. Built for 30-90+ day sales cycles.
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
    - long
    - lead-qualification-and-outbound
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Long-cycle
      enterprise nurture — value-first drip.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Long-cycle enterprise nurture — value-first drip.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Long-cycle enterprise
      nurture — value-first drip.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Long-cycle enterprise nurture — value-first drip.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: salesforce
      severity: blocking
---

# Long Cycle Enterprise Nurture Value First Drip

7-email enterprise nurture (insight → case study → competitor comparison → objection-handler → next step) for MQLs who haven't booked a meeting after 30 days. Built for 30-90+ day sales cycles.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Long-cycle enterprise nurture — value-first drip.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Long-cycle enterprise nurture — value-first drip.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Long-cycle enterprise nurture — value-first drip.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Long-cycle enterprise nurture — value-first drip.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **salesforce** (blocking)
