---
name: Business Review
description: Headline metrics, week-over-week deltas, wins, concerns, recommended actions, scheduled Slack digest.
intempt:
  id: business-review
  version: 1.0.0
  slashCommand: /business-review
  shortDescription: Headline metrics, week-over-week deltas, wins, concerns, recommended actions, scheduled Slack digest.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - all
    complexity: standard
    executionMode: live
    tags:
    - business-review
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  - name: report
    type: report
    description: Report produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: compose-br-dashboard
    describe: Compose a business review dashboard with headline KPIs, WoW deltas, top wins, and top concerns.
    produces: dashboard
  - id: generate-narrative-report
    describe: 'Generate a narrative report summarizing the period: what changed, why, and recommended actions.'
    produces: report
  - id: schedule-digest-workflow
    describe: Create a workflow that delivers the dashboard and narrative as a scheduled Slack digest at the chosen cadence.
    produces: workflow
---

# Business Review

Headline metrics, week-over-week deltas, wins, concerns, recommended actions, scheduled Slack digest.

## Outputs

- **dashboard** (dashboard): Dashboard produced by this recipe.
- **report** (report): Report produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Compose a business review dashboard with headline KPIs, WoW deltas, top wins, and top concerns.
2. Generate a narrative report summarizing the period: what changed, why, and recommended actions.
3. Create a workflow that delivers the dashboard and narrative as a scheduled Slack digest at the chosen cadence.
