---
frontmatter_id: order-status-flow
slash_command: /order-status-flow
description: Emails a daily digest of order volume alongside how many get fulfilled, refunded or cancelled, the rate for each,
  and flags against healthy benchmarks.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a daily digest of orders created, fulfilled, refunded and cancelled with their rates, the in-flight backlog
    and benchmark flags for the ops team.
  parameters:
  - name: compare_period
    type: duration
    label: Comparison period (prior period)
    default: 30 d
    required: false
  - name: fulfillment_healthy_rate
    type: number
    label: Healthy fulfillment rate (%)
    default: 95
    required: false
  - name: fulfillment_backlog_rate
    type: number
    label: Backlog warning fulfillment rate (%)
    default: 90
    required: false
  - name: refund_healthy_rate
    type: number
    label: Healthy refund rate (%)
    default: 3
    required: false
  - name: refund_high_rate
    type: number
    label: High refund rate (%)
    default: 10
    required: false
  - name: cancellation_healthy_rate
    type: number
    label: Healthy cancellation rate (%)
    default: 2
    required: false
  - name: cancellation_high_rate
    type: number
    label: High cancellation rate (%)
    default: 5
    required: false
  - name: fulfillment_drop_points
    type: number
    label: Fulfillment rate drop that triggers a flag (points vs trailing 7-day average)
    default: 5
    required: false
  - name: order_maturity_window
    type: duration
    label: Minimum order age before counting toward fulfillment rate
    default: 48 h
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
  - slot: order_fulfilled_event
    kind: event
    meaning: An order was fulfilled
  - slot: order_refunded_event
    kind: event
    meaning: An order was refunded
  - slot: order_cancelled_event
    kind: event
    meaning: An order was cancelled
  steps:
  - id: s1
    builds: automation
    uses:
    - placed_order_event
    - order_fulfilled_event
    - order_refunded_event
    - order_cancelled_event
    - compare_period
    - fulfillment_healthy_rate
    - fulfillment_backlog_rate
    - refund_healthy_rate
    - refund_high_rate
    - cancellation_healthy_rate
    - cancellation_high_rate
    - fulfillment_drop_points
    - order_maturity_window
    - digest_recipients
    instruction: 'Build an automation that runs every day at 08:00 on a schedule. Each run it analyzes orders in the last
      24 hours, the last 7 days and the last {compare_period} against the {compare_period} before, and writes these figures:
      orders created ({placed_order_event}), fulfilled ({order_fulfilled_event}), refunded ({order_refunded_event}), cancelled
      ({order_cancelled_event}); fulfillment rate %, fulfilled / created, counting only orders older than {order_maturity_window};
      refund rate %; cancellation rate %; the backlog, created minus fulfilled, over the last 7 days. Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. When the fulfillment rate is {fulfillment_drop_points}
      points or more below its 7-day average, the email''s first line says so. The email rates each figure: fulfillment healthy
      at {fulfillment_healthy_rate}%+, backlog below it, systemic issue below {fulfillment_backlog_rate}%; refunds healthy
      under {refund_healthy_rate}%, high over {refund_high_rate}%; cancellations healthy under {cancellation_healthy_rate}%,
      high over {cancellation_high_rate}%. Nothing else is sent.'
---

# Order status flow

Slash command: /order-status-flow

## Step 1: Email the daily order status digest

Build an automation that runs every day at 08:00 on a schedule. Each run it analyzes orders in the last 24 hours, the last 7 days and the last 30 d against the 30 d before, and writes these figures: orders created (placed order event), fulfilled (order fulfilled event), refunded (order refunded event), cancelled (order cancelled event); fulfillment rate %, fulfilled / created, counting only orders older than 48 h; refund rate %; cancellation rate %; the backlog, created minus fulfilled, over the last 7 days. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. When the fulfillment rate is 5 points or more below its 7-day average, the email's first line says so. The email rates each figure: fulfillment healthy at 95%+, backlog below it, systemic issue below 90%; refunds healthy under 3%, high over 10%; cancellations healthy under 2%, high over 5%. Nothing else is sent.
