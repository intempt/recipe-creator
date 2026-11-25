---
frontmatter_id: repeat-buyers
slash_command: /repeat-buyers
description: Customers who have ordered three or more times this quarter and spent real money, the right list for loyalty perks and review requests.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Builds a segment of customers who placed three or more orders in the last 90 days and have a lifetime value of
    at least 100, for loyalty perks and review requests.
  parameters:
  - name: order_count_min
    type: number
    label: Minimum number of orders
    default: 3
    required: false
  - name: lookback_window
    type: duration
    label: Lookback window
    default: 90 d
    required: false
  - name: min_lifetime_value
    type: number
    label: Minimum lifetime value
    default: 100
    required: false
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
  - slot: lifetime_value_attribute
    kind: attribute
    meaning: Customer lifetime value in money spent
  steps:
  - id: s1
    builds: segment
    uses:
    - placed_order_event
    - lifetime_value_attribute
    - order_count_min
    - lookback_window
    - min_lifetime_value
    instruction: Build a new segment named "Repeat Buyers" of users who did {placed_order_event} {order_count_min} or more
      times in the last {lookback_window} and whose {lifetime_value_attribute} is {min_lifetime_value} or more.
---

# Repeat buyers

Slash command: /repeat-buyers

## Step 1: Build the repeat-buyer list

Build a new segment named "Repeat Buyers" of users who did placed order event 3 or more times in the last 90 d and whose lifetime value attribute is 100 or more.
