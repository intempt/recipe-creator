---
name: Account Health Score Daily Recalculation
description: Daily composite health-score calculation across usage, engagement, and support signals. Flags at-risk accounts
  for CSM intervention before they churn.
intempt:
  id: account-health-score-daily-recalculation
  version: 1.0.1
  slashCommand: /account-health-score-daily-recalculation
  shortDescription: Daily composite health-score calculation across usage, engagement, and support signals. Flags at-risk
    accounts for CSM intervention before they churn.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - b2b
    complexity: standard
    executionMode: scheduled
    tags:
    - revenue-operations
    - account
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: event_mapping
    type: event-mapping
    description: Event Mapping produced by this recipe.
  - name: report
    type: report
    description: Report produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: map-event-taxonomy
    describe: 'Map source events from connected integrations to the canonical event taxonomy with proper attributes. (Tailored
      for: Account health score — daily recalculation.)'
    produces: event_mapping
  - id: build-core-reports
    describe: 'Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis),
      Paths (user flows). (Tailored for: Account health score — daily recalculation.)'
    produces: report
  - id: compose-exec-dashboard
    describe: 'Compose an executive dashboard surfacing headline metrics with comparisons and trends. (Tailored for: Account
      health score — daily recalculation.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Account Health Score Daily Recalculation

Daily composite health-score calculation across usage, engagement, and support signals. Flags at-risk accounts for CSM intervention before they churn.

## Outputs

- **event_mapping** (event-mapping): Event Mapping produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Map source events from connected integrations to the canonical event taxonomy with proper attributes. (Tailored for: Account health score — daily recalculation.)
2. Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis), Paths (user flows). (Tailored for: Account health score — daily recalculation.)
3. Compose an executive dashboard surfacing headline metrics with comparisons and trends. (Tailored for: Account health score — daily recalculation.)

## Prerequisites

- Integration: **slack** (blocking)
