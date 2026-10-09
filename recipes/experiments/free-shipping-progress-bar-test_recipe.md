---
name: free-shipping-progress-bar-test
description: |
  Use when a user mentions "free shipping progress bar test", or asks for related help. Test cart-page free-shipping progress bar (e.g., "$12 away from free shipping") vs. no progress bar. Top-cited AOV-lifting test in 2026 CRO content.
arguments: []
intempt:
  id: free-shipping-progress-bar-test
  version: 1.0.0
  slashCommand: /free-shipping-progress-bar-test
  group: Experiments
  title: 'Free shipping progress bar test'
  shortDescription: 'Compares a cart bar counting down to free shipping against no bar at all, scored on revenue and average order value.'
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
      title: 'Set up the progress bar test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Splits cart visitors 50/50 between the current cart and a cart showing a progress meter with dynamic copy such as 12 dollars away from free shipping. Only visitors under the threshold are included. The winner is the variant with more revenue within 24 hours.'
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Free Shipping Progress Bar".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (50%): no progress bar (existing cart page)
        - Variant B (50%): cart shows free-shipping progress bar with dynamic "$X away from free shipping" copy and progress meter

        Targeting:
        - Pages: page URL contains "/cart" OR mini-cart drawer is open on any page
        - Devices: any
        - Audience: visitors with at least one Cart created event in the current session AND cart subtotal > $0 AND cart subtotal < free_shipping_threshold
        - Display frequency: always

        Primary metric: Completed an experience goal for this experience AND value > 0 (revenue from Placed order within 24 hours of exposure)
        Secondary metrics:
        - AOV per variant (average order total (the key signal) does the progress bar lift AOV?)
        - Cart updated count per session (does the bar drive add-more behavior?)
        - Cart-to-order conversion rate (Cart created to Placed order within session)
        - Percentage of orders that hit the free-shipping threshold

        Guardrail: cart-abandonment rate must not increase >3% (some shoppers may walk away when they see they don't qualify)

        Schedule: 14 days

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (no DOM changes)

        Variant: B (progress bar)
          HTML target selector: .cart-summary (insert at the top, above the items list)
          Variant DOM:
          <div class="free-shipping-progress" data-variant="b">
            <div class="progress-message">
              <strong class="amount-remaining">$12</strong>
              <span class="message-text">away from <strong>free shipping</strong></span>
            </div>
            <div class="progress-bar-container" role="progressbar" aria-label="Free shipping progress">
              <div class="progress-bar-fill" style="width: 76%;"></div>
            </div>
            <div class="progress-cta">
              <a href="/shop" class="continue-shopping-link">Add more items</a>
            </div>
          </div>

          Lightweight JS that the user refines in the Visual Editor:
          - Subscribe to Cart updated events
          - Read cart subtotal and configured free_shipping_threshold
          - Update .amount-remaining and .progress-bar-fill width in real time
          - When subtotal >= threshold, swap to "🎉 You unlocked free shipping!" celebration state

        When the cart subtotal crosses the threshold, fire a custom DOM event so analytics can capture the threshold-hit moment.

        If you also run free-shipping-threshold-test, which is the server experiment testing the dollar value, schedule them sequentially rather than concurrently to avoid interaction effects. The progress bar's biggest signal is AOV lift: expect 8-15% AOV uplift for stores below the typical free-shipping threshold.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Free shipping progress bar test

Compares a cart bar counting down to free shipping against no bar at all, scored on revenue and average order value.

## What it does

1. **Set up the progress bar test** (`create_experiment`)

   Splits cart visitors 50/50 between the current cart and a cart showing a progress meter with dynamic copy such as 12 dollars away from free shipping. Only visitors under the threshold are included. The winner is the variant with more revenue within 24 hours.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
