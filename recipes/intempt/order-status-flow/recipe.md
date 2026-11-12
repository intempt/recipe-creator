---
frontmatter_id: order-status-flow
slash_command: /order-status-flow
description: Shows daily order volume alongside how many get fulfilled, refunded or cancelled, and the rate for each.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows daily order volume with fulfilled, refunded and cancelled counts and their rates, with benchmark flags and
    headline callouts for the ops team.
  parameters:
  - name: time_range
    type: duration
    label: Time range to analyse
    default: 30 d
    required: false
  - name: time_granularity
    type: enum
    label: Time granularity
    default: day
    required: false
    options:
    - day
    - week
  - name: compare_period
    type: duration
    label: Comparison period (prior period)
    default: 30 d
    required: false
  - name: fulfillment_healthy_rate
    type: number
    label: Healthy fulfillment rate (%)
    default: 95
    required: false
  - name: fulfillment_backlog_rate
    type: number
    label: Backlog warning fulfillment rate (%)
    default: 90
    required: false
  - name: refund_healthy_rate
    type: number
    label: Healthy refund rate (%)
    default: 3
    required: false
  - name: refund_high_rate
    type: number
    label: High refund rate (%)
    default: 10
    required: false
  - name: cancellation_healthy_rate
    type: number
    label: Healthy cancellation rate (%)
    default: 2
    required: false
  - name: cancellation_high_rate
    type: number
    label: High cancellation rate (%)
    default: 5
    required: false
  - name: fulfillment_drop_points
    type: number
    label: Fulfillment rate drop that triggers a flag (points vs trailing 7-day average)
    default: 5
    required: false
  - name: order_maturity_window
    type: duration
    label: Minimum order age before counting toward fulfillment rate
    default: 48 h
    required: false
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
  - slot: order_fulfilled_event
    kind: event
    meaning: An order was fulfilled
    properties:
    - name: fulfillment_status
      type: string
      meaning: Fulfillment state of the order, such as fulfilled, partial or pending
      optional: true
  - slot: order_refunded_event
    kind: event
    meaning: An order was refunded
  - slot: order_cancelled_event
    kind: event
    meaning: An order was cancelled
  steps:
  - id: s1
    builds: report
    uses:
    - placed_order_event
    - order_fulfilled_event
    - order_refunded_event
    - order_cancelled_event
    - time_range
    - time_granularity
    - compare_period
    - fulfillment_healthy_rate
    - fulfillment_backlog_rate
    - refund_healthy_rate
    - refund_high_rate
    - cancellation_healthy_rate
    - cancellation_high_rate
    - fulfillment_drop_points
    - order_maturity_window
    instruction: 'Create an Insights report named "Order Status Flow" showing order states over {time_range} at {time_granularity}
      granularity, with a prior-period comparison over {compare_period}. Series A: count of {placed_order_event}, labelled
      "Created". Series B: count of {order_fulfilled_event}, labelled "Fulfilled". Series C: count of {order_refunded_event},
      labelled "Refunded". Series D: count of {order_cancelled_event}, labelled "Cancelled". Series E: Series B divided by
      Series A times 100, unit %, labelled "Fulfillment Rate", counting only orders older than {order_maturity_window}. Series
      F: Series C divided by Series A times 100, unit %, labelled "Refund Rate". Series G: Series D divided by Series A times
      100, unit %, labelled "Cancellation Rate". Break down Series A by {order_fulfilled_event.fulfillment_status} where present.
      Chart type: stacked column chart of Series A to D as absolute counts over time, with Series E, F and G as overlay lines
      on a secondary percentage axis. Add benchmark annotations: fulfillment rate at or above {fulfillment_healthy_rate}%
      is healthy, between {fulfillment_backlog_rate}% and {fulfillment_healthy_rate}% indicates a backlog or capacity constraint,
      below {fulfillment_backlog_rate}% indicates a systemic operational issue. Refund rate below {refund_healthy_rate}% is
      healthy, above {refund_high_rate}% indicates product-quality or fit issues. Cancellation rate below {cancellation_healthy_rate}%
      is healthy, above {cancellation_high_rate}% indicates checkout-conversion or fraud-detection issues. Flag any day where
      Series E dropped more than {fulfillment_drop_points} points versus the trailing 7-day average for same-day investigation.
      Highlight the gap between Created and Fulfilled over the most recent days as the in-flight backlog; a growing gap signals
      a capacity constraint. Surface headline callouts for orders created, fulfilled, refunded and cancelled today.'
---

# Order status flow

Slash command: /order-status-flow

## Step 1: Track orders through their states

Create an Insights report called "Order Status Flow".
Series A: Event "Placed order", aggregation: Count, label: "Created"
Series B: Event "Order fulfilled", aggregation: Count, label: "Fulfilled"
Series C: Event "Order refunded", aggregation: Count, label: "Refunded"
Series D: Event "Order cancelled", aggregation: Count, label: "Cancelled"
Series E: Computed: Series B / Series A × 100, unit: %, label: "Fulfillment Rate"
Series F: Computed: Series C / Series A × 100, unit: %, label: "Refund Rate"
Series G: Computed: Series D / Series A × 100, unit: %, label: "Cancellation Rate"
Time granularity: Daily (with weekly rollup option)
Time range: Last 30 days
Breakdown for Series A: By "fulfillment_status" property on Order fulfilled where present (fulfilled, partial, etc.)
Compare: Previous period (prior 30 days)
Chart type: Stacked column chart for absolute counts (Series A: D) over time, with Series E/F/G as overlay lines on a secondary axis showing the rates
Annotations:
- Add benchmarks: healthy fulfillment rate is 95%+; 90: 95% indicates a backlog or capacity constraint; <90% suggests systemic operational issue.
- Add benchmarks: refund rate <3% is healthy DTC; 3: 8% varies by category (apparel typically higher); >10% suggests product-quality or fit-prediction issues.
- Add benchmarks: cancellation rate <2% is healthy; >5% suggests checkout-conversion issues (customers regret the purchase quickly) or fraud-detection cancellations.
- Flag any day where Series E (fulfillment rate) dropped >5 points vs. trailing-7-day average (operational issue requiring same-day investigation).
- Highlight the gap between Created and Fulfilled in the most recent days: this is the in-flight backlog. Growing gap = capacity constraint.
- Surface absolute volumes (orders today, fulfilled today, refunded today, cancelled today) as headline callouts.
Use case: the operational pulse for ecommerce ops/fulfillment teams. Surfaces both the volume picture (am I getting more orders?) and the quality picture (am I delivering them?) on a single canvas.
Taxonomy notes:
- All four order events are canonical: Placed order, Order fulfilled, Order refunded, Order cancelled.
- Order fulfilled.fulfillment_status is a real property (values vary by integration source: typically "fulfilled", "partial", "pending").
- For accurate rate computation, Series E/F/G should match against orders that had time to fulfill (e.g., exclude orders <48h old when computing fulfillment rate, since they may still be legitimately in pre-fulfillment).
