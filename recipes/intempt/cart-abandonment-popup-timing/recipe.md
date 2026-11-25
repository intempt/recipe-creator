---
frontmatter_id: cart-abandonment-popup-timing
slash_command: /cart-abandonment-popup-timing
description: Compares exit-intent, a 30 second delay and no popup at all on cart pages, scored on orders placed within 24 hours.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Tests exit-intent, a 30-second delay popup, and no popup on desktop cart pages, measuring which drives the most
    orders placed within 24 hours.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Cart Popup Timing
    required: false
  - name: traffic_split_control
    type: number
    label: Exit-intent (control) traffic share (%)
    default: 34
    required: false
  - name: traffic_split_variant_b
    type: number
    label: Delay popup traffic share (%)
    default: 33
    required: false
  - name: traffic_split_variant_c
    type: number
    label: No popup traffic share (%)
    default: 33
    required: false
  - name: idle_delay
    type: duration
    label: Idle delay before the delay popup
    default: 30 s
    required: false
  - name: attribution_window
    type: duration
    label: Order attribution window after exposure
    default: 24 h
    required: false
  - name: schedule_length
    type: duration
    label: Experiment run length
    default: 14 d
    required: false
  - name: bounce_guardrail_increase
    type: number
    label: Maximum allowed bounce rate increase (%)
    default: 10
    required: false
  requirements:
  - slot: cart_created_event
    kind: event
    meaning: A customer added an item to their cart
  - slot: cart_updated_event
    kind: event
    meaning: A customer changed the contents of their cart
    optional: true
  - slot: popup_submit_event
    kind: event
    meaning: A visitor submitted the email form in the cart save popup
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
  steps:
  - id: s1
    builds: experiment
    uses:
    - cart_created_event
    - cart_updated_event
    - popup_submit_event
    - order_placed_event
    - experiment_title
    - traffic_split_control
    - traffic_split_variant_b
    - traffic_split_variant_c
    - idle_delay
    - attribution_window
    - schedule_length
    - bounce_guardrail_increase
    instruction: 'Create a website experiment named "{experiment_title}" on pages whose URL contains "/cart", desktop only,
      for visitors who did {cart_created_event} in the current session, shown once per session, running {schedule_length}.
      Control ({traffic_split_control}%): a popup headed "Wait! Save your cart" with the text "We''ll save your items and
      email you a reminder.", an email field, a "Save my cart" button and a close button, shown when the mouse leaves the
      top of the window. Variant B ({traffic_split_variant_b}%): the same form headed "Still thinking it over?" with the text
      "Save your cart and we''ll send you a reminder: no pressure.", shown after {idle_delay} with no cart interaction ({cart_updated_event},
      click or page view). Variant C ({traffic_split_variant_c}%): no popup. Primary goal: {order_placed_event} within {attribution_window}
      of exposure. Secondary: {popup_submit_event} rate and popup close rate. Guardrail: the bounce rate after a popup shows
      must not rise more than {bounce_guardrail_increase}%.'
---

# Cart popup timing test

Slash command: /cart-abandonment-popup-timing

## Step 1: Set up the popup timing test

Create a website experiment named "Cart Popup Timing" on pages whose URL contains "/cart", desktop only, for visitors who did cart created event in the current session, shown once per session, running 14 d. Control (34%): a popup headed "Wait! Save your cart" with the text "We'll save your items and email you a reminder.", an email field, a "Save my cart" button and a close button, shown when the mouse leaves the top of the window. Variant B (33%): the same form headed "Still thinking it over?" with the text "Save your cart and we'll send you a reminder: no pressure.", shown after 30 s with no cart interaction (cart updated event, click or page view). Variant C (33%): no popup. Primary goal: order placed event within 24 h of exposure. Secondary: popup submit event rate and popup close rate. Guardrail: the bounce rate after a popup shows must not rise more than 10%.
