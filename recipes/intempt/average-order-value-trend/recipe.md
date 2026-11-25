---
frontmatter_id: average-order-value-trend
slash_command: /average-order-value-trend
description: Emails average order value weekly and splits the movement into how many items people buy versus what they pay
  per item, for new and returning customers.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a weekly digest of average order value split into units per order and price per unit, for new and returning
    customers, flagging large weekly swings.
  parameters:
  - name: trend_window
    type: duration
    label: Longer window for the average
    default: 12 w
    required: false
  - name: movement_threshold_pct
    type: number
    label: Weekly AOV change that is flagged (%)
    default: 5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total
      optional: false
    - name: items
      type: string
      meaning: Line items in the order
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - order_placed_event
    - trend_window
    - movement_threshold_pct
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes {order_placed_event}
      by customers and writes these figures for the last 7 days, the 7 days before, and the weekly average over the last {trend_window}:
      average order value, the average {order_placed_event.total_price}; units per order, the average number of line items
      in {order_placed_event.items}; price per unit, average order value divided by units per order; the same three for new
      customers (their first {order_placed_event}) and for returning customers (they did {order_placed_event} before). The
      first line says so when average order value moved more than {movement_threshold_pct}% against the 7 days before, and
      whether units, price or both drove it. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Average order value trend

Slash command: /average-order-value-trend

## Step 1: Email the weekly order value digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes order placed event by customers and writes these figures for the last 7 days, the 7 days before, and the weekly average over the last 12 w: average order value, the average total price; units per order, the average number of line items in items; price per unit, average order value divided by units per order; the same three for new customers (their first order placed event) and for returning customers (they did order placed event before). The first line says so when average order value moved more than 5% against the 7 days before, and whether units, price or both drove it. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
