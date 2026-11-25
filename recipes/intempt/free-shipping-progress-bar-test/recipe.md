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
    - bar_target_selector
    instruction: 'Create a client experiment titled "{experiment_title}" on the experiences page. Variants: Control at {control_split}%
      with no progress bar; Variant B at {variant_split}% showing a free-shipping progress bar inserted at {bar_target_selector},
      with the copy "You are" followed by the amount still needed "away from free shipping" and a meter that fills as the
      cart subtotal ({cart_updated_event.cart_subtotal}) approaches {free_shipping_threshold}. Targeting: pages whose URL
      contains "/cart" and the mini-cart drawer on any page; devices any; audience: visitors who did {cart_created_event}
      in the current session; display frequency always. Primary metric: revenue from {placed_order_event} within {attribution_window}
      of exposure ({experiment_exposure_event}). Secondary metrics: average {placed_order_event.total_price} per variant;
      {cart_updated_event} count per session; cart-to-order conversion within the session ({cart_created_event} to {placed_order_event});
      share of orders at or above {free_shipping_threshold}. Guardrail: cart abandonment must not rise by more than {abandonment_guardrail}%.
      Run for {test_duration}.'
---

# Free shipping progress bar test

Slash command: /free-shipping-progress-bar-test

## Step 1: Set up the progress bar test

Create a client experiment titled "Free Shipping Progress Bar" on the experiences page. Variants: Control at 50% with no progress bar; Variant B at 50% showing a free-shipping progress bar inserted at .cart-summary, with the copy "You are" followed by the amount still needed "away from free shipping" and a meter that fills as the cart subtotal (cart subtotal) approaches the free shipping threshold (USD). Targeting: pages whose URL contains "/cart" and the mini-cart drawer on any page; devices any; audience: visitors who did cart created event in the current session; display frequency always. Primary metric: revenue from placed order event within 24 h of exposure (experiment exposure event). Secondary metrics: average total price per variant; cart updated event count per session; cart-to-order conversion within the session (cart created event to placed order event); share of orders at or above the free shipping threshold (USD). Guardrail: cart abandonment must not rise by more than 3%. Run for 14 d.
