---
frontmatter_id: loyalty-program-entry-offer-test
slash_command: /loyalty-program-entry-offer-test
description: Compares four checkout offers for joining the loyalty programme, scored on how many first-time buyers actually join.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Tests four checkout offers for joining the loyalty programme with first-time buyers, scoring each offer by how
    many actually join and their repeat purchases.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Loyalty Programme Entry Offer
  - name: variant_b_discount_percent
    type: number
    label: Variant B discount on next order (%)
    default: 10
  - name: variant_c_points_multiplier
    type: number
    label: Variant C points multiplier on this order (x)
    default: 2
  - name: variant_d_free_shipping_orders
    type: number
    label: Variant D free shipping on next N orders
    default: 3
  - name: traffic_split_percent
    type: number
    label: Traffic share per variant (%)
    default: 25
  - name: checkout_path_contains
    type: string
    label: Checkout page URL contains
    default: /checkout
  - name: experiment_duration
    type: duration
    label: Experiment run length
    default: 30 d
  - name: repeat_purchase_window
    type: duration
    label: Repeat purchase window after joining
    default: 90 d
  - name: checkout_completion_guardrail_percent
    type: number
    label: Maximum allowed drop in checkout completion (%)
    default: 3
  requirements:
  - slot: checkout_created_event
    kind: event
    meaning: A customer started a checkout.
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order.
    properties:
    - name: total_price
      type: number
      meaning: Total price of the order
      optional: false
    - name: timestamp
      type: date
      meaning: When the order was placed
      optional: false
  - slot: tags_added_event
    kind: event
    meaning: A tag was added to a user record (user_tags_added).
    properties:
    - name: tag
      type: string
      meaning: The tag value added to the user
      optional: false
  - slot: goal_completed_event
    kind: event
    meaning: A goal was completed within an experience (goal_completed_in_experience).
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experience the goal completed in
      optional: false
  - slot: loyalty_member_tag
    kind: attribute
    meaning: A user tag marking a customer as a loyalty programme member, plus variant-specific offer tags.
  steps:
  - id: s1
    builds: experiment
    uses:
    - checkout_created_event
    - order_placed_event
    - tags_added_event
    - goal_completed_event
    - loyalty_member_tag
    - experiment_title
    - traffic_split_percent
    - checkout_path_contains
    - experiment_duration
    - checkout_completion_guardrail_percent
    - variant_b_discount_percent
    - variant_c_points_multiplier
    - variant_d_free_shipping_orders
    - repeat_purchase_window
    instruction: 'Create a client experiment named "{experiment_title}" targeting checkout pages whose URL contains "{checkout_path_contains}"
      on any device, shown only to visitors who have never done {order_placed_event} and displayed once per order. Run four
      variants at {traffic_split_percent}% each: Control with no loyalty prompt; Variant B: a {variant_b_discount_percent}%
      discount on the next order for joining; Variant C: {variant_c_points_multiplier}x points on this order for joining;
      Variant D: free shipping on the next {variant_d_free_shipping_orders} orders for joining. For Variants B, C and D, insert
      a banner before the submit button in the checkout summary: a heading inviting them to join the rewards programme, the
      offer text and a sign-up checkbox. Primary metric: {goal_completed_event} in the experience, where the goal fires when
      {tags_added_event} adds the {loyalty_member_tag} tag. Secondary metric: share of joiners who do {order_placed_event}
      again within {repeat_purchase_window}. Guardrail: checkout completion rate ({checkout_created_event} to {order_placed_event})
      must not drop more than {checkout_completion_guardrail_percent}%. Run for {experiment_duration}.'
---

# Loyalty signup offer test

Slash command: /loyalty-program-entry-offer-test

## Step 1: Set up the loyalty offer test

Create a client experiment named "Loyalty Programme Entry Offer" targeting checkout pages whose URL contains "/checkout" on any device, shown only to visitors who have never done order placed event and displayed once per order. Run four variants at 25% each: Control with no loyalty prompt; Variant B: a 10% discount on the next order for joining; Variant C: 2x points on this order for joining; Variant D: free shipping on the next 3 orders for joining. For Variants B, C and D, insert a banner before the submit button in the checkout summary: a heading inviting them to join the rewards programme, the offer text and a sign-up checkbox. Primary metric: goal completed event in the experience, where the goal fires when tags added event adds the loyalty member tag tag. Secondary metric: share of joiners who do order placed event again within 90 d. Guardrail: checkout completion rate (checkout created event to order placed event) must not drop more than 3%. Run for 30 d.
