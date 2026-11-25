---
frontmatter_id: mrr-trend
slash_command: /mrr-trend
description: Emails a monthly digest of recurring revenue by plan over the last 12 months, with the month on month change
  and how each month compares with the same month last year.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a monthly digest of recurring revenue by plan, with month-on-month change, year-over-year comparison and
    flags for contraction and plan mix shifts.
  parameters:
  - name: time_range
    type: duration
    label: Time range to chart
    default: 12 mo
    required: false
  - name: yoy_share_shift_threshold
    type: number
    label: YoY plan share shift threshold (percentage points)
    default: 5
    required: false
  - name: growth_average_window
    type: duration
    label: Trailing growth average window
    default: 3 mo
    required: false
  - name: recurring_type_value
    type: string
    label: Revenue type value that marks recurring revenue
    default: subscription
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: revenue_completed_event
    kind: event
    meaning: A customer completed a revenue payment
    properties:
    - name: amount
      type: number
      meaning: Payment amount in dollars
      optional: false
    - name: customer_id
      type: text
      meaning: Identifier of the paying customer
      optional: false
    - name: type
      type: text
      meaning: Revenue type, indicating whether the payment is recurring subscription revenue
      optional: false
    - name: source
      type: text
      meaning: Where the revenue payment originated
      optional: true
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription to a plan
    properties:
    - name: plan
      type: text
      meaning: Name of the subscription plan tier the customer started
      optional: false
    - name: customer_id
      type: text
      meaning: Identifier of the subscribing customer
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - revenue_completed_event
    - subscription_started_event
    - time_range
    - yoy_share_shift_threshold
    - growth_average_window
    - recurring_type_value
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes {revenue_completed_event}
      with {revenue_completed_event.type} equal to {recurring_type_value} and writes these figures: MRR, the sum of {revenue_completed_event.amount},
      for the last 30 days and for each 30 days over the last {time_range}; MRR split by plan, each customer ({revenue_completed_event.customer_id})
      taking the plan of their latest {subscription_started_event.plan} on the same {subscription_started_event.customer_id};
      net new MRR, this 30 days minus the 30 days before; the growth rate % and its average over the last {growth_average_window};
      MRR against the same 30 days a year ago. Then it emails these figures as plain-text lines, each with its window, to
      {digest_recipients}. When net new MRR is negative, the email''s first line says MRR contracted; it also names any plan
      whose share of MRR moved more than {yoy_share_shift_threshold} percentage points against a year ago. Nothing else is
      sent.'
---

# Monthly recurring revenue trend

Slash command: /mrr-trend

## Step 1: Email the monthly MRR digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes revenue completed event with type equal to subscription and writes these figures: MRR, the sum of amount, for the last 30 days and for each 30 days over the last 12 mo; MRR split by plan, each customer (customer id) taking the plan of their latest plan on the same customer id; net new MRR, this 30 days minus the 30 days before; the growth rate % and its average over the last 3 mo; MRR against the same 30 days a year ago. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. When net new MRR is negative, the email's first line says MRR contracted; it also names any plan whose share of MRR moved more than 5 percentage points against a year ago. Nothing else is sent.
