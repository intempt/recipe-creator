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
    label: Flat shipping fee when threshold not met (dollars)
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
    label: Max allowed increase in abandoned cart rate (%)
    default: 5
    required: false
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total value
      optional: false
    - name: items
      type: number
      meaning: Number of items in the order
      optional: true
  - slot: experience_exposure_event
    kind: event
    meaning: A visitor was exposed to an experience variant
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experience
      optional: false
  - slot: experience_goal_event
    kind: event
    meaning: A visitor completed the configured goal within an experience
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experience
      optional: false
    - name: value
      type: number
      meaning: Goal value attributed to the experience
      optional: false
  - slot: wholesale_account_segment
    kind: segment
    meaning: Visitors whose account type is wholesale, excluded from the test
  - slot: abandoned_cart_event
    kind: event
    meaning: A customer abandoned a cart without placing an order
    optional: true
  steps:
  - id: s1
    builds: experiment
    uses:
    - experiment_title
    - flag_key
    - control_threshold
    - variant_b_threshold
    - variant_c_threshold
    - fallback_shipping
    - traffic_split_per_variant
    - duration_days
    - abandon_rate_guardrail
    - placed_order_event
    - experience_exposure_event
    - experience_goal_event
    - wholesale_account_segment
    - abandoned_cart_event
    instruction: 'Create a server experiment titled "{experiment_title}" with flag key {flag_key} and no per-variant targeting.
      Define four variants at {traffic_split_per_variant}% each: Control with free shipping at ${control_threshold}, Variant
      B with free shipping at ${variant_b_threshold}, Variant C with free shipping at ${variant_c_threshold}, and Variant
      D with no free shipping (flat ${fallback_shipping}). Each variant''s JSON payload sets threshold_cents (threshold ×
      100, or null for Variant D), threshold_display, fallback_shipping_cents (fallback × 100), fallback_shipping_display,
      and a messaging line stating the threshold or the flat standard shipping fee. Targeting: apply to every page that calls
      getFlag for this flag (cart, checkout, and shipping-info banners on product pages); all devices; exclude {wholesale_account_segment}.
      Display frequency: always, with sticky assignment so each userId receives the same variant for the full run. Primary
      metric: revenue per session, measured as the sum of {placed_order_event.total_price} attributed through {experience_exposure_event}
      where {experience_goal_event} has value greater than 0. Secondary metrics: average order value from {placed_order_event.total_price},
      placed-order count per session, and {placed_order_event.items} per order. Guardrail: abandoned cart rate via {abandoned_cart_event}
      must not rise more than {abandon_rate_guardrail}% in lower-threshold variants. Run for {duration_days}. Report new and
      returning visitors separately.'
---

# Free shipping threshold test

Slash command: /free-shipping-threshold-test

## Step 1: Set up the threshold test

Create a SERVER EXPERIMENT on /experiences titled "Free Shipping Threshold".
═══ PATH 1: Top-level configuration (Setup tab) ═══
Experience type: server_experiment (Flag Key + JSON payload, no per-variant targeting)
Flag Key: free_shipping_threshold
Variants:
- Control (25%): free shipping at $75
- Variant B (25%): free shipping at $50
- Variant C (25%): free shipping at $99
- Variant D (25%): no free shipping (flat $5.99)
Targeting:
- Pages: any page where the free-shipping threshold logic applies: typically cart, checkout, and shipping-info banners on PDPs (whatever pages call getFlag for this experiment)
- Devices: any (server experiments are device-agnostic; the cart logic runs the same regardless of client device)
- Audience: all visitors except wholesale accounts (segment exclusion: account_type = "wholesale")
- Display frequency: always (sticky assignment: every cart calculation for a given userId uses the same variant for the experiment's duration)
Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue per session: sum of Placed order.total_price attributed via exposed_to_experience)
Secondary metrics:
- Placed order.total_price (AOV per variant)
- Placed order count per session (conversion rate)
- items_count on Placed order (units per order: does free shipping inflate cart size?)
Guardrail: Abandoned cart rate must not increase >5% in lower-threshold variants (some shoppers may abandon when realizing they don't qualify)
Schedule: 21 days. Track new vs. returning visitors separately (returning visitors may have shipping expectations from prior orders).
═══ PATH 2: Variant JSON payload (loaded as code via SDK) ═══
For SERVER experiments, each variant ships a JSON payload that the application loads via getFlag() and renders accordingly. The application code reads the payload and applies the threshold dynamically.
Variant: Control (75)
 JSON payload:
 {
 "threshold_cents": 7500,
 "threshold_display": "$75",
 "fallback_shipping_cents": 599,
 "fallback_shipping_display": "$5.99",
 "messaging": "Free shipping on orders over $75!"
 }
Variant: B (50)
 {
 "threshold_cents": 5000,
 "threshold_display": "$50",
 "fallback_shipping_cents": 599,
 "fallback_shipping_display": "$5.99",
 "messaging": "Free shipping on orders over $50!"
 }
Variant: C (99)
 {
 "threshold_cents": 9900,
 "threshold_display": "$99",
 "fallback_shipping_cents": 599,
 "fallback_shipping_display": "$5.99",
 "messaging": "Free shipping on orders over $99!"
 }
Variant: D (no free shipping)
 {
 "threshold_cents": null,
 "threshold_display": null,
 "fallback_shipping_cents": 599,
 "fallback_shipping_display": "$5.99",
 "messaging": "Standard shipping: $5.99"
 }
SDK integration example (JavaScript):
 const config = await intempt.getFlag('free_shipping_threshold', userId);
 // config.threshold_cents to number or null
 // applies in cart logic, displays in shipping banner
Taxonomy notes:
- Placed order.total_price is the canonical order value. items_count derives from Placed order.items length.
- exposed_to_experience fires when getFlag() is first called for the user; goal_completed_in_experience fires when the configured goal (Placed order within session) is reached.
- Server experiments do not have a Visual Editor: there is no DOM change. The variant's effect is purely via the JSON payload's effect on application logic.
- "Display frequency: always" for server experiments means the same variant returns on every getFlag call for a given userId (sticky assignment): this is what makes the experiment statistically valid. A user assigned to Variant B sees the $50 threshold consistently across sessions.
