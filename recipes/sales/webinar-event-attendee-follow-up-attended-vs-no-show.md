---
name: Webinar Event Attendee Follow Up Attended Vs No Show
description: 4-6 touch follow-up branched by attendance — attendees get demo-request CTAs, no-shows get the replay + re-engagement.
  Replaces single-email thank-you templates.
intempt:
  id: webinar-event-attendee-follow-up-attended-vs-no-show
  version: 1.0.0
  slashCommand: /webinar-event-attendee-follow-up-attended-vs-no-show
  shortDescription: 4-6 touch follow-up branched by attendance — attendees get demo-request CTAs, no-shows get the replay
    + re-engagement. Replaces single-email thank-you templates.
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
    - webinar
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
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Webinar
      / event attendee follow-up — attended vs no-show.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Webinar / event attendee follow-up — attended vs no-show.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Webinar / event attendee
      follow-up — attended vs no-show.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Webinar / event attendee follow-up — attended vs no-show.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: zoom
      severity: blocking
    - value: hubspot
      severity: blocking
---

# Webinar Event Attendee Follow Up Attended Vs No Show

4-6 touch follow-up branched by attendance — attendees get demo-request CTAs, no-shows get the replay + re-engagement. Replaces single-email thank-you templates.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Webinar / event attendee follow-up — attended vs no-show.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Webinar / event attendee follow-up — attended vs no-show.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Webinar / event attendee follow-up — attended vs no-show.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Webinar / event attendee follow-up — attended vs no-show.)

## Prerequisites

- Integration: **zoom** (blocking)
- Integration: **hubspot** (blocking)
