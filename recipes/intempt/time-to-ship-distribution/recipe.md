---
frontmatter_id: time-to-ship-distribution
slash_command: /time-to-ship-distribution
description: 'Emails a weekly time-to-ship digest: median, 75th and 95th percentile time from order to fulfillment, the share
  shipped fast, the long tail of slow orders and the slowest sources.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a weekly digest of how long orders take from creation to fulfillment, with median, p75 and p95, the fast-ship
    share and the long tail.
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
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
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
    builds: automation
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
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the orders with
      an {order_fulfilled_event} event in the last {window}, matched to their {placed_order_event} event on {order_fulfilled_event.order_id}
      = {placed_order_event.order_id}, where time to ship is {order_fulfilled_event.created_date} minus {placed_order_event.created_date},
      and writes these figures: the median, 75th percentile and 95th percentile time to ship, for the last {window} and the
      {comparison_window} before it; the share of orders shipped within {fast_ship_threshold}, for both windows; the share
      of orders that took longer than {long_tail_threshold}; the median time to ship by {order_fulfilled_event.source} and
      by {customer_country} when set, slowest first. When the share shipped within {fast_ship_threshold} fell by more than
      {fast_share_drop_alert_pts} percentage points, or the share above {long_tail_threshold} is above {long_tail_alert_pct}%,
      the email''s first line says so. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Time to ship

Slash command: /time-to-ship-distribution

## Step 1: Email the weekly time-to-ship digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the orders with an order fulfilled event event in the last 30 d, matched to their placed order event event on order id = order id, where time to ship is created date minus created date, and writes these figures: the median, 75th percentile and 95th percentile time to ship, for the last 30 d and the 30 d before it; the share of orders shipped within 24 h, for both windows; the share of orders that took longer than 7 d; the median time to ship by source and by customer country when set, slowest first. When the share shipped within 24 h fell by more than 10 percentage points, or the share above 7 d is above 5%, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
