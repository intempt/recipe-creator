---
name: checkout-form-friction
description: |
  Use when a user mentions "checkout form friction", or asks for related help. Checkout-stage drop-off with page-level friction surfacing — reveals form fields, payment methods, and steps that cause abandonment.
arguments: []
intempt:
  id: checkout-form-friction
  version: 1.0.0
  slashCommand: /checkout-form-friction
  group: Reports
  shortDescription: "Checkout-stage drop-off with page-level friction surfacing — reveals form fields, payment methods, and steps that cause abandonment."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
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
        Create a Funnel report called "Checkout Form Friction".

        Steps:
        1. Event "checkout_created" — "Started Checkout"
        2. Event "page_viewed" where page_url contains "/checkout/shipping" or equivalent shipping step — "Reached Shipping"
        3. Event "page_viewed" where page_url contains "/checkout/payment" or equivalent payment step — "Reached Payment"
        4. Event "page_viewed" where page_url contains "/checkout/review" or equivalent review step — "Reached Review"
        5. Event "checkout_completed" OR "order_created" — "Completed Order"

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
        - Highlight the abandoned_checkout volume in the same period — these are recoverable users; pair this report with abandoned-cart recovery.

        Industry benchmarks: average ecommerce checkout completion rate is ~50%; top-quartile is 70%+. Step-level: shipping → payment typically 80%+ of the drop-off.

        Use case: every ecommerce team optimizes the checkout but most see only the top-line drop-off, not the per-step diagnosis. This recipe surfaces exactly where the friction lives.

        Taxonomy notes:
        - checkout_created and checkout_completed are canonical (Stripe-sourced).
        - abandoned_checkout (Shopify) is canonical and complementary.
        - Per-step pages are derived from page_viewed.page_url patterns since separate canonical events for each checkout substep don't exist.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Checkout Form Friction

## Procedure

1. **Build Funnel Report** [`build_funnel_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Funnel report called "Checkout Form Friction".

   Steps:
   1. Event "checkout_created" — "Started Checkout"
   2. Event "page_viewed" where page_url contains "/checkout/shipping" or equivalent shipping step — "Reached Shipping"
   3. Event "page_viewed" where page_url contains "/checkout/payment" or equivalent payment step — "Reached Payment"
   4. Event "page_viewed" where page_url contains "/checkout/review" or equivalent review step — "Reached Review"
   5. Event "checkout_completed" OR "order_created" — "Completed Order"

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
   - Highlight the abandoned_checkout volume in the same period — these are recoverable users; pair this report with abandoned-cart recovery.

   Industry benchmarks: average ecommerce checkout completion rate is ~50%; top-quartile is 70%+. Step-level: shipping → payment typically 80%+ of the drop-off.

   Use case: every ecommerce team optimizes the checkout but most see only the top-line drop-off, not the per-step diagnosis. This recipe surfaces exactly where the friction lives.

   Taxonomy notes:
   - checkout_created and checkout_completed are canonical (Stripe-sourced).
   - abandoned_checkout (Shopify) is canonical and complementary.
   - Per-step pages are derived from page_viewed.page_url patterns since separate canonical events for each checkout substep don't exist.
   ```
