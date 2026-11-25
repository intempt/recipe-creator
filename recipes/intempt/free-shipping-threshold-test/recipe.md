---
frontmatter_id: free-shipping-threshold-test
slash_command: /free-shipping-threshold-test
description: Finds which free shipping threshold (50, 75, 99 dollars, or none) earns the most revenue per session, served as a server-side flag.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Tests which free shipping threshold ($50, $75, $99, or none) earns the most revenue per session, served as a server-side
    flag with sticky assignment.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Free Shipping Threshold
    required: false
  - name: flag_key
    type: string
    label: Feature flag key
    default: free_shipping_threshold
    required: false
  - name: control_threshold
    type: number
    label: Control free shipping threshold (dollars)
    default: 75
    required: false
  - name: variant_b_threshold
    type: number
    label: Variant B free shipping threshold (dollars)
    default: 50
    required: false
  - name: variant_c_threshold
    type: number
    label: Variant C free shipping threshold (dollars)
    default: 99
    required: false
  - name: fallback_shipping
    type: number
    label: Flat shipping fee when the threshold is not met (dollars)
    default: 5.99
    required: false
  - name: traffic_split_per_variant
    type: number
    label: Traffic percentage per variant
    default: 25
    required: false
  - name: duration_days
    type: duration
    label: Experiment duration
    default: 21 d
    required: false
  - name: abandon_rate_guardrail
    type: number
    label: Maximum allowed increase in abandoned cart rate (%)
    default: 5
    required: false
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total
      optional: false
    - name: items
      type: number
      meaning: Items in the order
      optional: false
  - slot: abandoned_cart_event
    kind: event
    meaning: A customer abandoned a cart without placing an order
    optional: true
  - slot: account_type
    kind: attribute
    meaning: The customer's account type, such as retail or wholesale
  steps:
  - id: s1
    builds: experiment
    uses:
    - placed_order_event
    - abandoned_cart_event
    - account_type
    - experiment_title
    - flag_key
    - control_threshold
    - variant_b_threshold
    - variant_c_threshold
    - fallback_shipping
    - traffic_split_per_variant
    - duration_days
    - abandon_rate_guardrail
    instruction: 'Create a server-side experiment named "{experiment_title}" with flag key {flag_key}, four variants at {traffic_split_per_variant}%
      each: Control, free shipping from ${control_threshold}; Variant B, from ${variant_b_threshold}; Variant C, from ${variant_c_threshold};
      Variant D, no free shipping and a flat ${fallback_shipping}. Each variant''s payload sets threshold_cents (null for
      Variant D), fallback_shipping_cents and a message line stating the threshold or the flat fee. It applies wherever the
      site reads this flag (cart, checkout and shipping banners), all devices, excluding users whose {account_type} is wholesale,
      with sticky assignment per user for the whole run. Primary goal: revenue per session, the sum of {placed_order_event.total_price}
      per exposed session. Secondary: average order value, orders per session and {placed_order_event.items} per order, split
      by new and returning visitors. Guardrail: the {abandoned_cart_event} rate must not rise more than {abandon_rate_guardrail}%
      in the lower-threshold variants. Run {duration_days}.'
---

# Free shipping threshold test

Slash command: /free-shipping-threshold-test

## Step 1: Set up the threshold test

Create a server-side experiment named "Free Shipping Threshold" with flag key free_shipping_threshold, four variants at 25% each: Control, free shipping from $75; Variant B, from $50; Variant C, from $99; Variant D, no free shipping and a flat $5.99. Each variant's payload sets threshold_cents (null for Variant D), fallback_shipping_cents and a message line stating the threshold or the flat fee. It applies wherever the site reads this flag (cart, checkout and shipping banners), all devices, excluding users whose account type is wholesale, with sticky assignment per user for the whole run. Primary goal: revenue per session, the sum of total price per exposed session. Secondary: average order value, orders per session and items per order, split by new and returning visitors. Guardrail: the abandoned cart event rate must not rise more than 5% in the lower-threshold variants. Run 21 d.
