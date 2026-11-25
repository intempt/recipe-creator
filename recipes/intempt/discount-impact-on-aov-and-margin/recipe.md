---
frontmatter_id: discount-impact-on-aov-and-margin
slash_command: /discount-impact-on-aov-and-margin
description: 'Emails a weekly digest comparing orders with and without a discount code: basket totals, discount cost, net
  revenue impact, code by code.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: 'Emails a weekly digest on whether discount codes grow order value: average order with and without a discount,
    code by code, net revenue impact and discount cost share.'
  parameters:
  - name: time_range
    type: duration
    label: Longer window compared
    default: 12 w
    required: false
  - name: top_codes_limit
    type: number
    label: Discount codes listed
    default: 10
    required: false
  - name: healthy_discount_cost_pct
    type: number
    label: Discount cost share that is healthy (%)
    default: 15
    required: false
  - name: over_reliance_discount_cost_pct
    type: number
    label: Discount cost share that flags over-reliance (%)
    default: 20
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
    - name: total_price
      type: number
      meaning: Order total
      optional: false
  - slot: discount_applied_event
    kind: event
    meaning: A discount code was applied to an order
    properties:
    - name: amount
      type: number
      meaning: Discount amount
      optional: false
    - name: code
      type: string
      meaning: Discount code
      optional: false
    - name: order_id
      type: string
      meaning: Order the discount was applied to
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - placed_order_event
    - discount_applied_event
    - time_range
    - top_codes_limit
    - healthy_discount_cost_pct
    - over_reliance_discount_cost_pct
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes customers'' {placed_order_event}
      in the last 7 days and in the last {time_range}, an order counting as discounted when a {discount_applied_event} has
      its {discount_applied_event.order_id}, and writes for both windows: average {placed_order_event.total_price} with and
      without a discount and the difference; total discount cost, the sum of {discount_applied_event.amount}; discount cost
      as % of order revenue; net revenue impact, discounted revenue minus discount cost minus discounted orders times the
      average order without a discount; the top {top_codes_limit} codes by {discount_applied_event.code} with uses, average
      order and discount cost. The first line says over-reliance when discount cost share is above {over_reliance_discount_cost_pct}%,
      or healthy when below {healthy_discount_cost_pct}%. Then it emails these figures as plain-text lines, each with its
      window, to {digest_recipients}. Nothing else is sent.'
---

# Discount impact on order value

Slash command: /discount-impact-on-aov-and-margin

## Step 1: Email the weekly discount impact digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes customers' placed order event in the last 7 days and in the last 12 w, an order counting as discounted when a discount applied event has its order id, and writes for both windows: average total price with and without a discount and the difference; total discount cost, the sum of amount; discount cost as % of order revenue; net revenue impact, discounted revenue minus discount cost minus discounted orders times the average order without a discount; the top 10 codes by code with uses, average order and discount cost. The first line says over-reliance when discount cost share is above 20%, or healthy when below 15%. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
