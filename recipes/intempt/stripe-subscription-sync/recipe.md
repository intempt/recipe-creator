---
description: Keeps plan, status, revenue and renewal dates on every profile in step with Stripe, so segmentation and churn reporting match billing reality.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - finance
  - media
---

# Sync Stripe subscriptions

Slash command: /stripe-subscription-sync

## Step 1: Hold the billing facts

Create attributes on the User object: 'subscription_status' (active / trialing / past_due / cancelled / none), 'plan_tier' (free / starter / professional / enterprise / custom), 'mrr' (current monthly recurring revenue), 'subscription_start_date', 'next_renewal_date', 'has_payment_failure' (boolean). Sourced from Stripe events, refreshed on every webhook. These are the source-of-truth fields for lifecycle segmentation.

## Step 2: Apply every Stripe event

Create a workflow firing on Stripe webhook events. Step sequence: (1) parse the Stripe event payload (subscription_created/updated/canceled/payment_failed/invoice_paid); (2) match to user via stripe_customer_id (create user if doesn't exist: checkout-without-signup case); (3) update all billing attributes; (4) update user lifecycle_stage based on transition: subscription_created to 'customer', subscription_canceled to 'churned', payment_failed to 'at_risk'; (5) emit derived events to the event catalog (subscription_started, subscription_churned, payment_recovered) so journeys can trigger on canonical names not Stripe-specific names; (6) account-level rollup: if this is the only seat on the account and just churned, set account.lifecycle = churned. Use the result of "Hold the billing facts".

## Step 3: Prove the two agree

Compose a billing-data integrity dashboard: % of users with subscription_status synced (against Stripe ground-truth: should be 100%), webhook delivery failure count (signal of integration issues), users with billing-attribute drift (Stripe shows active but profile shows cancelled = sync bug), and MRR computed-from-profile-attributes vs. MRR-from-Stripe-API (should match within 1%). This is the recipe that makes every other recipe's MRR/churn computation trustworthy. Use the result of "Hold the billing facts", "Apply every Stripe event".
