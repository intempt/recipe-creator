---
frontmatter_id: expansion-revenue-trend
slash_command: /expansion-revenue-trend
description: Emails a monthly digest of expansion revenue from subscription updates, split into plan upgrades and seat growth,
  as a share of new subscription revenue, with a stall flag.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a monthly digest of expansion revenue from plan upgrades and seat increases, and how it compares with new
    subscription revenue.
  parameters:
  - name: window
    type: duration
    label: Months of history in the digest
    default: 12 mo
    required: false
  - name: healthy_threshold
    type: number
    label: Healthy expansion as % of new MRR
    default: 30
    required: false
  - name: best_in_class_threshold
    type: number
    label: Best-in-class expansion as % of new MRR
    default: 50
    required: false
  - name: stall_decline_threshold
    type: number
    label: Month-over-month expansion decline that flags a stall (%)
    default: 15
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: subscription_updated_event
    kind: event
    meaning: A customer's subscription was updated
    properties:
    - name: subscription_id
      type: string
      meaning: Identifier of the subscription that changed
      optional: false
    - name: changed_fields
      type: text
      meaning: Names of the subscription fields that changed, such as plan or line items
      optional: false
    - name: plan_items
      type: text
      meaning: Plan line items with price, quantity and product after the update
      optional: false
    - name: amount
      type: number
      meaning: Subscription amount after the update
      optional: false
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: subscription_id
      type: string
      meaning: Identifier of the new subscription
      optional: false
    - name: amount
      type: number
      meaning: Starting subscription amount
      optional: false
    - name: plan
      type: string
      meaning: Starting plan tier used to break down results
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - subscription_updated_event
    - subscription_started_event
    - window
    - healthy_threshold
    - best_in_class_threshold
    - stall_decline_threshold
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes the
      last 30 days and writes these figures: upgrade revenue, the sum of positive changes in {subscription_updated_event.amount}
      against the previous amount on the same {subscription_updated_event.subscription_id} where {subscription_updated_event.changed_fields}
      shows a plan change; seat revenue, the same sum where {subscription_updated_event.plan_items} shows a quantity increase;
      new revenue, the sum of {subscription_started_event.amount}; expansion as a % of new revenue, (upgrade + seat) / new
      x 100, split by starting {subscription_started_event.plan}; and each figure per month over the last {window}. Negative
      changes are contraction and are left out. Then it emails these figures as plain-text lines, each with its window, to
      {digest_recipients}. When expansion revenue fell more than {stall_decline_threshold}% against the month before, the
      email''s first line says so; it also says if expansion is under {healthy_threshold}% (below healthy) or at least {best_in_class_threshold}%
      (best in class) of new revenue. Nothing else is sent.'
---

# Expansion revenue trend

Slash command: /expansion-revenue-trend

## Step 1: Email the monthly expansion digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes the last 30 days and writes these figures: upgrade revenue, the sum of positive changes in amount against the previous amount on the same subscription id where changed fields shows a plan change; seat revenue, the same sum where plan items shows a quantity increase; new revenue, the sum of amount; expansion as a % of new revenue, (upgrade + seat) / new x 100, split by starting plan; and each figure per month over the last 12 mo. Negative changes are contraction and are left out. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. When expansion revenue fell more than 15% against the month before, the email's first line says so; it also says if expansion is under 30% (below healthy) or at least 50% (best in class) of new revenue. Nothing else is sent.
