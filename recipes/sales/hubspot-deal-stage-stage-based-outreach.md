---
name: Hubspot Deal Stage Stage Based Outreach
description: Generic stage-based outreach automation that fires different emails as deals progress through HubSpot pipeline
  stages. Ensures no deal stage lacks a structured follow-up.
intempt:
  id: hubspot-deal-stage-stage-based-outreach
  version: 1.0.1
  slashCommand: /hubspot-deal-stage-stage-based-outreach
  shortDescription: Generic stage-based outreach automation that fires different emails as deals progress through HubSpot
    pipeline stages. Ensures no deal stage lacks a structured follow-up.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: outreach-rep
    mode:
    - b2b
    complexity: standard
    executionMode: oneshot
    tags:
    - deal-progression
    - hubspot
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: deal
    type: deal
    description: Deal produced by this recipe.
  - name: task
    type: task
    description: Task produced by this recipe.
  - name: meeting
    type: meeting
    description: Meeting produced by this recipe.
  - name: account
    type: account
    description: Account produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: review-deal-health
    describe: 'Review each deal''s health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored
      for: HubSpot deal stage — stage-based outreach.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: HubSpot deal stage — stage-based outreach.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: HubSpot
      deal stage — stage-based outreach.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: HubSpot
      deal stage — stage-based outreach.)'
    produces: account
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
---

# Hubspot Deal Stage Stage Based Outreach

Generic stage-based outreach automation that fires different emails as deals progress through HubSpot pipeline stages. Ensures no deal stage lacks a structured follow-up.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: HubSpot deal stage — stage-based outreach.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: HubSpot deal stage — stage-based outreach.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: HubSpot deal stage — stage-based outreach.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: HubSpot deal stage — stage-based outreach.)

## Prerequisites

- Integration: **hubspot** (blocking)
