---
frontmatter_id: post-purchase-upsell-on-page-placement
slash_command: /post-purchase-upsell-on-page-placement
description: Compares three places to put the upsell on the order confirmation page, scored on extra revenue within 24 hours.
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
  - name: traffic_split_control
    type: number
    label: Control traffic share (%)
    default: 34
  - name: traffic_split_variant_b
    type: number
    label: Variant B traffic share (%)
    default: 33
  - name: traffic_split_variant_c
    type: number
    label: Variant C traffic share (%)
    default: 33
  - name: modal_delay
    type: duration
    label: Modal delay after page load
    default: 5 s
  - name: revenue_window
    type: duration
    label: Revenue attribution window
    default: 24 h
  - name: add_to_second_order_window
    type: duration
    label: Add-to-second-order window
    default: 1 h
  - name: satisfaction_window
    type: duration
    label: Satisfaction feedback window after order
    default: 7 d
  - name: modal_dismiss_threshold
    type: number
    label: Maximum modal dismiss rate (%)
    default: 80
  - name: test_duration
    type: duration
    label: Experiment duration
    default: 30 d
  requirements:
  - slot: upsell_placed_order_event
    kind: event
    meaning: A customer completed an order (Placed order)
  - slot: upsell_click_event
    kind: event
    meaning: A customer clicked an upsell product button on the website
    properties:
    - name: target_id
      type: text
      meaning: Identifier of the clicked element, starting with upsell-product-
      optional: false
  - slot: cart_created_event
    kind: event
    meaning: A customer created a cart
  - slot: feedback_event
    kind: event
    meaning: A customer submitted feedback with a satisfaction score
    properties:
    - name: score
      type: number
      meaning: Satisfaction score submitted
      optional: false
  - slot: dismiss_event
    kind: event
    meaning: A customer dismissed the upsell modal on the website
  - slot: upsell_accepted_value
    kind: attribute
    meaning: Value of an upsell product added to an order
  steps:
  - id: s1
    builds: experiment
    uses:
    - experiment_title
    - traffic_split_control
    - traffic_split_variant_b
    - traffic_split_variant_c
    - modal_delay
    - revenue_window
    - add_to_second_order_window
    - satisfaction_window
    - modal_dismiss_threshold
    - test_duration
    - upsell_placed_order_event
    - upsell_click_event
    - cart_created_event
    - feedback_event
    - dismiss_event
    - upsell_accepted_value
    instruction: 'Create a client-side website experiment titled "{experiment_title}" that runs for {test_duration}. Targeting:
      pages whose URL contains "/order-confirmation" or "/thank-you", any device, customers who just completed a {upsell_placed_order_event},
      shown once per order. Variants: Control ({traffic_split_control}%) shows an upsell carousel above the order details;
      Variant B ({traffic_split_variant_b}%) shows an upsell strip below the order details; Variant C ({traffic_split_variant_c}%)
      shows an inline modal that opens {modal_delay} after the confirmation page loads. Control HTML: a section with class
      post-purchase-upsell and heading "Customers like you also bought", containing a carousel of three product cards, each
      with an image, product name, price, and an "Add to Order" button with ids upsell-product-1, upsell-product-2, upsell-product-3.
      Insert before the order confirmation block. Variant B: same carousel markup, inserted after the order confirmation block.
      Variant C: a hidden modal overlay with a close button (id upsell-modal-dismiss, aria-label Close) and heading "One more
      thing: customers also love these", containing the same three product buttons; appended to the body. Trigger: after the
      page view on the confirmation page, wait {modal_delay} and then unhide the overlay; add a CSS fade animation. Primary
      goal: a {upsell_placed_order_event} within {revenue_window} of upsell exposure (incremental revenue). Secondary metrics:
      click rate on {upsell_click_event} for upsell-product buttons; {cart_created_event} within {add_to_second_order_window}
      for shown users; average {upsell_accepted_value} when accepted. Guardrails: the average {feedback_event} score within
      {satisfaction_window} of the order must not drop; {dismiss_event} rate for Variant C must not exceed {modal_dismiss_threshold}%.
      Attribute upsell-driven orders by joining the upsell click to a later order within the revenue window.'
---

# Post-purchase upsell placement test

Slash command: /post-purchase-upsell-on-page-placement

## Step 1: Set up the upsell placement test

Create a CLIENT EXPERIMENT on /experiences titled "Post-Purchase Upsell: On-Page Placement".
NOTE: This recipe was previously authored with email and push notification variants. The current product scope is website-only personalizations and experiments: email and push are outside the product. The recipe now focuses exclusively on the on-page placement dimension.
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants:
- Control (34%): upsell carousel above order details on the confirmation page
- Variant B (33%): upsell strip below order details on the confirmation page
- Variant C (33%): inline modal that appears 5 seconds after order confirmation page loads
Targeting:
- Pages: page URL contains "/order-confirmation" OR "/thank-you"
- Devices: any
- Audience: customers who just completed an Placed order event
- Display frequency: once (per order)
Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on additional Placed order within 24 hours of upsell exposure: incremental revenue)
Secondary metrics:
- Click on where target_id starts with "upsell-product-" (upsell engagement rate)
- Add-to-second-order rate (Cart created within 1 hour for any user shown the upsell)
- Average upsell value when accepted
Guardrail: customer satisfaction (Feedback submitted score within 7 days of order) must not drop; modal-dismiss rate (variant C) must not exceed 80% (high dismissal = annoyance signal)
Schedule: 30 days
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (above order details)
 HTML target selector: .order-confirmation (insert before)
 Variant DOM:
 <section class="post-purchase-upsell" data-variant="control" data-placement="above-order">
 <h2>Customers like you also bought</h2>
 <div class="upsell-carousel">
 <article class="upsell-product"><img /><h3>[Product]</h3><span>[$X.XX]</span><button id="upsell-product-1">Add to Order</button></article>
 <article class="upsell-product"><img /><h3>[Product]</h3><span>[$X.XX]</span><button id="upsell-product-2">Add to Order</button></article>
 <article class="upsell-product"><img /><h3>[Product]</h3><span>[$X.XX]</span><button id="upsell-product-3">Add to Order</button></article>
 </div>
 </section>
Variant: B (below order details)
 HTML target selector: .order-confirmation (append after)
 Same upsell carousel HTML as Control.
Variant: C (inline modal, 5s delay)
 HTML target selector: body (append modal)
 Variant DOM:
 <div class="upsell-modal-overlay" data-variant="c" data-trigger="5s-delay" hidden>
 <div class="upsell-modal">
 <button class="modal-close" id="upsell-modal-dismiss" aria-label="Close">×</button>
 <h2>One more thing: customers also love these</h2>
 <div class="upsell-carousel">
 <!-- 3 upsell products with id="upsell-product-1/2/3" -->
 </div>
 </div>
 </div>
 Trigger JS: setTimeout 5000ms after View page on /order-confirmation, set overlay hidden=false. Pair with a CSS modal animation.
Taxonomy notes:
- Email and push variants from the original template are explicitly removed because the product scope is website-only.
- The "incremental revenue" measurement requires the upsell-attributed Placed order to be distinguished from the original purchase: typically done by session tracking joining Click on (target_id starts with "upsell-") to a subsequent Placed order within the attribution window.
