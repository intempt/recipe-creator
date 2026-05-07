---
name: Revenue Forecasting
description: Weighted pipeline, commit categories, forecast vs actual variance.
intempt:
  id: revenue-forecasting
  version: 1.0.0
  slashCommand: /revenue-forecasting
  shortDescription: Weighted pipeline, commit categories, forecast vs actual variance.
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
    - revenue-forecasting
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
    describe: Define forecast categories (Best Case, Commit, Most Likely) and the criteria for each per deal stage.
    produces: deal
  - id: build-rollup-workflow
    describe: Create a workflow that recalculates weighted pipeline weekly based on stage probability and forecast category.
    produces: workflow
  - id: build-forecast-dashboard
    describe: Compose a dashboard showing weighted pipeline by category, week-over-week change, and forecast vs actual variance.
    produces: dashboard
---

# Revenue Forecasting

Weighted pipeline, commit categories, forecast vs actual variance.

## Outputs

- **deal** (deal): Deal produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define forecast categories (Best Case, Commit, Most Likely) and the criteria for each per deal stage.
2. Create a workflow that recalculates weighted pipeline weekly based on stage probability and forecast category.
3. Compose a dashboard showing weighted pipeline by category, week-over-week change, and forecast vs actual variance.
