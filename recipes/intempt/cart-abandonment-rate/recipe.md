---
frontmatter_id: cart-abandonment-rate
slash_command: /cart-abandonment-rate
description: Builds a segment of shoppers who add to cart but never order, and emails a weekly digest of the cart abandonment
  rate by device against the 70% benchmark.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Builds the abandoned-cart shoppers segment and emails a weekly digest of the cart abandonment rate by device, with
    a 70% benchmark and a flag on sharp rises.
  parameters:
  - name: abandon_window
    type: duration
    label: Days since adding to cart with no order
    default: 7 d
    required: false
  - name: lookback_window
    type: duration
    label: Weeks of weekly rates in the digest
    default: 8 w
    required: false
  - name: benchmark_rate
    type: number
    label: Benchmark abandonment rate (%)
    default: 70
    required: false
  - name: alert_threshold_pp
    type: number
    label: Rise over the previous week that gets flagged (percentage points)
    default: 5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: cart_created_event
    kind: event
    meaning: A customer created a cart by adding items to it
    properties:
    - name: cart_id
      type: string
      meaning: Identifier of the cart
      optional: true
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
  - slot: device_type
    kind: attribute
    meaning: The device type a user shops on (desktop, mobile, tablet)
  steps:
  - id: s1
    builds: segment
    uses:
    - cart_created_event
    - placed_order_event
    - abandon_window
    instruction: 'Build a new segment of users named "Abandoned Cart Shoppers": users who did {cart_created_event} in the
      last {abandon_window} and did not do {placed_order_event} after their latest {cart_created_event}.'
  - id: s2
    builds: automation
    uses:
    - s1
    - cart_created_event
    - placed_order_event
    - device_type
    - lookback_window
    - benchmark_rate
    - alert_threshold_pp
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {cart_created_event}
      and writes these figures: the cart abandonment rate for the last 7 days, the share of unique users who did {cart_created_event}
      and did not do {placed_order_event} afterwards in that week, next to the 7 days before; the same rate split by {device_type};
      the weekly rate for each of the last {lookback_window}; the gap between the mobile and desktop rate this week and 4
      weeks ago; the number of users in the segment from "Find shoppers who left their cart". When this week''s rate is above
      {benchmark_rate}% or more than {alert_threshold_pp} percentage points above the week before, the email''s first line
      says so. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else
      is sent.'
---

# Cart abandonment rate

Slash command: /cart-abandonment-rate

## Step 1: Find shoppers who left their cart

Build a new segment of users named "Abandoned Cart Shoppers": users who did cart created event in the last 7 d and did not do placed order event after their latest cart created event.

## Step 2: Email the weekly abandonment digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did cart created event and writes these figures: the cart abandonment rate for the last 7 days, the share of unique users who did cart created event and did not do placed order event afterwards in that week, next to the 7 days before; the same rate split by device type; the weekly rate for each of the last 8 w; the gap between the mobile and desktop rate this week and 4 weeks ago; the number of users in the segment from "Find shoppers who left their cart". When this week's rate is above 70% or more than 5 percentage points above the week before, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
