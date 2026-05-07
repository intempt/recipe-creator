---
name: Route New Inbound Lead To The Right Rep
description: Generic inbound lead routing based on territory, company size, and round-robin. Fallback for any inbound signup
  that doesn't hit a more specific trigger (demo request, enterprise signup...
intempt:
  id: route-new-inbound-lead-to-the-right-rep
  version: 1.0.0
  slashCommand: /route-new-inbound-lead-to-the-right-rep
  shortDescription: Generic inbound lead routing based on territory, company size, and round-robin. Fallback for any inbound
    signup that doesn't hit a more specific trigger (demo request, enterprise signup...
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
    - route
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Route new
      inbound lead to the right rep.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Route new inbound lead to the right rep.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Route new inbound lead
      to the right rep.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Route new inbound lead to the right rep.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: slack
      severity: blocking
---

# Route New Inbound Lead To The Right Rep

Generic inbound lead routing based on territory, company size, and round-robin. Fallback for any inbound signup that doesn't hit a more specific trigger (demo request, enterprise signup...

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Route new inbound lead to the right rep.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Route new inbound lead to the right rep.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Route new inbound lead to the right rep.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Route new inbound lead to the right rep.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **slack** (blocking)
