---
name: Deal Management
description: Health review, follow-ups, meeting prep, and forecast input.
intempt:
  id: deal-management
  version: 1.0.1
  slashCommand: /deal-management
  shortDescription: Health review, follow-ups, meeting prep, and forecast input.
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
    - deal-management
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
    describe: 'Review each deal''s health: last touch date, stakeholder engagement, time-in-stage, risk signals.'
    produces: deal
  - id: create-followup-tasks
    describe: Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context.
    produces: task
  - id: schedule-prep-meetings
    describe: Schedule meeting-prep time before key calls (demo, proposal review, executive briefing).
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth.'
    produces: account
---

# Deal Management

Health review, follow-ups, meeting prep, and forecast input.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals.
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context.
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing).
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth.
