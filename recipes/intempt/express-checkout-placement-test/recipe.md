---
frontmatter_id: express-checkout-placement-test
slash_command: /express-checkout-placement-test
description: Tests different express checkout button placements on the product page and cart drawer against the standard checkout
  flow.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Tests where express checkout buttons (Apple Pay, Google Pay) go, on the product page, in the cart drawer or both,
    against standard checkout to see which lifts revenue.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Express Checkout Placement
    required: false
  - name: duration_days
    type: duration
    label: Test duration
    default: 14 d
    required: false
  - name: min_mobile_sessions_per_variant
    type: number
    label: Minimum mobile sessions per variant
    default: 3000
    required: false
  - name: control_traffic_percent
    type: number
    label: Traffic share per variant (%)
    default: 25
    required: false
  requirements:
  - slot: cart_created_event
    kind: event
    meaning: A visitor created a cart or opened the cart drawer
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: payment_method
      type: string
      meaning: How the order was paid
      optional: false
    - name: order_value
      type: number
      meaning: Order total
      optional: false
  - slot: express_button_click_event
    kind: event
    meaning: A visitor clicked an express checkout button
    properties:
    - name: target_id
      type: string
      meaning: Which button was clicked
      optional: false
  - slot: device_type_attribute
    kind: attribute
    meaning: The visitor's device type (mobile or desktop)
  steps:
  - id: s1
    builds: experiment
    uses:
    - cart_created_event
    - order_placed_event
    - express_button_click_event
    - device_type_attribute
    - experiment_title
    - duration_days
    - min_mobile_sessions_per_variant
    - control_traffic_percent
    instruction: 'Create a website experiment named "{experiment_title}" on the storefront, all visitors, all devices, shown
      always, with four variants at {control_traffic_percent}% traffic each. Control: express checkout buttons only on the
      cart and checkout pages, unchanged. Variant B: express checkout buttons above Add to Cart on pages whose URL contains
      /products/. Variant C: express checkout buttons in the cart drawer when it opens after {cart_created_event}. Variant
      D: buttons on the product page, in the cart drawer and at checkout. Primary goal: revenue, the sum of {order_placed_event.order_value}
      in the session of exposure. Secondary: {express_button_click_event} by {express_button_click_event.target_id}; the share
      of orders by {order_placed_event.payment_method} per variant; conversion split by {device_type_attribute}; average order
      value. Guardrail: the standard checkout completion rate must not drop. Run {duration_days} and until each variant has
      {min_mobile_sessions_per_variant} mobile sessions; do not run alongside a checkout length test.'
---

# Express checkout placement test

Slash command: /express-checkout-placement-test

## Step 1: Set up the placement test

Create a website experiment named "Express Checkout Placement" on the storefront, all visitors, all devices, shown always, with four variants at 25% traffic each. Control: express checkout buttons only on the cart and checkout pages, unchanged. Variant B: express checkout buttons above Add to Cart on pages whose URL contains /products/. Variant C: express checkout buttons in the cart drawer when it opens after cart created event. Variant D: buttons on the product page, in the cart drawer and at checkout. Primary goal: revenue, the sum of order value in the session of exposure. Secondary: express button click event by target id; the share of orders by payment method per variant; conversion split by device type attribute; average order value. Guardrail: the standard checkout completion rate must not drop. Run 14 d and until each variant has 3000 mobile sessions; do not run alongside a checkout length test.
