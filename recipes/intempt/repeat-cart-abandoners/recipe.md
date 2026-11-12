---
frontmatter_id: repeat-cart-abandoners
slash_command: /repeat-cart-abandoners
description: People who have walked away from checkout twice or more this month without buying, usually a sign of friction or price resistance.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Builds a segment of customers who abandoned checkout two or more times in the last 30 days without placing an order,
    flagging friction or price resistance.
  parameters:
  - name: abandon_threshold
    type: number
    label: Minimum abandoned checkouts
    default: 2
  - name: lookback_window
    type: duration
    label: Lookback window
    default: 30 d
  requirements:
  - slot: abandoned_checkout
    kind: event
    meaning: A customer abandoned checkout without completing the purchase
  - slot: placed_order
    kind: event
    meaning: A customer placed an order
  steps:
  - id: s1
    builds: segment
    uses:
    - abandoned_checkout
    - placed_order
    - abandon_threshold
    - lookback_window
    instruction: Build a segment named "Repeat Cart Abandoners" of users who did {abandoned_checkout} at least {abandon_threshold}
      times in the last {lookback_window} and did not do {placed_order} in the last {lookback_window}.
---

# Repeat cart abandoners

Slash command: /repeat-cart-abandoners

## Step 1: Build the repeat-abandoner list

Build a segment of users named "Repeat Cart Abandoners".
A user is in the segment only when all of these are true:
- they did the Abandoned checkout event 2 or more times in the last 30 days
- they did not do the Placed order event in the last 30 days
