---
name: Forecast Rollup Weekly Pipeline Snapshot
description: Weekly pipeline snapshot for sales leadership with stage distribution, weighted forecast, at-risk deals flagged,
  and week-over-week movement.
intempt:
  id: forecast-rollup-weekly-pipeline-snapshot
  version: 1.0.0
  slashCommand: /forecast-rollup-weekly-pipeline-snapshot
  shortDescription: Weekly pipeline snapshot for sales leadership with stage distribution, weighted forecast, at-risk deals
    flagged, and week-over-week movement.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: revops-automator
    mode:
    - b2b
    complexity: standard
    executionMode: live
    tags:
    - sales-automation
    - forecast
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
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: define-forecast-categories
    describe: 'Define forecast categories (Best Case, Commit, Most Likely) and the criteria for each per deal stage. (Tailored
      for: Forecast rollup — weekly pipeline snapshot.)'
    produces: deal
  - id: build-rollup-workflow
    describe: 'Create a workflow that recalculates weighted pipeline weekly based on stage probability and forecast category.
      (Tailored for: Forecast rollup — weekly pipeline snapshot.)'
    produces: workflow
  - id: build-forecast-dashboard
    describe: 'Compose a dashboard showing weighted pipeline by category, week-over-week change, and forecast vs actual variance.
      (Tailored for: Forecast rollup — weekly pipeline snapshot.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Forecast Rollup Weekly Pipeline Snapshot

Weekly pipeline snapshot for sales leadership with stage distribution, weighted forecast, at-risk deals flagged, and week-over-week movement.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define forecast categories (Best Case, Commit, Most Likely) and the criteria for each per deal stage. (Tailored for: Forecast rollup — weekly pipeline snapshot.)
2. Create a workflow that recalculates weighted pipeline weekly based on stage probability and forecast category. (Tailored for: Forecast rollup — weekly pipeline snapshot.)
3. Compose a dashboard showing weighted pipeline by category, week-over-week change, and forecast vs actual variance. (Tailored for: Forecast rollup — weekly pipeline snapshot.)

## Prerequisites

- Integration: **slack** (blocking)
