---
frontmatter_id: refund-rate-by-product-and-category
slash_command: /refund-rate-by-product-and-category
description: Shows which products get refunded most often and which ones are getting worse, over the last 90 days.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows which products get refunded most often and which are getting worse over the last 90 days, flagging high refund
    rates and quality issues.
  parameters:
  - name: time_window
    type: duration
    label: Analysis time range
    default: 90 d
    required: false
  - name: top_n_products
    type: number
    label: Number of top products by refund count
    default: 20
    required: false
  - name: refund_rate_threshold
    type: number
    label: High refund rate threshold (%)
    default: 8
    required: false
  - name: rate_increase_threshold
    type: number
    label: Refund rate increase threshold (percentage points)
    default: 3
    required: false
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
    - name: reason
      type: text
      meaning: Free-text refund reason
      optional: true
    - name: order_total
      type: number
      meaning: Total value of the order
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
    properties:
    - name: product_id
      type: string
      meaning: Unique product identifier
      optional: false
    - name: category
      type: string
      meaning: Product category
      optional: true
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - order_refunded_event
    - placed_order_event
    - products_object
    - time_window
    - top_n_products
    - refund_rate_threshold
    - rate_increase_threshold
    instruction: 'Create an Insights report titled "Refund Rate by Product". Series A: count of {order_refunded_event}. Series
      B: count of {placed_order_event}. Formula: (A / B) × 100, unit %, labeled "Refund Rate". Break down by {placed_order_event.items}
      product_id, extracted from the line items (which flatten product_id, title, quantity, price, sku), showing the top {top_n_products}
      products by absolute refund count. Time range: last {time_window}, compared against the prior period of the same length.
      Chart: bar chart sorted by refund rate descending, plus a secondary view grouping the same products into category buckets
      from {products_object} category metadata, if available. Annotations: flag any product whose refund rate exceeds {refund_rate_threshold}%;
      flag any product whose refund rate rose by more than {rate_increase_threshold} percentage points versus the prior period;
      highlight products with both a rising rate and rising refund volume as the highest-priority quality issues. Resolve
      product to category by joining product_id against {products_object}. Do not group by refund reason text.'
---

# Refund rate by product

Slash command: /refund-rate-by-product-and-category

## Step 1: Find the most refunded products

Create an Insights report called "Refund Rate by Product".
Series A: Event "Order refunded", aggregation: Count
Series B: Event "Placed order", aggregation: Count
Formula: (A / B) × 100, unit: %, label: "Refund Rate"
Breakdown: By product_id (extracted from Placed order.items, which flattens product_id, title, quantity, price, sku): top 20 products by absolute refund count
Time range: Last 90 days
Compare: Previous period (prior 90 days)
Chart type: Bar chart sorted by refund rate descending, secondary view grouping the same products into product-category buckets if the Products object has category metadata available
Annotations:
- Flag any product whose refund rate exceeds 8% (typical apparel/consumer-goods quality threshold).
- Flag any item whose refund rate increased by more than 3 percentage points vs. the prior period.
- Highlight items with both rising rate AND rising volume: the highest-priority quality issues.
Taxonomy notes:
- Placed order.items contains product_id, title, quantity, price, sku per line item. Resolve product to category by joining product_id against the Products record-object (Products has 27 attributes including category metadata).
- Order refunded carries order_id (relation to Orders), refund_amount, reason, and Order total. Reason text is unstructured; not used for grouping here.
