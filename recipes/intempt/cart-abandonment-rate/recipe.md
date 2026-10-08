---
description: Shows what share of shoppers who add to cart never order, week by week and by device, against the 70% industry line.
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

# Cart abandonment rate

Slash command: /cart-abandonment-rate

## Step 1: Track carts that never convert

Create an Insights report called "Cart Abandonment Rate".
Series A: Event "cart_created", aggregation: Count Unique Users
Series B: Event "order_created", aggregation: Count Unique Users
Formula: ((A - B) / A) × 100, unit: %, label: "Abandonment Rate"
Time granularity: Weekly
Time range: Last 8 weeks
Breakdown: By "device_type" attribute on the Users object (desktop, mobile, tablet)
Compare: Previous period (previous 8 weeks)
Chart type: Line chart with previous-period overlay
Annotations:
- Add a horizontal benchmark line at 70% (industry baseline; abandonment above this is losing material revenue).
- Highlight any week where abandonment rate exceeded the previous period by 5 percentage points or more.
Identify which device type has the highest abandonment rate and whether the gap between mobile and desktop is widening over time.
Taxonomy notes:
- "cart_created" and "order_created" are canonical events. cart_created carries cart_id and items.
- Users object has device_type as an enum attribute.
