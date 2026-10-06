---
id: browse-to-buy-retention
title: Browse to buy retention
slash_command: /browse-to-buy-retention
group: Reports
owner: intempt
curator: aman
summary: Measures how long first time visitors take to place an order, by acquisition source, so you can
  tell fast converting channels from slow ones.
description: >-
  First-visit-to-purchase retention with W1/W4/W12 benchmarks and channel-source comparison.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  industry:
    - ecommerce
    - media
  vertical: []
  complexity: quick
  executionMode: live
  tags:
    - retention
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Track first visit to first order"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Track first visit to first order
    summary: >-
      Weekly cohorts anchored on a visitor's first session, measuring who places an order in weeks 1,
      2, 4, 8 and 12, split by the top 6 traffic sources. Flags any source still under 8% at week 12.
    builds: report
    description: |-
      Create a Retention report called "Browse to Buy Retention".
      Anchor event: session_start (each user's first session_start)
      Return event: order_created
      Cohort granularity: Weekly
      Time range: Last 12 weeks
      Breakdown: By Users.utm_source (top 6 sources)
      Compare: Previous period (prior 12 weeks of cohorts)
      Chart type: Retention curve plus cohort table with W1 / W2 / W4 / W8 / W12 columns
      Annotations:
      - Add benchmarks: W1 first-purchase rate of 5% is typical for considered-purchase DTC, 10%+ for impulse-buy.
      - Flag any source where W12 first-purchase rate is below 8% (browse-to-buy gap).
      - Highlight the source with the fastest first-purchase rate (steepest W1 conversion).
      - Highlight the source with the highest W12 conversion (best overall, even if slower).
      Surface which sources produce "fast converters" vs "slow converters."
      Taxonomy notes:
      - session_start and order_created are canonical. Users.utm_source is canonical.
      - "first session" per-user is determined by the earliest session_start for that customer_id.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Browse to buy retention

Measures how long first time visitors take to place an order, by acquisition source, so you can tell fast converting channels from slow ones.

## Steps

1. **Track first visit to first order** (builds report)

   Weekly cohorts anchored on a visitor's first session, measuring who places an order in weeks 1, 2, 4, 8 and 12, split by the top 6 traffic sources. Flags any source still under 8% at week 12.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Track first visit to first order"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
