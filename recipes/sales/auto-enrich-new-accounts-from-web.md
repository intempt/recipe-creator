---
name: Auto Enrich New Accounts From Web
description: Run AI research and firmographic enrichment on every newly-created account so the AE/SDR sees a complete briefing
  the first time they open it.
intempt:
  id: auto-enrich-new-accounts-from-web
  version: 1.0.1
  slashCommand: /auto-enrich-new-accounts-from-web
  shortDescription: Run AI research and firmographic enrichment on every newly-created account so the AE/SDR sees a complete
    briefing the first time they open it.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: account-researcher
    mode:
    - b2b
    complexity: standard
    executionMode: scheduled
    tags:
    - sales-automation
    - auto
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: attribute
    type: attribute
    description: Attribute produced by this recipe.
  - name: account
    type: account
    description: Account produced by this recipe.
  - name: task
    type: task
    description: Task produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: research-stakeholders
    describe: 'Research the account''s stakeholders: roles, decision-influence, engagement history, recent changes (LinkedIn,
      news). (Tailored for: Auto-enrich new accounts from web.)'
    produces: attribute
  - id: update-account
    describe: 'Update the account record with research findings, stakeholder map, and engagement summary. (Tailored for: Auto-enrich
      new accounts from web.)'
    produces: account
  - id: create-coverage-tasks
    describe: 'Create tasks for the AE to engage missing stakeholders or under-engaged decision-makers. (Tailored for: Auto-enrich
      new accounts from web.)'
    produces: task
  - id: build-coverage-dashboard
    describe: 'Compose a dashboard showing buying-committee coverage, stakeholder engagement depth, and risk indicators. (Tailored
      for: Auto-enrich new accounts from web.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
---

# Auto Enrich New Accounts From Web

Run AI research and firmographic enrichment on every newly-created account so the AE/SDR sees a complete briefing the first time they open it.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **account** (account): Account produced by this recipe.
- **task** (task): Task produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Research the account's stakeholders: roles, decision-influence, engagement history, recent changes (LinkedIn, news). (Tailored for: Auto-enrich new accounts from web.)
2. Update the account record with research findings, stakeholder map, and engagement summary. (Tailored for: Auto-enrich new accounts from web.)
3. Create tasks for the AE to engage missing stakeholders or under-engaged decision-makers. (Tailored for: Auto-enrich new accounts from web.)
4. Compose a dashboard showing buying-committee coverage, stakeholder engagement depth, and risk indicators. (Tailored for: Auto-enrich new accounts from web.)

## Prerequisites

- Integration: **hubspot** (blocking)
