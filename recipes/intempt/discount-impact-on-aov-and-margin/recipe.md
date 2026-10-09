---
description: Tracks orders that applied a discount code and their basket totals, code by code.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
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
