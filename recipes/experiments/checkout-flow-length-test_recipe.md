---
name: checkout-flow-length-test
description: |
  Use when a user mentions "checkout flow length test", or asks for related help. Test whether single-page or multi-step checkout reduces abandonment. Client experiment.
arguments: []
intempt:
  id: checkout-flow-length-test
  version: 1.0.1
  slashCommand: /experiment-recipe
  group: Experiments
  shortDescription: "Test whether single-page or multi-step checkout reduces abandonment. Client experiment."
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
      title: "Configure Website Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: "Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2)."
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Checkout Flow Length".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (50%): single-page checkout — all fields on one screen
        - Variant B (50%): 3-step checkout — Shipping → Payment → Review

        Targeting:
        - Pages: page URL contains "/checkout"
        - Devices: track desktop and mobile separately (both run the experiment, but split analysis by device)
        - Audience: all visitors who reach checkout
        - Display frequency: always

        Primary metric: goal_completed_in_experience where experience_id = <this> (goal: order_created within 1 hour of checkout_created)
        Secondary metrics:
        - checkout_completed rate (checkout_completed / checkout_created)
        - order_created within 1 hour (final conversion)
        - Time-in-checkout (median time from checkout_created to order_created)
        - Per-step abandonment rate (variant B only — see instrumentation note below)

        Guardrail: card decline rate (payment_failed) must not increase >2%; cart_abandoned within checkout must not increase >5%

        Schedule: 14 days, 3,000 checkouts per variant minimum

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (single-page — no DOM changes if existing checkout is single-page)
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

        ═══ Per-step page_viewed instrumentation (CRITICAL for measurement) ═══

        For per-step abandonment to be measurable, each step transition MUST fire a distinct page_viewed event.

        Two implementation approaches:

        Approach A — Distinct URLs per step (recommended for SSR sites):
          - Step 1: /checkout/shipping → page_viewed automatically fires with page_url = "/checkout/shipping"
          - Step 2: /checkout/payment → page_viewed fires with page_url = "/checkout/payment"
          - Step 3: /checkout/review → page_viewed fires with page_url = "/checkout/review"
          - Measure step-by-step funnel via standard page_viewed funnel: /checkout/shipping → /checkout/payment → /checkout/review → order_created

        Approach B — Synthetic page_viewed for SPA (recommended for single-page-app sites):
          When the user advances to step 2 or step 3 without URL change, fire a synthetic page_viewed event manually:
            intempt.track('page_viewed', {
              page_url: '/checkout/payment',
              page_title: 'Checkout — Payment',
              checkout_step: 'payment',
              checkout_step_number: 2,
              experience_id: '<this experience id>',
              variant_id: 'b'
            });
          Same pattern for step 3 (/checkout/review). This makes per-step abandonment measurable identically to Approach A.

        Without one of these approaches, Variant B's per-step abandonment cannot be measured and the test loses its most informative secondary metric.

        The Visual Editor allows the user to refine step copy, validation messages, and button placement. The synthetic page_viewed firing logic should be added once and shared across all step transitions.

        Taxonomy notes:
        - checkout_created and checkout_completed are canonical (typically Stripe-sourced).
        - page_viewed is canonical and accepts arbitrary properties (page_url, page_title, plus any custom dimensions like checkout_step). Use this for synthetic step-tracking events in SPA implementations.
        - payment_failed is project-defined; if your stack doesn't emit it, derive the guardrail from order_created absence after a checkout_completed (i.e., declined orders that started but didn't finish).
        - Variant B's full DOM patch above includes hidden sections that the page's existing JS reveals on step-continue. The Visual Editor lets the user customize the styling but the show/hide logic typically lives in the application code.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---

# Checkout Flow Length Test

## Procedure

1. **Configure Website Experiment** [`create_experiment`] — Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2). → produces: experiment

   ```text
   Create a CLIENT EXPERIMENT on /experiences titled "Checkout Flow Length".

   ═══ PATH 1: Top-level configuration ═══

   Experience type: client_experiment

   Variants:
   - Control (50%): single-page checkout — all fields on one screen
   - Variant B (50%): 3-step checkout — Shipping → Payment → Review

   Targeting:
   - Pages: page URL contains "/checkout"
   - Devices: track desktop and mobile separately (both run the experiment, but split analysis by device)
   - Audience: all visitors who reach checkout
   - Display frequency: always

   Primary metric: goal_completed_in_experience where experience_id = <this> (goal: order_created within 1 hour of checkout_created)
   Secondary metrics:
   - checkout_completed rate (checkout_completed / checkout_created)
   - order_created within 1 hour (final conversion)
   - Time-in-checkout (median time from checkout_created to order_created)
   - Per-step abandonment rate (variant B only — see instrumentation note below)

   Guardrail: card decline rate (payment_failed) must not increase >2%; cart_abandoned within checkout must not increase >5%

   Schedule: 14 days, 3,000 checkouts per variant minimum

   ═══ PATH 2: Variant HTML content (Visual Editor) ═══

   Variant: Control (single-page — no DOM changes if existing checkout is single-page)
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

   ═══ Per-step page_viewed instrumentation (CRITICAL for measurement) ═══

   For per-step abandonment to be measurable, each step transition MUST fire a distinct page_viewed event.

   Two implementation approaches:

   Approach A — Distinct URLs per step (recommended for SSR sites):
     - Step 1: /checkout/shipping → page_viewed automatically fires with page_url = "/checkout/shipping"
     - Step 2: /checkout/payment → page_viewed fires with page_url = "/checkout/payment"
     - Step 3: /checkout/review → page_viewed fires with page_url = "/checkout/review"
     - Measure step-by-step funnel via standard page_viewed funnel: /checkout/shipping → /checkout/payment → /checkout/review → order_created

   Approach B — Synthetic page_viewed for SPA (recommended for single-page-app sites):
     When the user advances to step 2 or step 3 without URL change, fire a synthetic page_viewed event manually:
       intempt.track('page_viewed', {
         page_url: '/checkout/payment',
         page_title: 'Checkout — Payment',
         checkout_step: 'payment',
         checkout_step_number: 2,
         experience_id: '<this experience id>',
         variant_id: 'b'
       });
     Same pattern for step 3 (/checkout/review). This makes per-step abandonment measurable identically to Approach A.

   Without one of these approaches, Variant B's per-step abandonment cannot be measured and the test loses its most informative secondary metric.

   The Visual Editor allows the user to refine step copy, validation messages, and button placement. The synthetic page_viewed firing logic should be added once and shared across all step transitions.

   Taxonomy notes:
   - checkout_created and checkout_completed are canonical (typically Stripe-sourced).
   - page_viewed is canonical and accepts arbitrary properties (page_url, page_title, plus any custom dimensions like checkout_step). Use this for synthetic step-tracking events in SPA implementations.
   - payment_failed is project-defined; if your stack doesn't emit it, derive the guardrail from order_created absence after a checkout_completed (i.e., declined orders that started but didn't finish).
   - Variant B's full DOM patch above includes hidden sections that the page's existing JS reveals on step-continue. The Visual Editor lets the user customize the styling but the show/hide logic typically lives in the application code.
   ```
