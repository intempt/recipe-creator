---
name: browse-to-buy-retention
description: |
  Use when a user mentions "browse-to-buy retention", or asks for related help. First-visit-to-purchase retention with W1/W4/W12 benchmarks and channel-source comparison.
arguments: []
intempt:
  id: browse-to-buy-retention
  version: 1.0.0
  slashCommand: /browse-to-buy-retention
  group: Reports
  title: "Browse to buy retention"
  shortDescription: "Measures how long first time visitors take to place an order, by acquisition source, so you can tell fast converting channels from slow ones."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: quick
    executionMode: live
    tags: [retention]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_retention_report
  procedure:
    - step: 1
      title: "Track first visit to first order"
      command: build_retention_report
      produces: report
      bindsAs: report
      description: "Weekly cohorts anchored on a visitor's first session, measuring who places an order in weeks 1, 2, 4, 8 and 12, split by the top 6 traffic sources. Flags any source still under 8% at week 12."
      prompt: |
        Create a Retention report called "Browse to Buy Retention".

        Anchor event: Session start (each user's first Session start)
        Return event: Placed order
        Cohort granularity: Weekly
        Time range: Last 12 weeks
        Breakdown: By UTM source (top 6 sources)
        Compare: Previous period (prior 12 weeks of cohorts)
        Chart type: Retention curve plus cohort table with W1 / W2 / W4 / W8 / W12 columns

        Annotations:
        - Add benchmarks: W1 first-purchase rate of 5% is typical for considered-purchase DTC, 10%+ for impulse-buy.
        - Flag any source where W12 first-purchase rate is below 8% (browse-to-buy gap).
        - Highlight the source with the fastest first-purchase rate (steepest W1 conversion).
        - Highlight the source with the highest W12 conversion (best overall, even if slower).

        Surface which sources produce "fast converters" vs "slow converters."
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Browse to buy retention

Measures how long first time visitors take to place an order, by acquisition source, so you can tell fast converting channels from slow ones.

## What it does

1. **Track first visit to first order** (`build_retention_report`)

   Weekly cohorts anchored on a visitor's first session, measuring who places an order in weeks 1, 2, 4, 8 and 12, split by the top 6 traffic sources. Flags any source still under 8% at week 12.

## What you end up with

- **report** (report): Report produced by this recipe.
