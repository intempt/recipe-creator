---
name: Post Meeting Ai Summary And Action Items
description: After a meeting, automatically generate a summary, extract action items, and create follow-up tasks.
intempt:
  id: post-meeting-ai-summary-and-action-items
  version: 1.0.1
  slashCommand: /post-meeting-ai-summary-and-action-items
  shortDescription: After a meeting, automatically generate a summary, extract action items, and create follow-up tasks.
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
    - ai-powered-meeting-workflows
    - post
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
      for: Post-meeting AI summary and action items.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Post-meeting AI summary and action items.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Post-meeting
      AI summary and action items.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Post-meeting
      AI summary and action items.)'
    produces: account
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Post Meeting Ai Summary And Action Items

After a meeting, automatically generate a summary, extract action items, and create follow-up tasks.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Post-meeting AI summary and action items.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Post-meeting AI summary and action items.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Post-meeting AI summary and action items.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Post-meeting AI summary and action items.)

## Prerequisites

- Integration: **slack** (blocking)
