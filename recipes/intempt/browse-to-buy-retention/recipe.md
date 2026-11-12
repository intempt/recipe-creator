---
frontmatter_id: browse-to-buy-retention
slash_command: /browse-to-buy-retention
description: Measures how long first time visitors take to place an order, by acquisition source, so you can tell fast converting channels from slow ones.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows how long first-time visitors take to place an order, broken down by acquisition source, to spot fast and
    slow converting channels.
  parameters:
  - name: cohort_granularity
    type: enum
    label: Cohort granularity
    default: weekly
    required: false
    options:
    - daily
    - weekly
    - monthly
  - name: time_range
    type: duration
    label: Cohort time range
    default: 12 w
    required: false
  - name: breakdown_top_n
    type: number
    label: Number of top sources to break down
    default: 6
    required: false
  - name: benchmark_w1_rate
    type: number
    label: Typical W1 first-purchase rate benchmark (%)
    default: 5
    required: false
  - name: impulse_w1_rate
    type: number
    label: Impulse-buy W1 first-purchase rate benchmark (%)
    default: 10
    required: false
  - name: w12_flag_threshold
    type: number
    label: W12 browse-to-buy gap flag threshold (%)
    default: 8
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A visitor started a session on the site or app
    properties:
    - name: customer_id
      type: text
      meaning: Identifier of the customer who started the session
      optional: false
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: customer_id
      type: text
      meaning: Identifier of the customer who placed the order
      optional: false
  - slot: utm_source_attribute
    kind: attribute
    meaning: The UTM source that brought the user to the site
  steps:
  - id: s1
    builds: report
    uses:
    - session_start_event
    - placed_order_event
    - utm_source_attribute
    - cohort_granularity
    - time_range
    - breakdown_top_n
    - benchmark_w1_rate
    - impulse_w1_rate
    - w12_flag_threshold
    instruction: 'Create a retention report named "Browse to Buy Retention". Anchor event: each user''s first {session_start_event}
      (earliest per customer_id). Return event: {placed_order_event}. Cohort granularity: {cohort_granularity}. Time range:
      last {time_range}. Breakdown: by {utm_source_attribute}, top {breakdown_top_n} sources. Compare against the previous
      period (prior {time_range} of cohorts). Chart: retention curve plus cohort table with W1, W2, W4, W8 and W12 columns.
      Annotations: add benchmarks showing a typical W1 first-purchase rate of {benchmark_w1_rate}% for considered-purchase
      DTC and {impulse_w1_rate}% or higher for impulse-buy. Flag any source whose W12 first-purchase rate is below {w12_flag_threshold}%
      as a browse-to-buy gap. Highlight the source with the fastest first-purchase rate (steepest W1 conversion). Highlight
      the source with the highest W12 conversion (best overall, even if slower). Surface which sources produce fast converters
      and which produce slow converters.'
---

# Browse to buy retention

Slash command: /browse-to-buy-retention

## Step 1: Track first visit to first order

Create a Retention report called "Browse to Buy Retention".
Anchor event: Session start (each user's first Session start)
Return event: Placed order
Cohort granularity: Weekly
Time range: Last 12 weeks
Breakdown: By Users.UTM source (top 6 sources)
Compare: Previous period (prior 12 weeks of cohorts)
Chart type: Retention curve plus cohort table with W1 / W2 / W4 / W8 / W12 columns
Annotations:
- Add benchmarks: W1 first-purchase rate of 5% is typical for considered-purchase DTC, 10%+ for impulse-buy.
- Flag any source where W12 first-purchase rate is below 8% (browse-to-buy gap).
- Highlight the source with the fastest first-purchase rate (steepest W1 conversion).
- Highlight the source with the highest W12 conversion (best overall, even if slower).
Surface which sources produce "fast converters" vs "slow converters."
Taxonomy notes:
- Session start and Placed order are canonical. Users.UTM source is canonical.
- "first session" per-user is determined by the earliest Session start for that customer_id.
