---
name: Outbound Cold Sequence Multi Touch
description: 4-5 touch outbound cold email sequence with progressive value-add. Built around the SMB 4-email cadence and designed
  to work alongside LinkedIn touches by the SDR.
intempt:
  id: outbound-cold-sequence-multi-touch
  version: 1.0.0
  slashCommand: /outbound-cold-sequence-multi-touch
  shortDescription: 4-5 touch outbound cold email sequence with progressive value-add. Built around the SMB 4-email cadence
    and designed to work alongside LinkedIn touches by the SDR.
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
    - outbound
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Outbound
      cold sequence — multi-touch.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Outbound cold sequence — multi-touch.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Outbound cold sequence
      — multi-touch.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Outbound cold sequence — multi-touch.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: linkedin
      severity: blocking
---

# Outbound Cold Sequence Multi Touch

4-5 touch outbound cold email sequence with progressive value-add. Built around the SMB 4-email cadence and designed to work alongside LinkedIn touches by the SDR.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Outbound cold sequence — multi-touch.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Outbound cold sequence — multi-touch.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Outbound cold sequence — multi-touch.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Outbound cold sequence — multi-touch.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **linkedin** (blocking)
