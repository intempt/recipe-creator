---
frontmatter_id: customer-360-dashboard
slash_command: /customer-360-dashboard
description: Emails a weekly breakdown of customers across the six lifecycle stages, how they moved between stages, repeat-purchase
  timing and cohort lifetime value.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: 'Emails a weekly customer lifecycle digest: counts per lifecycle stage, stage movement, time to second order and
    first-order cohort lifetime value.'
  parameters:
  - name: date_range
    type: enum
    label: Window the digest covers
    default: last_90_days
    required: false
    options:
    - last_30_days
    - last_90_days
    - last_12_months
  - name: ltv_months
    type: number
    label: Months after first order for cohort lifetime value
    default: 6
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: customer_placed_order
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Total value of the order
      optional: false
  - slot: users_lifecycle_score
    kind: attribute
    meaning: 'The user''s lifecycle stage: At risk, Needs attention, New customers, Promising, Regulars or Champions'
  steps:
  - id: s1
    builds: automation
    uses:
    - customer_placed_order
    - users_lifecycle_score
    - date_range
    - ltv_months
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {customer_placed_order}
      in the {date_range} window and writes these figures: the count of users in each {users_lifecycle_score} stage (At risk,
      Needs attention, New customers, Promising, Regulars, Champions) now and 30 days ago; the share of customers who did
      a second {customer_placed_order} and the median days from first to second order; for each month of first order, the
      average sum of {customer_placed_order.total_price} per customer in the {ltv_months} months after it. Then it emails
      these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Customer lifecycle overview

Slash command: /customer-360-dashboard

## Step 1: Email the weekly lifecycle digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did customer placed order in the last_90_days window and writes these figures: the count of users in each users lifecycle score stage (At risk, Needs attention, New customers, Promising, Regulars, Champions) now and 30 days ago; the share of customers who did a second customer placed order and the median days from first to second order; for each month of first order, the average sum of total price per customer in the 6 months after it. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
