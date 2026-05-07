---
name: Post Event Attendee Nurture
description: Generic post-event follow-up for conference/trade-show attendees you met in person. Distinct from webinar follow-up
  — assumes warm in-person connection already established.
intempt:
  id: post-event-attendee-nurture
  version: 1.0.0
  slashCommand: /post-event-attendee-nurture
  shortDescription: Generic post-event follow-up for conference/trade-show attendees you met in person. Distinct from webinar
    follow-up — assumes warm in-person connection already established.
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
    - post
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Post-event
      attendee nurture.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Post-event attendee nurture.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Post-event attendee
      nurture.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Post-event attendee nurture.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
---

# Post Event Attendee Nurture

Generic post-event follow-up for conference/trade-show attendees you met in person. Distinct from webinar follow-up — assumes warm in-person connection already established.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Post-event attendee nurture.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Post-event attendee nurture.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Post-event attendee nurture.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Post-event attendee nurture.)

## Prerequisites

- Integration: **hubspot** (blocking)
