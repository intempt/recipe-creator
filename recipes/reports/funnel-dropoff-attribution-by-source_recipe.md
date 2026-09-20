---
name: funnel-dropoff-attribution-by-source
description: |
  Use when a user mentions "funnel drop-off attribution by source", or asks for related help. Same funnel run separately by Users.utm_source: surfaces which acquisition channels actually convert.
arguments: []
intempt:
  id: funnel-dropoff-attribution-by-source
  version: 1.0.0
  slashCommand: /funnel-dropoff-attribution-by-source
  group: Reports
  title: "Funnel drop off by source"
  shortDescription: "Runs the same acquisition to retention funnel separately for each traffic source, so you can see which channels bring people who actually stick."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [all]
    complexity: quick
    executionMode: live
    tags: [funnel]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_funnel_report
  procedure:
    - step: 1
      title: "Run one funnel per source"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "A configurable funnel from signup to activation, conversion and a return visit 30 days later, inside a 60 day window, drawn as one small funnel per source for the top 8 sources, with a summary table of volume, end to end conversion and revenue."
      prompt: |
        Create a Funnel report called "Funnel Drop-off by Acquisition Source".

        This is a configurable funnel: the user specifies which canonical events make up the funnel. Defaults if unspecified:

        1. Event "user_created": "Acquired"
        2. Event "goal_completed_in_journey" (configurable journey_id): "Activated"
        3. Event "subscription_created" (saas) OR "order_created" (ecommerce): "Converted"
        4. Event "session_start" with date 30+ days after the conversion event: "Retained 30 days"

        Conversion window: 60 days
        Breakdown: By Users.utm_source (top 8 sources by Step 1 volume)
        Compare: Previous period (prior 60 days)

        Render as small-multiples: one funnel per source, sorted by end-to-end conversion rate descending.

        Also include a summary table:
        - Source · Volume at Step 1 · End-to-end conversion % · Volume at final step · Per-source revenue (sum of subscription_created.amount or order_created.total_price for users who reached Step 3+)

        Annotations:
        - Flag the source with highest end-to-end conversion AND volume above the 33rd percentile.
        - Flag any source where Step 1 to 2 conversion is below 50% of the average across sources (lead-quality issue).
        - Flag any source where Step 3 to 4 conversion is below average (conversion fine but customers don't retain).
        - Highlight the largest gap between sources at any single step.

        Surface the actual revenue-weighted ROI per source.

        Taxonomy notes:
        - All steps reference canonical events. Users.utm_source is a real first-touch attribution attribute.
        - Note: this recipe does NOT compute CAC because ad-spend is not in the canonical taxonomy. Per-source revenue is the closest proxy.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Funnel drop off by source

Runs the same acquisition to retention funnel separately for each traffic source, so you can see which channels bring people who actually stick.

## What it does

1. **Run one funnel per source** (`build_funnel_report`)

   A configurable funnel from signup to activation, conversion and a return visit 30 days later, inside a 60 day window, drawn as one small funnel per source for the top 8 sources, with a summary table of volume, end to end conversion and revenue.

## What you end up with

- **report** (report): Report produced by this recipe.
