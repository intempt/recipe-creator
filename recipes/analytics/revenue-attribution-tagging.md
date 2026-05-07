---
name: Revenue Attribution Tagging
description: Tag the first revenue event with the originating journey, campaign, and acquisition source. Enables accurate
  journey-level ROI reporting.
intempt:
  id: revenue-attribution-tagging
  version: 1.0.1
  slashCommand: /revenue-attribution-tagging
  shortDescription: Tag the first revenue event with the originating journey, campaign, and acquisition source. Enables accurate
    journey-level ROI reporting.
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
    - revenue
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
      for: Revenue attribution tagging.)'
    produces: event_mapping
  - id: build-core-reports
    describe: 'Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis),
      Paths (user flows). (Tailored for: Revenue attribution tagging.)'
    produces: report
  - id: compose-exec-dashboard
    describe: 'Compose an executive dashboard surfacing headline metrics with comparisons and trends. (Tailored for: Revenue
      attribution tagging.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: stripe
      severity: blocking
---

# Revenue Attribution Tagging

Tag the first revenue event with the originating journey, campaign, and acquisition source. Enables accurate journey-level ROI reporting.

## Outputs

- **event_mapping** (event-mapping): Event Mapping produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Map source events from connected integrations to the canonical event taxonomy with proper attributes. (Tailored for: Revenue attribution tagging.)
2. Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis), Paths (user flows). (Tailored for: Revenue attribution tagging.)
3. Compose an executive dashboard surfacing headline metrics with comparisons and trends. (Tailored for: Revenue attribution tagging.)

## Prerequisites

- Integration: **stripe** (blocking)
