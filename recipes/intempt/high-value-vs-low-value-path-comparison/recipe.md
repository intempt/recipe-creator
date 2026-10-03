---
id: high-value-vs-low-value-path-comparison
title: High value versus low value paths
slash_command: /high-value-vs-low-value-path-comparison
group: Reports
owner: intempt
curator: aman
summary: Puts the journeys of big spenders next to the journeys of small spenders and non buyers, and
  names the steps that only show up on the profitable side.
description: >-
  Two Path reports side-by-side: paths taken by users who placed >$X orders vs <$X or non-converters.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  complexity: quick
  executionMode: live
  tags:
    - path
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Contrast big and small basket paths"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Contrast big and small basket paths
    summary: >-
      Two 7 step journeys from a first session inside a 7 day window over the last 60 days: one ending
      in an order above the high value threshold (100 dollars by default), one ending below it or with
      no order at all. Surfaces the events unique to each side.
    builds: report
    description: |-
      Create a Path report called "High-Value vs Low-Value Path Comparison".
      This recipe runs two Path reports in parallel and surfaces them side-by-side.
      Configuration:
      - Threshold for "high value": default $100 (configurable; or use the 75th-percentile order_created.total_price)
      - Threshold for "low value": default <$50 OR no order placed in the window (configurable)
      Path A: High-value paths:
      - Anchor event: session_start (user's first session in the window)
      - End event: order_created where total_price >= high-value threshold
      - Direction: forward
      - Depth: 7 steps
      - Window: 7 days
      - Loop compression: on
      Path B: Low-value paths:
      - Anchor event: session_start
      - End event: order_created where total_price < low-value threshold OR session_end without any order_created
      - Direction: forward
      - Depth: 7 steps
      - Window: 7 days
      - Loop compression: on
      Time range: Last 60 days
      Render the two Path reports side-by-side and compute a "lift" view: events that appear in Path A's top 10 paths but NOT in Path B's top 10, and vice versa.
      Annotations:
      - Surface the top 5 events that appear disproportionately in high-value paths (the "high-value-buyer signals").
      - Surface the top 5 events that appear in low-value paths (the "low-value-buyer signals": typically discount_applied events, single product detail page_viewed without category browsing, etc.).
      - Surface the median path length (number of steps) for each segment: high-value buyers typically take longer, more deliberate paths.
      Use case: identify behaviors that predict high-value purchase intent in the first session, so you can trigger personalization for users showing those signals.
      Taxonomy notes:
      - session_start, order_created, session_end are all canonical. order_created.total_price is the value used for the threshold filter.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# High value versus low value paths

Puts the journeys of big spenders next to the journeys of small spenders and non buyers, and names the steps that only show up on the profitable side.

## Steps

1. **Contrast big and small basket paths** (builds report)

   Two 7 step journeys from a first session inside a 7 day window over the last 60 days: one ending in an order above the high value threshold (100 dollars by default), one ending below it or with no order at all. Surfaces the events unique to each side.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Contrast big and small basket paths"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
