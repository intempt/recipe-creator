---
frontmatter_id: big-basket-buyers
slash_command: /big-basket-buyers
description: Customers who spend heavily on every single order, so premium bundles and higher tiers go to people who already buy big.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Builds a segment of customers whose average order value and lifetime value are high and who have placed at least
    two orders, so premium bundles and higher tiers can target them.
  parameters:
  - name: aov_threshold
    type: number
    label: Minimum average order value
    default: 150
  - name: order_count_threshold
    type: number
    label: Minimum number of Placed order events
    default: 2
  - name: ltv_threshold
    type: number
    label: Minimum lifetime value
    default: 300
  requirements:
  - slot: average_order_value
    kind: attribute
    meaning: The average order value of a customer across their orders
  - slot: lifetime_value
    kind: attribute
    meaning: The total lifetime value a customer has generated
  - slot: placed_order
    kind: event
    meaning: A customer placed an order
  steps:
  - id: s1
    builds: segment
    uses:
    - average_order_value
    - placed_order
    - lifetime_value
    - aov_threshold
    - order_count_threshold
    - ltv_threshold
    instruction: 'Build a segment named "Big-Basket Buyers" of users who meet all of these conditions: {average_order_value}
      is {aov_threshold} or more; they did {placed_order} {order_count_threshold} or more times at any time; and {lifetime_value}
      is {ltv_threshold} or more.'
---

# Big basket buyers

Slash command: /big-basket-buyers

## Step 1: Build the big-basket list

Build a segment of users named "Big-Basket Buyers".
A user is in the segment only when all of these are true:
- their Average order value attribute is 150 or more
- they did the Placed order event 2 or more times, at any time
- their Lifetime value attribute is 300 or more
