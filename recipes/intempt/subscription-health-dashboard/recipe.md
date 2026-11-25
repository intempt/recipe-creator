---
frontmatter_id: subscription-health-dashboard
slash_command: /subscription-health-dashboard
description: 'Emails a finance or revenue lead a monthly digest of whether subscription revenue is compounding or eroding:
  revenue movement, net revenue retention, logo retention, failed-payment recovery and expansion share.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: 'Emails a monthly subscription health digest: revenue movement, net revenue and logo retention, failed-payment
    recovery and expansion share, with alert lines on erosion.'
  parameters:
  - name: nrrErosionThreshold
    type: number
    label: Net revenue retention below which the digest warns (%)
    default: 90
    required: false
  - name: dunningRecoveryTarget
    type: number
    label: Failed-payment recovery target (%)
    default: 70
    required: false
  - name: expansionShareTarget
    type: number
    label: Expansion share of new revenue target (%)
    default: 30
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: subscription_started
    kind: event
    meaning: A customer started a subscription
  - slot: subscription_canceled
    kind: event
    meaning: A customer canceled a subscription
  - slot: subscription_resumed
    kind: event
    meaning: A customer resumed a paused or canceled subscription
    optional: true
  - slot: invoice_paid
    kind: event
    meaning: A customer's invoice was paid
    properties:
    - name: amount
      type: number
      meaning: Amount paid
      optional: false
  - slot: invoice_payment_failed
    kind: event
    meaning: A customer's invoice payment failed
  - slot: plan
    kind: attribute
    meaning: The subscription plan a customer is on
  steps:
  - id: s1
    builds: automation
    uses:
    - subscription_started
    - subscription_canceled
    - subscription_resumed
    - invoice_paid
    - invoice_payment_failed
    - plan
    - nrrErosionThreshold
    - dunningRecoveryTarget
    - expansionShareTarget
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes paying
      customers by their {invoice_paid.amount} in the last 30 days against the 30 days before and writes these figures, in
      total and per {plan}: revenue; revenue movement split into new (first {subscription_started}), expansion (paid more),
      contraction (paid less), churn ({subscription_canceled}), reactivation ({subscription_resumed}) and net new; net revenue
      retention, what customers who paid between 365 and 395 days ago paid in the last 30 days over what they paid then; logo
      retention, the share of customers paying 30 to 60 days ago still paying; failed-payment recovery, the share of customers
      with {invoice_payment_failed} between 14 and 44 days ago who did {invoice_paid} within 14 days after; expansion''s share
      of new plus expansion revenue. When net revenue retention is below {nrrErosionThreshold}%, recovery is below {dunningRecoveryTarget}%
      or expansion share is below {expansionShareTarget}%, the email''s first line says so. Then it emails these figures as
      plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Subscription revenue health

Slash command: /subscription-health-dashboard

## Step 1: Email the monthly subscription health digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes paying customers by their amount in the last 30 days against the 30 days before and writes these figures, in total and per plan: revenue; revenue movement split into new (first subscription started), expansion (paid more), contraction (paid less), churn (subscription canceled), reactivation (subscription resumed) and net new; net revenue retention, what customers who paid between 365 and 395 days ago paid in the last 30 days over what they paid then; logo retention, the share of customers paying 30 to 60 days ago still paying; failed-payment recovery, the share of customers with invoice payment failed between 14 and 44 days ago who did invoice paid within 14 days after; expansion's share of new plus expansion revenue. When net revenue retention is below 90%, recovery is below 70% or expansion share is below 30%, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
