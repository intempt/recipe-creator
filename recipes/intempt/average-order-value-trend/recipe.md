---
description: Tracks average order value weekly and splits the movement into how many items people buy versus what they pay per item, for new and returning customers.
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

# Average order value trend

Slash command: /average-order-value-trend

## Step 1: Break down AOV week by week

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
