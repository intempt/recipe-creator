---
name: Champion Change Detection New Senior Stakeholder On
description: Spot the most expansion-relevant moment in a customer account — a new senior stakeholder arriving.
intempt:
  id: champion-change-detection-new-senior-stakeholder-on
  version: 1.0.1
  slashCommand: /champion-change-detection-new-senior-stakeholder-on
  shortDescription: Spot the most expansion-relevant moment in a customer account — a new senior stakeholder arriving.
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
    - revenue-operations
    - champion
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
      for: Champion change detection — new senior stakeholder on.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Champion change detection — new senior stakeholder on.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Champion
      change detection — new senior stakeholder on.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Champion
      change detection — new senior stakeholder on.)'
    produces: account
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Champion Change Detection New Senior Stakeholder On

Spot the most expansion-relevant moment in a customer account — a new senior stakeholder arriving.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Champion change detection — new senior stakeholder on.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Champion change detection — new senior stakeholder on.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Champion change detection — new senior stakeholder on.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Champion change detection — new senior stakeholder on.)

## Prerequisites

- Integration: **slack** (blocking)
