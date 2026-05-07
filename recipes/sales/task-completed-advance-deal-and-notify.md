---
name: Task Completed Advance Deal And Notify
description: When a rep marks a key task complete, automatically advance the deal stage and create the next step.
intempt:
  id: task-completed-advance-deal-and-notify
  version: 1.0.1
  slashCommand: /task-completed-advance-deal-and-notify
  shortDescription: When a rep marks a key task complete, automatically advance the deal stage and create the next step.
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
    - sdr-and-ae-task-automation
    - task
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
      for: Task completed — advance deal and notify.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Task completed — advance deal and notify.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Task
      completed — advance deal and notify.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Task completed
      — advance deal and notify.)'
    produces: account
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: slack
      severity: blocking
---

# Task Completed Advance Deal And Notify

When a rep marks a key task complete, automatically advance the deal stage and create the next step.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Task completed — advance deal and notify.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Task completed — advance deal and notify.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Task completed — advance deal and notify.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Task completed — advance deal and notify.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **slack** (blocking)
