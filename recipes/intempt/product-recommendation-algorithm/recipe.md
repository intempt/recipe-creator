---
frontmatter_id: product-recommendation-algorithm
slash_command: /product-recommendation-algorithm
description: Runs a server-side test of three recommendation methods (also bought, recently viewed, trending) on product and
  category pages to find which drives the most cross-sell revenue.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Runs a server-side test of three recommendation methods (also bought, recently viewed, trending) to find which
    drives the most cross-sell revenue.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Recommendation Algorithm Test
    required: false
  - name: flag_key
    type: string
    label: Flag key
    default: recommendation_algorithm
    required: false
  - name: control_weight
    type: number
    label: Control traffic share (%)
    default: 33
    required: false
  - name: variant_b_weight
    type: number
    label: Recently viewed traffic share (%)
    default: 33
    required: false
  - name: variant_c_weight
    type: number
    label: Trending traffic share (%)
    default: 34
    required: false
  - name: max_items
    type: number
    label: Products shown per block
    default: 4
    required: false
  - name: schedule_duration
    type: duration
    label: Test duration
    default: 14 d
    required: false
  - name: guardrail_max_drop_pct
    type: number
    label: Max drop in product view to cart rate (%)
    default: 5
    required: false
  requirements:
  - slot: recommendation_click
    kind: event
    meaning: A customer clicked a recommended product in a recommendation block
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked recommendation, rec- plus its position
      optional: false
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total
      optional: false
    - name: items
      type: string
      meaning: Products in the order
      optional: false
  - slot: cart_created
    kind: event
    meaning: A customer created a cart
  - slot: product_page_view
    kind: event
    meaning: A customer viewed a product detail page
  steps:
  - id: s1
    builds: experiment
    uses:
    - recommendation_click
    - order_placed
    - cart_created
    - product_page_view
    - experiment_title
    - flag_key
    - control_weight
    - variant_b_weight
    - variant_c_weight
    - max_items
    - schedule_duration
    - guardrail_max_drop_pct
    instruction: 'Create a server-side experiment named "{experiment_title}" with flag key {flag_key}, for all visitors on
      pages whose URL contains /products/ or /category/, sticky per user, running {schedule_duration}. Variants, each showing
      {max_items} products with target_id rec- plus the position: Control ({control_weight}%) "Customers also bought" from
      products bought together; Variant B ({variant_b_weight}%) "Recently viewed by you" from the visitor''s session, falling
      back to trending; Variant C ({variant_c_weight}%) "Trending now" from the most-ordered products. Primary metric: sum
      of {order_placed.total_price} for orders whose {order_placed.items} include a product the visitor clicked through {recommendation_click}.
      Secondary metrics: {recommendation_click} rate and clicks per {recommendation_click.target_id} position. Guardrail:
      the share of visitors with {product_page_view} who then did {cart_created} must not drop more than {guardrail_max_drop_pct}%
      below Control.'
---

# Recommendation algorithm test

Slash command: /product-recommendation-algorithm

## Step 1: Set up the algorithm test

Create a server-side experiment named "Recommendation Algorithm Test" with flag key recommendation_algorithm, for all visitors on pages whose URL contains /products/ or /category/, sticky per user, running 14 d. Variants, each showing 4 products with target_id rec- plus the position: Control (33%) "Customers also bought" from products bought together; Variant B (33%) "Recently viewed by you" from the visitor's session, falling back to trending; Variant C (34%) "Trending now" from the most-ordered products. Primary metric: sum of total price for orders whose items include a product the visitor clicked through recommendation click. Secondary metrics: recommendation click rate and clicks per target id position. Guardrail: the share of visitors with product page view who then did cart created must not drop more than 5% below Control.
