---
name: post-purchase-upsell-on-page-placement
description: |
  Use when a user mentions "post-purchase upsell: on-page placement", or asks for related help. Test where to show the post-purchase upsell on the order confirmation page (above order details, below order details, or as inline modal). Website-only: email and push variants are out of scope.
arguments: []
intempt:
  id: post-purchase-upsell-on-page-placement
  version: 1.0.0
  slashCommand: /post-purchase-upsell-on-page-placement
  group: Experiments
  title: 'Post-purchase upsell placement test'
  shortDescription: 'Compares three places to put the upsell on the order confirmation page, scored on extra revenue within 24 hours.'
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
  invokesCommands:
    - create_experiment
  procedure:
    - step: 1
      title: 'Set up the upsell placement test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Splits order confirmation traffic three ways: an upsell carousel above the order details, a strip below them, or a modal 5 seconds after the page loads. The winner produces the most additional orders within 24 hours. On-page only, not email or push.'
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Post-Purchase Upsell: On-Page Placement".

        NOTE: This recipe was previously authored with email and push notification variants. The current product scope is website-only personalizations and experiments: email and push are outside the product. The recipe now focuses exclusively on the on-page placement dimension.

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (34%): upsell carousel above order details on the confirmation page
        - Variant B (33%): upsell strip below order details on the confirmation page
        - Variant C (33%): inline modal that appears 5 seconds after order confirmation page loads

        Targeting:
        - Pages: page URL contains "/order-confirmation" OR "/thank-you"
        - Devices: any
        - Audience: customers who just triggered a Placed order event
        - Display frequency: once (per order)

        Primary metric: Completed an experience goal for this experience (goal fires on an additional Placed order within 24 hours of upsell exposure: incremental revenue). To tell upsell-attributed orders apart from the original purchase, join a Click on where the target ID starts with "upsell-" to a subsequent Placed order within the attribution window.
        Secondary metrics:
        - Click on where the target ID starts with "upsell-product-" (upsell engagement rate)
        - Add-to-second-order rate (Cart created within 1 hour for any user shown the upsell)
        - Average upsell value when accepted

        Guardrail: customer satisfaction (Feedback submitted score within 7 days of order) must not drop; modal-dismiss rate (variant C) must not exceed 80% (high dismissal = annoyance signal)

        Schedule: 30 days

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (above order details)
          HTML target selector: .order-confirmation (insert before)
          Variant DOM:
          <section class="post-purchase-upsell" data-variant="control" data-placement="above-order">
            <h2>Customers like you also bought</h2>
            <div class="upsell-carousel">
              <article class="upsell-product"><img /><h3>[Product]</h3><span>[$X.XX]</span><button id="upsell-product-1">Add to Order</button></article>
              <article class="upsell-product"><img /><h3>[Product]</h3><span>[$X.XX]</span><button id="upsell-product-2">Add to Order</button></article>
              <article class="upsell-product"><img /><h3>[Product]</h3><span>[$X.XX]</span><button id="upsell-product-3">Add to Order</button></article>
            </div>
          </section>

        Variant: B (below order details)
          HTML target selector: .order-confirmation (append after)
          Same upsell carousel HTML as Control.

        Variant: C (inline modal, 5s delay)
          HTML target selector: body (append modal)
          Variant DOM:
          <div class="upsell-modal-overlay" data-variant="c" data-trigger="5s-delay" hidden>
            <div class="upsell-modal">
              <button class="modal-close" id="upsell-modal-dismiss" aria-label="Close">×</button>
              <h2>One more thing: customers also love these</h2>
              <div class="upsell-carousel">
                <!-- 3 upsell products with id="upsell-product-1/2/3" -->
              </div>
            </div>
          </div>

          Trigger JS: setTimeout 5000ms after View page on /order-confirmation, set overlay hidden=false. Pair with a CSS modal animation.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Post-purchase upsell placement test

Compares three places to put the upsell on the order confirmation page, scored on extra revenue within 24 hours.

## What it does

1. **Set up the upsell placement test** (`create_experiment`)

   Splits order confirmation traffic three ways: an upsell carousel above the order details, a strip below them, or a modal 5 seconds after the page loads. The winner produces the most additional orders within 24 hours. On-page only, not email or push.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
