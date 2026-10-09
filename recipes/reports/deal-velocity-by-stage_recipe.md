---
name: deal-velocity-by-stage
description: |
  Use when a user mentions "deal velocity by stage", or asks for related help. Median time spent in each deal stage with bottleneck-stage identification and won/lost velocity comparison.
arguments: []
intempt:
  id: deal-velocity-by-stage
  version: 1.0.0
  slashCommand: /deal-velocity-by-stage
  group: Reports
  title: "Deal velocity by stage"
  shortDescription: "Shows how long deals sit in each sales stage and which stage is the bottleneck, with won deals set against lost ones."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [b2b]
    complexity: quick
    executionMode: live
    tags: [insights]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Time deals in each stage"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Median, average and 75th percentile time in each stage across the last 90 days of stage changes, compared with the prior 90. Adds a side by side of won versus lost deals and flags the slowest stage and any stage that got 30% worse."
      prompt: |
        Create an Insights report called "Deal Velocity by Stage".

        Series A: Event "Deal stage changed", aggregation: Average of time spent in the previous stage: computed as the time between consecutive Deal stage changed events for the same deal (or between Deal created and the first Deal stage changed for the entry-into-first-stage case)
        Series B: Same as A but using Median instead of Average (less sensitive to outlier slow deals)
        Series C: 75th-percentile time-in-stage (the "long tail" of slow deals)
        Breakdown: By the previous stage
        Time range: Last 90 days of stage transitions
        Compare: Previous period (prior 90 days)
        Chart type: Horizontal bar chart per stage with median (Series B) as the bar, p75 (Series C) as a whisker, and average (Series A) as a marker

        Also include a parallel comparison view:
        - For deals that ultimately reached Deal won (won deals): median time-in-stage per stage
        - For deals that ultimately reached Deal lost (lost deals): median time-in-stage per stage
        - The delta surfaces which stages distinguish winners from losers (won deals are typically faster through middle stages; lost deals stall in qualification or proposal)

        Annotations:
        - Flag the stage with the longest median time-in-stage (the primary bottleneck).
        - Flag any stage where median velocity worsened by >30% vs. previous period (deteriorating sales process).
        - Highlight stages where won-deal velocity is materially faster than lost-deal velocity (>2× faster): these are the stages where decisive movement predicts close.
        - Surface the total median sales-cycle length (sum of stage medians) and the trend.

        Use case: knowing which stage is your bottleneck is the foundation of every sales-process improvement. Most CRMs report stage-conversion rate but not stage-velocity; this is the missing half.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Deal velocity by stage

Shows how long deals sit in each sales stage and which stage is the bottleneck, with won deals set against lost ones.

## What it does

1. **Time deals in each stage** (`build_insights_report`)

   Median, average and 75th percentile time in each stage across the last 90 days of stage changes, compared with the prior 90. Adds a side by side of won versus lost deals and flags the slowest stage and any stage that got 30% worse.

## What you end up with

- **report** (report): Report produced by this recipe.
