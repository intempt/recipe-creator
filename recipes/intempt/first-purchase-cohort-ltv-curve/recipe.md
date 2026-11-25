---
frontmatter_id: first-purchase-cohort-ltv-curve
slash_command: /first-purchase-cohort-ltv-curve
description: Emails a monthly digest of each first-purchase cohort's cumulative revenue per customer by cohort age, the best
  and worst cohorts, and acquisition channels whose lifetime value is rising.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a monthly digest comparing lifetime value per customer across monthly first-purchase cohorts and acquisition
    channels, with flags for one-time-buyer cohorts.
  parameters:
  - name: cohort_window
    type: duration
    label: Cohorts covered
    default: 12 months
    required: false
  - name: ltv_checkpoint_early
    type: number
    label: Early checkpoint (cohort age in months)
    default: 6
    required: false
  - name: ltv_checkpoint_late
    type: number
    label: Late checkpoint (cohort age in months)
    default: 12
    required: false
  - name: flattening_check_month
    type: number
    label: Cohort age from which a flat curve is flagged (months)
    default: 3
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
      meaning: Total price of the order
      optional: false
  - slot: user_acquisition_source
    kind: attribute
    meaning: The user's first-touch acquisition source (UTM source)
  steps:
  - id: s1
    builds: automation
    uses:
    - placed_order_event
    - user_acquisition_source
    - cohort_window
    - ltv_checkpoint_early
    - ltv_checkpoint_late
    - flattening_check_month
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes users
      whose first {placed_order_event} was in the last {cohort_window}, grouped into monthly cohorts by the month of that
      first order, and writes these figures: for each cohort, its size and its cumulative sum of {placed_order_event.total_price}
      per member at cohort ages 1, 3, {ltv_checkpoint_early} and {ltv_checkpoint_late} months, marking ages not yet reached
      as incomplete; the highest and lowest cohort at month {ltv_checkpoint_early} and at month {ltv_checkpoint_late}; cohorts
      whose value per member grew less than 5% between month {flattening_check_month} and month {ltv_checkpoint_early}, called
      likely one-time-buyer cohorts; value per member at month {ltv_checkpoint_early} by {user_acquisition_source} for the
      last 3 complete cohorts, saying which sources are rising. Then it emails these figures as plain-text lines, each with
      its window, to {digest_recipients}. Nothing else is sent.'
---

# First purchase LTV curve

Slash command: /first-purchase-cohort-ltv-curve

## Step 1: Email the monthly cohort LTV digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes users whose first placed order event was in the last 12 months, grouped into monthly cohorts by the month of that first order, and writes these figures: for each cohort, its size and its cumulative sum of total price per member at cohort ages 1, 3, 6 and 12 months, marking ages not yet reached as incomplete; the highest and lowest cohort at month 6 and at month 12; cohorts whose value per member grew less than 5% between month 3 and month 6, called likely one-time-buyer cohorts; value per member at month 6 by user acquisition source for the last 3 complete cohorts, saying which sources are rising. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
