---
name: stripe-subscription-sync
description: Use when a user mentions "stripe subscription sync", "subscription state workflow", "billing event integration", or asks for related help. When Stripe sends a subscription_created / updated / cancelled / payment_failed event, sync the state to the user profile + account lifecycle stage, so segmentation, retention, and reporting always reflect actual billing reality.
arguments: []
intempt:
  id: stripe-subscription-sync
  version: 1.0.0
  slashCommand: /stripe-subscription-sync
  group: Workflows
  shortDescription: "Create User attributes (subscription_status, plan_tier, mrr, renewal dates, has_payment_failure) and a Stripe-webhook workflow that keeps them synced for lifecycle segmentation."
  availability: coming-soon
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
      title: Build Billing State Attributes
      command: create_attribute
      produces: attribute
      bindsAs: billing_attrs
      description: 'Create attributes on the User object: ''subscription_status'' (active / trialing / past_due / cancelled / none), ''plan_tier'' (free / starter / professional / enterprise / custom), ''mrr'' (current monthly recurring revenue), ''subscription_start_date'', ''next_renewal_date'', ''has_payment_failure'' (boolean). Sourced from Stripe events, refreshed on every webhook. These are the source-of-truth fields for lifecycle segmentation.'
      prompt: 'Create attributes on the User object: ''subscription_status'' (active / trialing / past_due / cancelled / none), ''plan_tier'' (free / starter / professional / enterprise / custom), ''mrr'' (current monthly recurring revenue), ''subscription_start_date'', ''next_renewal_date'', ''has_payment_failure'' (boolean). Sourced from Stripe events, refreshed on every webhook. These are the source-of-truth fields for lifecycle segmentation.'
    - step: 2
      title: Build Stripe Sync Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - billing_attrs
      description: 'Create a workflow firing on Stripe webhook events. Step sequence: (1) parse the Stripe event payload (subscription_created/updated/canceled/payment_failed/invoice_paid); (2) match to user via stripe_customer_id (create user if doesn''t exist — checkout-without-signup case); (3) update all billing attributes; (4) update user lifecycle_stage based on transition: subscription_created → ''customer'', subscription_canceled → ''churned'', payment_failed → ''at_risk''; (5) emit derived events to the event catalog (subscription_started, subscription_churned, payment_recovered) so journeys can trigger on canonical names not Stripe-specific names; (6) account-level rollup: if this is the only seat on the account and just churned, set account.lifecycle = churned.'
      prompt: 'Create a workflow firing on Stripe webhook events. Step sequence: (1) parse the Stripe event payload (subscription_created/updated/canceled/payment_failed/invoice_paid); (2) match to user via stripe_customer_id (create user if doesn''t exist — checkout-without-signup case); (3) update all billing attributes; (4) update user lifecycle_stage based on transition: subscription_created → ''customer'', subscription_canceled → ''churned'', payment_failed → ''at_risk''; (5) emit derived events to the event catalog (subscription_started, subscription_churned, payment_recovered) so journeys can trigger on canonical names not Stripe-specific names; (6) account-level rollup: if this is the only seat on the account and just churned, set account.lifecycle = churned.'
    - step: 3
      title: Build Billing Data Integrity Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - billing_attrs
      - workflow
      description: 'Compose a billing-data integrity dashboard: % of users with subscription_status synced (against Stripe ground-truth — should be 100%), webhook delivery failure count (signal of integration issues), users with billing-attribute drift (Stripe shows active but profile shows cancelled = sync bug), and MRR computed-from-profile-attributes vs. MRR-from-Stripe-API (should match within 1%). This is the recipe that makes every other recipe''s MRR/churn computation trustworthy.'
      prompt: 'Compose a billing-data integrity dashboard: % of users with subscription_status synced (against Stripe ground-truth — should be 100%), webhook delivery failure count (signal of integration issues), users with billing-attribute drift (Stripe shows active but profile shows cancelled = sync bug), and MRR computed-from-profile-attributes vs. MRR-from-Stripe-API (should match within 1%). This is the recipe that makes every other recipe''s MRR/churn computation trustworthy.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Stripe Subscription Sync

## Procedure

1. **Build Billing State Attributes** [`create_attribute`] — Create attributes on the User object: 'subscription_status' (active / trialing / past_due / cancelled / none), 'plan_tier' (free / starter / professional / enterprise / custom), 'mrr' (current monthly recurring revenue), 'subscription_start_date', 'next_renewal_date', 'has_payment_failure' (boolean). Sourced from Stripe events, refreshed on every webhook. These are the source-of-truth fields for lifecycle segmentation. → produces: attribute
2. **Build Stripe Sync Workflow** [`create_workflow`] — Create a workflow firing on Stripe webhook events. Step sequence: (1) parse the Stripe event payload (subscription_created/updated/canceled/payment_failed/invoice_paid); (2) match to user via stripe_customer_id (create user if doesn't exist — checkout-without-signup case); (3) update all billing attributes; (4) update user lifecycle_stage based on transition: subscription_created → 'customer', subscription_canceled → 'churned', payment_failed → 'at_risk'; (5) emit derived events to the event catalog (subscription_started, subscription_churned, payment_recovered) so journeys can trigger on canonical names not Stripe-specific names; (6) account-level rollup: if this is the only seat on the account and just churned, set account.lifecycle = churned. → produces: workflow
3. **Build Billing Data Integrity Dashboard** [`create_dashboard`] — Compose a billing-data integrity dashboard: % of users with subscription_status synced (against Stripe ground-truth — should be 100%), webhook delivery failure count (signal of integration issues), users with billing-attribute drift (Stripe shows active but profile shows cancelled = sync bug), and MRR computed-from-profile-attributes vs. MRR-from-Stripe-API (should match within 1%). This is the recipe that makes every other recipe's MRR/churn computation trustworthy. → produces: dashboard
