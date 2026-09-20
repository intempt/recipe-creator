---
name: stripe-subscription-sync
description: Use when a user mentions "stripe subscription sync", "subscription state workflow", "billing event integration", or asks for related help. When Stripe sends a subscription_created / updated / cancelled / payment_failed event, sync the state to the user profile + account lifecycle stage, so segmentation, retention, and reporting always reflect actual billing reality.
arguments: []
intempt:
  id: stripe-subscription-sync
  title: "Sync Stripe subscriptions"
  version: 1.0.0
  slashCommand: /stripe-subscription-sync
  group: Workflows
  shortDescription: "Keeps plan, status, revenue and renewal dates on every profile in step with Stripe, so segmentation and churn reporting match billing reality."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [saas]
    complexity: standard
    executionMode: live
    tags: [stripe-sync, billing-events, data-integrity]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: subscription_created, severity: blocking }
      - { value: subscription_updated, severity: recommended }
      - { value: subscription_canceled, severity: recommended }
    integrations:
      - { value: stripe, severity: blocking }
  invokesCommands:
    - create_attribute
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Hold the billing facts"
      command: create_attribute
      produces: attribute
      bindsAs: billing_attrs
      description: "On each person: subscription status of active, trialing, past due, cancelled or none, the plan tier, current monthly revenue, the start date, the next renewal date, and whether a payment has failed. All sourced from Stripe and refreshed on every webhook."
      prompt: 'Create attributes on the User object: ''subscription_status'' (active / trialing / past_due / cancelled / none), ''plan_tier'' (free / starter / professional / enterprise / custom), ''mrr'' (current monthly recurring revenue), ''subscription_start_date'', ''next_renewal_date'', ''has_payment_failure'' (boolean). Sourced from Stripe events, refreshed on every webhook. These are the source-of-truth fields for lifecycle segmentation.'
    - step: 2
      title: "Apply every Stripe event"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - billing_attrs
      description: "On each webhook it reads the event, matches the Stripe customer to a user and creates one where they checked out without signing up, updates every billing field, moves the lifecycle stage, with a new subscription making them a customer, a cancellation churned and a failed payment at risk, emits events under your own names so journeys do not depend on Stripe's, and marks the account churned when its last seat goes."
      prompt: 'Create a workflow firing on Stripe webhook events. Step sequence: (1) parse the Stripe event payload (subscription_created/updated/canceled/payment_failed/invoice_paid); (2) match to user via stripe_customer_id (create user if doesn''t exist: checkout-without-signup case); (3) update all billing attributes; (4) update user lifecycle_stage based on transition: subscription_created to ''customer'', subscription_canceled to ''churned'', payment_failed to ''at_risk''; (5) emit derived events to the event catalog (subscription_started, subscription_churned, payment_recovered) so journeys can trigger on canonical names not Stripe-specific names; (6) account-level rollup: if this is the only seat on the account and just churned, set account.lifecycle = churned.'
    - step: 3
      title: "Prove the two agree"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - billing_attrs
      - workflow
      description: "The share of users whose status matches Stripe, which should be all of them, failed webhook deliveries, profiles that disagree with Stripe, which means a sync bug, and monthly revenue computed from profiles against Stripe's own figure, which should match within 1%."
      prompt: 'Compose a billing-data integrity dashboard: % of users with subscription_status synced (against Stripe ground-truth: should be 100%), webhook delivery failure count (signal of integration issues), users with billing-attribute drift (Stripe shows active but profile shows cancelled = sync bug), and MRR computed-from-profile-attributes vs. MRR-from-Stripe-API (should match within 1%). This is the recipe that makes every other recipe''s MRR/churn computation trustworthy.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Sync Stripe subscriptions

Keeps plan, status, revenue and renewal dates on every profile in step with Stripe, so segmentation and churn reporting match billing reality.

## Before you run it

- Connect stripe
- Send the `subscription_created` event
- Send the `subscription_updated` event
- Send the `subscription_canceled` event

## What it does

1. **Hold the billing facts** (`create_attribute`)

   On each person: subscription status of active, trialing, past due, cancelled or none, the plan tier, current monthly revenue, the start date, the next renewal date, and whether a payment has failed. All sourced from Stripe and refreshed on every webhook.

2. **Apply every Stripe event** (`create_workflow`)

   On each webhook it reads the event, matches the Stripe customer to a user and creates one where they checked out without signing up, updates every billing field, moves the lifecycle stage, with a new subscription making them a customer, a cancellation churned and a failed payment at risk, emits events under your own names so journeys do not depend on Stripe's, and marks the account churned when its last seat goes.

3. **Prove the two agree** (`create_dashboard`)

   The share of users whose status matches Stripe, which should be all of them, failed webhook deliveries, profiles that disagree with Stripe, which means a sync bug, and monthly revenue computed from profiles against Stripe's own figure, which should match within 1%.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
