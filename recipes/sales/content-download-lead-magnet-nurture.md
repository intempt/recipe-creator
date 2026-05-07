---
name: Content Download Lead Magnet Nurture
description: 4-email educational drip triggered by ebook/whitepaper/gated-content download. Positions your solution against
  the problem the asset addresses without feeling salesy.
intempt:
  id: content-download-lead-magnet-nurture
  version: 1.0.0
  slashCommand: /content-download-lead-magnet-nurture
  shortDescription: 4-email educational drip triggered by ebook/whitepaper/gated-content download. Positions your solution
    against the problem the asset addresses without feeling salesy.
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
    - content
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Content
      download / lead magnet nurture.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Content download / lead magnet nurture.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Content download /
      lead magnet nurture.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Content download / lead magnet nurture.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
---

# Content Download Lead Magnet Nurture

4-email educational drip triggered by ebook/whitepaper/gated-content download. Positions your solution against the problem the asset addresses without feeling salesy.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Content download / lead magnet nurture.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Content download / lead magnet nurture.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Content download / lead magnet nurture.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Content download / lead magnet nurture.)

## Prerequisites

- Integration: **hubspot** (blocking)
