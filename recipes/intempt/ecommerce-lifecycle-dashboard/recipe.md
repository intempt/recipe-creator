---
frontmatter_id: ecommerce-lifecycle-dashboard
slash_command: /ecommerce-lifecycle-dashboard
description: Emails a weekly digest of lifecycle distribution and stage movement, when shoppers reorder, and whether discount
  codes add revenue or eat into it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails the team a weekly digest of how customers move between lifecycle stages, when they reorder, and whether
    discount codes add or cut revenue.
  parameters:
  - name: dateRange
    type: enum
    label: Window the digest covers
    default: last_90_days
    required: false
    options:
    - last_30_days
    - last_90_days
    - last_365_days
  - name: migrationWindow
    type: duration
    label: Stage movement look-back window
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
    - name: discount_code
      type: string
      meaning: Discount code used on the order, empty when none
      optional: false
    - name: total_price
      type: number
      meaning: Total value of the order
      optional: false
  - slot: lifecycle_score_attribute
    kind: attribute
    meaning: 'The customer''s lifecycle stage: At risk, Needs attention, New customers, Promising, Regulars or Champions'
  steps:
  - id: s1
    builds: automation
    uses:
    - placed_order_event
    - lifecycle_score_attribute
    - dateRange
    - migrationWindow
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {placed_order_event}
      in the {dateRange} window and writes these figures: the count in each {lifecycle_score_attribute} stage now and {migrationWindow}
      ago, and the largest moves between stages; the share who placed a second order and the median days from first to second
      order; for each {placed_order_event.discount_code}, the orders, the average {placed_order_event.total_price} against
      orders with no code, and the share of its users who ordered again without a code. Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Ecommerce lifecycle and retention

Slash command: /ecommerce-lifecycle-dashboard

## Step 1: Email the weekly lifecycle digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did placed order event in the last_90_days window and writes these figures: the count in each lifecycle score attribute stage now and 30 d ago, and the largest moves between stages; the share who placed a second order and the median days from first to second order; for each discount code, the orders, the average total price against orders with no code, and the share of its users who ordered again without a code. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
