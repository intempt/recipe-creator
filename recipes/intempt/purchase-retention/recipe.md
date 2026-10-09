---
description: Shows what share of first time buyers come back to buy again, by month and by the category they bought first.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
  - media
---

# Repeat purchase retention

Slash command: /purchase-retention

## Step 1: Track buyers back for more

Create a Retention report called "Purchase Retention".
Anchor event: Placed order (per user, scope: their first Placed order to cohort by month of first purchase)
Return event: Placed order (any subsequent order)
Cohort granularity: Monthly
Time range: Last 12 months
Breakdown: By the first-purchase product category: derived from the first order's items.product_id resolved via Products object
Compare: Previous period (prior 12 months of cohorts)
Chart type: Retention curve plus cohort table with M1 / M3 / M6 / M12 columns
Also include a secondary view: "Time from 1st to 2nd purchase" distribution: histogram of days-between, bucketed into 0-7 / 8-30 / 31-90 / 91+ days.
Annotations:
- Add benchmarks: 27% of first-time DTC buyers make a 2nd purchase ever; brands at 45%+ are top-quartile.
- Flag any category where M6 repeat rate is below 15% (one-time-purchase pattern).
- Flag any cohort where M3 repeat rate dropped >5 percentage points vs. prior cohort (recent acquisition-quality drop).
- Highlight categories with M3 repeat rate > 30% (high natural-replenishment products: candidates for subscribe-and-save).
Surface the median time from 1st to 2nd purchase per category: this is the right delay for replenishment journeys.
Taxonomy notes:
- "first_order_created" as an event does not exist. "First order" is computed as the earliest Placed order per customer_id.
- "first_purchase_category" is derived from first order's items.product_id to Products.category.
