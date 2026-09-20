---
name: order-status-flow
description: |
  Use when a user mentions "order status flow", or asks for related help. Order distribution across created/fulfilled/refunded/cancelled states over time — the operational pulse of order flow.
arguments: []
intempt:
  id: order-status-flow
  version: 1.0.0
  slashCommand: /order-status-flow
  group: Reports
  shortDescription: 'Order distribution across created/fulfilled/refunded/cancelled states over time: the operational pulse of order flow.'
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
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "Order Status Flow".

        Series A: Event "order_created", aggregation: Count, label: "Created"
        Series B: Event "order_fulfilled", aggregation: Count, label: "Fulfilled"
        Series C: Event "order_refunded", aggregation: Count, label: "Refunded"
        Series D: Event "order_cancelled", aggregation: Count, label: "Cancelled"
        Series E: Computed — Series B / Series A × 100, unit: %, label: "Fulfillment Rate"
        Series F: Computed — Series C / Series A × 100, unit: %, label: "Refund Rate"
        Series G: Computed — Series D / Series A × 100, unit: %, label: "Cancellation Rate"

        Time granularity: Daily (with weekly rollup option)
        Time range: Last 30 days
        Breakdown for Series A: By "fulfillment_status" property on order_fulfilled where present (fulfilled, partial, etc.)
        Compare: Previous period (prior 30 days)
        Chart type: Stacked column chart for absolute counts (Series A–D) over time, with Series E/F/G as overlay lines on a secondary axis showing the rates

        Annotations:
        - Add benchmarks: healthy fulfillment rate is 95%+; 90–95% indicates a backlog or capacity constraint; <90% suggests systemic operational issue.
        - Add benchmarks: refund rate <3% is healthy DTC; 3–8% varies by category (apparel typically higher); >10% suggests product-quality or fit-prediction issues.
        - Add benchmarks: cancellation rate <2% is healthy; >5% suggests checkout-conversion issues (customers regret the purchase quickly) or fraud-detection cancellations.
        - Flag any day where Series E (fulfillment rate) dropped >5 points vs. trailing-7-day average (operational issue requiring same-day investigation).
        - Highlight the gap between Created and Fulfilled in the most recent days — this is the in-flight backlog. Growing gap = capacity constraint.
        - Surface absolute volumes (orders today, fulfilled today, refunded today, cancelled today) as headline callouts.

        Use case: the operational pulse for ecommerce ops/fulfillment teams. Surfaces both the volume picture (am I getting more orders?) and the quality picture (am I delivering them?) on a single canvas.

        Taxonomy notes:
        - All four order events are canonical: order_created, order_fulfilled, order_refunded, order_cancelled.
        - order_fulfilled.fulfillment_status is a real property (values vary by integration source — typically "fulfilled", "partial", "pending").
        - For accurate rate computation, Series E/F/G should match against orders that had time to fulfill (e.g., exclude orders <48h old when computing fulfillment rate, since they may still be legitimately in pre-fulfillment).
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Order Status Flow

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Order Status Flow".

   Series A: Event "order_created", aggregation: Count, label: "Created"
   Series B: Event "order_fulfilled", aggregation: Count, label: "Fulfilled"
   Series C: Event "order_refunded", aggregation: Count, label: "Refunded"
   Series D: Event "order_cancelled", aggregation: Count, label: "Cancelled"
   Series E: Computed — Series B / Series A × 100, unit: %, label: "Fulfillment Rate"
   Series F: Computed — Series C / Series A × 100, unit: %, label: "Refund Rate"
   Series G: Computed — Series D / Series A × 100, unit: %, label: "Cancellation Rate"

   Time granularity: Daily (with weekly rollup option)
   Time range: Last 30 days
   Breakdown for Series A: By "fulfillment_status" property on order_fulfilled where present (fulfilled, partial, etc.)
   Compare: Previous period (prior 30 days)
   Chart type: Stacked column chart for absolute counts (Series A–D) over time, with Series E/F/G as overlay lines on a secondary axis showing the rates

   Annotations:
   - Add benchmarks: healthy fulfillment rate is 95%+; 90–95% indicates a backlog or capacity constraint; <90% suggests systemic operational issue.
   - Add benchmarks: refund rate <3% is healthy DTC; 3–8% varies by category (apparel typically higher); >10% suggests product-quality or fit-prediction issues.
   - Add benchmarks: cancellation rate <2% is healthy; >5% suggests checkout-conversion issues (customers regret the purchase quickly) or fraud-detection cancellations.
   - Flag any day where Series E (fulfillment rate) dropped >5 points vs. trailing-7-day average (operational issue requiring same-day investigation).
   - Highlight the gap between Created and Fulfilled in the most recent days — this is the in-flight backlog. Growing gap = capacity constraint.
   - Surface absolute volumes (orders today, fulfilled today, refunded today, cancelled today) as headline callouts.

   Use case: the operational pulse for ecommerce ops/fulfillment teams. Surfaces both the volume picture (am I getting more orders?) and the quality picture (am I delivering them?) on a single canvas.

   Taxonomy notes:
   - All four order events are canonical: order_created, order_fulfilled, order_refunded, order_cancelled.
   - order_fulfilled.fulfillment_status is a real property (values vary by integration source — typically "fulfilled", "partial", "pending").
   - For accurate rate computation, Series E/F/G should match against orders that had time to fulfill (e.g., exclude orders <48h old when computing fulfillment rate, since they may still be legitimately in pre-fulfillment).
   ```
