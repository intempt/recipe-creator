---
frontmatter_id: mobile-sticky-add-to-cart-test
slash_command: /mobile-sticky-add-to-cart-test
description: Compares a standard add-to-cart button against two sticky bottom bars on mobile product pages, scored on carts created.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Tests a standard add-to-cart button against two sticky bottom bars on mobile product pages, measuring which variant
    drives the most carts created.
  parameters:
  - name: test_duration
    type: duration
    label: Test duration
    default: 14 d
    required: false
  - name: control_traffic_share
    type: number
    label: Control traffic share (%)
    default: 34
    required: false
  - name: variant_b_traffic_share
    type: number
    label: Variant B traffic share (%)
    default: 33
    required: false
  - name: variant_c_traffic_share
    type: number
    label: Variant C traffic share (%)
    default: 33
    required: false
  - name: page_url_contains
    type: string
    label: Page URL contains
    default: /products/
    required: false
  - name: max_mobile_viewport_width
    type: number
    label: Mobile viewport max width (px, exclusive)
    default: 768
    required: false
  - name: order_window
    type: duration
    label: Post-exposure order window
    default: 24 h
    required: false
  requirements:
  - slot: add_to_cart_click
    kind: event
    meaning: A customer clicked an add-to-cart button on a product page
    properties:
    - name: target_id
      type: text
      meaning: Identifier of the clicked element (sticky or main add-to-cart button)
      optional: false
  - slot: cart_created
    kind: event
    meaning: A customer created a cart
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
  steps:
  - id: s1
    builds: experiment
    uses:
    - add_to_cart_click
    - cart_created
    - order_placed
    - test_duration
    - control_traffic_share
    - variant_b_traffic_share
    - variant_c_traffic_share
    - page_url_contains
    - max_mobile_viewport_width
    - order_window
    instruction: 'Create a client-side experiment named "Mobile Sticky Add-to-Cart" for all visitors on pages whose URL contains
      {page_url_contains}, on mobile only (viewport narrower than {max_mobile_viewport_width} px), shown always. Variants:
      Control ({control_traffic_share}%) keeps the standard add-to-cart button; Variant B ({variant_b_traffic_share}%) adds
      a bar fixed to the bottom of the screen with the product title, price and an add-to-cart button with id sticky-add-to-cart-button;
      Variant C ({variant_c_traffic_share}%) adds the same bar plus a quantity selector from 1 to 99, default 1. Both bars
      are hidden at {max_mobile_viewport_width} px or wider. Primary metric: visitors who did {cart_created} in the same session
      as exposure. Secondary metrics: {add_to_cart_click} with {add_to_cart_click.target_id} equal to sticky-add-to-cart-button,
      and equal to main-add-to-cart-button; {order_placed} within {order_window} of exposure. Guardrail: the share of exposed
      visitors who did {order_placed} must not drop below Control. Run for {test_duration}.'
---

# Mobile sticky add to cart test

Slash command: /mobile-sticky-add-to-cart-test

## Step 1: Set up the sticky cart test

Create a client-side experiment named "Mobile Sticky Add-to-Cart" for all visitors on pages whose URL contains /products/, on mobile only (viewport narrower than 768 px), shown always. Variants: Control (34%) keeps the standard add-to-cart button; Variant B (33%) adds a bar fixed to the bottom of the screen with the product title, price and an add-to-cart button with id sticky-add-to-cart-button; Variant C (33%) adds the same bar plus a quantity selector from 1 to 99, default 1. Both bars are hidden at 768 px or wider. Primary metric: visitors who did cart created in the same session as exposure. Secondary metrics: add to cart click with target id equal to sticky-add-to-cart-button, and equal to main-add-to-cart-button; order placed within 24 h of exposure. Guardrail: the share of exposed visitors who did order placed must not drop below Control. Run for 14 d.
