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
  title: "Average order value trend"
  shortDescription: "Tracks average order value weekly and splits the movement into how many items people buy versus what they pay per item, for new and returning customers."
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
  prerequisites:
    integrations:
      - { value: shopify, severity: blocking }
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Break down AOV week by week"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Average order value, units per order and average price per unit over the last 12 weeks, compared with the prior 12 and split by new versus returning customers. Flags any week where order value moved more than 5% and names whether units or price caused it."
      prompt: |
        Create an Insights report called "AOV Trend".

        Series A: Event "order_created", aggregation: Average of "total_price" property, unit: $, label: "AOV"
        Series B: Event "order_created", aggregation: Average of items length (count of line items in items array), label: "Units per Order"
        Series C: Computed: Series A / Series B, unit: $, label: "Average Price per Unit"
        Time granularity: Weekly
        Time range: Last 12 weeks
        Breakdown: By customer type: derive new vs returning from the User.lifetime_value computed attribute (lifetime_value > 0 at the time of the order = returning, otherwise new) OR from User.orders_count.
        Compare: Previous period (previous 12 weeks)
        Chart type: Multi-line chart with all three series, separate axes for AOV/Price-per-Unit ($) and Units-per-Order (#)

        Annotations:
        - Add a callout showing the period-over-period change in each component (AOV, Units/Order, Price/Unit).
        - Flag any week where AOV moved >5%: and identify whether the move came from units, price, or both.
        - Highlight the AOV gap between new and returning customers (returning typically 1.5: 2× new for healthy DTC).

        AOV moving via price suggests merchandising/pricing impact; AOV moving via units suggests bundling/cross-sell impact.

        Taxonomy notes:
        - order_created has total_price (Shopify) and items (flattened: product_id, title, quantity, price, sku). "order_total" is not a real property.
        - Users.lifetime_value and User.orders_count (system-computed) are real attributes.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Average order value trend

Tracks average order value weekly and splits the movement into how many items people buy versus what they pay per item, for new and returning customers.

## Before you run it

- Connect shopify

## What it does

1. **Break down AOV week by week** (`build_insights_report`)

   Average order value, units per order and average price per unit over the last 12 weeks, compared with the prior 12 and split by new versus returning customers. Flags any week where order value moved more than 5% and names whether units or price caused it.

## What you end up with

- **report** (report): Report produced by this recipe.
