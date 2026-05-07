---
name: Rfm Score Recalculation Weekly
description: Weekly batch recalculation of Recency/Frequency/Monetary scores for all active users — keeps RFM-driven segmentation
  fresh for downstream journeys and campaigns.
intempt:
  id: rfm-score-recalculation-weekly
  version: 1.0.1
  slashCommand: /rfm-score-recalculation-weekly
  shortDescription: Weekly batch recalculation of Recency/Frequency/Monetary scores for all active users — keeps RFM-driven
    segmentation fresh for downstream journeys and campaigns.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - ecommerce
    complexity: standard
    executionMode: scheduled
    tags:
    - revenue-operations
    - rfm
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
      for: RFM score recalculation — weekly.)'
    produces: event_mapping
  - id: build-core-reports
    describe: 'Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis),
      Paths (user flows). (Tailored for: RFM score recalculation — weekly.)'
    produces: report
  - id: compose-exec-dashboard
    describe: 'Compose an executive dashboard surfacing headline metrics with comparisons and trends. (Tailored for: RFM score
      recalculation — weekly.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: shopify
      severity: blocking
---

# Rfm Score Recalculation Weekly

Weekly batch recalculation of Recency/Frequency/Monetary scores for all active users — keeps RFM-driven segmentation fresh for downstream journeys and campaigns.

## Outputs

- **event_mapping** (event-mapping): Event Mapping produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Map source events from connected integrations to the canonical event taxonomy with proper attributes. (Tailored for: RFM score recalculation — weekly.)
2. Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis), Paths (user flows). (Tailored for: RFM score recalculation — weekly.)
3. Compose an executive dashboard surfacing headline metrics with comparisons and trends. (Tailored for: RFM score recalculation — weekly.)

## Prerequisites

- Integration: **shopify** (blocking)
