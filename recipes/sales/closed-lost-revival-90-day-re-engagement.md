---
name: Closed Lost Revival 90 Day Re Engagement
description: 90-day post-loss re-engagement. Catches prospects whose timing/budget/champion situation may have changed. Product
  updates + soft re-opener.
intempt:
  id: closed-lost-revival-90-day-re-engagement
  version: 1.0.1
  slashCommand: /closed-lost-revival-90-day-re-engagement
  shortDescription: 90-day post-loss re-engagement. Catches prospects whose timing/budget/champion situation may have changed.
    Product updates + soft re-opener.
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
    - customer-success-and-renewal
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
      for: Closed-lost revival — 90-day re-engagement.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Closed-lost revival — 90-day re-engagement.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Closed-lost
      revival — 90-day re-engagement.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Closed-lost
      revival — 90-day re-engagement.)'
    produces: account
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: salesforce
      severity: blocking
---

# Closed Lost Revival 90 Day Re Engagement

90-day post-loss re-engagement. Catches prospects whose timing/budget/champion situation may have changed. Product updates + soft re-opener.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Closed-lost revival — 90-day re-engagement.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Closed-lost revival — 90-day re-engagement.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Closed-lost revival — 90-day re-engagement.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Closed-lost revival — 90-day re-engagement.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **salesforce** (blocking)
