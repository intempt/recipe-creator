---
frontmatter_id: ecommerce-revenue-dashboard
slash_command: /ecommerce-revenue-dashboard
description: 'Emails a weekly digest of how much revenue you are making, which channels drive it, and whether the trend is
  holding: revenue, order value, cart-to-order conversion and repeat purchases.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: 'Emails founders a weekly revenue digest: revenue by channel against last year, order value, the view-to-order
    funnel by device, top categories and repeat purchases.'
  parameters:
  - name: date_range
    type: duration
    label: Window the figures cover
    default: 30 d
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
    - name: channel
      type: string
      meaning: Sales or acquisition channel of the order
      optional: false
    - name: device_type
      type: string
      meaning: Device the order was placed on
      optional: false
    - name: order_value
      type: number
      meaning: Order total
      optional: false
    - name: units
      type: number
      meaning: Units in the order
      optional: false
    - name: product_category
      type: string
      meaning: Main product category of the order
      optional: false
  - slot: view_page_event
    kind: event
    meaning: A visitor viewed a page
    properties:
    - name: device_type
      type: string
      meaning: Device of the visit
      optional: false
  - slot: cart_created_event
    kind: event
    meaning: A customer created a shopping cart
  - slot: checkout_created_event
    kind: event
    meaning: A customer started checkout
  steps:
  - id: s1
    builds: automation
    uses:
    - placed_order_event
    - view_page_event
    - cart_created_event
    - checkout_created_event
    - date_range
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes orders and writes
      these figures: the sum of {placed_order_event.order_value} in the last {date_range}, in the {date_range} before that
      and in the same window one year earlier, in total and per {placed_order_event.channel}; average order value and average
      {placed_order_event.units} per order in the last {date_range} against the {date_range} before; the share of visitors
      who did {view_page_event} who then did {cart_created_event}, {checkout_created_event} and {placed_order_event} in the
      last {date_range}, per {placed_order_event.device_type}; the share of carts with no {placed_order_event} within 24 hours;
      the 5 {placed_order_event.product_category} values with the most revenue and their share of the total; the share of
      orders in the last {date_range} from customers who had ordered before. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Ecommerce revenue overview

Slash command: /ecommerce-revenue-dashboard

## Step 1: Email the weekly revenue digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes orders and writes these figures: the sum of order value in the last 30 d, in the 30 d before that and in the same window one year earlier, in total and per channel; average order value and average units per order in the last 30 d against the 30 d before; the share of visitors who did view page event who then did cart created event, checkout created event and placed order event in the last 30 d, per device type; the share of carts with no placed order event within 24 hours; the 5 product category values with the most revenue and their share of the total; the share of orders in the last 30 d from customers who had ordered before. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
