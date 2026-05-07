---
name: Account Intelligence
description: Stakeholder mapping, engagement scoring, risk and expansion signals.
intempt:
  id: account-intelligence
  version: 1.0.1
  slashCommand: /account-intelligence
  shortDescription: Stakeholder mapping, engagement scoring, risk and expansion signals.
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
    - account-intelligence
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
      news).'
    produces: attribute
  - id: update-account
    describe: Update the account record with research findings, stakeholder map, and engagement summary.
    produces: account
  - id: create-coverage-tasks
    describe: Create tasks for the AE to engage missing stakeholders or under-engaged decision-makers.
    produces: task
  - id: build-coverage-dashboard
    describe: Compose a dashboard showing buying-committee coverage, stakeholder engagement depth, and risk indicators.
    produces: dashboard
---

# Account Intelligence

Stakeholder mapping, engagement scoring, risk and expansion signals.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **account** (account): Account produced by this recipe.
- **task** (task): Task produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Research the account's stakeholders: roles, decision-influence, engagement history, recent changes (LinkedIn, news).
2. Update the account record with research findings, stakeholder map, and engagement summary.
3. Create tasks for the AE to engage missing stakeholders or under-engaged decision-makers.
4. Compose a dashboard showing buying-committee coverage, stakeholder engagement depth, and risk indicators.
