---
frontmatter_id: payment-failure-recovery-funnel
slash_command: /payment-failure-recovery-funnel
description: This recipe helps subscription and billing teams see where failed payments are won back or lost, then act on the customers who are still unpaid. It tracks recovery from the first failure through to payment, builds a list of unrecovered customers, and sets up a hand-off to a person.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
---

# Payment recovery funnel

## Step 1: Follow failed payments to recovery

Create a Funnel report called "Payment Recovery Funnel".
Steps:
1. Event "Invoice payment failed": "Payment Failed"
2. Event "Email opened" where the email's Email sent.campaign_id matches the dunning template: "Opened Recovery Email"
3. Event "View page" where Page URL contains "/billing" or "/account": "Visited Billing Page"
4. Event "Invoice paid" within 14 days of step 1, same customer_id: "Payment Recovered"
Conversion window: 14 days
Breakdown: By "attempt_number" property on Invoice payment failed (1st, 2nd, 3rd, 4th or more)
Compare: Previous period (prior 14 days)
For each step, also surface:
- Revenue at stake at this stage (sum of amount_due_cents divided by 100, for users currently at this step)
- Median time-to-recover for users who reach the final step
Annotations:
- Flag the recovery rate (Step 4 divided by Step 1) against a 70 percent benchmark.
- Highlight which attempt_number has the lowest recovery rate.
Taxonomy notes:
- Invoice payment failed has attempt_number, amount_due_cents, next_retry_at.
- Invoice paid has amount_paid_cents.
- "failure_reason" is not a property on Invoice payment failed; use Charge failed.failure_code or failure_message for a reason-level breakdown instead.

## Step 2: Escalate payments still unrecovered after the automated retries

Build a segment of users named "Unrecovered Failed Payments". A user is in the segment only when all of these are true: they have an "Invoice payment failed" event with attempt_number of 3 or more in the last 14 days; they do not have an "Invoice paid" event for the same customer_id since that failure. Use the result of "Follow failed payments to recovery".

## Step 3: Hand unrecovered payments to a person

Build a workflow triggered when a user enters "Unrecovered Failed Payments". Create a task for the billing owner with the failed invoice amount, the number of retry attempts, and next_retry_at, due within 1 business day. Send the user a final recovery email offering a direct link to update their payment method and a link to contact billing support. Exit when the invoice is paid or when the subscription is canceled for non-payment. Use the result of "Follow failed payments to recovery", "Escalate payments still unrecovered after the automated retries".
