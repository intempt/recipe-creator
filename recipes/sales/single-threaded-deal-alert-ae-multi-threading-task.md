---
name: Single Threaded Deal Alert Ae Multi Threading Task
description: Flag high-value deals with only one engaged contact so the AE can build the buying committee.
intempt:
  id: single-threaded-deal-alert-ae-multi-threading-task
  version: 1.0.1
  slashCommand: /single-threaded-deal-alert-ae-multi-threading-task
  shortDescription: Flag high-value deals with only one engaged contact so the AE can build the buying committee.
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
    - sales-automation
    - single
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
      for: Single-threaded deal alert — AE multi-threading task.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Single-threaded deal alert — AE multi-threading task.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Single-threaded
      deal alert — AE multi-threading task.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Single-threaded
      deal alert — AE multi-threading task.)'
    produces: account
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Single Threaded Deal Alert Ae Multi Threading Task

Flag high-value deals with only one engaged contact so the AE can build the buying committee.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Single-threaded deal alert — AE multi-threading task.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Single-threaded deal alert — AE multi-threading task.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Single-threaded deal alert — AE multi-threading task.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Single-threaded deal alert — AE multi-threading task.)

## Prerequisites

- Integration: **slack** (blocking)
