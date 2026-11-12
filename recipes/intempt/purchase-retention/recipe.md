---
frontmatter_id: purchase-retention
slash_command: /purchase-retention
description: Shows what share of first time buyers come back to buy again, by month and by the category they bought first.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows what share of first-time buyers place a repeat order, by acquisition month and first-purchase category, with
    time-to-second-purchase timing for replenishment journeys.
  parameters:
  - name: time_range
    type: duration
    label: Analysis time range
    default: 12 m
    required: false
  - name: cohort_granularity
    type: enum
    label: Cohort granularity
    default: monthly
    required: false
    options:
    - monthly
    - weekly
    - quarterly
  - name: repeat_rate_flag_threshold
    type: number
    label: Flag categories with M6 repeat rate below (%)
    default: 15
    required: false
  - name: cohort_drop_threshold
    type: number
    label: Flag cohorts whose M3 repeat rate dropped more than (percentage points)
    default: 5
    required: false
  - name: high_replenishment_threshold
    type: number
    label: Highlight categories with M3 repeat rate above (%)
    default: 30
    required: false
  - name: benchmark_repeat_rate
    type: number
    label: Benchmark share of first-time DTC buyers making a 2nd purchase (%)
    default: 27
    required: false
  - name: top_quartile_repeat_rate
    type: number
    label: Top-quartile benchmark repeat rate (%)
    default: 45
    required: false
  - name: compare_period
    type: enum
    label: Comparison period
    default: previous_period
    required: false
    options:
    - previous_period
    - none
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: customer_id
      type: string
      meaning: Identifier of the customer who placed the order
      optional: false
    - name: items.product_id
      type: string
      meaning: Product identifiers of the items in the order
      optional: false
    - name: order_timestamp
      type: date
      meaning: When the order was placed
      optional: false
  - slot: products_catalog
    kind: product_feed
    meaning: Product catalog that maps each product to its category
  steps:
  - id: s1
    builds: report
    uses:
    - placed_order_event
    - products_catalog
    - time_range
    - cohort_granularity
    - compare_period
    - benchmark_repeat_rate
    - top_quartile_repeat_rate
    - repeat_rate_flag_threshold
    - cohort_drop_threshold
    - high_replenishment_threshold
    instruction: 'Create a retention report titled "Purchase Retention". Anchor event: {placed_order_event}, counted per customer
      as their first occurrence, cohorting users by month of first purchase. Return event: {placed_order_event}, any subsequent
      occurrence. Cohort granularity: {cohort_granularity}. Time range: last {time_range}. Breakdown: by first-purchase product
      category, derived from the first order''s {placed_order_event.items.product_id} resolved against {products_catalog}
      to its category. The first order is the earliest {placed_order_event} per {placed_order_event.customer_id}. Comparison:
      {compare_period}, using the prior equal period of cohorts. Chart: retention curve plus a cohort table with M1, M3, M6
      and M12 columns. Add a secondary view showing the distribution of days between first and second purchase, bucketed 0-7,
      8-30, 31-90 and 91+ days. Annotations: add a benchmark note that {benchmark_repeat_rate}% of first-time DTC buyers make
      a second purchase, and that brands at {top_quartile_repeat_rate}%+ are top quartile. Flag any category whose M6 repeat
      rate is below {repeat_rate_flag_threshold}% as a one-time-purchase pattern. Flag any cohort whose M3 repeat rate fell
      more than {cohort_drop_threshold} percentage points versus the prior cohort as a recent acquisition-quality drop. Highlight
      any category whose M3 repeat rate is above {high_replenishment_threshold}% as a candidate for subscribe-and-save. Surface
      the median days from first to second purchase per category as the suggested delay for replenishment journeys.'
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
