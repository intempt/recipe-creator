---
id: average-order-value-trend
title: Average order value trend
slash_command: /average-order-value-trend
group: Reports
owner: intempt
curator: aman
summary: Tracks average order value weekly and splits the movement into how many items people buy versus
  what they pay per item, for new and returning customers.
description: >-
  AOV over time with units-per-order vs price-per-unit decomposition and new-vs-returning comparison.
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
    - insights
prerequisites:
  integrations:
    - value: shopify
      severity: blocking
touches:
  reads:
    - Your Shopify connection
  writes:
    - A new report, from step 1 "Break down AOV week by week"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Break down AOV week by week
    summary: >-
      Average order value, units per order and average price per unit over the last 12 weeks, compared
      with the prior 12 and split by new versus returning customers. Flags any week where order value
      moved more than 5% and names whether units or price caused it.
    builds: report
    description: |-
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
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Average order value trend

Tracks average order value weekly and splits the movement into how many items people buy versus what they pay per item, for new and returning customers.

## Steps

1. **Break down AOV week by week** (builds report)

   Average order value, units per order and average price per unit over the last 12 weeks, compared with the prior 12 and split by new versus returning customers. Flags any week where order value moved more than 5% and names whether units or price caused it.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Your Shopify connection

Writes:

- A new report, from step 1 "Break down AOV week by week"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
