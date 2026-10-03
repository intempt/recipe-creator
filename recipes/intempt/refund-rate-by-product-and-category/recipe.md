---
id: refund-rate-by-product-and-category
title: Refund rate by product
slash_command: /refund-rate-by-product-and-category
group: Reports
owner: intempt
summary: Shows which products get refunded most often and which ones are getting worse, over the last
  90 days.
description: >-
  Refund rate by product (from order line items) with previous-period comparison and quality-issue flagging.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  complexity: quick
  executionMode: live
  tags:
    - insights
steps:
  - id: s1
    title: Find the most refunded products
    summary: >-
      Refunds as a percentage of orders for the top 20 products by refund count over 90 days, compared
      with the prior 90 and grouped into categories. Flags any product over 8% and any that rose more
      than 3 points.
    builds: report
    description: |-
      Create an Insights report called "Refund Rate by Product".
      Series A: Event "order_refunded", aggregation: Count
      Series B: Event "order_created", aggregation: Count
      Formula: (A / B) × 100, unit: %, label: "Refund Rate"
      Breakdown: By product_id (extracted from order_created.items, which flattens product_id, title, quantity, price, sku): top 20 products by absolute refund count
      Time range: Last 90 days
      Compare: Previous period (prior 90 days)
      Chart type: Bar chart sorted by refund rate descending, secondary view grouping the same products into product-category buckets if the Products object has category metadata available
      Annotations:
      - Flag any product whose refund rate exceeds 8% (typical apparel/consumer-goods quality threshold).
      - Flag any item whose refund rate increased by more than 3 percentage points vs. the prior period.
      - Highlight items with both rising rate AND rising volume: the highest-priority quality issues.
      Taxonomy notes:
      - order_created.items contains product_id, title, quantity, price, sku per line item. Resolve product to category by joining product_id against the Products record-object (Products has 27 attributes including category metadata).
      - order_refunded carries order_id (relation to Orders), refund_amount, reason, and total_amount. Reason text is unstructured; not used for grouping here.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Refund rate by product

Shows which products get refunded most often and which ones are getting worse, over the last 90 days.

## Steps

1. **Find the most refunded products** (builds report)

   Refunds as a percentage of orders for the top 20 products by refund count over 90 days, compared with the prior 90 and grouped into categories. Flags any product over 8% and any that rose more than 3 points.

## What you end up with

- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build report.
