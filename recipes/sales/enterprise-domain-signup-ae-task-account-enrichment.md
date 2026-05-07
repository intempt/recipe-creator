---
name: Enterprise Domain Signup Ae Task Account Enrichment
description: Short-circuit nurture for signups from enterprise-eligible domains with instant enrichment and AE handoff.
intempt:
  id: enterprise-domain-signup-ae-task-account-enrichment
  version: 1.0.1
  slashCommand: /enterprise-domain-signup-ae-task-account-enrichment
  shortDescription: Short-circuit nurture for signups from enterprise-eligible domains with instant enrichment and AE handoff.
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
    - enterprise
    - sales-automation
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
      for: Enterprise-domain signup → AE task + account enrichment.)'
    produces: deal
  - id: create-followup-tasks
    describe: 'Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored
      for: Enterprise-domain signup → AE task + account enrichment.)'
    produces: task
  - id: schedule-prep-meetings
    describe: 'Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Enterprise-domain
      signup → AE task + account enrichment.)'
    produces: meeting
  - id: update-account-rollups
    describe: 'Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Enterprise-domain
      signup → AE task + account enrichment.)'
    produces: account
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Enterprise Domain Signup Ae Task Account Enrichment

Short-circuit nurture for signups from enterprise-eligible domains with instant enrichment and AE handoff.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **account** (account): Account produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Review each deal's health: last touch date, stakeholder engagement, time-in-stage, risk signals. (Tailored for: Enterprise-domain signup → AE task + account enrichment.)
2. Create follow-up tasks for at-risk deals or stale stakeholders, assigned to the deal owner with context. (Tailored for: Enterprise-domain signup → AE task + account enrichment.)
3. Schedule meeting-prep time before key calls (demo, proposal review, executive briefing). (Tailored for: Enterprise-domain signup → AE task + account enrichment.)
4. Update account-level metrics: total pipeline, last-engaged date, multi-thread depth. (Tailored for: Enterprise-domain signup → AE task + account enrichment.)

## Prerequisites

- Integration: **slack** (blocking)
