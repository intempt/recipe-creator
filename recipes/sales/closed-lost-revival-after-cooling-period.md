---
name: Closed Lost Revival After Cooling Period
description: Revisit closed-lost deals after enough time has passed for circumstances to change.
intempt:
  id: closed-lost-revival-after-cooling-period
  version: 1.0.1
  slashCommand: /closed-lost-revival-after-cooling-period
  shortDescription: Revisit closed-lost deals after enough time has passed for circumstances to change.
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
    - closed
    - sales-automation
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
      for: Closed-lost revival after cooling period.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Closed-lost revival after cooling period.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Closed-lost
      revival after cooling period.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Closed-lost
      revival after cooling period.)'
    produces: account
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Closed Lost Revival After Cooling Period

Revisit closed-lost deals after enough time has passed for circumstances to change.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Closed-lost revival after cooling period.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Closed-lost revival after cooling period.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Closed-lost revival after cooling period.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Closed-lost revival after cooling period.)

## Prerequisites

- Integration: **slack** (blocking)
