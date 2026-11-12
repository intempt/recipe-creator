---
frontmatter_id: time-to-ship-distribution
slash_command: /time-to-ship-distribution
description: Shows order fulfillment time from order creation to fulfillment, with median, 75th, and 95th percentile callouts.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows how long orders take from creation to fulfillment, with a histogram, cumulative share, and median, p75 and
    p95 callouts to expose the long tail.
  parameters:
  - name: window
    type: duration
    label: Analysis window
    default: 30 d
    required: false
  - name: comparison_window
    type: duration
    label: Comparison period
    default: 30 d
    required: false
  - name: fast_ship_threshold
    type: duration
    label: Fast-ship threshold
    default: 24 h
    required: false
  - name: long_tail_threshold
    type: duration
    label: Long-tail threshold
    default: 7 d
    required: false
  - name: long_tail_alert_pct
    type: number
    label: Long-tail alert share (%)
    default: 5
    required: false
  - name: fast_share_drop_alert_pts
    type: number
    label: Fast-ship share drop alert (percentage points)
    default: 10
    required: false
  - name: breakdown_property
    type: enum
    label: Breakdown dimension
    default: source
    required: false
    options:
    - source
    - country
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: order_id
      type: string
      meaning: Unique order identifier used to join with fulfillment
      optional: false
    - name: created_date
      type: date
      meaning: When the order was created
      optional: false
  - slot: order_fulfilled_event
    kind: event
    meaning: An order was fulfilled and shipped
    properties:
    - name: order_id
      type: string
      meaning: Unique order identifier used to join with the placed order
      optional: false
    - name: created_date
      type: date
      meaning: When the fulfillment was created
      optional: false
    - name: source
      type: string
      meaning: Warehouse, fulfillment center or 3PL that fulfilled the order
      optional: true
  - slot: customer_country
    kind: attribute
    meaning: The country of the customer
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - placed_order_event
    - order_fulfilled_event
    - customer_country
    - window
    - comparison_window
    - fast_ship_threshold
    - long_tail_threshold
    - long_tail_alert_pct
    - fast_share_drop_alert_pts
    - breakdown_property
    instruction: 'Create an Insights report titled "Time-to-Ship Distribution". Series A: histogram of fulfillment time per
      order, computed as the {order_fulfilled_event.created_date} minus the {placed_order_event.created_date} for each fulfilled
      order, joined on {order_fulfilled_event.order_id} = {placed_order_event.order_id}. Buckets: 0 to {fast_ship_threshold};
      {fast_ship_threshold} to 48 h; 48 h to 72 h; 3 to 5 days; 5 to 7 days; 7 to 14 days; 14+ days. Series B: cumulative
      percentage of orders shipped within each time X. Time range: last {window} of {order_fulfilled_event} events, cohorted
      by the fulfillment date, since orders fulfilled in the period may have been created earlier. Breakdown: by {order_fulfilled_event.source}
      or by {customer_country} as selected with {breakdown_property}. Compare against the previous {comparison_window}. Chart
      type: histogram with Series A as bars and Series B as a cumulative line overlay. Show headline callouts for the median,
      75th percentile and 95th percentile fulfillment times. Annotations: (1) benchmark note that top-quartile direct-to-consumer
      brands ship within {fast_ship_threshold}, 48 h is the industry median, and more than 72 h to first ship is competitively
      weak. (2) Flag if the share shipped within {fast_ship_threshold} dropped by more than {fast_share_drop_alert_pts} percentage
      points versus the previous period, as an operational regression. (3) Flag the long tail: report the percentage of orders
      taking longer than {long_tail_threshold} to ship; flag any value above {long_tail_alert_pct}% as a fulfillment-process
      and customer-experience problem. (4) Highlight the median as the typical experience, p75 as the experience customers
      complain about, and p95 as the experience that drives bad reviews. (5) Surface any source or warehouse with materially
      worse times than the others, since single-facility issues are easier to fix than systemic ones. Orders with no Order
      fulfilled event are excluded; pair with an in-flight order status view for backlog.'
---

# Time to ship

Slash command: /time-to-ship-distribution

## Step 1: Measure how fast orders ship

Create an Insights report called "Time-to-Ship Distribution".
Series A: Distribution histogram of fulfillment-time per order: computed by Lovable as (Order fulfilled.Created date − Placed order.Created date) for each fulfilled order, joined on order_id
Buckets for Series A: 0 (24h / 24) 48h / 48 (72h / 3) 5 days / 5 (7 days / 7) 14 days / 14+ days
Series B: Cumulative percentage: what % of orders ship within X time
Time range: Last 30 days of Order fulfilled events (use the fulfillment date for cohorting, since orders fulfilled in the period may have been created before)
Breakdown: By "source" property on Order fulfilled (warehouse, fulfillment center, or 3PL: varies by integration) OR by Users.country for geographic distribution analysis
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
- Placed order.Created date and Order fulfilled.Created date are both real datetime properties; the join is on order_id.
- Order fulfilled.source is a real property (warehouse / 3PL identifier; varies by integration).
- This recipe excludes orders where fulfillment hasn't yet occurred (no Order fulfilled event). For an "in-flight" backlog view, pair this recipe with order-status-flow.
