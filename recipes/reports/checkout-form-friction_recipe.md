---
name: checkout-form-friction
description: |
  Use when a user mentions "checkout form friction", or asks for related help. Checkout-stage drop-off with page-level friction surfacing: reveals form fields, payment methods, and steps that cause abandonment.
arguments: []
intempt:
  id: checkout-form-friction
  version: 1.0.0
  slashCommand: /checkout-form-friction
  group: Reports
  title: "Checkout friction"
  shortDescription: "Shows which checkout step loses you orders, how long shoppers sit on each one, and where mobile is worse than desktop."
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
  prerequisites:
    integrations:
      - { value: shopify, severity: blocking, group: checkout-source }
      - { value: stripe, severity: blocking, group: checkout-source }
  invokesCommands:
    - build_funnel_report
  procedure:
    - step: 1
      title: "Find the stalling checkout step"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "A five step funnel through checkout start, shipping, payment, review and order, completed inside one hour and split by device. Flags the biggest drop, any step where median time on page passes 90 seconds, and any step where mobile trails desktop by more than 15 points."
      prompt: |
        Create a Funnel report called "Checkout Form Friction".

        Steps:
        1. Event "Checkout created": "Started Checkout"
        2. Event "View page" where the page URL contains "/checkout/shipping" or equivalent shipping step: "Reached Shipping"
        3. Event "View page" where the page URL contains "/checkout/payment" or equivalent payment step: "Reached Payment"
        4. Event "View page" where the page URL contains "/checkout/review" or equivalent review step: "Reached Review"
        5. Event "Checkout completed" OR "Placed order": "Completed Order"

        Conversion window: 1 hour (in-session checkout completion)
        Breakdown: By device type (mobile checkout typically 30% lower conversion than desktop)
        Compare: Previous period (prior 30 days)

        For each step, also surface:
        - Median and 75th-percentile time on the step page (long times suggest friction)
        - Drop-off rate vs. previous period
        - For users who reached but didn't pass each step: what was their last in-checkout action (helps identify the specific field/element that caused exit)

        Annotations:
        - Flag the step with the largest drop-off (the primary checkout bottleneck).
        - Flag any step where median time-on-page exceeds 90 seconds (typically signals form complexity, validation issues, or payment-method confusion).
        - Flag if mobile drop-off at any step is >15 percentage points worse than desktop (mobile-specific UX issue at that step).
        - Highlight the Abandoned checkout volume in the same period: these are recoverable users; pair this report with abandoned-cart recovery.

        Industry benchmarks: average ecommerce checkout completion rate is ~50%; top-quartile is 70%+. Step-level: shipping to payment typically 80%+ of the drop-off.

        Use case: every ecommerce team optimizes the checkout but most see only the top-line drop-off, not the per-step diagnosis. This recipe surfaces exactly where the friction lives.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Checkout friction

Shows which checkout step loses you orders, how long shoppers sit on each one, and where mobile is worse than desktop.

## Before you run it

- Connect shopify
- Connect stripe

## What it does

1. **Find the stalling checkout step** (`build_funnel_report`)

   A five step funnel through checkout start, shipping, payment, review and order, completed inside one hour and split by device. Flags the biggest drop, any step where median time on page passes 90 seconds, and any step where mobile trails desktop by more than 15 points.

## What you end up with

- **report** (report): Report produced by this recipe.
