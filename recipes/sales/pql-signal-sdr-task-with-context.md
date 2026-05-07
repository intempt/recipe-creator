---
name: Pql Signal Sdr Task With Context
description: Route product-qualified leads to SDRs in real time when their purchase intent jumps.
intempt:
  id: pql-signal-sdr-task-with-context
  version: 1.0.1
  slashCommand: /pql-signal-sdr-task-with-context
  shortDescription: Route product-qualified leads to SDRs in real time when their purchase intent jumps.
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
    - sdr-and-ae-task-automation
    - pql
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
      for: PQL signal → SDR task with context.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: PQL signal → SDR task with context.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: PQL
      signal → SDR task with context.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: PQL signal
      → SDR task with context.)'
    produces: account
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Pql Signal Sdr Task With Context

Route product-qualified leads to SDRs in real time when their purchase intent jumps.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: PQL signal → SDR task with context.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: PQL signal → SDR task with context.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: PQL signal → SDR task with context.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: PQL signal → SDR task with context.)

## Prerequisites

- Integration: **slack** (blocking)
