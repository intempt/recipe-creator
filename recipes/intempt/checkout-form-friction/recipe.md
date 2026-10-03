---
id: checkout-form-friction
title: Checkout friction
slash_command: /checkout-form-friction
group: Reports
owner: intempt
summary: Shows which checkout step loses you orders, how long shoppers sit on each one, and where mobile
  is worse than desktop.
description: >-
  Checkout-stage drop-off with page-level friction surfacing: reveals form fields, payment methods, and
  steps that cause abandonment.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  complexity: quick
  executionMode: live
  tags:
    - funnel
prerequisites:
  integrations:
    - value: shopify
      severity: blocking
      group: checkout-source
    - value: stripe
      severity: blocking
      group: checkout-source
touches:
  reads:
    - Your Shopify connection
    - Your Stripe connection
  writes:
    - A new report, from step 1 "Find the stalling checkout step"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find the stalling checkout step
    summary: >-
      A five step funnel through checkout start, shipping, payment, review and order, completed inside
      one hour and split by device. Flags the biggest drop, any step where median time on page passes
      90 seconds, and any step where mobile trails desktop by more than 15 points.
    builds: report
    description: |-
      Create a Funnel report called "Checkout Form Friction".
      Steps:
      1. Event "checkout_created": "Started Checkout"
      2. Event "page_viewed" where page_url contains "/checkout/shipping" or equivalent shipping step: "Reached Shipping"
      3. Event "page_viewed" where page_url contains "/checkout/payment" or equivalent payment step: "Reached Payment"
      4. Event "page_viewed" where page_url contains "/checkout/review" or equivalent review step: "Reached Review"
      5. Event "checkout_completed" OR "order_created": "Completed Order"
      Conversion window: 1 hour (in-session checkout completion)
      Breakdown: By "device_type" attribute on the Users object (mobile checkout typically 30% lower conversion than desktop)
      Compare: Previous period (prior 30 days)
      For each step, also surface:
      - Median and 75th-percentile time on the step page (long times suggest friction)
      - Drop-off rate vs. previous period
      - For users who reached but didn't pass each step: what was their last in-checkout action (helps identify the specific field/element that caused exit)
      Annotations:
      - Flag the step with the largest drop-off (the primary checkout bottleneck).
      - Flag any step where median time-on-page exceeds 90 seconds (typically signals form complexity, validation issues, or payment-method confusion).
      - Flag if mobile drop-off at any step is >15 percentage points worse than desktop (mobile-specific UX issue at that step).
      - Highlight the abandoned_checkout volume in the same period: these are recoverable users; pair this report with abandoned-cart recovery.
      Industry benchmarks: average ecommerce checkout completion rate is ~50%; top-quartile is 70%+. Step-level: shipping to payment typically 80%+ of the drop-off.
      Use case: every ecommerce team optimizes the checkout but most see only the top-line drop-off, not the per-step diagnosis. This recipe surfaces exactly where the friction lives.
      Taxonomy notes:
      - checkout_created and checkout_completed are canonical (Stripe-sourced).
      - abandoned_checkout (Shopify) is canonical and complementary.
      - Per-step pages are derived from page_viewed.page_url patterns since separate canonical events for each checkout substep don't exist.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Checkout friction

Shows which checkout step loses you orders, how long shoppers sit on each one, and where mobile is worse than desktop.

## Steps

1. **Find the stalling checkout step** (builds report)

   A five step funnel through checkout start, shipping, payment, review and order, completed inside one hour and split by device. Flags the biggest drop, any step where median time on page passes 90 seconds, and any step where mobile trails desktop by more than 15 points.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Your Shopify connection
- Your Stripe connection

Writes:

- A new report, from step 1 "Find the stalling checkout step"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
