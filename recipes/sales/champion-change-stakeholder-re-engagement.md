---
name: Champion Change Stakeholder Re Engagement
description: Fires when the deal champion leaves their company or changes role. Kicks off re-discovery outreach to remaining
  stakeholders to preserve the deal — most deals die on champion change without...
intempt:
  id: champion-change-stakeholder-re-engagement
  version: 1.0.1
  slashCommand: /champion-change-stakeholder-re-engagement
  shortDescription: Fires when the deal champion leaves their company or changes role. Kicks off re-discovery outreach to
    remaining stakeholders to preserve the deal — most deals die on champion change without...
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
      for: Champion change — stakeholder re-engagement.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Champion change — stakeholder re-engagement.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Champion
      change — stakeholder re-engagement.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Champion
      change — stakeholder re-engagement.)'
    produces: account
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: linkedin
      severity: blocking
---

# Champion Change Stakeholder Re Engagement

Fires when the deal champion leaves their company or changes role. Kicks off re-discovery outreach to remaining stakeholders to preserve the deal — most deals die on champion change without...

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Champion change — stakeholder re-engagement.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Champion change — stakeholder re-engagement.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Champion change — stakeholder re-engagement.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Champion change — stakeholder re-engagement.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **linkedin** (blocking)
