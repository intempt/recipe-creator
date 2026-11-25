---
frontmatter_id: post-purchase-second-order-velocity
slash_command: /post-purchase-second-order-velocity
description: Emails a monthly digest of the time from a customer's first order to their second, by product category, so replenishment
  reminders can be timed to the typical gap.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a monthly digest of days from first to second order by product category, with high-velocity and long-cycle
    flags, compared with an older cohort.
  parameters:
  - name: first_order_min_age
    type: duration
    label: Minimum age of first order (cohort must have full follow-up window)
    default: 6 mo
    required: false
  - name: comparison_window_start
    type: duration
    label: Comparison cohort first order age, start (months ago)
    default: 18 mo
    required: false
  - name: comparison_window_end
    type: duration
    label: Comparison cohort first order age, end (months ago)
    default: 12 mo
    required: false
  - name: top_categories
    type: number
    label: Number of top first-order categories to break down by
    default: 6
    required: false
  - name: early_loyalty_window
    type: duration
    label: Early loyalty window (days from first to second order)
    default: 30 d
    required: false
  - name: high_velocity_threshold
    type: duration
    label: High-velocity median threshold (flag categories below this)
    default: 14 d
    required: false
  - name: long_cycle_threshold
    type: duration
    label: Long-cycle median threshold (flag categories above this)
    default: 180 d
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
    - name: items
      type: text
      meaning: Products included in the order; each product_id resolves to a category
      optional: false
  - slot: product_category_catalog
    kind: product_feed
    meaning: Product catalog that maps each product to its category
  steps:
  - id: s1
    builds: automation
    uses:
    - placed_order_event
    - product_category_catalog
    - first_order_min_age
    - comparison_window_start
    - comparison_window_end
    - top_categories
    - early_loyalty_window
    - high_velocity_threshold
    - long_cycle_threshold
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes customers
      whose first {placed_order_event} was between {first_order_min_age} and 12 months ago, grouped by the category of their
      first order''s {placed_order_event.items} in {product_category_catalog} (top {top_categories} categories), and writes
      these figures per category: the % who placed a second order; the median days from first to second order; the % of repeat
      buyers back within 7, 30, 90 and 180 days; the % back within {early_loyalty_window}; the same median for customers whose
      first order was between {comparison_window_start} and {comparison_window_end} ago. Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. The email names categories with a median under {high_velocity_threshold}
      as replenishment candidates and over {long_cycle_threshold} as long-cycle. Nothing else is sent.'
---

# Time to second purchase

Slash command: /post-purchase-second-order-velocity

## Step 1: Email the monthly second order digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes customers whose first placed order event was between 6 mo and 12 months ago, grouped by the category of their first order's items in product category catalog (top 6 categories), and writes these figures per category: the % who placed a second order; the median days from first to second order; the % of repeat buyers back within 7, 30, 90 and 180 days; the % back within 30 d; the same median for customers whose first order was between 18 mo and 12 mo ago. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email names categories with a median under 14 d as replenishment candidates and over 180 d as long-cycle. Nothing else is sent.
