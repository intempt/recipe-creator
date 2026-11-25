---
frontmatter_id: cohort-acquisition-ltv-dashboard
slash_command: /cohort-acquisition-ltv-dashboard
description: Emails a monthly digest of customer lifetime value by acquisition channel and first-order cohort, with repeat-purchase
  rates, days to second order and lifecycle mix per channel.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a monthly digest of lifetime value by acquisition channel and first-order cohort, repeat-purchase rates,
    days to second order and lifecycle mix per channel.
  parameters:
  - name: subscribeRetentionThreshold
    type: number
    label: Month-3 repeat rate that suits subscribe-and-save (%)
    default: 30
    required: false
  - name: oneTimeRetentionThreshold
    type: number
    label: Month-3 repeat rate below which a category is a one-time purchase (%)
    default: 10
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
      meaning: Order total
      optional: false
  - slot: utm_source_attribute
    kind: attribute
    meaning: The customer's first-touch UTM source (acquisition channel)
  - slot: lifecycle_score_attribute
    kind: attribute
    meaning: The customer's lifecycle stage, such as At risk, New customers, Regulars or Champions
  - slot: first_order_category_attribute
    kind: attribute
    meaning: The product category of the customer's first order
    optional: true
  steps:
  - id: s1
    builds: automation
    uses:
    - placed_order_event
    - utm_source_attribute
    - lifecycle_score_attribute
    - first_order_category_attribute
    - subscribeRetentionThreshold
    - oneTimeRetentionThreshold
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes customers
      by the month of their first {placed_order_event} and by {utm_source_attribute}, and writes these figures: the average
      cumulative {placed_order_event.total_price} per customer 6 months and 12 months after the first order, per {utm_source_attribute},
      for customers whose first order was between 12 and 18 months ago; the share of customers whose first order was between
      3 and 15 months ago who placed a second order within 90 days of it, per {first_order_category_attribute} when it is
      set, marking categories above {subscribeRetentionThreshold}% and below {oneTimeRetentionThreshold}%; the median days
      from first to second order per category; the sum of {placed_order_event.total_price} in the last 30 days per {utm_source_attribute};
      the share of each channel''s customers in each {lifecycle_score_attribute} stage. Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Cohort LTV by acquisition channel

Slash command: /cohort-acquisition-ltv-dashboard

## Step 1: Email the monthly cohort LTV digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes customers by the month of their first placed order event and by utm source attribute, and writes these figures: the average cumulative total price per customer 6 months and 12 months after the first order, per utm source attribute, for customers whose first order was between 12 and 18 months ago; the share of customers whose first order was between 3 and 15 months ago who placed a second order within 90 days of it, per first order category attribute when it is set, marking categories above 30% and below 10%; the median days from first to second order per category; the sum of total price in the last 30 days per utm source attribute; the share of each channel's customers in each lifecycle score attribute stage. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
