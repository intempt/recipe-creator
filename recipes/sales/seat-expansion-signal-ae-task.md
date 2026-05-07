---
name: Seat Expansion Signal Ae Task
description: Surface in-account expansion opportunities when teams start inviting more seats.
intempt:
  id: seat-expansion-signal-ae-task
  version: 1.0.1
  slashCommand: /seat-expansion-signal-ae-task
  shortDescription: Surface in-account expansion opportunities when teams start inviting more seats.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: outreach-rep
    mode:
    - saas
    complexity: standard
    executionMode: oneshot
    tags:
    - sales-automation
    - seat
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
      for: Seat expansion signal → AE task.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Seat expansion signal → AE task.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Seat
      expansion signal → AE task.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Seat expansion
      signal → AE task.)'
    produces: account
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Seat Expansion Signal Ae Task

Surface in-account expansion opportunities when teams start inviting more seats.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Seat expansion signal → AE task.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Seat expansion signal → AE task.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Seat expansion signal → AE task.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Seat expansion signal → AE task.)

## Prerequisites

- Integration: **slack** (blocking)
