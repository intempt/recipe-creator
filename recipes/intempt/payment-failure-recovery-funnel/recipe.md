---
frontmatter_id: payment-failure-recovery-funnel
slash_command: /payment-failure-recovery-funnel
description: Shows how much failed payment revenue you get back, which retry attempt recovers it, and how much is still at risk.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
  - media-entertainment
  - ecommerce-retail
portable:
  summary: Shows how much failed payment revenue is recovered, which retry attempt recovers it, and how much revenue is still
    at risk.
  parameters:
  - name: conversion_window
    type: duration
    label: Conversion window
    default: 14 d
    required: false
  - name: benchmark_recovery_rate
    type: number
    label: Benchmark recovery rate (%)
    default: 70
    required: false
  - name: comparison_period
    type: enum
    label: Comparison period
    default: previous_period
    required: false
    options:
    - previous_period
    - previous_year
    - none
  - name: report_name
    type: string
    label: Report name
    default: Payment Recovery Funnel
    required: false
  requirements:
  - slot: payment_failed_event
    kind: event
    meaning: A customer's invoice payment failed
    properties:
    - name: attempt_number
      type: number
      meaning: Retry attempt number of the failed payment
      optional: false
    - name: amount_due_cents
      type: number
      meaning: Amount due on the invoice in cents
      optional: false
    - name: next_retry_at
      type: date
      meaning: Time of the next scheduled retry
      optional: true
    - name: customer_id
      type: string
      meaning: Identifier of the customer
      optional: false
  - slot: dunning_email_opened_event
    kind: event
    meaning: A customer opened an email sent as part of the dunning campaign
    properties:
    - name: campaign_id
      type: string
      meaning: Campaign identifier of the email that was sent
      optional: false
  - slot: billing_page_view_event
    kind: event
    meaning: A customer viewed a billing or account page on the website
    properties:
    - name: page_url
      type: string
      meaning: URL of the page viewed
      optional: false
  - slot: invoice_paid_event
    kind: event
    meaning: A customer's invoice was paid
    properties:
    - name: amount_paid_cents
      type: number
      meaning: Amount paid on the invoice in cents
      optional: false
    - name: customer_id
      type: string
      meaning: Identifier of the customer
      optional: false
  - slot: charge_failed_event
    kind: event
    meaning: A customer's charge attempt failed, with a failure code and message
    properties:
    - name: failure_code
      type: string
      meaning: Code describing why the charge failed
      optional: true
    - name: failure_message
      type: string
      meaning: Message describing why the charge failed
      optional: true
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - payment_failed_event
    - dunning_email_opened_event
    - billing_page_view_event
    - invoice_paid_event
    - charge_failed_event
    - conversion_window
    - comparison_period
    - benchmark_recovery_rate
    - report_name
    instruction: 'Create a funnel report named "{report_name}" with these steps in order: 1) {payment_failed_event}; 2) {dunning_email_opened_event}
      where the email belongs to the dunning campaign (campaign_id matches the dunning template); 3) {billing_page_view_event}
      where the page URL contains "/billing" or "/account"; 4) {invoice_paid_event} within {conversion_window} of step 1,
      matched on the same customer_id. Set the conversion window to {conversion_window}. Break down by the attempt_number
      property of {payment_failed_event} into buckets 1st, 2nd, 3rd, and 4th or later. Compare against {comparison_period}.
      For each step, show revenue at stake: the sum of {payment_failed_event.amount_due_cents} divided by 100 for users currently
      at that step. For users who reach the final step, show the median time to recover. Annotate the recovery rate (step
      4 divided by step 1) and compare it to a benchmark of {benchmark_recovery_rate}%. Highlight the attempt_number bucket
      with the lowest recovery rate, since later attempts usually recover less and this informs when to escalate to manual
      outreach. Show total revenue recovered (sum of {invoice_paid_event.amount_paid_cents} / 100) versus revenue lost in
      the period. If reason-level detail is needed, use {charge_failed_event.failure_code} or {charge_failed_event.failure_message}
      rather than a failure_reason property on the payment failed event.'
---

# Payment recovery funnel

Slash command: /payment-failure-recovery-funnel

## Step 1: Follow failed payments to recovery

Create a Funnel report called "Payment Recovery Funnel".
Steps:
1. Event "Invoice payment failed": "Payment Failed"
2. Event "Email opened" where the email is part of the dunning campaign (filter by Email sent.campaign_id matching dunning template): "Opened Recovery Email"
3. Event "View page" where Page URL contains "/billing" or "/account": "Visited Billing Page"
4. Event "Invoice paid" within 14 days of step 1 (same customer_id): "Payment Recovered"
Conversion window: 14 days
Breakdown: By "attempt_number" property on Invoice payment failed (1st attempt, 2nd, 3rd, 4th+): the canonical event has attempt_number
Compare: Previous period (prior 14 days)
For each step, also surface:
- Revenue at stake at this stage (sum of amount_due_cents / 100 for users currently at this step)
- Median time-to-recover for users who reach the final step
Annotations:
- Flag the recovery rate (Step 4 / Step 1) and benchmark against 70%.
- Highlight which attempt_number has the lowest recovery rate (later attempts typically recover at lower rates: informs when to escalate to manual outreach).
Surface the total revenue recovered vs. revenue lost in the period.
Taxonomy notes:
- Invoice payment failed has attempt_number, amount_due_cents, next_retry_at.
- Invoice paid has amount_paid_cents.
- "failure_reason" is not a property on Invoice payment failed; if reason-level breakdown is needed, use Charge failed.failure_code or failure_message instead.
