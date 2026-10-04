---
id: stripe-subscription-sync
title: Sync Stripe subscriptions
slash_command: /stripe-subscription-sync
group: Workflows
owner: intempt
curator: trishik
summary: Keeps plan, status, revenue and renewal dates on every profile in step with Stripe, so segmentation
  and churn reporting match billing reality.
description: >-
  When Stripe sends a subscription_created / updated / cancelled / payment_failed event, sync the state
  to the user profile + account lifecycle stage, so segmentation, retention, and reporting always reflect
  actual billing reality.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - saas
  complexity: standard
  executionMode: live
  tags:
    - stripe-sync
    - billing-events
    - data-integrity
prerequisites:
  events:
    - value: subscription_created
      severity: blocking
    - value: subscription_updated
      severity: recommended
    - value: subscription_canceled
      severity: recommended
  integrations:
    - value: stripe
      severity: blocking
touches:
  reads:
    - The subscription_created event in your project
    - The subscription_updated event in your project
    - The subscription_canceled event in your project
    - Your Stripe connection
  writes:
    - A new attribute, from step 1 "Hold the billing facts"
    - A new workflow, from step 2 "Apply every Stripe event"
    - A new dashboard, from step 3 "Prove the two agree"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Hold the billing facts
    summary: >-
      On each person: subscription status of active, trialing, past due, cancelled or none, the plan tier,
      current monthly revenue, the start date, the next renewal date, and whether a payment has failed.
      All sourced from Stripe and refreshed on every webhook.
    builds: attribute
    description: >-
      Create attributes on the User object: 'subscription_status' (active / trialing / past_due / cancelled
      / none), 'plan_tier' (free / starter / professional / enterprise / custom), 'mrr' (current monthly
      recurring revenue), 'subscription_start_date', 'next_renewal_date', 'has_payment_failure' (boolean).
      Sourced from Stripe events, refreshed on every webhook. These are the source-of-truth fields for
      lifecycle segmentation.
  - id: s2
    title: Apply every Stripe event
    summary: >-
      On each webhook it reads the event, matches the Stripe customer to a user and creates one where
      they checked out without signing up, updates every billing field, moves the lifecycle stage, with
      a new subscription making them a customer, a cancellation churned and a failed payment at risk,
      emits events under your own names so journeys do not depend on Stripe's, and marks the account churned
      when its last seat goes.
    builds: workflow
    description: >-
      Create a workflow firing on Stripe webhook events. Step sequence: (1) parse the Stripe event payload
      (subscription_created/updated/canceled/payment_failed/invoice_paid); (2) match to user via stripe_customer_id
      (create user if doesn't exist: checkout-without-signup case); (3) update all billing attributes;
      (4) update user lifecycle_stage based on transition: subscription_created to 'customer', subscription_canceled
      to 'churned', payment_failed to 'at_risk'; (5) emit derived events to the event catalog (subscription_started,
      subscription_churned, payment_recovered) so journeys can trigger on canonical names not Stripe-specific
      names; (6) account-level rollup: if this is the only seat on the account and just churned, set account.lifecycle
      = churned. Use the result of "Hold the billing facts".
    dependsOn:
      - s1
  - id: s3
    title: Prove the two agree
    summary: >-
      The share of users whose status matches Stripe, which should be all of them, failed webhook deliveries,
      profiles that disagree with Stripe, which means a sync bug, and monthly revenue computed from profiles
      against Stripe's own figure, which should match within 1%.
    builds: dashboard
    description: >-
      Compose a billing-data integrity dashboard: % of users with subscription_status synced (against
      Stripe ground-truth: should be 100%), webhook delivery failure count (signal of integration issues),
      users with billing-attribute drift (Stripe shows active but profile shows cancelled = sync bug),
      and MRR computed-from-profile-attributes vs. MRR-from-Stripe-API (should match within 1%). This
      is the recipe that makes every other recipe's MRR/churn computation trustworthy. Use the result
      of "Hold the billing facts", "Apply every Stripe event".
    dependsOn:
      - s1
      - s2
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Sync Stripe subscriptions

Keeps plan, status, revenue and renewal dates on every profile in step with Stripe, so segmentation and churn reporting match billing reality.

## Steps

1. **Hold the billing facts** (builds attribute)

   On each person: subscription status of active, trialing, past due, cancelled or none, the plan tier, current monthly revenue, the start date, the next renewal date, and whether a payment has failed. All sourced from Stripe and refreshed on every webhook.

2. **Apply every Stripe event** (builds workflow)

   On each webhook it reads the event, matches the Stripe customer to a user and creates one where they checked out without signing up, updates every billing field, moves the lifecycle stage, with a new subscription making them a customer, a cancellation churned and a failed payment at risk, emits events under your own names so journeys do not depend on Stripe's, and marks the account churned when its last seat goes.

3. **Prove the two agree** (builds dashboard)

   The share of users whose status matches Stripe, which should be all of them, failed webhook deliveries, profiles that disagree with Stripe, which means a sync bug, and monthly revenue computed from profiles against Stripe's own figure, which should match within 1%.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The subscription_created event in your project
- The subscription_updated event in your project
- The subscription_canceled event in your project
- Your Stripe connection

Writes:

- A new attribute, from step 1 "Hold the billing facts"
- A new workflow, from step 2 "Apply every Stripe event"
- A new dashboard, from step 3 "Prove the two agree"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
