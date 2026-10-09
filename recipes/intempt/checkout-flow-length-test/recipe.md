---
description: Compares a one-page checkout against a three-step checkout, scored on orders completed within an hour of starting.
author:
  first_name: V
  last_name: Ranadheer
  job_title: Design Engineer
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
---

# Checkout flow length test

Slash command: /checkout-flow-length-test

## Step 1: Set up the checkout length test

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
Primary metric: goal_completed_in_experience where experience_id = <this> (goal: Placed order within 1 hour of Checkout created)
Secondary metrics:
- Checkout completed rate (Checkout completed / Checkout created)
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
 - Step 1: /checkout/shipping to View page automatically fires with Page URL = "/checkout/shipping"
 - Step 2: /checkout/payment to View page fires with Page URL = "/checkout/payment"
 - Step 3: /checkout/review to View page fires with Page URL = "/checkout/review"
 - Measure step-by-step funnel via standard View page funnel: /checkout/shipping to /checkout/payment to /checkout/review to Placed order
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
Taxonomy notes:
- Checkout created and Checkout completed are canonical (typically Stripe-sourced).
- View page is canonical and accepts arbitrary properties (Page URL, page_title, plus any custom dimensions like checkout_step). Use this for synthetic step-tracking events in SPA implementations.
- Payment failed is project-defined; if your stack doesn't emit it, derive the guardrail from Placed order absence after a Checkout completed (i.e., declined orders that started but didn't finish).
- Variant B's full DOM patch above includes hidden sections that the page's existing JS reveals on step-continue. The Visual Editor lets the user customize the styling but the show/hide logic typically lives in the application code.
