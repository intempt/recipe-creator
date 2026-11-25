---
frontmatter_id: refund-rate-by-product-and-category
slash_command: /refund-rate-by-product-and-category
description: Emails a weekly digest of which products and categories get refunded most often over the last 90 days and which
  are getting worse, flagging high refund rates and quality issues.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a weekly digest of refund rates by product and category over the last 90 days, flagging high rates and products
    whose refunds are rising.
  parameters:
  - name: time_window
    type: duration
    label: Window analyzed
    default: 90 d
    required: false
  - name: top_n_products
    type: number
    label: Products listed in the digest
    default: 20
    required: false
  - name: refund_rate_threshold
    type: number
    label: Refund rate above which a product is flagged (%)
    default: 8
    required: false
  - name: rate_increase_threshold
    type: number
    label: Rise in refund rate that gets flagged (percentage points)
    default: 3
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: order_refunded_event
    kind: event
    meaning: A customer had an order refunded
    properties:
    - name: order_id
      type: string
      meaning: Order the refund belongs to
      optional: false
    - name: refund_amount
      type: number
      meaning: Amount refunded
      optional: true
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: items
      type: json
      meaning: Line items with product_id, title, quantity, price, sku
      optional: false
  - slot: products_object
    kind: product_feed
    meaning: Product catalog records with category metadata, joined by product_id
    optional: true
    properties:
    - name: product_id
      type: string
      meaning: Unique product identifier
      optional: false
    - name: category
      type: string
      meaning: Product category
      optional: true
  steps:
  - id: s1
    builds: automation
    uses:
    - order_refunded_event
    - placed_order_event
    - products_object
    - time_window
    - top_n_products
    - refund_rate_threshold
    - rate_increase_threshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes {placed_order_event}
      and {order_refunded_event} in the last {time_window}, linking each refund to its order by {order_refunded_event.order_id}
      and to products through the product_id in {placed_order_event.items}, and writes these figures: for the top {top_n_products}
      products by refund count, the refund count, orders, refund rate (refunds divided by orders) and {order_refunded_event.refund_amount}
      total, next to the rate for the {time_window} before; the same refund rate by {products_object.category} when the catalog
      has it. When a product''s refund rate is above {refund_rate_threshold}% or rose by more than {rate_increase_threshold}
      percentage points, the email''s first line names it; products where both the rate and the refund count rose are listed
      first as quality issues. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Refund rate by product

Slash command: /refund-rate-by-product-and-category

## Step 1: Email the weekly refund digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes placed order event and order refunded event in the last 90 d, linking each refund to its order by order id and to products through the product_id in items, and writes these figures: for the top 20 products by refund count, the refund count, orders, refund rate (refunds divided by orders) and refund amount total, next to the rate for the 90 d before; the same refund rate by category when the catalog has it. When a product's refund rate is above 8% or rose by more than 3 percentage points, the email's first line names it; products where both the rate and the refund count rose are listed first as quality issues. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
