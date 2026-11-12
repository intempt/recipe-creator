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
    label: Control variant traffic share (%)
    default: 34
    required: false
  - name: traffic_split_variant_b
    type: number
    label: Variant B traffic share (%)
    default: 33
    required: false
  - name: traffic_split_variant_c
    type: number
    label: Variant C (no popup) traffic share (%)
    default: 33
    required: false
  - name: idle_delay
    type: duration
    label: Idle delay before Variant B popup
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
  - slot: cart_click_event
    kind: event
    meaning: A customer clicked an element within the cart page
    optional: true
  - slot: page_view_event
    kind: event
    meaning: A visitor viewed a page
    properties:
    - name: url
      type: text
      meaning: The URL of the page viewed
      optional: false
  - slot: popup_click_event
    kind: event
    meaning: A visitor clicked an element inside the cart save popup
    properties:
    - name: target_id
      type: text
      meaning: The identifier of the element clicked, such as the save or dismiss button
      optional: false
  - slot: popup_submit_event
    kind: event
    meaning: A visitor submitted the email form in the cart save popup
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
  - slot: cart_popup_experiment
    kind: integration
    meaning: A client-side experiment tool that can serve variant DOM, targeting rules and goals on the website
    channel: hubspot
  steps:
  - id: s1
    builds: experiment
    uses:
    - cart_created_event
    - page_view_event
    - popup_click_event
    - popup_submit_event
    - order_placed_event
    - cart_popup_experiment
    - experiment_title
    - traffic_split_control
    - traffic_split_variant_b
    - traffic_split_variant_c
    - idle_delay
    - attribution_window
    - schedule_length
    - bounce_guardrail_increase
    - cart_updated_event
    - cart_click_event
    instruction: 'Create a client-side experiment named "{experiment_title}" in {cart_popup_experiment}, running for {schedule_length}.
      Variants: Control ({traffic_split_control}%) shows an exit-intent popup when the mouse leaves the top of the viewport;
      Variant B ({traffic_split_variant_b}%) shows a popup after {idle_delay} of cart inactivity; Variant C ({traffic_split_variant_c}%)
      shows no popup as the baseline. Targeting: page URL contains "/cart" or {cart_created_event} occurred in the current
      session; desktop only; audience is visitors with at least one {cart_created_event} in the current session; display once
      per session. Control popup: a hidden fixed-position overlay with a heading "Wait! Save your cart", body text "We''ll
      save your items and email you a reminder.", an email input, a "Save my cart" submit button, and a close button; on exit-intent
      set it visible and store a session flag so it does not fire again. Variant B popup: heading "Still thinking it over?",
      body "Save your cart and we''ll send you a reminder: no pressure.", same email form and close button; start a timer
      on {cart_created_event}, show the popup if no {cart_updated_event}, {cart_click_event} or {page_view_event} occurs in
      the window, and reset the timer on any cart interaction. Popup elements carry the target identifiers "popup-save-cart"
      (submit) and "popup-dismiss" (close). Variant C has no DOM changes. Primary goal: {order_placed_event} within {attribution_window}
      of exposure. Secondary metrics: clicks on "popup-save-cart", clicks on "popup-dismiss", {popup_submit_event} rate, and
      orders within {attribution_window}. Guardrail: bounce rate for sessions ending right after popup display must not increase
      more than {bounce_guardrail_increase}%.'
---

# Cart popup timing test

Slash command: /cart-abandonment-popup-timing

## Step 1: Set up the popup timing test

Create a CLIENT EXPERIMENT on /experiences titled "Cart Popup Timing".
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants:
- Control (34%): exit-intent popup (mouse leaves viewport)
- Variant B (33%): 30-second delay popup after cart is idle
- Variant C (33%): no popup (control baseline: measures intrinsic recovery rate)
Targeting:
- Pages: page URL contains "/cart" OR Cart created has occurred in the current session
- Devices: desktop only (exit-intent requires mouse tracking; mobile doesn't have hover events)
- Audience: visitors with at least one Cart created in the current session
- Display frequency: once_per_session
Primary metric: goal_completed_in_experience where experience_id = <this> (goal: Placed order within 24 hours of exposure)
Secondary metrics:
- Click on where target_id = "popup-save-cart" (popup engagement rate)
- Click on where target_id = "popup-dismiss" (dismissal rate)
- Email capture rate from popup (Submit on the popup form)
- Placed order within 24 hours
Guardrail: bounce rate (sessions ending immediately after popup display) must not increase >10%
Schedule: 14 days
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (exit-intent popup)
 HTML target selector: body (append fixed-position element on exit-intent trigger)
 Variant DOM (rendered when mouse leaves viewport top):
 <div class="cart-save-popup" data-variant="control" data-trigger="exit-intent" hidden>
 <div class="popup-overlay"></div>
 <div class="popup-content">
 <button class="popup-close" id="popup-dismiss" aria-label="Close">×</button>
 <h2>Wait! Save your cart</h2>
 <p>We'll save your items and email you a reminder.</p>
 <form class="popup-email-form" id="popup-email-form">
 <input type="email" name="email" placeholder="you@example.com" required />
 <button type="submit" class="popup-cta" id="popup-save-cart">Save my cart</button>
 </form>
 </div>
 </div>
 Trigger logic: attach mouseleave listener to document.documentElement. When the cursor leaves the top edge of the viewport (e.target === document.documentElement && e.clientY <= 0), set the popup's hidden attribute to false and store a sessionStorage flag so it doesn't fire again in the same session.
Variant: B (30-second delay popup)
 HTML target selector: body (append fixed-position element)
 Variant DOM:
 <div class="cart-save-popup" data-variant="b" data-trigger="delay-30s" hidden>
 <div class="popup-overlay"></div>
 <div class="popup-content">
 <button class="popup-close" id="popup-dismiss" aria-label="Close">×</button>
 <h2>Still thinking it over?</h2>
 <p>Save your cart and we'll send you a reminder: no pressure.</p>
 <form class="popup-email-form" id="popup-email-form">
 <input type="email" name="email" placeholder="you@example.com" required />
 <button type="submit" class="popup-cta" id="popup-save-cart">Save my cart</button>
 </form>
 </div>
 </div>
 Trigger logic: when Cart created fires, start a 30-second timer. If no cart_updated, Click on within the cart context, or View page event occurs within that window, the popup shows. Reset the timer on any cart interaction so active shoppers aren't interrupted.
Variant: C (no popup: baseline)
 No DOM changes: measures the intrinsic recovery rate without any popup intervention. This baseline is critical: without it you can't tell whether the popups CAUSE recovery or whether users would have returned anyway.
The Visual Editor allows the user to refine the popup copy, styling, animation (slide-up vs. fade-in), and the email-capture handoff to the merchant's email tool.
Taxonomy notes:
- Cart created is canonical (fires when items are added).
- target_id values "popup-save-cart" and "popup-dismiss" are preserved across Variants Control and B for consistent Click on aggregation. Variant C has neither (no popup rendered).
- The "popup engagement rate" = Click on (target_id = "popup-save-cart") count / total exposures with that variant.
- Variant C's baseline is essential and not optional. Skipping it makes the experiment unable to distinguish causal lift from return-anyway behavior.
- For Variant B's "cart idle" detection, the timer resets on any cart-related interaction. The 30-second window is a starting point; tune based on your audience's typical cart-decision time.
- Email capture from the popup feeds into your existing abandoned-cart email journey: this experiment tests whether the popup adds value above intrinsic return, not whether email recovery itself works.
