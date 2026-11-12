---
frontmatter_id: free-shipping-progress-bar-test
slash_command: /free-shipping-progress-bar-test
description: Compares a cart bar counting down to free shipping against no bar at all, scored on revenue and average order value.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows shoppers a cart progress bar counting down to free shipping, then tests it against no bar to see effects
    on revenue and average order value.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Free Shipping Progress Bar
    required: false
  - name: control_split
    type: number
    label: Control traffic share (%)
    default: 50
    required: false
  - name: variant_split
    type: number
    label: Variant B traffic share (%)
    default: 50
    required: false
  - name: free_shipping_threshold
    type: number
    label: Free shipping threshold (USD)
    required: true
  - name: test_duration
    type: duration
    label: Experiment duration
    default: 14 d
    required: false
  - name: attribution_window
    type: duration
    label: Revenue attribution window after exposure
    default: 24 h
    required: false
  - name: abandonment_guardrail
    type: number
    label: Maximum allowed increase in cart abandonment (%)
    default: 3
    required: false
  - name: bar_target_selector
    type: string
    label: HTML insertion selector for progress bar
    default: .cart-summary
    required: false
  requirements:
  - slot: cart_created_event
    kind: event
    meaning: A customer created a cart
    properties:
    - name: session_id
      type: string
      meaning: Session identifier of the visit
      optional: false
  - slot: cart_updated_event
    kind: event
    meaning: A customer updated the contents of their cart
    properties:
    - name: cart_subtotal
      type: number
      meaning: Cart subtotal in USD after the update
      optional: false
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total price in USD
      optional: false
  - slot: experiment_exposure_event
    kind: event
    meaning: A visitor was exposed to an experiment variant
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experiment
      optional: false
  - slot: cart_visitor_audience
    kind: segment
    meaning: Visitors with a cart created in the current session and a cart subtotal above zero but below the free shipping
      threshold
    creatable: true
    definition: users who did {cart_created_event} in the current session AND whose cart subtotal is greater than 0 AND less
      than {free_shipping_threshold}
  - slot: storefront_site
    kind: destination
    meaning: The storefront website where the cart page and mini-cart drawer are shown
    channel: shopify
  steps:
  - id: s1
    builds: experiment
    uses:
    - experiment_title
    - control_split
    - variant_split
    - test_duration
    - attribution_window
    - abandonment_guardrail
    - free_shipping_threshold
    - cart_created_event
    - cart_updated_event
    - placed_order_event
    - experiment_exposure_event
    - cart_visitor_audience
    - storefront_site
    - bar_target_selector
    instruction: 'Create a client experiment titled "{experiment_title}" on the experiences page. Variants: Control at {control_split}%
      with no progress bar (existing cart page); Variant B at {variant_split}% showing a free-shipping progress bar with dynamic
      "$X away from free shipping" copy and a progress meter. Targeting: page URL contains "/cart" OR mini-cart drawer open
      on any page; devices any; audience {cart_visitor_audience}; display frequency always. Primary metric: revenue from {placed_order_event}
      within {attribution_window} of exposure from {experiment_exposure_event}. Secondary metrics: average {placed_order_event.total_price}
      per variant; cart_updated count per session from {cart_updated_event}; cart-to-order conversion within session (from
      {cart_created_event} to {placed_order_event}); percentage of orders reaching {free_shipping_threshold}. Guardrail: cart
      abandonment rate must not increase more than {abandonment_guardrail}%. Schedule: {test_duration}.'
---

# Free shipping progress bar test

Slash command: /free-shipping-progress-bar-test

## Step 1: Set up the progress bar test

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
Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from Placed order within 24 hours of exposure)
Secondary metrics:
- AOV per variant (average Placed order.total_price (the key signal) does the progress bar lift AOV?)
- cart_updated count per session (does the bar drive add-more behavior?)
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
 - Subscribe to cart_updated events
 - Read cart subtotal and configured free_shipping_threshold
 - Update .amount-remaining and .progress-bar-fill width in real time
 - When subtotal >= threshold, swap to "🎉 You unlocked free shipping!" celebration state
When the cart subtotal crosses the threshold, fire a custom DOM event so analytics can capture the threshold-hit moment.
Taxonomy notes:
- This recipe assumes the merchant has a configured free shipping threshold. If you also run free-shipping-threshold-test (server experiment testing the dollar value), schedule them sequentially: don't run them concurrently to avoid interaction effects.
- "Cart subtotal" is read from cart state (Cart created, cart_updated events with Order total property).
- The progress bar's biggest signal is AOV lift; expect 8-15% AOV uplift for stores below the typical free-shipping threshold.
