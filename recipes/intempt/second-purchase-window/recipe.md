---
frontmatter_id: second-purchase-window
slash_command: /second-purchase-window
description: Customers who bought for the first time in the last month, the period when most second purchases happen.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Builds a segment of customers who placed their first order in the last 30 days, the window when most second purchases
    happen.
  parameters:
  - name: repeat_window
    type: duration
    label: Repeat window
    default: 30 d
    required: false
  - name: order_count
    type: number
    label: Number of orders placed
    default: 1
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
    - order_count
    - repeat_window
    instruction: Build a segment named "Second-Purchase Window" of users who did {placed_order} exactly {order_count} time(s)
      at any time, and whose most recent {placed_order} happened in the last {repeat_window}.
---

# First-time buyers in the repeat window

Slash command: /second-purchase-window

## Step 1: Build the second-purchase list

Build a segment of users named "Second-Purchase Window".
A user is in the segment only when all of these are true:
- they did the Placed order event exactly 1 time, at any time
- that Placed order event happened in the last 30 days
