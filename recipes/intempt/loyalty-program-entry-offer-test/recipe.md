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
  - name: cohort_tracking_duration
    type: duration
    label: Additional cohort tracking length
    default: 90 d
  - name: repeat_purchase_window
    type: duration
    label: Repeat purchase window after joining
    default: 90 d
  - name: checkout_completion_guardrail_percent
    type: number
    label: Maximum allowed drop in checkout completion (%)
    default: 3
  requirements:
  - slot: loyalty_offer_experience
    kind: destination
    meaning: A client-side experiment surface on the checkout page where the four loyalty offer variants are shown.
    channel: hubspot
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
  - slot: first_time_buyer_segment
    kind: segment
    meaning: Customers who have never placed an order (lifetime value zero or orders count zero).
  - slot: loyalty_member_tag
    kind: attribute
    meaning: A user tag marking a customer as a loyalty programme member, plus variant-specific offer tags.
  steps:
  - id: s1
    builds: experiment
    uses:
    - loyalty_offer_experience
    - checkout_created_event
    - order_placed_event
    - tags_added_event
    - goal_completed_event
    - first_time_buyer_segment
    - loyalty_member_tag
    - experiment_title
    - traffic_split_percent
    - checkout_path_contains
    - experiment_duration
    - checkout_completion_guardrail_percent
    - variant_b_discount_percent
    - variant_c_points_multiplier
    - variant_d_free_shipping_orders
    instruction: 'Create a client experiment named "{experiment_title}" on the experiences page, targeting checkout pages
      whose URL contains "{checkout_path_contains}" on any device, shown only to the {first_time_buyer_segment} audience and
      displayed once per order. Run four variants: Control at {traffic_split_percent}% with no loyalty prompt; Variant B at
      {traffic_split_percent}% with a {variant_b_discount_percent}% discount on the next order for joining; Variant C at {traffic_split_percent}%
      with {variant_c_points_multiplier}x points on this order for joining; Variant D at {traffic_split_percent}% with free
      shipping on the next {variant_d_free_shipping_orders} orders for joining. For Variants B, C and D, insert a banner before
      the submit button in the checkout summary with a heading inviting the customer to join the rewards programme, the offer
      text, and a checkbox labelled to sign up for the rewards programme. Primary metric: goal completed in the experience,
      where the goal fires on a tag being added with the loyalty member tag. Guardrail: checkout completion rate must not
      drop more than {checkout_completion_guardrail_percent}%. Run for {experiment_duration}.'
---

# Loyalty signup offer test

Slash command: /loyalty-program-entry-offer-test

## Step 1: Set up the loyalty offer test

Create a CLIENT EXPERIMENT on /experiences titled "Loyalty Programme Entry Offer".
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants:
- Control (25%): no loyalty prompt at checkout
- Variant B (25%): 10% discount on next order for joining
- Variant C (25%): 2× points on this order for joining
- Variant D (25%): free shipping on next 3 orders for joining
Targeting:
- Pages: page URL contains "/checkout"
- Devices: any
- Audience: first-time buyers only: segment definition: Lifetime value = 0 OR orders_count = 0 (this is their first checkout)
- Display frequency: once per order
Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on user_tags_added with "loyalty_member" tag within session)
Secondary metrics:
- 90-day repeat purchase rate per joined cohort (see cohort tagging below: this is the most important downstream signal)
- Placed order.total_price on the current order (does the offer increase basket size?)
- Per-variant loyalty join rate (loyalty_member tag added / Checkout created within experiment)
Guardrail: checkout completion rate must not drop >3% (offer banner shouldn't slow conversion)
Schedule: 30 days for the experiment itself; 90 additional days for cohort-tracking the repeat-purchase rate.
═══ Cohort tagging for 90-day repeat purchase measurement ═══
The "90-day repeat purchase rate per variant" is the most informative signal but requires cohort tagging at signup. The recipe expects the loyalty-join firing logic to capture which variant the user joined under:
When the user checks the loyalty checkbox in any variant, fire BOTH events together:
 1. user_tags_added with tag = "loyalty_member"
 2. user_tags_added with tag = "loyalty_offer:b" (or "c" or "d" matching the variant they joined under)
The variant-specific tag persists on the user record. Then 90 days later, segment cohorts:
 - Cohort B = users with both "loyalty_member" AND "loyalty_offer:b" tags
 - Cohort C = users with both "loyalty_member" AND "loyalty_offer:c" tags
 - Cohort D = users with both "loyalty_member" AND "loyalty_offer:d" tags
 - Cohort Control = first-time-buyers in Variant Control who completed checkout (didn't see a prompt)
90-day repeat-purchase rate per cohort = count(users in cohort with Placed order.timestamp > join_timestamp AND Placed order.timestamp < join_timestamp + 90 days) / cohort size.
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (no DOM changes: no prompt)
 Existing checkout flow. Measures intrinsic loyalty join rate via other channels.
Variant: B (10% off next order)
 HTML target selector: .checkout-summary (insert before submit button)
 Variant DOM:
 <div class="loyalty-offer-banner" data-variant="b" data-offer-code="loyalty_offer_b">
 <h3>Join our rewards program</h3>
 <p>Get <strong>10% off your next order</strong></p>
 <label class="loyalty-checkbox-label">
 <input type="checkbox" id="loyalty-join-checkbox" data-variant="b" data-offer-code="loyalty_offer_b" />
 <span>Yes, sign me up for [Brand] rewards</span>
 </label>
 </div>
Variant: C (2× points this order)
 HTML target selector: .checkout-summary
 Variant DOM:
 <div class="loyalty-offer-banner" data-variant="c" data-offer-code="loyalty_offer_c">
 <h3>Join our rewards program</h3>
 <p>Earn <strong>double points on this order</strong></p>
 <label class="loyalty-checkbox-label">
 <input type="checkbox" id="loyalty-join-checkbox" data-variant="c" data-offer-code="loyalty_offer_c" />
 <span>Yes, sign me up for [Brand] rewards</span>
 </label>
 </div>
Variant: D (free shipping next 3 orders)
 HTML target selector: .checkout-summary
 Variant DOM:
 <div class="loyalty-offer-banner" data-variant="d" data-offer-code="loyalty_offer_d">
 <h3>Join our rewards program</h3>
 <p>Get <strong>free shipping on your next 3 orders</strong></p>
 <label class="loyalty-checkbox-label">
 <input type="checkbox" id="loyalty-join-checkbox" data-variant="d" data-offer-code="loyalty_offer_d" />
 <span>Yes, sign me up for [Brand] rewards</span>
 </label>
 </div>
When the user submits checkout with the loyalty-join-checkbox checked, fire user_tags_added twice: once with "loyalty_member" and once with the variant-specific tag from the data-offer-code attribute. The goal_completed_in_experience event fires automatically based on the loyalty_member tag addition.
Taxonomy notes:
- user_tags_added is a canonical event that fires when tags are added to a user record.
- Segment definitions for the 90-day cohort comparison use the tags-on-user-object pattern (Users.tags array contains "loyalty_offer:b" etc.).
- The 90-day window is the standard repeat-purchase measurement window for ecom; some categories (apparel) may need 60 days, others (consumables) may need 30.
- Cohort Control (first-time buyers who saw no prompt and didn't join) is essential for measuring CAUSAL repeat-purchase lift: without it you only know which offer-cohort returns most often, not whether the program itself moves the needle vs. doing nothing.
- The Placed order.total_price secondary metric measures whether the offer affects current-order basket size. Some offers (free shipping next-order) shouldn't move current AOV; some (2× points) might.
