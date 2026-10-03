---
id: browse-purchase-funnel
title: Browse to purchase funnel
slash_command: /browse-purchase-funnel
group: Reports
owner: intempt
summary: Shows how many shoppers move from a category page to a product page, cart, checkout and a completed
  order, and where you lose them on each device.
description: >-
  Browse-to-purchase funnel using canonical page_viewed/cart/order events with device-comparison conversion.
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
    - funnel
steps:
  - id: s1
    title: Trace category page to order
    summary: >-
      A five step funnel from a category page view to a product page, cart, checkout and order, inside
      a 7 day window, split by desktop, mobile and tablet. Flags the biggest drop and any step where mobile
      trails desktop by more than 10 points.
    builds: report
    description: |-
      Create a Funnel report called "Browse to Purchase".
      Steps:
      1. Event "page_viewed" where content_type indicates a category/listing page (or page_url contains /collections/ or /category/): "Browsed Category"
      2. Event "page_viewed" where page_url indicates a product detail page (e.g. contains /products/): "Viewed Product Detail"
      3. Event "cart_created": "Added to Cart"
      4. Event "checkout_created": "Started Checkout"
      5. Event "order_created": "Completed Purchase"
      Conversion window: 7 days
      Breakdown: By "device_type" attribute on the Users object (desktop, mobile, tablet)
      Compare: Previous period (prior 7 days)
      For each step, also surface:
      - Median time-to-convert from previous step
      - Per-device conversion rate at each step
      Annotations:
      - Flag the step with the largest drop-off (the primary bottleneck).
      - Flag any step where mobile conversion lags desktop by >10 percentage points (mobile UX issue).
      - Highlight any step where overall drop-off worsened by >3 percentage points vs. previous period.
      Industry benchmarks: 2-3% browse-to-buy for fashion, 4-6% for electronics.
      Taxonomy notes:
      - "product_list_viewed" and "product_viewed" as standalone events do not exist. Page-type discrimination is done via page_viewed.page_url path patterns or page_viewed.content_type.
      - "checkout_started" does not exist; checkout_created is the canonical pre-payment marker.
      - order_created is the canonical purchase event (cart_converted is also valid for cart-source attribution).
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Browse to purchase funnel

Shows how many shoppers move from a category page to a product page, cart, checkout and a completed order, and where you lose them on each device.

## Steps

1. **Trace category page to order** (builds report)

   A five step funnel from a category page view to a product page, cart, checkout and order, inside a 7 day window, split by desktop, mobile and tablet. Flags the biggest drop and any step where mobile trails desktop by more than 10 points.

## What you end up with

- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build report.
