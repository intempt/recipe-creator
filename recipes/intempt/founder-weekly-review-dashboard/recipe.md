---
frontmatter_id: founder-weekly-review-dashboard
slash_command: /founder-weekly-review-dashboard
description: 'The one email to read before the Monday team meeting: new signups, new paying customers, churn, revenue and
  engagement, each against last week and last year.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a founder every Monday the new signups, paying customers, churn, revenue and engagement, each compared with
    last week and last year.
  parameters:
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: user_signed_up
    kind: event
    meaning: A new user signed up
  - slot: subscription_started
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: amount
      type: number
      meaning: Subscription amount
      optional: false
  - slot: subscription_canceled
    kind: event
    meaning: A customer canceled their paid subscription
  - slot: payment_received
    kind: event
    meaning: A payment or order was received
    properties:
    - name: amount
      type: number
      meaning: Amount received
      optional: false
  - slot: session_start
    kind: event
    meaning: A user started a session in the product
  steps:
  - id: s1
    builds: automation
    uses:
    - user_signed_up
    - subscription_started
    - subscription_canceled
    - payment_received
    - session_start
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 07:00 on a schedule. Each run it analyzes the last full week
      and writes these figures, each with the change against the week before and the same week last year: users who did {user_signed_up};
      users who did {subscription_started}; users who did {subscription_canceled}; net new paying customers, started minus
      canceled; revenue, the sum of {payment_received.amount}; daily active users, users doing {session_start} per day averaged
      over the week. It adds revenue and net new customers for each of the last 12 weeks. Then it emails these figures as
      plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Monday morning scorecard

Slash command: /founder-weekly-review-dashboard

## Step 1: Email the Monday scorecard

Build an automation that runs every Monday at 07:00 on a schedule. Each run it analyzes the last full week and writes these figures, each with the change against the week before and the same week last year: users who did user signed up; users who did subscription started; users who did subscription canceled; net new paying customers, started minus canceled; revenue, the sum of amount; daily active users, users doing session start per day averaged over the week. It adds revenue and net new customers for each of the last 12 weeks. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
