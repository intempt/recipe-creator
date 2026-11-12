---
frontmatter_id: stripe-subscription-sync
slash_command: /stripe-subscription-sync
description: Keeps plan, status, revenue and renewal dates on every profile in step with Stripe, so segmentation and churn reporting match billing reality.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Keeps each user's plan, subscription status, revenue and renewal dates in step with Stripe, so segments and churn
    reports match billing, and checks the data agrees.
  parameters:
  - name: churn_seat_check
    type: boolean
    label: Roll up churn to the account when the only seat churns
    default: true
    required: false
  - name: drift_tolerance_percent
    type: number
    label: Allowed MRR mismatch between profiles and Stripe (%)
    default: 1
    required: false
  requirements:
  - slot: stripe_user_attributes
    kind: attribute
    meaning: User profile attributes that hold subscription status, plan tier, MRR, start date, next renewal date and payment
      failure flag
  - slot: stripe_customer_id
    kind: attribute
    meaning: User attribute storing the customer identifier from Stripe
  - slot: lifecycle_stage
    kind: attribute
    meaning: User attribute holding the lifecycle stage of the customer
  - slot: account_lifecycle
    kind: attribute
    meaning: Account attribute holding the account lifecycle stage
  - slot: stripe_webhook_events
    kind: integration
    meaning: A connected Stripe account delivering subscription and invoice webhook events
    channel: hubspot
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
  - slot: subscription_churned_event
    kind: event
    meaning: A customer's subscription was canceled
  - slot: payment_recovered_event
    kind: event
    meaning: A customer's failed payment was recovered
  steps:
  - id: s1
    builds: attribute
    uses:
    - stripe_user_attributes
    instruction: 'Create these User attributes, sourced from Stripe events and refreshed on every webhook: subscription_status
      (active, trialing, past_due, cancelled, none); plan_tier (free, starter, professional, enterprise, custom); mrr (current
      monthly recurring revenue); subscription_start_date; next_renewal_date; has_payment_failure (boolean). These are the
      source-of-truth fields for lifecycle segmentation.'
  - id: s2
    builds: automation
    uses:
    - s1
    - stripe_user_attributes
    - stripe_customer_id
    - lifecycle_stage
    - account_lifecycle
    - stripe_webhook_events
    - subscription_started_event
    - subscription_churned_event
    - payment_recovered_event
    - churn_seat_check
    instruction: 'Create a workflow triggered by Stripe webhook events (subscription started, subscription updated, subscription
      canceled, payment failed, invoice paid). Step 1: parse the Stripe event payload. Step 2: match the user by stripe_customer_id;
      if no user exists, create one (checkout-without-signup case). Step 3: update all billing attributes from the "Hold the
      billing facts" step. Step 4: update lifecycle_stage by transition: subscription started sets ''customer'', subscription
      canceled sets ''churned'', payment failed sets ''at_risk''. Step 5: emit derived events {subscription_started_event}
      for started, {subscription_churned_event} for canceled, and {payment_recovered_event} for recovered invoices, so journeys
      trigger on canonical names instead of Stripe-specific names. Step 6: if {churn_seat_check} is true, and the user is
      the only seat on the account and has just churned, set {account_lifecycle} to churned.'
  - id: s3
    builds: dashboard
    uses:
    - s1
    - s2
    - drift_tolerance_percent
    - stripe_webhook_events
    instruction: 'Build a billing data integrity dashboard with: percent of users whose subscription_status is synced with
      Stripe ground truth (target 100%); webhook delivery failure count; users with billing drift, where Stripe shows active
      but the profile shows cancelled; and MRR computed from profile attributes compared with MRR from the Stripe API, flagged
      when the difference exceeds {drift_tolerance_percent} percent. Use the attributes from "Hold the billing facts" and
      the workflow from "Apply every Stripe event".'
---

# Sync Stripe subscriptions

Slash command: /stripe-subscription-sync

## Step 1: Hold the billing facts

Create attributes on the User object: 'subscription_status' (active / trialing / past_due / cancelled / none), 'plan_tier' (free / starter / professional / enterprise / custom), 'mrr' (current monthly recurring revenue), 'subscription_start_date', 'next_renewal_date', 'has_payment_failure' (boolean). Sourced from Stripe events, refreshed on every webhook. These are the source-of-truth fields for lifecycle segmentation.

## Step 2: Apply every Stripe event

Create a workflow firing on Stripe webhook events. Step sequence: (1) parse the Stripe event payload (Subscription started/updated/canceled/Payment failed/Invoice paid); (2) match to user via stripe_customer_id (create user if doesn't exist: checkout-without-signup case); (3) update all billing attributes; (4) update user lifecycle_stage based on transition: Subscription started to 'customer', Subscription canceled to 'churned', Payment failed to 'at_risk'; (5) emit derived events to the event catalog (subscription_started, subscription_churned, payment_recovered) so journeys can trigger on canonical names not Stripe-specific names; (6) account-level rollup: if this is the only seat on the account and just churned, set account.lifecycle = churned. Use the result of "Hold the billing facts".

## Step 3: Prove the two agree

Compose a billing-data integrity dashboard: % of users with subscription_status synced (against Stripe ground-truth: should be 100%), webhook delivery failure count (signal of integration issues), users with billing-attribute drift (Stripe shows active but profile shows cancelled = sync bug), and MRR computed-from-profile-attributes vs. MRR-from-Stripe-API (should match within 1%). This is the recipe that makes every other recipe's MRR/churn computation trustworthy. Use the result of "Hold the billing facts", "Apply every Stripe event".
