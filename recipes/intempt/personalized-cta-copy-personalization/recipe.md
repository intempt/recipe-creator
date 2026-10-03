---
id: personalized-cta-copy-personalization
title: CTA wording by account state
slash_command: /personalized-cta-copy-personalization
group: Personalizations
owner: intempt
summary: The main button reads differently for a first-time visitor, a returning one, someone mid-trial,
  a free-plan user and a paying customer, instead of one generic prompt.
description: >-
  Show personalized CTA copy per audience segment (first-time: "Start your free trial"; returning: "Continue
  where you left off"; existing customer: "Upgrade to Pro"). 202% lift cited.
version: 2.0.0
classification:
  product:
    - experiences
  agent: experiment-strategist
  mode:
    - saas
    - b2b
  complexity: standard
  executionMode: live
  tags:
    - personalization
    - client
steps:
  - id: s1
    title: Set up the five CTA variants
    summary: >-
      A first visit reads Start your free trial, a return visit without an account reads Continue exploring,
      a live trial reads Continue your trial, a free plan reads Upgrade to Pro, and a paying customer
      reads Open dashboard.
    builds: personalization
    description: |-
      Create a CLIENT PERSONALIZATION on /experiences titled "Personalized CTA Copy".
      This personalization changes the primary CTA copy per audience segment. Each variant binds to a lifecycle audience.
      ═══ PATH 1: Top-level configuration ═══
      Experience type: client_personalization
      Variants (each binds to a lifecycle/visitor-stage audience):
      - Control (audience = all (fallback): generic CTA) "Get started"
      - Variant B (audience = "First-time visitors / no account"): "Start your free trial"
       - Audience: Users.first_seen_at within current session OR Users.first_seen_at is null
       - AND Users has no subscription_created event
      - Variant C (audience = "Returning visitors / no account / no signup"): "Continue exploring [Brand]"
       - Audience: Users.first_seen_at older than current session AND Users has no user_created event
      - Variant D (audience = "Free trial users currently on trial"): "Continue your trial"
       - Audience: Users has user_created event AND Users has no subscription_created event with billing_period set
      - Variant E (audience = "Active free plan users"): "Upgrade to Pro"
       - Audience: Users has subscription_created where plan_name = "free"
      - Variant F (audience = "Paying customers"): "Open dashboard"
       - Audience: Users has subscription_created where plan_name != "free" AND no subscription_cancelled
      Targeting:
      - Pages: homepage "/", marketing pages, /pricing, /features
      - Devices: any
      - Display frequency: always
      Metrics (CRM/CDP):
      - click_on per CTA copy per audience (per-segment CTR is the headline metric)
      - Downstream conversion: signup, trial-to-paid, free-to-paid upgrade: measured per audience
      Schedule: continuous
      ═══ PATH 2: Variant HTML content (Visual Editor) ═══
      Variant: Control (no DOM changes: fallback "Get started" remains)
      Variant: B (first-time visitors)
       HTML target selector: .primary-cta-button (the page's primary CTA)
       Replacement HTML:
       <button class="primary-cta" data-variant="b" data-audience="first-time" id="primary-cta">
       Start your free trial
       </button>
      Variant: C (returning, no account)
       HTML target selector: .primary-cta-button
       Replacement HTML:
       <button class="primary-cta" data-variant="c" data-audience="returning" id="primary-cta">
       Continue exploring [Brand]
       </button>
      Variant: D (trial users)
       HTML target selector: .primary-cta-button
       Replacement HTML:
       <button class="primary-cta" data-variant="d" data-audience="trial" id="primary-cta">
       Continue your trial
       </button>
      Variant: E (free plan users)
       HTML target selector: .primary-cta-button
       Replacement HTML:
       <button class="primary-cta" data-variant="e" data-audience="free-plan" id="primary-cta">
       Upgrade to Pro
       </button>
      Variant: F (paying customers)
       HTML target selector: .primary-cta-button
       Replacement HTML:
       <button class="primary-cta" data-variant="f" data-audience="paying" id="primary-cta">
       Open dashboard
       </button>
      The Visual Editor allows the user to refine the exact copy ("Start MY free trial" first-person tested 202% lift). The CTA's link target also changes per audience: trial users go to /app, free-plan users go to /upgrade, paying customers go to /dashboard.
      Taxonomy notes:
      - Uses canonical events: Users.first_seen_at, user_created, subscription_created (with plan_name and billing_period properties).
      - The CTA target_id remains "primary-cta" across variants for consistent click_on aggregation.
      - The 202% lift figure (cited multiple times in 2026 SaaS research) is for first-person CTA copy ("Start MY free trial") personalized by visitor intent. This recipe enables that pattern.
      - Don't over-segment: 5-6 lifecycle audiences is the sweet spot. Beyond that, content authoring overhead exceeds the gains.
      - Combine with source-based-personalization for compounding effect: a first-time visitor from LinkedIn enterprise ads sees both source-matched hero (Variant B from source-based) AND first-person CTA copy (Variant B from this recipe). Order precedence: source beats lifecycle when both apply.
outputs:
  - key: personalization
    producedByStep: s1
    type: personalization
    description: Website personalization created on /experiences.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# CTA wording by account state

The main button reads differently for a first-time visitor, a returning one, someone mid-trial, a free-plan user and a paying customer, instead of one generic prompt.

## Steps

1. **Set up the five CTA variants** (builds personalization)

   A first visit reads Start your free trial, a return visit without an account reads Continue exploring, a live trial reads Continue your trial, a free plan reads Upgrade to Pro, and a paying customer reads Open dashboard.

## What you end up with

- **personalization** (personalization): Website personalization created on /experiences.

## Availability

Coming soon: waiting on the engine to build personalization.
