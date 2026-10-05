---
name: average-order-value-trend
description: |
  Use when a user mentions "average order value trend", or asks for related help. AOV over time with units-per-order vs price-per-unit decomposition and new-vs-returning comparison.
arguments: []
intempt:
  id: average-order-value-trend
  version: 1.0.0
  slashCommand: /average-order-value-trend
  group: Reports
  shortDescription: "Builds a weekly Insights report of average order value, units per order, average price per unit, and new-vs-returning customer breakdown over the last 12 weeks."
  availability: coming-soon
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
        Create an Insights report called "AOV Trend".

        Series A: Event "order_created", aggregation: Average of "total_price" property, unit: $, label: "AOV"
        Series B: Event "order_created", aggregation: Average of items length (count of line items in items array), label: "Units per Order"
        Series C: Computed — Series A / Series B, unit: $, label: "Average Price per Unit"
        Time granularity: Weekly
        Time range: Last 12 weeks
        Breakdown: By customer type — derive new vs returning from the User.lifetime_value computed attribute (lifetime_value > 0 at the time of the order = returning, otherwise new) OR from User.orders_count.
        Compare: Previous period (previous 12 weeks)
        Chart type: Multi-line chart with all three series, separate axes for AOV/Price-per-Unit ($) and Units-per-Order (#)

        Annotations:
        - Add a callout showing the period-over-period change in each component (AOV, Units/Order, Price/Unit).
        - Flag any week where AOV moved >5% — and identify whether the move came from units, price, or both.
        - Highlight the AOV gap between new and returning customers (returning typically 1.5–2× new for healthy DTC).

        AOV moving via price suggests merchandising/pricing impact; AOV moving via units suggests bundling/cross-sell impact.

        Taxonomy notes:
        - order_created has total_price (Shopify) and items (flattened: product_id, title, quantity, price, sku). "order_total" is not a real property.
        - Users.lifetime_value and User.orders_count (system-computed) are real attributes.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Average Order Value Trend

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "AOV Trend".

   Series A: Event "order_created", aggregation: Average of "total_price" property, unit: $, label: "AOV"
   Series B: Event "order_created", aggregation: Average of items length (count of line items in items array), label: "Units per Order"
   Series C: Computed — Series A / Series B, unit: $, label: "Average Price per Unit"
   Time granularity: Weekly
   Time range: Last 12 weeks
   Breakdown: By customer type — derive new vs returning from the User.lifetime_value computed attribute (lifetime_value > 0 at the time of the order = returning, otherwise new) OR from User.orders_count.
   Compare: Previous period (previous 12 weeks)
   Chart type: Multi-line chart with all three series, separate axes for AOV/Price-per-Unit ($) and Units-per-Order (#)

   Annotations:
   - Add a callout showing the period-over-period change in each component (AOV, Units/Order, Price/Unit).
   - Flag any week where AOV moved >5% — and identify whether the move came from units, price, or both.
   - Highlight the AOV gap between new and returning customers (returning typically 1.5–2× new for healthy DTC).

   AOV moving via price suggests merchandising/pricing impact; AOV moving via units suggests bundling/cross-sell impact.

   Taxonomy notes:
   - order_created has total_price (Shopify) and items (flattened: product_id, title, quantity, price, sku). "order_total" is not a real property.
   - Users.lifetime_value and User.orders_count (system-computed) are real attributes.
   ```
