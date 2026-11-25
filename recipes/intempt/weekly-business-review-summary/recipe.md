---
frontmatter_id: weekly-business-review-summary
slash_command: /weekly-business-review-summary
description: 'Emails the six numbers to look at every Monday: new signups, new paying customers, churn, revenue, net new customers
  and engagement, each against last week and the weeks before.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a Monday digest of six weekly numbers (signups, new paying customers, churn, revenue, net new customers,
    engagement) with week-over-week changes and warnings.
  parameters:
  - name: window_weeks
    type: number
    label: Lookback window (weeks)
    default: 12
    required: false
  - name: wow_alert_threshold
    type: number
    label: Week-over-week alert threshold (%)
    default: 15
    required: false
  - name: durable_trend_weeks
    type: number
    label: Consecutive weeks for durable wrong-direction trend
    default: 4
    required: false
  - name: dau_window
    type: duration
    label: Engagement trailing window
    default: 7 d
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: signup_event
    kind: event
    meaning: A new user account was created
  - slot: paid_subscription_event
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: trial_end
      type: date
      meaning: When the trial ended; empty for direct paid signups
      optional: true
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
  - slot: revenue_event
    kind: event
    meaning: Recurring revenue was completed for a customer
    properties:
    - name: amount
      type: number
      meaning: Revenue amount
      optional: false
    - name: type
      type: string
      meaning: Revenue type, indicating whether it is recurring
      optional: false
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  steps:
  - id: s1
    builds: automation
    uses:
    - signup_event
    - paid_subscription_event
    - subscription_canceled_event
    - revenue_event
    - session_start_event
    - window_weeks
    - wow_alert_threshold
    - durable_trend_weeks
    - dau_window
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last 7 days,
      the 7 days before, and each of the last {window_weeks} weeks, and writes these figures: new signups, the unique users
      who did {signup_event}; new paying customers, the unique users who did {paid_subscription_event}; churned customers,
      the unique users who did {subscription_canceled_event}; revenue, the sum of {revenue_event.amount} where {revenue_event.type}
      is recurring; net new customers, new paying customers minus churned customers; engagement, the average daily unique
      users who did {session_start_event} over the last {dau_window}. Each figure shows last week, the week before, the change
      in % and the average of the 4 weeks before. When a figure moved more than {wow_alert_threshold}% week over week, or
      moved the wrong way {durable_trend_weeks} weeks in a row, the email''s first line says so. Then it emails these figures
      as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Weekly business review

Slash command: /weekly-business-review-summary

## Step 1: Email the weekly business review

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last 7 days, the 7 days before, and each of the last 12 weeks, and writes these figures: new signups, the unique users who did signup event; new paying customers, the unique users who did paid subscription event; churned customers, the unique users who did subscription canceled event; revenue, the sum of amount where type is recurring; net new customers, new paying customers minus churned customers; engagement, the average daily unique users who did session start event over the last 7 d. Each figure shows last week, the week before, the change in % and the average of the 4 weeks before. When a figure moved more than 15% week over week, or moved the wrong way 4 weeks in a row, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
