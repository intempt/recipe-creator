---
name: Analytics Foundation
description: Map events, build core reports (Insights, Funnels, Retention, Paths), compose executive dashboard.
intempt:
  id: analytics-foundation
  version: 1.0.1
  slashCommand: /analytics-foundation
  shortDescription: Map events, build core reports (Insights, Funnels, Retention, Paths), compose executive dashboard.
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
    executionMode: scheduled
    tags:
    - analytics-foundation
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
    describe: Map source events from connected integrations to the canonical event taxonomy with proper attributes.
    produces: event_mapping
  - id: build-core-reports
    describe: 'Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis),
      Paths (user flows).'
    produces: report
  - id: compose-exec-dashboard
    describe: Compose an executive dashboard surfacing headline metrics with comparisons and trends.
    produces: dashboard
---

# Analytics Foundation

Map events, build core reports (Insights, Funnels, Retention, Paths), compose executive dashboard.

## Outputs

- **event_mapping** (event-mapping): Event Mapping produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Map source events from connected integrations to the canonical event taxonomy with proper attributes.
2. Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis), Paths (user flows).
3. Compose an executive dashboard surfacing headline metrics with comparisons and trends.
