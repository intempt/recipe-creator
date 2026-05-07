---
name: Proposal Stage Deal 24hr To 14 Day Follow Up
description: 'Post-proposal follow-up starting within 24 hours of send (research: 24hr window most predictive of win rate).
  Addresses legal/security/procurement objections and provides champion enablement.'
intempt:
  id: proposal-stage-deal-24hr-to-14-day-follow-up
  version: 1.0.1
  slashCommand: /proposal-stage-deal-24hr-to-14-day-follow-up
  shortDescription: 'Post-proposal follow-up starting within 24 hours of send (research: 24hr window most predictive of win
    rate). Addresses legal/security/procurement objections and provides champion enablement.'
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
    - proposal
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
      for: Proposal-stage deal — 24hr to 14-day follow-up.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Proposal-stage deal — 24hr to 14-day follow-up.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Proposal-stage
      deal — 24hr to 14-day follow-up.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Proposal-stage
      deal — 24hr to 14-day follow-up.)'
    produces: account
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: salesforce
      severity: blocking
---

# Proposal Stage Deal 24hr To 14 Day Follow Up

Post-proposal follow-up starting within 24 hours of send (research: 24hr window most predictive of win rate). Addresses legal/security/procurement objections and provides champion enablement.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Proposal-stage deal — 24hr to 14-day follow-up.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Proposal-stage deal — 24hr to 14-day follow-up.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Proposal-stage deal — 24hr to 14-day follow-up.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Proposal-stage deal — 24hr to 14-day follow-up.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **salesforce** (blocking)
