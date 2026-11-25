---
frontmatter_id: ecommerce-operations-dashboard
slash_command: /ecommerce-operations-dashboard
description: Emails operations a weekly digest of whether orders ship on time and where refunds and cancellations cluster
  by product category, with an alert line when the fulfillment rate falls below target.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails operations a weekly digest of fulfillment rate, time to ship, refund and cancellation rates by product category
    and the checkout step losing most shoppers.
  parameters:
  - name: fulfillmentTargetPct
    type: number
    label: Fulfillment rate below which the digest warns (%)
    default: 90
    required: false
  - name: topCategoryCount
    type: number
    label: Categories listed by refund rate
    default: 5
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
    - name: order_id
      type: string
      meaning: Order identifier
      optional: false
    - name: product_category
      type: string
      meaning: Product category of the order's items
      optional: false
  - slot: order_fulfilled_event
    kind: event
    meaning: An order was fulfilled and shipped
    properties:
    - name: order_id
      type: string
      meaning: Order identifier
      optional: false
  - slot: order_refunded_event
    kind: event
    meaning: An order was refunded
    properties:
    - name: order_id
      type: string
      meaning: Order identifier
      optional: false
    - name: product_category
      type: string
      meaning: Product category of the refunded items
      optional: false
  - slot: order_cancelled_event
    kind: event
    meaning: An order was cancelled
    properties:
    - name: order_id
      type: string
      meaning: Order identifier
      optional: false
  - slot: checkout_step_event
    kind: event
    meaning: A customer reached a checkout step
    optional: true
    properties:
    - name: checkout_step
      type: string
      meaning: Name of the checkout step
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - placed_order_event
    - order_fulfilled_event
    - order_refunded_event
    - order_cancelled_event
    - checkout_step_event
    - fulfillmentTargetPct
    - topCategoryCount
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes orders, joining
      events on order_id, and writes these figures: the count of {placed_order_event} in the last 30 days; the fulfillment
      rate, the share of orders placed between 3 and 33 days ago that have an {order_fulfilled_event}; the median hours from
      {placed_order_event} to {order_fulfilled_event} for orders fulfilled in the last 30 days; the refund rate and the cancellation
      rate ({order_refunded_event}, {order_cancelled_event}) of orders placed in the last 30 days, per {placed_order_event.product_category};
      the {topCategoryCount} categories with the highest refund rate; the {checkout_step_event.checkout_step} that the most
      shoppers reached without reaching the next step in the last 30 days, when that event exists. When the fulfillment rate
      is below {fulfillmentTargetPct}%, the email''s first line says so. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Fulfillment, returns and refunds

Slash command: /ecommerce-operations-dashboard

## Step 1: Email the weekly operations digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes orders, joining events on order_id, and writes these figures: the count of placed order event in the last 30 days; the fulfillment rate, the share of orders placed between 3 and 33 days ago that have an order fulfilled event; the median hours from placed order event to order fulfilled event for orders fulfilled in the last 30 days; the refund rate and the cancellation rate (order refunded event, order cancelled event) of orders placed in the last 30 days, per product category; the 5 categories with the highest refund rate; the checkout step that the most shoppers reached without reaching the next step in the last 30 days, when that event exists. When the fulfillment rate is below 90%, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
