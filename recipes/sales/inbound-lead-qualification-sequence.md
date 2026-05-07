---
name: Inbound Lead Qualification Sequence
description: Routes inbound leads based on ICP fit score and intent — high-fit leads get direct AE outreach, medium-fit get
  SDR nurture, low-fit get self-serve resources. Prevents AE time wasted on bad-fit leads.
intempt:
  id: inbound-lead-qualification-sequence
  version: 1.0.0
  slashCommand: /inbound-lead-qualification-sequence
  shortDescription: Routes inbound leads based on ICP fit score and intent — high-fit leads get direct AE outreach, medium-fit
    get SDR nurture, low-fit get self-serve resources. Prevents AE time wasted on bad-fit leads.
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
    - inbound
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Inbound
      lead qualification sequence.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Inbound lead qualification sequence.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Inbound lead qualification
      sequence.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Inbound lead qualification sequence.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: salesforce
      severity: blocking
---

# Inbound Lead Qualification Sequence

Routes inbound leads based on ICP fit score and intent — high-fit leads get direct AE outreach, medium-fit get SDR nurture, low-fit get self-serve resources. Prevents AE time wasted on bad-fit leads.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Inbound lead qualification sequence.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Inbound lead qualification sequence.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Inbound lead qualification sequence.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Inbound lead qualification sequence.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **salesforce** (blocking)
