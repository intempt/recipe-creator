---
frontmatter_id: deal-velocity-by-stage
slash_command: /deal-velocity-by-stage
description: Shows how long deals sit in each sales stage and which stage is the bottleneck, with won deals set against lost ones.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows how long deals stay in each sales stage, which stage is the bottleneck, and how won deals' stage speed compares
    with lost deals.
  parameters:
  - name: lookback_window
    type: duration
    label: Time range for stage transitions
    default: 90 d
    required: false
  - name: comparison_window
    type: duration
    label: Comparison period (previous period length)
    default: 90 d
    required: false
  - name: worsening_threshold_pct
    type: number
    label: Flag stage when median time worsens by more than (%)
    default: 30
    required: false
  - name: won_vs_lost_speed_ratio
    type: number
    label: Flag stage when won-deal velocity is faster than lost by at least (x)
    default: 2
    required: false
  requirements:
  - slot: deal_stage_changed_event
    kind: event
    meaning: A deal moved from one sales stage to another
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
    - name: previous_stage
      type: string
      meaning: Stage the deal left
      optional: false
    - name: new_stage
      type: string
      meaning: Stage the deal entered
      optional: false
    - name: time_in_previous_stage
      type: number
      meaning: Time the deal spent in the previous stage
      optional: true
  - slot: deal_created_event
    kind: event
    meaning: A new deal was created
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
  - slot: deal_won_event
    kind: event
    meaning: A customer's deal was won (closed won)
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
  - slot: deal_lost_event
    kind: event
    meaning: A customer's deal was lost (closed lost)
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
  steps:
  - id: s1
    builds: report
    uses:
    - deal_stage_changed_event
    - deal_created_event
    - lookback_window
    - comparison_window
    instruction: 'Create an Insights report titled "Deal Velocity by Stage". Time range: last {lookback_window} of stage transitions,
      compared against the prior {comparison_window}. Compute time in stage from successive {deal_stage_changed_event} events
      on the same {deal_stage_changed_event.deal_id}; for the first stage, use the time between {deal_created_event} and the
      first {deal_stage_changed_event}. Series A: average of time in previous stage. Series B: median of time in previous
      stage. Series C: 75th-percentile time in previous stage. Break down all series by {deal_stage_changed_event.previous_stage}.
      Chart as horizontal bars per stage: median as the bar, p75 as the whisker, average as a marker.'
---

# Deal velocity by stage

Slash command: /deal-velocity-by-stage

## Step 1: Time deals in each stage

Create an Insights report called "Deal Velocity by Stage".
Series A: Event "Deal stage changed", aggregation: Average of "time_in_previous_stage": computed by Lovable as the time delta between consecutive Deal stage changed events for the same deal_id (or between Deal created and the first Deal stage changed for the entry-into-first-stage case)
Series B: Same as A but using Median instead of Average (less sensitive to outlier slow deals)
Series C: 75th-percentile time-in-stage (the "long tail" of slow deals)
Breakdown: By "previous_stage" property on Deal stage changed
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
Taxonomy notes:
- Deal stage changed has previous_stage and new_stage relations, plus deal_id.
- "Time in stage" is computed by Lovable from successive Deal stage changed events on the same deal_id.
- Deal won and Deal lost are canonical terminal states; deal_closed_won and deal_closed_lost may also fire depending on integration.
