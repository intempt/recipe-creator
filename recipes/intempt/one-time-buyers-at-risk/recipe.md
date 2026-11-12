---
frontmatter_id: one-time-buyers-at-risk
slash_command: /one-time-buyers-at-risk
description: Customers who bought once, have not been back in two months, and are not trending well, so you can give them a reason to return.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Builds a segment of customers who bought exactly once, have been inactive for 60 or more days, and are not in the
    Regulars or Promising lifecycle groups, so they can be won back.
  parameters:
  - name: order_count
    type: number
    label: Number of placed orders that defines a one-time buyer
    default: 1
    required: false
  - name: inactive_days
    type: number
    label: Minimum days since last activity
    default: 60
    required: false
  - name: segment_name
    type: string
    label: Name of the segment to build
    default: One-Time Buyers At Risk
    required: false
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
  - slot: days_since_last_activity
    kind: attribute
    meaning: Number of days since the customer's last activity
  - slot: lifecycle_score
    kind: attribute
    meaning: Customer lifecycle score group (for example Regulars, Promising, At Risk)
  steps:
  - id: s1
    builds: segment
    uses:
    - placed_order_event
    - days_since_last_activity
    - lifecycle_score
    - order_count
    - inactive_days
    - segment_name
    instruction: 'Build a segment named "{segment_name}". A user is in the segment only when all of these are true: they did
      {placed_order_event} exactly {order_count} time(s), at any time; their {days_since_last_activity} is {inactive_days}
      or more; their {lifecycle_score} is neither "Regulars" nor "Promising".'
---

# One-time buyers going cold

Slash command: /one-time-buyers-at-risk

## Step 1: Build the one-time-buyer list

Build a segment of users named "One-Time Buyers At Risk".
A user is in the segment only when all of these are true:
- they did the Placed order event exactly 1 time, at any time
- their Days since last activity attribute is 60 or more
- their Lifecycle score attribute is neither "Regulars" nor "Promising"
