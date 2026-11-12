---
frontmatter_id: discount-impact-on-aov-and-margin
slash_command: /discount-impact-on-aov-and-margin
description: Tracks orders that applied a discount code and their basket totals, code by code.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows whether discount codes grow order value by comparing average basket totals with and without a discount, code
    by code, plus net revenue impact and discount cost share.
  parameters:
  - name: time_granularity
    type: enum
    label: Time granularity
    default: week
    required: false
    options:
    - day
    - week
    - month
  - name: time_range
    type: duration
    label: Time range
    default: 12 w
    required: false
  - name: comparison_window
    type: duration
    label: Comparison period
    default: 12 w
    required: false
  - name: top_codes_limit
    type: number
    label: Number of top discount codes to break down by
    default: 10
    required: false
  - name: healthy_discount_cost_pct
    type: number
    label: Healthy discount cost threshold (% of revenue)
    default: 15
    required: false
  - name: over_reliance_discount_cost_pct
    type: number
    label: Over-reliance discount cost threshold (% of revenue)
    default: 20
    required: false
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order basket total
      optional: false
  - slot: discount_applied_event
    kind: event
    meaning: A discount code was applied to an order
    properties:
    - name: amount
      type: number
      meaning: Discount amount applied
      optional: false
    - name: code
      type: string
      meaning: Discount code used
      optional: false
    - name: order_id
      type: string
      meaning: Order the discount was applied to
      optional: false
  - slot: total_revenue_source
    kind: attribute
    meaning: Total revenue of the business over the trailing period
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - placed_order_event
    - discount_applied_event
    - time_granularity
    - time_range
    - comparison_window
    - top_codes_limit
    instruction: 'Create an Insights report titled "Discount Impact on AOV". Series A: event {placed_order_event} filtered
      to orders that have a linked {discount_applied_event} via order_id, aggregation average of {placed_order_event.total_price},
      label "AOV with Discount". Series B: event {placed_order_event} filtered to orders with NO linked {discount_applied_event},
      aggregation average of {placed_order_event.total_price}, label "AOV without Discount". Series C: computed Series A minus
      Series B, unit dollars, label "AOV Lift from Discount". Series D: computed sum of {discount_applied_event.amount} across
      all discounted orders, unit dollars, label "Total Discount Cost". Series E: computed (sum of {placed_order_event.total_price}
      for discounted orders minus Series D) minus (count of discounted orders times Series B), label "Net Revenue Impact";
      this answers whether discounts grew the pie or shifted it. Time granularity {time_granularity}, time range {time_range},
      compare to previous period of {comparison_window}. Break down by {discount_applied_event.code}, top {top_codes_limit}
      codes by usage volume. Chart: dual-axis, left axis AOV in dollars showing Series A and Series B as side-by-side bars
      per code; right axis Series E as a line.'
---

# Discount impact on order value

Slash command: /discount-impact-on-aov-and-margin

## Step 1: Test whether discounts grow baskets

Create an Insights report called "Discount Impact on AOV".
Series A: Event "Placed order" filtered to orders with a linked discount_applied event (orders with discount), aggregation: Average of total_price, label: "AOV with Discount"
Series B: Event "Placed order" filtered to orders with NO linked discount_applied event, aggregation: Average of total_price, label: "AOV without Discount"
Series C: Computed: Series A − Series B, unit: $, label: "AOV Lift from Discount"
Series D: Computed: Sum of discount_applied.amount across all discounted orders, unit: $, label: "Total Discount Cost"
Series E: Computed: (Sum of total_price for discounted orders − Series D) − (count of discounted orders × Series B), label: "Net Revenue Impact": answers: did discounts grow the pie or just shift it?
Time granularity: Weekly
Time range: Last 12 weeks
Breakdown: By "code" property on discount_applied (top 10 codes by usage volume)
Compare: Previous period (prior 12 weeks)
Chart type: Dual-axis: left axis AOV ($) showing Series A and Series B side-by-side bars per discount code, right axis Series E (net revenue impact) as a line
Annotations:
- Flag any discount code where AOV with discount is LOWER than AOV without (the discount is being used by lower-intent buyers: pure margin loss with no basket-growth benefit).
- Flag any discount code with negative Series E (Net Revenue Impact): this code is cannibalizing full-price demand more than it's creating new orders.
- Highlight discount codes where AOV with discount > AOV without (the discount actually grows the basket: keep these and scale).
- Surface the trailing-12-week total discount cost as a % of total revenue (industry benchmark: <15% for healthy DTC; >20% indicates over-reliance on promotions).
Use case: the cannibalization question is the most important and most-avoided ecommerce analysis. Most brands track discount usage but never measure whether discounts CREATE orders that wouldn't otherwise happen, vs. just SHIFTING demand to discounted moments. This recipe makes the distinction visible.
Taxonomy notes:
- discount_applied has amount, code, currency, customer_id, order_id, type (and amount_off / percent_off depending on source).
- Placed order has total_price (Shopify) and items.
- Linking an order to a discount uses discount_applied.order_id.
