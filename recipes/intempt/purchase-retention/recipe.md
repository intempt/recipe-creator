---
frontmatter_id: purchase-retention
slash_command: /purchase-retention
description: Emails a monthly digest of what share of first time buyers come back to buy again, by month of first purchase
  and by the category they bought first.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a monthly digest of repeat purchase rates by first-purchase month and category, with time to second purchase
    and flags for weak cohorts.
  parameters:
  - name: time_range
    type: duration
    label: Analysis time range
    default: 12 mo
    required: false
  - name: repeat_rate_flag_threshold
    type: number
    label: Flag categories with M6 repeat rate below (%)
    default: 15
    required: false
  - name: cohort_drop_threshold
    type: number
    label: Flag cohorts whose M3 repeat rate dropped more than (percentage points)
    default: 5
    required: false
  - name: high_replenishment_threshold
    type: number
    label: Highlight categories with M3 repeat rate above (%)
    default: 30
    required: false
  - name: benchmark_repeat_rate
    type: number
    label: Benchmark share of first-time DTC buyers making a 2nd purchase (%)
    default: 27
    required: false
  - name: top_quartile_repeat_rate
    type: number
    label: Top-quartile benchmark repeat rate (%)
    default: 45
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
    - name: customer_id
      type: string
      meaning: Identifier of the customer who placed the order
      optional: false
    - name: items.product_id
      type: string
      meaning: Product identifiers of the items in the order
      optional: false
  - slot: products_catalog
    kind: product_feed
    meaning: Product catalog that maps each product to its category
  steps:
  - id: s1
    builds: automation
    uses:
    - placed_order_event
    - products_catalog
    - time_range
    - repeat_rate_flag_threshold
    - cohort_drop_threshold
    - high_replenishment_threshold
    - benchmark_repeat_rate
    - top_quartile_repeat_rate
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it groups customers
      ({placed_order_event.customer_id}) by the month of their first {placed_order_event} in the last {time_range}, and by
      the category of that order''s {placed_order_event.items.product_id} in {products_catalog}. It writes per cohort month
      and per category: buyers; the % who placed another order within 1, 3, 6 and 12 months (M1, M3, M6, M12); the median
      days from first to second order; the share of second orders within 7, 30, 90 and 90+ days. Then it emails these figures
      as plain-text lines, each with its window, to {digest_recipients}. The email compares the overall repeat rate with {benchmark_repeat_rate}%
      (top quartile {top_quartile_repeat_rate}%), flags categories with M6 under {repeat_rate_flag_threshold}%, cohorts whose
      M3 fell more than {cohort_drop_threshold} points against the cohort before, and names categories with M3 over {high_replenishment_threshold}%
      as replenishment candidates. Nothing else is sent.'
---

# Repeat purchase retention

Slash command: /purchase-retention

## Step 1: Email the monthly repeat purchase digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it groups customers (customer id) by the month of their first placed order event in the last 12 mo, and by the category of that order's {placed_order_event.items.product_id} in products catalog. It writes per cohort month and per category: buyers; the % who placed another order within 1, 3, 6 and 12 months (M1, M3, M6, M12); the median days from first to second order; the share of second orders within 7, 30, 90 and 90+ days. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email compares the overall repeat rate with 27% (top quartile 45%), flags categories with M6 under 15%, cohorts whose M3 fell more than 5 points against the cohort before, and names categories with M3 over 30% as replenishment candidates. Nothing else is sent.
