---
frontmatter_id: product-category-performance
slash_command: /product-category-performance
description: Emails a weekly digest of revenue, units and average order value by product category, flagging softening demand,
  price erosion and the top momentum categories.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a weekly digest of revenue, units and average order value by product category, flagging demand softening,
    price erosion and top momentum categories.
  parameters:
  - name: window
    type: duration
    label: Analysis time range
    default: 30 d
    required: false
  - name: topCategories
    type: number
    label: Number of categories shown before grouping the rest as Other
    default: 12
    required: false
  - name: momentumMinShare
    type: number
    label: Minimum revenue share (%) for momentum highlight
    default: 5
    required: false
  - name: revenueChangeFlat
    type: number
    label: Change (%) treated as flat for price erosion flag
    default: 0
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
      meaning: Total order price
      optional: false
    - name: items
      type: array
      meaning: Line items in the order, each with product_id, title, quantity, price and sku
      optional: false
  - slot: products_catalog
    kind: product_feed
    meaning: Product catalog that maps each product_id to its category
  steps:
  - id: s1
    builds: automation
    uses:
    - placed_order_event
    - products_catalog
    - window
    - topCategories
    - momentumMinShare
    - revenueChangeFlat
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes {placed_order_event}
      in the last {window}, the {window} before, and the same {window} a year ago, giving each line item in {placed_order_event.items}
      the category of its product_id in {products_catalog}. It writes these figures for the top {topCategories} categories
      by revenue, the rest grouped as Other: revenue (the sum of line item price x quantity) and its share %; units sold;
      average order value; the change in each against the period before and a year ago; the top 3 categories by year-over-year
      revenue growth among those with at least {momentumMinShare}% of revenue. Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. The email flags categories where revenue and units both fell (demand
      softening) and where units rose but revenue changed by {revenueChangeFlat}% or less (price erosion). Nothing else is
      sent.'
---

# Category performance

Slash command: /product-category-performance

## Step 1: Email the weekly category digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes placed order event in the last 30 d, the 30 d before, and the same 30 d a year ago, giving each line item in items the category of its product_id in products catalog. It writes these figures for the top 12 categories by revenue, the rest grouped as Other: revenue (the sum of line item price x quantity) and its share %; units sold; average order value; the change in each against the period before and a year ago; the top 3 categories by year-over-year revenue growth among those with at least 5% of revenue. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email flags categories where revenue and units both fell (demand softening) and where units rose but revenue changed by 0% or less (price erosion). Nothing else is sent.
