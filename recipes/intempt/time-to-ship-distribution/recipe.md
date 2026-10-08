---
description: Shows order fulfillment time from order creation to fulfillment, with median, 75th, and 95th percentile callouts.
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

# Time to ship

Slash command: /time-to-ship-distribution

## Step 1: Measure how fast orders ship

Create an Insights report called "Time-to-Ship Distribution".
Series A: Distribution histogram of fulfillment-time per order: computed by Lovable as (order_fulfilled.created_at − order_created.created_at) for each fulfilled order, joined on order_id
Buckets for Series A: 0 (24h / 24) 48h / 48 (72h / 3) 5 days / 5 (7 days / 7) 14 days / 14+ days
Series B: Cumulative percentage: what % of orders ship within X time
Time range: Last 30 days of order_fulfilled events (use the fulfillment date for cohorting, since orders fulfilled in the period may have been created before)
Breakdown: By "source" property on order_fulfilled (warehouse, fulfillment center, or 3PL: varies by integration) OR by Users.country for geographic distribution analysis
Compare: Previous period (prior 30 days)
Chart type: Histogram chart with Series A as the bar distribution, Series B as a cumulative line overlay; secondary callouts for median, p75, p95 fulfillment times
Annotations:
- Add benchmarks: top-quartile DTC ships within 24h (Amazon-trained customer expectations); 24: 48h is industry median; >72h to first ship is competitively weak.
- Flag if the share shipping within 24h dropped >10 percentage points vs. previous period (operational regression).
- Flag the long tail: what % of orders take >7 days to ship? Anything above 5% is a fulfillment-process problem and a customer-experience issue (these customers are likely to complain or refund).
- Highlight the median and p75 times as headline numbers: the median is the typical experience, p75 is the experience customers complain about, p95 is the experience that drives bad reviews.
- Surface any source/warehouse with materially worse times than others: single facility issues are easier to fix than systemic ones.
Use case: post-purchase customer experience is increasingly a competitive lever. Brands that ship fast retain better. This recipe makes the actual time-to-ship distribution visible (most ops dashboards only show "average ship time" which obscures the long tail).
Taxonomy notes:
- order_created.created_at and order_fulfilled.created_at are both real datetime properties; the join is on order_id.
- order_fulfilled.source is a real property (warehouse / 3PL identifier; varies by integration).
- This recipe excludes orders where fulfillment hasn't yet occurred (no order_fulfilled event). For an "in-flight" backlog view, pair this recipe with order-status-flow.
