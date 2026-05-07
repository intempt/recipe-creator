---
name: Target Account Added To Abm List Enrichment Kickoff
description: Onboard every new ABM target account with a deep briefing so AE/SDR can work it from day one.
intempt:
  id: target-account-added-to-abm-list-enrichment-kickoff
  version: 1.0.1
  slashCommand: /target-account-added-to-abm-list-enrichment-kickoff
  shortDescription: Onboard every new ABM target account with a deep briefing so AE/SDR can work it from day one.
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
    - target
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
      news). (Tailored for: Target account added to ABM list → enrichment + kickoff.)'
    produces: attribute
  - id: update-account
    describe: 'Update the account record with research findings, stakeholder map, and engagement summary. (Tailored for: Target
      account added to ABM list → enrichment + kickoff.)'
    produces: account
  - id: create-coverage-tasks
    describe: 'Create tasks for the AE to engage missing stakeholders or under-engaged decision-makers. (Tailored for: Target
      account added to ABM list → enrichment + kickoff.)'
    produces: task
  - id: build-coverage-dashboard
    describe: 'Compose a dashboard showing buying-committee coverage, stakeholder engagement depth, and risk indicators. (Tailored
      for: Target account added to ABM list → enrichment + kickoff.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Target Account Added To Abm List Enrichment Kickoff

Onboard every new ABM target account with a deep briefing so AE/SDR can work it from day one.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **account** (account): Account produced by this recipe.
- **task** (task): Task produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Research the account's stakeholders: roles, decision-influence, engagement history, recent changes (LinkedIn, news). (Tailored for: Target account added to ABM list → enrichment + kickoff.)
2. Update the account record with research findings, stakeholder map, and engagement summary. (Tailored for: Target account added to ABM list → enrichment + kickoff.)
3. Create tasks for the AE to engage missing stakeholders or under-engaged decision-makers. (Tailored for: Target account added to ABM list → enrichment + kickoff.)
4. Compose a dashboard showing buying-committee coverage, stakeholder engagement depth, and risk indicators. (Tailored for: Target account added to ABM list → enrichment + kickoff.)

## Prerequisites

- Integration: **slack** (blocking)
