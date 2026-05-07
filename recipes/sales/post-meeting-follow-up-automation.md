---
name: Post Meeting Follow Up Automation
description: Immediate post-meeting follow-up — sends recap, action items, and next-step CTA within 1 hour of meeting end.
  Preserves momentum from discovery/demo calls.
intempt:
  id: post-meeting-follow-up-automation
  version: 1.0.1
  slashCommand: /post-meeting-follow-up-automation
  shortDescription: Immediate post-meeting follow-up — sends recap, action items, and next-step CTA within 1 hour of meeting
    end. Preserves momentum from discovery/demo calls.
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
      for: Post-meeting follow-up automation.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Post-meeting follow-up automation.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Post-meeting
      follow-up automation.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Post-meeting
      follow-up automation.)'
    produces: account
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: salesforce
      severity: blocking
---

# Post Meeting Follow Up Automation

Immediate post-meeting follow-up — sends recap, action items, and next-step CTA within 1 hour of meeting end. Preserves momentum from discovery/demo calls.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Post-meeting follow-up automation.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Post-meeting follow-up automation.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Post-meeting follow-up automation.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Post-meeting follow-up automation.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **salesforce** (blocking)
