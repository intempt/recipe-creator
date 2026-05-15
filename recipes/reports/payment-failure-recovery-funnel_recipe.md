---
name: payment-failure-recovery-funnel
description: |
  Use when a user mentions "payment failure recovery funnel", or asks for related help. Dunning recovery funnel using canonical billing events with per-attempt success rate and revenue-at-risk.
arguments: []
intempt:
  id: payment-failure-recovery-funnel
  version: 1.0.0
  slashCommand: /payment-failure-recovery-funnel
  group: Reports
  shortDescription: "Dunning recovery funnel using canonical billing events with per-attempt success rate and revenue-at-risk."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [funnel]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_funnel_report
  procedure:
    - step: 1
      title: "Build Funnel Report"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Funnel report called "Payment Recovery Funnel".

        Steps:
        1. Event "invoice_payment_failed" — "Payment Failed"
        2. Event "email_opened" where the email is part of the dunning campaign (filter by email_sent.campaign_id matching dunning template) — "Opened Recovery Email"
        3. Event "page_viewed" where page_url contains "/billing" or "/account" — "Visited Billing Page"
        4. Event "invoice_paid" within 14 days of step 1 (same customer_id) — "Payment Recovered"

        Conversion window: 14 days
        Breakdown: By "attempt_number" property on invoice_payment_failed (1st attempt, 2nd, 3rd, 4th+) — the canonical event has attempt_number
        Compare: Previous period (prior 14 days)

        For each step, also surface:
        - Revenue at stake at this stage (sum of amount_due_cents / 100 for users currently at this step)
        - Median time-to-recover for users who reach the final step

        Annotations:
        - Flag the recovery rate (Step 4 / Step 1) and benchmark against 70%.
        - Highlight which attempt_number has the lowest recovery rate (later attempts typically recover at lower rates — informs when to escalate to manual outreach).

        Surface the total revenue recovered vs. revenue lost in the period.

        Taxonomy notes:
        - invoice_payment_failed has attempt_number, amount_due_cents, next_retry_at.
        - invoice_paid has amount_paid_cents.
        - "failure_reason" is not a property on invoice_payment_failed; if reason-level breakdown is needed, use charge_failed.failure_code or failure_message instead.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Payment failure recovery funnel

## Procedure

1. **Build Funnel Report** [`build_funnel_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Funnel report called "Payment Recovery Funnel".

   Steps:
   1. Event "invoice_payment_failed" — "Payment Failed"
   2. Event "email_opened" where the email is part of the dunning campaign (filter by email_sent.campaign_id matching dunning template) — "Opened Recovery Email"
   3. Event "page_viewed" where page_url contains "/billing" or "/account" — "Visited Billing Page"
   4. Event "invoice_paid" within 14 days of step 1 (same customer_id) — "Payment Recovered"

   Conversion window: 14 days
   Breakdown: By "attempt_number" property on invoice_payment_failed (1st attempt, 2nd, 3rd, 4th+) — the canonical event has attempt_number
   Compare: Previous period (prior 14 days)

   For each step, also surface:
   - Revenue at stake at this stage (sum of amount_due_cents / 100 for users currently at this step)
   - Median time-to-recover for users who reach the final step

   Annotations:
   - Flag the recovery rate (Step 4 / Step 1) and benchmark against 70%.
   - Highlight which attempt_number has the lowest recovery rate (later attempts typically recover at lower rates — informs when to escalate to manual outreach).

   Surface the total revenue recovered vs. revenue lost in the period.

   Taxonomy notes:
   - invoice_payment_failed has attempt_number, amount_due_cents, next_retry_at.
   - invoice_paid has amount_paid_cents.
   - "failure_reason" is not a property on invoice_payment_failed; if reason-level breakdown is needed, use charge_failed.failure_code or failure_message instead.
   ```
