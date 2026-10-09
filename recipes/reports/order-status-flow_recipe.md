---
name: order-status-flow
description: |
  Use when a user mentions "order status flow", or asks for related help. Order distribution across created/fulfilled/refunded/cancelled states over time: the operational pulse of order flow.
arguments: []
intempt:
  id: order-status-flow
  version: 1.0.0
  slashCommand: /order-status-flow
  group: Reports
  title: "Order status flow"
  shortDescription: "Shows daily order volume alongside how many get fulfilled, refunded or cancelled, and the rate for each."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
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
      title: "Track orders through their states"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Daily counts of orders created, fulfilled, refunded and cancelled over the last 30 days, with fulfilment, refund and cancellation rates as overlay lines. Benchmarks fulfilment at 95% and a refund rate under 3%."
      prompt: |
        Create an Insights report called "Order Status Flow".

        Series A: Placed order events, aggregation: Count, label: "Created"
        Series B: Order fulfilled events, aggregation: Count, label: "Fulfilled"
        Series C: Order refunded events, aggregation: Count, label: "Refunded"
        Series D: Order cancelled events, aggregation: Count, label: "Cancelled"
        Series E: Computed: Series B / Series A × 100, unit: %, label: "Fulfillment Rate"
        Series F: Computed: Series C / Series A × 100, unit: %, label: "Refund Rate"
        Series G: Computed: Series D / Series A × 100, unit: %, label: "Cancellation Rate"

        Time granularity: Daily (with weekly rollup option)
        Time range: Last 30 days
        Breakdown for Series A: By fulfillment status on Order fulfilled where present (fulfilled, partial, etc.)
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

        For accurate rate computation, the fulfillment, refund and cancellation rates should only count orders that have had time to fulfill: exclude orders less than 48h old when computing the fulfillment rate, since they may still be legitimately in pre-fulfillment.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Order status flow

Shows daily order volume alongside how many get fulfilled, refunded or cancelled, and the rate for each.

## What it does

1. **Track orders through their states** (`build_insights_report`)

   Daily counts of orders created, fulfilled, refunded and cancelled over the last 30 days, with fulfilment, refund and cancellation rates as overlay lines. Benchmarks fulfilment at 95% and a refund rate under 3%.

## What you end up with

- **report** (report): Report produced by this recipe.
