---
frontmatter_id: cart-abandonment-rate
slash_command: /cart-abandonment-rate
description: Shows what share of shoppers who add to cart never order, week by week and by device, against the 70% industry line.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows the weekly share of shoppers who add to cart but never order, broken down by device, with a 70% benchmark
    and alerts for sharp week-over-week rises.
  parameters:
  - name: time_granularity
    type: enum
    label: Time granularity
    default: weekly
    required: false
    options:
    - daily
    - weekly
    - monthly
  - name: lookback_window
    type: duration
    label: Lookback window
    default: 8 w
    required: false
  - name: benchmark_rate
    type: number
    label: Benchmark abandonment rate (%)
    default: 70
    required: false
  - name: alert_threshold_pp
    type: number
    label: Alert threshold over previous period (percentage points)
    default: 5
    required: false
  requirements:
  - slot: cart_created_event
    kind: event
    meaning: A customer created a cart by adding items to it
    properties:
    - name: cart_id
      type: string
      meaning: Identifier of the cart
      optional: false
    - name: items
      type: text
      meaning: Items placed in the cart
      optional: false
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
  - slot: device_type
    kind: attribute
    meaning: The device type a user shops on (desktop, mobile, tablet)
  steps:
  - id: s1
    builds: report
    uses:
    - cart_created_event
    - placed_order_event
    - device_type
    - time_granularity
    - lookback_window
    - benchmark_rate
    - alert_threshold_pp
    instruction: 'Create an Insights report called "Cart Abandonment Rate". Series A: {cart_created_event}, aggregation: count
      of unique users. Series B: {placed_order_event}, aggregation: count of unique users. Formula: ((A - B) / A) × 100, unit:
      %, label: "Abandonment Rate". Time granularity: {time_granularity}. Time range: last {lookback_window}. Breakdown: by
      {device_type} on the users object (desktop, mobile, tablet). Compare: previous period (previous {lookback_window}).
      Chart type: line chart with previous-period overlay. Annotations: add a horizontal benchmark line at {benchmark_rate}%.
      Highlight any week where abandonment rate exceeded the previous period by {alert_threshold_pp} percentage points or
      more. Identify which device type has the highest abandonment rate and whether the gap between mobile and desktop is
      widening over time.'
---

# Cart abandonment rate

Slash command: /cart-abandonment-rate

## Step 1: Track carts that never convert

Create an Insights report called "Cart Abandonment Rate".
Series A: Event "Cart created", aggregation: Count Unique Users
Series B: Event "Placed order", aggregation: Count Unique Users
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
- "Cart created" and "Placed order" are canonical events. Cart created carries cart_id and items.
- Users object has device_type as an enum attribute.
