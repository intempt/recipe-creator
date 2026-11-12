---
frontmatter_id: average-order-value-trend
slash_command: /average-order-value-trend
description: Tracks average order value weekly and splits the movement into how many items people buy versus what they pay per item, for new and returning customers.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows weekly average order value and splits its movement into units per order versus price per unit, for new and
    returning customers, with alerts on large weekly swings.
  parameters:
  - name: trend_window
    type: duration
    label: Time range to chart
    default: 12 w
    required: false
  - name: compare_window
    type: duration
    label: Comparison period
    default: 12 w
    required: false
  - name: movement_threshold_pct
    type: number
    label: Weekly AOV move that gets flagged (%)
    default: 5
    required: false
  - name: returning_gap_low
    type: number
    label: Expected returning-to-new AOV ratio, low end
    default: 1.5
    required: false
  - name: returning_gap_high
    type: number
    label: Expected returning-to-new AOV ratio, high end
    default: 2
    required: false
  requirements:
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Total price of the order
      optional: false
    - name: items
      type: array
      meaning: Line items in the order, each with product_id, title, quantity, price and sku
      optional: false
  - slot: customer_lifetime_value
    kind: attribute
    meaning: Computed lifetime value of the customer who placed the order
  - slot: customer_orders_count
    kind: attribute
    meaning: System-computed count of orders placed by the customer
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - order_placed_event
    - customer_lifetime_value
    - customer_orders_count
    - trend_window
    - compare_window
    - movement_threshold_pct
    - returning_gap_low
    - returning_gap_high
    instruction: 'Create an Insights report titled "AOV Trend". Series A: event {order_placed_event}, aggregation average
      of {order_placed_event.total_price}, unit $, label "AOV". Series B: event {order_placed_event}, aggregation average
      of the count of line items in {order_placed_event.items}, label "Units per Order". Series C: computed as Series A divided
      by Series B, unit $, label "Average Price per Unit". Time granularity weekly over the last {trend_window}. Breakdown
      by customer type: classify as returning if {customer_lifetime_value} is greater than 0 at the time of the order, otherwise
      new; alternatively use {customer_orders_count} to classify. Compare against the previous {compare_window}. Chart as
      a multi-line chart with all three series, using separate axes for AOV and Price per Unit in $ and Units per Order in
      #. Add a callout showing the period-over-period change for AOV, Units per Order and Price per Unit. Flag any week where
      AOV moved more than {movement_threshold_pct}% and state whether the move came from units, price, or both. Highlight
      the AOV gap between returning and new customers, noting whether it falls between {returning_gap_low} and {returning_gap_high}
      times the new-customer AOV. Interpretation: AOV moving via price suggests merchandising or pricing impact; AOV moving
      via units suggests bundling or cross-sell impact.'
---

# Average order value trend

Slash command: /average-order-value-trend

## Step 1: Break down AOV week by week

Create an Insights report called "AOV Trend".
Series A: Event "Placed order", aggregation: Average of "total_price" property, unit: $, label: "AOV"
Series B: Event "Placed order", aggregation: Average of items length (count of line items in items array), label: "Units per Order"
Series C: Computed: Series A / Series B, unit: $, label: "Average Price per Unit"
Time granularity: Weekly
Time range: Last 12 weeks
Breakdown: By customer type: derive new vs returning from the User.Lifetime value computed attribute (Lifetime value > 0 at the time of the order = returning, otherwise new) OR from User.orders_count.
Compare: Previous period (previous 12 weeks)
Chart type: Multi-line chart with all three series, separate axes for AOV/Price-per-Unit ($) and Units-per-Order (#)
Annotations:
- Add a callout showing the period-over-period change in each component (AOV, Units/Order, Price/Unit).
- Flag any week where AOV moved >5%: and identify whether the move came from units, price, or both.
- Highlight the AOV gap between new and returning customers (returning typically 1.5: 2× new for healthy DTC).
AOV moving via price suggests merchandising/pricing impact; AOV moving via units suggests bundling/cross-sell impact.
Taxonomy notes:
- Placed order has total_price (Shopify) and items (flattened: product_id, title, quantity, price, sku). "order_total" is not a real property.
- Users.Lifetime value and User.orders_count (system-computed) are real attributes.
