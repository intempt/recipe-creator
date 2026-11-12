---
frontmatter_id: first-purchase-cohort-ltv-curve
slash_command: /first-purchase-cohort-ltv-curve
description: Compare revenue trends across monthly customer cohorts over calendar time. Use the report to see how cohort revenue changes as calendar dates progress.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows how each monthly customer cohort's cumulative revenue per member grows by cohort age, so you can compare
    lifetime value across cohorts and acquisition channels.
  parameters:
  - name: cohort_window
    type: duration
    label: Cohort window (how far back to include monthly cohorts)
    default: 12 months
    required: false
  - name: ltv_checkpoint_early
    type: number
    label: Early LTV checkpoint month
    default: 6
    required: false
  - name: ltv_checkpoint_late
    type: number
    label: Late LTV checkpoint month
    default: 12
    required: false
  - name: flattening_check_month
    type: number
    label: Month by which flattening LTV growth is checked
    default: 3
    required: false
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Total price of the order
      optional: false
  - slot: user_acquisition_source
    kind: attribute
    meaning: The user's first-touch acquisition source (UTM source) stored on the user profile
  steps:
  - id: s1
    builds: report
    uses:
    - placed_order_event
    - user_acquisition_source
    - cohort_window
    - ltv_checkpoint_early
    - ltv_checkpoint_late
    - flattening_check_month
    instruction: 'Create an Insights report titled "First-Purchase Cohort LTV Curve". Series A: count sum of {placed_order_event.total_price}
      per user, cumulative from each user''s first {placed_order_event} event. Series B: Series A divided by cohort size,
      unit $, labeled "Cumulative Revenue per Cohort Member". Cohort: monthly cohorts defined by the month of each user''s
      first {placed_order_event} event, covering the last {cohort_window}; flag the most recent cohorts with an "incomplete
      cohort" label. Breakdown: by {user_acquisition_source}. Chart: multi-line, one line per cohort, X axis cohort age in
      months (0 to 12), Y axis cumulative revenue per cohort member. Annotations: highlight the highest and lowest LTV cohort
      at month {ltv_checkpoint_early} and month {ltv_checkpoint_late}; flag any cohort whose LTV curve goes flat by month
      {flattening_check_month} to {ltv_checkpoint_early} as a likely one-time-buyer cohort; highlight channels whose LTV is
      rising across recent cohorts.'
---

# First purchase LTV curve

Slash command: /first-purchase-cohort-ltv-curve

## Step 1: Plot revenue per cohort by age

Create an Insights report called "First-Purchase Cohort LTV Curve".
Series A: Event "Placed order", aggregation: Sum of "total_price", scoped per user, cumulative from each user's first Placed order
Series B: Computed: Series A / cohort size, unit: $, label: "Cumulative Revenue per Cohort Member"
Cohort: Monthly cohort defined by month of first Placed order (each user's first Placed order event determines their cohort)
Time range: Last 12 months of cohorts (allow some cohorts to have shorter LTV tails: surface "incomplete cohort" labels for the most recent ones)
Breakdown: By Users.UTM source (the user's first-touch acquisition channel, from the Users object)
Chart type: Multi-line chart: each line is a cohort, X axis is cohort age in months (0, 1, 2, ..., 12), Y axis is cumulative revenue per cohort member
Annotations:
- Highlight the highest-LTV cohort and lowest-LTV cohort at month 6 and month 12.
- Flag any cohort where LTV growth flattens prematurely (LTV-curve "going horizontal" by month 3-6 indicates a one-time-buyer cohort).
- Highlight channels where cohort LTV is increasing across recent cohorts (acquisition quality improving).
Taxonomy notes:
- "First purchase" is determined per-user by the earliest Placed order event for that customer_id.
- Users.UTM source is a real first-touch attribution attribute on the Users object.
- LTV is cumulative sum of Placed order.total_price per user from first purchase onward.
