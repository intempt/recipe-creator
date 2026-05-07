---
name: Sales Pipeline
description: Stages, auto-transitions, stale detection, and won/lost handling.
intempt:
  id: sales-pipeline
  version: 1.0.0
  slashCommand: /sales-pipeline
  shortDescription: Stages, auto-transitions, stale detection, and won/lost handling.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: revops-automator
    mode:
    - b2b
    complexity: advanced
    executionMode: live
    tags:
    - sales-pipeline
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: deal
    type: deal
    description: Deal produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  - name: task
    type: task
    description: Task produced by this recipe.
  - name: account
    type: account
    description: Account produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: define-deal-stages
    describe: Define deal stage taxonomy with entry criteria and exit definitions per stage.
    produces: deal
  - id: build-transition-workflow
    describe: Create a workflow that auto-transitions deals based on activity signals (meeting booked, proposal sent, contract
      signed).
    produces: workflow
  - id: build-stale-detection-tasks
    describe: Create tasks for deals stuck in stage beyond expected duration, assigned to the deal owner.
    produces: task
  - id: build-account-link
    describe: Link deals to parent accounts and roll up account-level metrics (deal count, pipeline value).
    produces: account
  - id: build-pipeline-dashboard
    describe: Compose a dashboard showing pipeline value by stage, velocity, win rate, and forecast vs commit.
    produces: dashboard
---

# Sales Pipeline

Stages, auto-transitions, stale detection, and won/lost handling.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **task** (task): Task produced by this recipe.
- **account** (account): Account produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define deal stage taxonomy with entry criteria and exit definitions per stage.
2. Create a workflow that auto-transitions deals based on activity signals (meeting booked, proposal sent, contract signed).
3. Create tasks for deals stuck in stage beyond expected duration, assigned to the deal owner.
4. Link deals to parent accounts and roll up account-level metrics (deal count, pipeline value).
5. Compose a dashboard showing pipeline value by stage, velocity, win rate, and forecast vs commit.
