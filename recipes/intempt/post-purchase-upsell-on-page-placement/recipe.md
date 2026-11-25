---
frontmatter_id: post-purchase-upsell-on-page-placement
slash_command: /post-purchase-upsell-on-page-placement
description: Tests three on-page places for a post-purchase upsell on the order confirmation page, scored by extra orders
  placed within 24 hours.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Tests three on-page places for a post-purchase upsell on the order confirmation page, scored by extra revenue from
    additional orders within 24 hours.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: 'Post-Purchase Upsell: On-Page Placement'
    required: false
  - name: traffic_split_control
    type: number
    label: Control traffic share (%)
    default: 34
    required: false
  - name: traffic_split_variant_b
    type: number
    label: Variant B traffic share (%)
    default: 33
    required: false
  - name: traffic_split_variant_c
    type: number
    label: Variant C traffic share (%)
    default: 33
    required: false
  - name: modal_delay
    type: duration
    label: Delay before the Variant C modal opens
    default: 5 s
    required: false
  - name: revenue_window
    type: duration
    label: Window for an extra order after exposure
    default: 24 h
    required: false
  - name: satisfaction_window
    type: duration
    label: Feedback window after the order
    default: 7 d
    required: false
  - name: modal_dismiss_threshold
    type: number
    label: Max Variant C dismiss rate (%)
    default: 80
    required: false
  - name: test_duration
    type: duration
    label: Test duration
    default: 30 d
    required: false
  requirements:
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total
      optional: false
  - slot: upsell_click
    kind: event
    meaning: A customer clicked an upsell product button on the website
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked upsell button
      optional: false
  - slot: feedback_submitted
    kind: event
    meaning: A customer submitted feedback with a satisfaction score
    optional: true
    properties:
    - name: score
      type: number
      meaning: Satisfaction score
      optional: false
  - slot: upsell_dismissed
    kind: event
    meaning: A customer closed the upsell modal on the website
    optional: true
  steps:
  - id: s1
    builds: experiment
    uses:
    - order_placed
    - upsell_click
    - feedback_submitted
    - upsell_dismissed
    - experiment_title
    - traffic_split_control
    - traffic_split_variant_b
    - traffic_split_variant_c
    - modal_delay
    - revenue_window
    - satisfaction_window
    - modal_dismiss_threshold
    - test_duration
    instruction: 'Create a client-side experiment named "{experiment_title}" for customers on pages whose URL contains /order-confirmation
      or /thank-you, all devices, shown once per order, running {test_duration}. Each variant shows the heading "Customers
      like you also bought" and three product cards with an "Add to order" button (ids upsell-product-1 to upsell-product-3).
      Control ({traffic_split_control}%): the cards as a carousel above the order details. Variant B ({traffic_split_variant_b}%):
      the same carousel below the order details. Variant C ({traffic_split_variant_c}%): the cards in a modal with a close
      button (id upsell-modal-dismiss) that opens {modal_delay} after the page loads. Primary metric: sum of {order_placed.total_price}
      of a further {order_placed} within {revenue_window} of exposure. Secondary metrics: {upsell_click} where {upsell_click.target_id}
      starts with upsell-product. Guardrails: average {feedback_submitted.score} within {satisfaction_window} of the order
      must not drop below Control; Variant C''s {upsell_dismissed} rate must stay under {modal_dismiss_threshold}%.'
---

# Post-purchase upsell placement test

Slash command: /post-purchase-upsell-on-page-placement

## Step 1: Set up the upsell placement test

Create a client-side experiment named "Post-Purchase Upsell: On-Page Placement" for customers on pages whose URL contains /order-confirmation or /thank-you, all devices, shown once per order, running 30 d. Each variant shows the heading "Customers like you also bought" and three product cards with an "Add to order" button (ids upsell-product-1 to upsell-product-3). Control (34%): the cards as a carousel above the order details. Variant B (33%): the same carousel below the order details. Variant C (33%): the cards in a modal with a close button (id upsell-modal-dismiss) that opens 5 s after the page loads. Primary metric: sum of total price of a further order placed within 24 h of exposure. Secondary metrics: upsell click where target id starts with upsell-product. Guardrails: average score within 7 d of the order must not drop below Control; Variant C's upsell dismissed rate must stay under 80%.
