---
name: B2B Nurture
description: Score leads, segment by readiness, route hot leads to sales, nurture the rest.
intempt:
  id: b2b-nurture
  version: 1.0.0
  slashCommand: /b2b-nurture
  shortDescription: Score leads, segment by readiness, route hot leads to sales, nurture the rest.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - b2b
    complexity: advanced
    executionMode: live
    tags:
    - b2b-nurture
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
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: compute-lead-score
    describe: Define a Qualification scoring attribute weighting firmographic fit, intent signals, and engagement depth.
    produces: attribute
  - id: build-routing-workflow
    describe: Create a workflow routing hot leads to sales (assign owner, create task) and adding warm/cold leads to nurture
      journeys.
    produces: workflow
  - id: build-content
    describe: 'Generate nurture content tailored per segment: hot=demo offer, warm=case studies + ROI calc, cold=education
      content.'
    produces: content
  - id: build-journey
    describe: Build per-segment nurture journeys with appropriate cadence and content.
    produces: journey
  - id: build-dashboard
    describe: Compose a dashboard tracking score distribution, hot-lead handoff rate, and nurture-to-MQL conversion.
    produces: dashboard
---

# B2B Nurture

Score leads, segment by readiness, route hot leads to sales, nurture the rest.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification scoring attribute weighting firmographic fit, intent signals, and engagement depth.
2. Create a workflow routing hot leads to sales (assign owner, create task) and adding warm/cold leads to nurture journeys.
3. Generate nurture content tailored per segment: hot=demo offer, warm=case studies + ROI calc, cold=education content.
4. Build per-segment nurture journeys with appropriate cadence and content.
5. Compose a dashboard tracking score distribution, hot-lead handoff rate, and nurture-to-MQL conversion.
