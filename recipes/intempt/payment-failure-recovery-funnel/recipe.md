---
description: Shows how much failed payment revenue you get back, which retry attempt recovers it, and how much is still at risk.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - finance
---

# Payment recovery funnel

Slash command: /payment-failure-recovery-funnel

## Step 1: Follow failed payments to recovery

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
