---
name: checkout-flow-length-test
description: |
  Use when a user mentions "checkout flow length test", or asks for related help. Test whether single-page or multi-step checkout reduces abandonment. Client experiment.
arguments: []
intempt:
  id: checkout-flow-length-test
  version: 1.0.1
  slashCommand: /checkout-flow-length-test
  group: Experiments
  title: 'Checkout flow length test'
  shortDescription: 'Compares a one-page checkout against a three-step checkout, scored on orders completed within an hour of starting.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [ecommerce]
    complexity: standard
    executionMode: live
    tags: [experiment, client]
    experimentType: a-b
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: stripe, severity: blocking }
  invokesCommands:
    - create_experiment
  procedure:
    - step: 1
      title: 'Set up the checkout length test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Splits checkout visitors 50/50 between all fields on one screen and a three-step flow of shipping, payment and review. The winner is the variant with more orders within an hour of checkout starting. Desktop and mobile are analysed separately.'
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Checkout Flow Length".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (50%): single-page checkout: all fields on one screen
        - Variant B (50%): 3-step checkout: Shipping to Payment to Review

        Targeting:
        - Pages: page URL contains "/checkout"
        - Devices: track desktop and mobile separately (both run the experiment, but split analysis by device)
        - Audience: all visitors who reach checkout
        - Display frequency: always

        Primary metric: Completed an experience goal for this experience (goal: Placed order within 1 hour of Checkout created)
        Secondary metrics:
        - Checkout completed rate (Checkout completed divided by Checkout created)
        - Placed order within 1 hour (final conversion)
        - Time-in-checkout (median time from Checkout created to Placed order)
        - Per-step abandonment rate (variant B only: see instrumentation note below)

        Guardrail: card decline rate (Payment failed) must not increase >2%; Abandoned cart within checkout must not increase >5%

        Schedule: 14 days, 3,000 checkouts per variant minimum

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (single-page: no DOM changes if existing checkout is single-page)
          Existing checkout layout remains.

        Variant: B (3-step checkout)
          HTML target selector: .checkout-container (replace structure)
          Replacement HTML:
          <div class="checkout-multistep" data-variant="b" data-current-step="1">
            <header class="step-progress">
              <div class="step active" data-step="1">1. Shipping</div>
              <div class="step" data-step="2">2. Payment</div>
              <div class="step" data-step="3">3. Review</div>
            </header>

            <section class="step-shipping" data-step-content="1">
              <h2>Shipping address</h2>
              <form><!-- shipping fields: name, address, city, zip, country --></form>
              <button class="step-continue" id="checkout-step-1-continue">Continue to Payment</button>
            </section>

            <section class="step-payment" data-step-content="2" hidden>
              <h2>Payment</h2>
              <form><!-- card fields, billing toggle --></form>
              <button class="step-back" id="checkout-step-2-back">Back</button>
              <button class="step-continue" id="checkout-step-2-continue">Continue to Review</button>
            </section>

            <section class="step-review" data-step-content="3" hidden>
              <h2>Review your order</h2>
              <div class="order-summary"><!-- items, shipping, taxes, total --></div>
              <button class="step-back" id="checkout-step-3-back">Back</button>
              <button class="checkout-submit" id="checkout-submit">Place Order</button>
            </section>
          </div>

        ═══ Per-step View page instrumentation (CRITICAL for measurement) ═══

        For per-step abandonment to be measurable, each step transition MUST fire a distinct View page event.

        Two implementation approaches:

        Approach A: Distinct URLs per step (recommended for SSR sites):
          - Step 1: /checkout/shipping to a View page event automatically fires with Page URL = "/checkout/shipping"
          - Step 2: /checkout/payment to a View page event fires with Page URL = "/checkout/payment"
          - Step 3: /checkout/review to a View page event fires with Page URL = "/checkout/review"
          - Measure the step-by-step funnel via a standard View page funnel: /checkout/shipping to /checkout/payment to /checkout/review to Placed order

        Approach B: Synthetic View page for SPA (recommended for single-page-app sites):
          When the user advances to step 2 or step 3 without URL change, fire a synthetic View page event manually:
            intempt.track('View page', {
              Page URL: '/checkout/payment',
              page_title: 'Checkout: Payment',
              checkout_step: 'payment',
              checkout_step_number: 2,
              experience_id: '<this experience id>',
              variant_id: 'b'
            });
          Same pattern for step 3 (/checkout/review). This makes per-step abandonment measurable identically to Approach A.

        Without one of these approaches, Variant B's per-step abandonment cannot be measured and the test loses its most informative secondary metric.

        The Visual Editor allows the user to refine step copy, validation messages, and button placement. The synthetic View page firing logic should be added once and shared across all step transitions.

        Notes:
        - A View page event accepts arbitrary properties (Page URL, page title, plus custom dimensions like checkout step), which is what makes the synthetic step-tracking events in single-page-app implementations work.
        - If your stack doesn't emit a Payment failed event, derive the decline guardrail from the absence of a Placed order after a Checkout completed (orders that started but didn't finish).
        - Variant B's full DOM patch above includes hidden sections that the page's existing JS reveals on step-continue. The Visual Editor lets the user customize the styling, but the show/hide logic typically lives in the application code.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Checkout flow length test

Compares a one-page checkout against a three-step checkout, scored on orders completed within an hour of starting.

## Before you run it

- Connect stripe

## What it does

1. **Set up the checkout length test** (`create_experiment`)

   Splits checkout visitors 50/50 between all fields on one screen and a three-step flow of shipping, payment and review. The winner is the variant with more orders within an hour of checkout starting. Desktop and mobile are analysed separately.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
