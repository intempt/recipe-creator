---
frontmatter_id: power-user-concentration
slash_command: /power-user-concentration
description: 'Emails a weekly digest of how concentrated activity is across users: each percentile group''s share of total
  events, or of revenue for stores, compared with the prior period.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of the share of activity or revenue held by the top 1%, 5%, 10%, 25% and 50% of users, against
    the prior period, with concentration flags.
  parameters:
  - name: time_window
    type: duration
    label: Window analyzed
    default: 30 d
    required: false
  - name: comparison_window
    type: duration
    label: Earlier window it is compared with
    default: 30 d
    required: false
  - name: breakdown_mode
    type: enum
    label: Business type
    default: saas
    required: false
    options:
    - saas
    - ecommerce
  - name: top_share_alert_pct
    type: number
    label: Top 1% share above which it is flagged (%)
    default: 25
    required: false
  - name: long_tail_alert_pct
    type: number
    label: Bottom 50% share below which it is flagged (%)
    default: 10
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A customer started a session in the product
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    optional: true
    properties:
    - name: total_price
      type: number
      meaning: Total price of the placed order
      optional: false
  - slot: plan_attribute
    kind: attribute
    meaning: The subscription plan a user belongs to
    optional: true
  - slot: lifetime_value_attribute
    kind: attribute
    meaning: The lifetime value bucket of a user
    optional: true
  steps:
  - id: s1
    builds: automation
    uses:
    - session_start_event
    - placed_order_event
    - plan_attribute
    - lifetime_value_attribute
    - time_window
    - comparison_window
    - breakdown_mode
    - top_share_alert_pct
    - long_tail_alert_pct
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it ranks users by their count
      of {session_start_event} in the last {time_window}; when {breakdown_mode} is ecommerce it ranks them by their sum of
      {placed_order_event.total_price} instead. It writes these figures: the share of the total held by the top 1%, top 5%,
      top 10%, top 25% and top 50% of users and by the bottom 50%, next to the same shares for the {comparison_window} before,
      saying whether concentration is rising or falling; the top 10% share split by {plan_attribute} when {breakdown_mode}
      is saas, or by {lifetime_value_attribute} when it is ecommerce. When the top 1% share is above {top_share_alert_pct}%
      or the bottom 50% share is below {long_tail_alert_pct}%, the email''s first line says so. Then it emails these figures
      as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Power user concentration

Slash command: /power-user-concentration

## Step 1: Email the weekly concentration digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it ranks users by their count of session start event in the last 30 d; when saas is ecommerce it ranks them by their sum of total price instead. It writes these figures: the share of the total held by the top 1%, top 5%, top 10%, top 25% and top 50% of users and by the bottom 50%, next to the same shares for the 30 d before, saying whether concentration is rising or falling; the top 10% share split by plan attribute when saas is saas, or by lifetime value attribute when it is ecommerce. When the top 1% share is above 25% or the bottom 50% share is below 10%, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
