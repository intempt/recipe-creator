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
  shortDescription: "Create an insights report measuring average, median, and 75th percentile time spent in each deal stage."
  availability: coming-soon
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
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "Deal Velocity by Stage".

        Series A: Event "deal_stage_changed", aggregation: Average of "time_in_previous_stage" — computed by Lovable as the time delta between consecutive deal_stage_changed events for the same deal_id (or between deal_created and the first deal_stage_changed for the entry-into-first-stage case)
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
        - Highlight stages where won-deal velocity is materially faster than lost-deal velocity (>2× faster) — these are the stages where decisive movement predicts close.
        - Surface the total median sales-cycle length (sum of stage medians) and the trend.

        Use case: knowing which stage is your bottleneck is the foundation of every sales-process improvement. Most CRMs report stage-conversion rate but not stage-velocity; this is the missing half.

        Taxonomy notes:
        - deal_stage_changed has previous_stage and new_stage relations, plus deal_id.
        - "Time in stage" is computed by Lovable from successive deal_stage_changed events on the same deal_id.
        - deal_won and deal_lost are canonical terminal states; deal_closed_won and deal_closed_lost may also fire depending on integration.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Deal Velocity by Stage

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Deal Velocity by Stage".

   Series A: Event "deal_stage_changed", aggregation: Average of "time_in_previous_stage" — computed by Lovable as the time delta between consecutive deal_stage_changed events for the same deal_id (or between deal_created and the first deal_stage_changed for the entry-into-first-stage case)
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
   - Highlight stages where won-deal velocity is materially faster than lost-deal velocity (>2× faster) — these are the stages where decisive movement predicts close.
   - Surface the total median sales-cycle length (sum of stage medians) and the trend.

   Use case: knowing which stage is your bottleneck is the foundation of every sales-process improvement. Most CRMs report stage-conversion rate but not stage-velocity; this is the missing half.

   Taxonomy notes:
   - deal_stage_changed has previous_stage and new_stage relations, plus deal_id.
   - "Time in stage" is computed by Lovable from successive deal_stage_changed events on the same deal_id.
   - deal_won and deal_lost are canonical terminal states; deal_closed_won and deal_closed_lost may also fire depending on integration.
   ```
