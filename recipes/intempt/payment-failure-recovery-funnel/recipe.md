---
id: payment-failure-recovery-funnel
title: Payment recovery funnel
slash_command: /payment-failure-recovery-funnel
group: Reports
owner: intempt
summary: Shows how much failed payment revenue you get back, which retry attempt recovers it, and how
  much is still at risk.
description: >-
  Dunning recovery funnel using canonical billing events with per-attempt success rate and revenue-at-risk.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  complexity: quick
  executionMode: live
  tags:
    - funnel
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Follow failed payments to recovery"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Follow failed payments to recovery
    summary: >-
      A four step funnel over 14 days from a failed invoice payment to opening the recovery email, visiting
      billing and paying, split by retry attempt number, with the revenue at stake at each stage and a
      70% recovery benchmark.
    builds: report
    description: |-
      Create a Funnel report called "Payment Recovery Funnel".
      Steps:
      1. Event "invoice_payment_failed": "Payment Failed"
      2. Event "email_opened" where the email is part of the dunning campaign (filter by email_sent.campaign_id matching dunning template): "Opened Recovery Email"
      3. Event "page_viewed" where page_url contains "/billing" or "/account": "Visited Billing Page"
      4. Event "invoice_paid" within 14 days of step 1 (same customer_id): "Payment Recovered"
      Conversion window: 14 days
      Breakdown: By "attempt_number" property on invoice_payment_failed (1st attempt, 2nd, 3rd, 4th+): the canonical event has attempt_number
      Compare: Previous period (prior 14 days)
      For each step, also surface:
      - Revenue at stake at this stage (sum of amount_due_cents / 100 for users currently at this step)
      - Median time-to-recover for users who reach the final step
      Annotations:
      - Flag the recovery rate (Step 4 / Step 1) and benchmark against 70%.
      - Highlight which attempt_number has the lowest recovery rate (later attempts typically recover at lower rates: informs when to escalate to manual outreach).
      Surface the total revenue recovered vs. revenue lost in the period.
      Taxonomy notes:
      - invoice_payment_failed has attempt_number, amount_due_cents, next_retry_at.
      - invoice_paid has amount_paid_cents.
      - "failure_reason" is not a property on invoice_payment_failed; if reason-level breakdown is needed, use charge_failed.failure_code or failure_message instead.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Payment recovery funnel

Shows how much failed payment revenue you get back, which retry attempt recovers it, and how much is still at risk.

## Steps

1. **Follow failed payments to recovery** (builds report)

   A four step funnel over 14 days from a failed invoice payment to opening the recovery email, visiting billing and paying, split by retry attempt number, with the revenue at stake at each stage and a 70% recovery benchmark.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Follow failed payments to recovery"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
