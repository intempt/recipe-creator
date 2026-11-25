---
frontmatter_id: payment-failure-recovery-funnel
slash_command: /payment-failure-recovery-funnel
description: Builds a segment of users whose failed payment is still unpaid and emails a weekly digest of how much failed
  payment revenue you get back, by retry attempt, and how much is still at risk.
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
  summary: Builds a segment of users with unrecovered failed payments and emails a weekly digest of recovered and at-risk
    revenue by retry attempt.
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
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
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
  - slot: dunning_email_opened_event
    kind: event
    meaning: A customer opened an email sent as part of the dunning campaign
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
  - slot: charge_failed_event
    kind: event
    meaning: A customer's charge attempt failed, with a failure code and message
    properties:
    - name: failure_code
      type: string
      meaning: Code describing why the charge failed
      optional: false
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - payment_failed_event
    - invoice_paid_event
    - conversion_window
    instruction: Build a new segment of users named "Unrecovered Failed Payments". A user is in it when they did {payment_failed_event}
      in the last {conversion_window} and did not do {invoice_paid_event} after their latest {payment_failed_event}.
  - id: s2
    builds: automation
    uses:
    - s1
    - payment_failed_event
    - dunning_email_opened_event
    - billing_page_view_event
    - invoice_paid_event
    - charge_failed_event
    - conversion_window
    - benchmark_recovery_rate
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {payment_failed_event}
      in the last 30 days, against the 30 days before, through these steps within {conversion_window}: payment failed; opened
      a dunning email ({dunning_email_opened_event}); viewed billing ({billing_page_view_event} with {billing_page_view_event.page_url}
      containing "/billing" or "/account"); paid ({invoice_paid_event}). It writes: users at each step; recovery rate %, paid
      / failed, split by {payment_failed_event.attempt_number} as 1st, 2nd, 3rd and 4th or later; median days to recover;
      revenue recovered, the sum of {invoice_paid_event.amount_paid_cents} / 100; revenue still at risk, the sum of {payment_failed_event.amount_due_cents}
      / 100 for users in the segment from "Find users with unrecovered failed payments"; the top {charge_failed_event.failure_code}
      values when it is set. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      The email compares the recovery rate with {benchmark_recovery_rate}% and names the attempt with the lowest recovery
      rate. Nothing else is sent.'
---

# Payment recovery funnel

Slash command: /payment-failure-recovery-funnel

## Step 1: Find users with unrecovered failed payments

Build a new segment of users named "Unrecovered Failed Payments". A user is in it when they did payment failed event in the last 14 d and did not do invoice paid event after their latest payment failed event.

## Step 2: Email the weekly payment recovery digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did payment failed event in the last 30 days, against the 30 days before, through these steps within 14 d: payment failed; opened a dunning email (dunning email opened event); viewed billing (billing page view event with page url containing "/billing" or "/account"); paid (invoice paid event). It writes: users at each step; recovery rate %, paid / failed, split by attempt number as 1st, 2nd, 3rd and 4th or later; median days to recover; revenue recovered, the sum of amount paid cents / 100; revenue still at risk, the sum of amount due cents / 100 for users in the segment from "Find users with unrecovered failed payments"; the top failure code values when it is set. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email compares the recovery rate with 70% and names the attempt with the lowest recovery rate. Nothing else is sent.
