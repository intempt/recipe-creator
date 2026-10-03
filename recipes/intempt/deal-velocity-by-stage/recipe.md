---
id: deal-velocity-by-stage
title: Deal velocity by stage
slash_command: /deal-velocity-by-stage
group: Reports
owner: intempt
summary: Shows how long deals sit in each sales stage and which stage is the bottleneck, with won deals
  set against lost ones.
description: >-
  Median time spent in each deal stage with bottleneck-stage identification and won/lost velocity comparison.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - b2b
  complexity: quick
  executionMode: live
  tags:
    - insights
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Time deals in each stage"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Time deals in each stage
    summary: >-
      Median, average and 75th percentile time in each stage across the last 90 days of stage changes,
      compared with the prior 90. Adds a side by side of won versus lost deals and flags the slowest stage
      and any stage that got 30% worse.
    builds: report
    description: |-
      Create an Insights report called "Deal Velocity by Stage".
      Series A: Event "deal_stage_changed", aggregation: Average of "time_in_previous_stage": computed by Lovable as the time delta between consecutive deal_stage_changed events for the same deal_id (or between deal_created and the first deal_stage_changed for the entry-into-first-stage case)
      Series B: Same as A but using Median instead of Average (less sensitive to outlier slow deals)
      Series C: 75th-percentile time-in-stage (the "long tail" of slow deals)
      Breakdown: By "previous_stage" property on deal_stage_changed
      Time range: Last 90 days of stage transitions
      Compare: Previous period (prior 90 days)
      Chart type: Horizontal bar chart per stage with median (Series B) as the bar, p75 (Series C) as a whisker, and average (Series A) as a marker
      Also include a parallel comparison view:
      - For deals that ultimately reached deal_won (won deals): median time-in-stage per stage
      - For deals that ultimately reached deal_lost (lost deals): median time-in-stage per stage
      - The delta surfaces which stages distinguish winners from losers (won deals are typically faster through middle stages; lost deals stall in qualification or proposal)
      Annotations:
      - Flag the stage with the longest median time-in-stage (the primary bottleneck).
      - Flag any stage where median velocity worsened by >30% vs. previous period (deteriorating sales process).
      - Highlight stages where won-deal velocity is materially faster than lost-deal velocity (>2× faster): these are the stages where decisive movement predicts close.
      - Surface the total median sales-cycle length (sum of stage medians) and the trend.
      Use case: knowing which stage is your bottleneck is the foundation of every sales-process improvement. Most CRMs report stage-conversion rate but not stage-velocity; this is the missing half.
      Taxonomy notes:
      - deal_stage_changed has previous_stage and new_stage relations, plus deal_id.
      - "Time in stage" is computed by Lovable from successive deal_stage_changed events on the same deal_id.
      - deal_won and deal_lost are canonical terminal states; deal_closed_won and deal_closed_lost may also fire depending on integration.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Deal velocity by stage

Shows how long deals sit in each sales stage and which stage is the bottleneck, with won deals set against lost ones.

## Steps

1. **Time deals in each stage** (builds report)

   Median, average and 75th percentile time in each stage across the last 90 days of stage changes, compared with the prior 90. Adds a side by side of won versus lost deals and flags the slowest stage and any stage that got 30% worse.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Time deals in each stage"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
