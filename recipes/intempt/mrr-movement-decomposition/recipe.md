---
frontmatter_id: mrr-movement-decomposition
slash_command: /mrr-movement-decomposition
description: Emails a monthly digest that splits recurring revenue movement into new, expansion, contraction, churned and
  reactivated MRR, with net new MRR and net revenue retention.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a monthly digest splitting MRR movement into new, expansion, contraction, churn and reactivation, with net
    new MRR and NRR.
  parameters:
  - name: time_range
    type: duration
    label: Time range
    default: 12 mo
    required: false
  - name: reactivation_window
    type: duration
    label: Reactivation lookback window
    default: 90 d
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: amount
      type: number
      meaning: Recurring amount of the new subscription
      optional: false
    - name: customer_id
      type: string
      meaning: Identifier of the customer
      optional: false
  - slot: subscription_updated_event
    kind: event
    meaning: A customer's subscription was changed
    properties:
    - name: amount
      type: number
      meaning: New recurring amount after the change
      optional: false
    - name: prior_amount
      type: number
      meaning: Recurring amount before the change
      optional: false
    - name: subscription_id
      type: string
      meaning: Identifier of the subscription
      optional: false
    - name: changed_fields
      type: text
      meaning: Which subscription fields changed
      optional: false
    - name: plan_items
      type: text
      meaning: New plan state after the change
      optional: true
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
    properties:
    - name: prior_amount
      type: number
      meaning: Recurring amount of the subscription before cancellation
      optional: false
    - name: customer_id
      type: string
      meaning: Identifier of the customer
      optional: false
  - slot: subscription_resumed_event
    kind: event
    meaning: A customer resumed a previously paused or canceled subscription
    properties:
    - name: amount
      type: number
      meaning: Recurring amount when resumed
      optional: false
    - name: customer_id
      type: string
      meaning: Identifier of the customer
      optional: false
  - slot: active_subscription_status
    kind: attribute
    meaning: Whether a customer currently has an active subscription
  steps:
  - id: s1
    builds: automation
    uses:
    - subscription_started_event
    - subscription_updated_event
    - subscription_canceled_event
    - subscription_resumed_event
    - active_subscription_status
    - time_range
    - reactivation_window
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes subscription
      revenue in the last 30 days and in each 30 days over the last {time_range}, and writes these figures: new MRR, the sum
      of {subscription_started_event.amount} for customers with no active subscription before ({active_subscription_status});
      expansion MRR, the sum of positive {subscription_updated_event.amount} minus {subscription_updated_event.prior_amount}
      per {subscription_updated_event.subscription_id}; contraction MRR, the sum of the negative ones; churned MRR, the sum
      of {subscription_canceled_event.prior_amount}; reactivation MRR, the sum of {subscription_resumed_event.amount} for
      customers whose cancellation was within {reactivation_window} before; net new MRR (new + expansion + reactivation -
      contraction - churned); net revenue retention %, (starting MRR + expansion + reactivation - contraction - churned) /
      starting MRR x 100; and the same figures for the same 30 days a year ago. Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# MRR movement waterfall

Slash command: /mrr-movement-decomposition

## Step 1: Email the monthly MRR movement digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes subscription revenue in the last 30 days and in each 30 days over the last 12 mo, and writes these figures: new MRR, the sum of amount for customers with no active subscription before (active subscription status); expansion MRR, the sum of positive amount minus prior amount per subscription id; contraction MRR, the sum of the negative ones; churned MRR, the sum of prior amount; reactivation MRR, the sum of amount for customers whose cancellation was within 90 d before; net new MRR (new + expansion + reactivation - contraction - churned); net revenue retention %, (starting MRR + expansion + reactivation - contraction - churned) / starting MRR x 100; and the same figures for the same 30 days a year ago. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
