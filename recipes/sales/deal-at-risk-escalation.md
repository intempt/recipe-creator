---
name: Deal At Risk Escalation
description: Fires on deal stagnation signals — no activity for X days, champion silence, reduced engagement. Escalates to
  AE action while the deal is still salvageable.
intempt:
  id: deal-at-risk-escalation
  version: 1.0.1
  slashCommand: /deal-at-risk-escalation
  shortDescription: Fires on deal stagnation signals — no activity for X days, champion silence, reduced engagement. Escalates
    to AE action while the deal is still salvageable.
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
    - deal
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
      for: Deal at risk escalation.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Deal at risk escalation.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Deal
      at risk escalation.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Deal at
      risk escalation.)'
    produces: account
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: salesforce
      severity: blocking
---

# Deal At Risk Escalation

Fires on deal stagnation signals — no activity for X days, champion silence, reduced engagement. Escalates to AE action while the deal is still salvageable.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Deal at risk escalation.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Deal at risk escalation.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Deal at risk escalation.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Deal at risk escalation.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **salesforce** (blocking)
