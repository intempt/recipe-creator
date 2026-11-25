---
frontmatter_id: plan-tier-mix-shift
slash_command: /plan-tier-mix-shift
description: Emails a monthly digest of how revenue and customers spread across subscription plans, and whether the revenue
  mix is drifting up market or down market.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a monthly digest of revenue and customer share by subscription plan, flagging plan shifts and gaps between
    revenue mix and customer mix.
  parameters:
  - name: time_range
    type: duration
    label: Time range to analyze
    default: 12 mo
    required: false
  - name: shift_threshold_pp
    type: number
    label: Revenue share shift flag threshold (percentage points, YoY)
    default: 5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: revenue_event
    kind: event
    meaning: A customer completed a revenue payment
    properties:
    - name: amount
      type: number
      meaning: Payment amount in dollars
      optional: false
    - name: revenue_type
      type: string
      meaning: Type of revenue, such as recurring
      optional: false
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: plan
      type: string
      meaning: Subscription plan tier
      optional: false
    - name: subscription_id
      type: string
      meaning: Unique subscription identifier
      optional: false
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
    properties:
    - name: subscription_id
      type: string
      meaning: Unique subscription identifier
      optional: false
  - slot: subscription_expired_event
    kind: event
    meaning: A customer's subscription expired
    properties:
    - name: subscription_id
      type: string
      meaning: Unique subscription identifier
      optional: false
    optional: true
  steps:
  - id: s1
    builds: automation
    uses:
    - revenue_event
    - subscription_started_event
    - subscription_canceled_event
    - subscription_expired_event
    - time_range
    - shift_threshold_pp
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it gives each user
      the plan of their latest {subscription_started_event.plan}; a subscription is active when no {subscription_canceled_event}
      or {subscription_expired_event} came after it for the same {subscription_started_event.subscription_id}. It writes these
      figures per plan for the last 30 days, for each 30 days over the last {time_range}, and for the same 30 days a year
      ago: recurring revenue, the sum of {revenue_event.amount} with {revenue_event.revenue_type} equal to recurring, and
      its share %; active customers and their share %; the change in each share in percentage points against a year ago. Then
      it emails these figures as plain-text lines, each with its window, to {digest_recipients}. The email names any plan
      whose revenue share moved more than {shift_threshold_pp} points, and any plan whose revenue share and customer share
      moved in opposite directions. Nothing else is sent.'
---

# Plan tier mix shift

Slash command: /plan-tier-mix-shift

## Step 1: Email the monthly plan mix digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it gives each user the plan of their latest plan; a subscription is active when no subscription canceled event or subscription expired event came after it for the same subscription id. It writes these figures per plan for the last 30 days, for each 30 days over the last 12 mo, and for the same 30 days a year ago: recurring revenue, the sum of amount with revenue type equal to recurring, and its share %; active customers and their share %; the change in each share in percentage points against a year ago. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email names any plan whose revenue share moved more than 5 points, and any plan whose revenue share and customer share moved in opposite directions. Nothing else is sent.
