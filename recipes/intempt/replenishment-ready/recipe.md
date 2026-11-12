---
frontmatter_id: replenishment-ready
slash_command: /replenishment-ready
description: Customers whose last order was one to two months ago and who are about due for another, the moment a running-low reminder lands best.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Builds a segment of customers whose last order was one to two months ago, so they can receive a running-low reminder
    at the right moment to re-order.
  parameters:
  - name: order_window_start
    type: duration
    label: Earliest order age (window start)
    default: 60 d
    required: false
  - name: recent_exclusion_window
    type: duration
    label: Recent order exclusion window
    default: 30 d
    required: false
  requirements:
  - slot: placed_order
    kind: event
    meaning: A customer placed an order
  steps:
  - id: s1
    builds: segment
    uses:
    - placed_order
    - order_window_start
    - recent_exclusion_window
    instruction: Build a segment named "Replenishment-Ready" of users who did {placed_order} at least once between {order_window_start}
      and {recent_exclusion_window} ago, and who did not do {placed_order} in the last {recent_exclusion_window}.
---

# Customers due to re-order

Slash command: /replenishment-ready

## Step 1: Build the replenishment list

Build a segment of users named "Replenishment-Ready".
A user is in the segment only when all of these are true:
- they did the Placed order event at least once between 30 and 60 days ago
- they did not do the Placed order event in the last 30 days
