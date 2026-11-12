---
frontmatter_id: express-checkout-placement-test
slash_command: /express-checkout-placement-test
description: Tests different express checkout button configurations on the product page against a standard checkout flow.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Runs a placement test of express checkout buttons (Apple Pay, Google Pay, Shop Pay) on the product page and cart
    drawer against standard checkout to see which setup lifts revenue.
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
  - name: revenue_goal_window
    type: duration
    label: Attribution window for revenue after exposure
    default: session
    required: false
  requirements:
  - slot: experiment_exposure_event
    kind: event
    meaning: A visitor was exposed to a client experiment variant
  - slot: cart_created_event
    kind: event
    meaning: A visitor created a cart or opened the cart drawer
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: payment_method
      type: string
      meaning: Payment method used for the order (e.g. apple_pay, google_pay, shop_pay)
      optional: false
    - name: order_value
      type: number
      meaning: Total value of the order
      optional: false
  - slot: express_button_click_event
    kind: event
    meaning: A visitor clicked an express checkout button
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked element (apple-pay-button, google-pay-button, shop-pay-button)
      optional: false
  - slot: experiment_goal_event
    kind: event
    meaning: A goal was completed within a client experiment exposure
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experiment experience
      optional: false
    - name: value
      type: number
      meaning: Revenue value attributed to the goal
      optional: false
  - slot: mobile_device_attribute
    kind: attribute
    meaning: The device type of a visitor (mobile or desktop)
  - slot: ecommerce_website
    kind: destination
    meaning: The storefront where the client experiment runs
    channel: shopify
  steps:
  - id: s1
    builds: experiment
    uses:
    - experiment_title
    - duration_days
    - min_mobile_sessions_per_variant
    - control_traffic_percent
    - revenue_goal_window
    - experiment_exposure_event
    - cart_created_event
    - order_placed_event
    - express_button_click_event
    - experiment_goal_event
    - mobile_device_attribute
    - ecommerce_website
    instruction: 'Create a client experiment titled "{experiment_title}" on the storefront {ecommerce_website}. Use four variants
      at {control_traffic_percent}% traffic each: Control (express checkout only on cart and checkout pages, no DOM change);
      Variant B (express checkout buttons placed above Add to Cart on the product page); Variant C (express checkout buttons
      placed in the cart drawer, shown when it opens); Variant D (combined placement on product page, cart drawer and checkout).
      Targeting: Variant B on pages whose URL contains /products/; Variant C on any page where the cart drawer opens after
      {cart_created_event}; Variant D on all pages where the buttons are visible. Include all devices, all visitors, display
      frequency always. Run for {duration_days}, with at least {min_mobile_sessions_per_variant} mobile sessions per variant.
      Primary metric: revenue from {order_placed_event} within {revenue_goal_window} of exposure, measured through {experiment_goal_event}
      where value is greater than 0. Secondary metrics: clicks on {express_button_click_event} by target_id (apple-pay-button,
      google-pay-button, shop-pay-button); share of {order_placed_event} where payment_method is apple_pay, google_pay or
      shop_pay per variant; mobile versus desktop conversion split using {mobile_device_attribute}; average order value per
      variant from {order_placed_event.order_value}. Guardrail: standard checkout completion rate must not drop. Do not run
      concurrently with a checkout-flow-length test.'
---

# Express checkout placement test

Slash command: /express-checkout-placement-test

## Step 1: Set up the placement test

Create a CLIENT EXPERIMENT on /experiences titled "Express Checkout Placement".
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants:
- Control (25%): express checkout buttons in cart and checkout pages only (existing for most stores)
- Variant B (25%): adds express checkout above Add to Cart on PDP: Apple Pay / Google Pay / Shop Pay buttons visible directly on the product page
- Variant C (25%): adds express checkout in cart drawer (mini-cart): buttons visible when the cart drawer opens
- Variant D (25%): combined: express checkout on PDP + cart drawer + checkout (maximum visibility)
Targeting:
- Pages:
 - Variant B: page URL contains "/products/"
 - Variant C: any page where the cart drawer opens (triggered by Cart created event)
 - Variant D: all pages where the buttons are visible per their placement
- Devices: any (mobile is where express checkout has the largest impact, but desktop also benefits)
- Audience: all visitors
- Display frequency: always
Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from Placed order within session of exposure)
Secondary metrics:
- Click on where target_id = "apple-pay-button" OR "google-pay-button" OR "shop-pay-button" (express-checkout engagement rate)
- Placed order where payment_method IN ("apple_pay", "google_pay", "shop_pay"): share of express orders per variant
- Mobile vs. desktop conversion rate split (express checkout is mobile-dominant)
- AOV per variant (express checkout users may have different basket profiles)
Guardrail: standard checkout completion rate must not drop (express checkout shouldn't cannibalize properly-considered checkouts; both should rise)
Schedule: 14 days, sufficient mobile traffic per variant (~3,000 sessions)
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (no DOM changes: express checkout only on cart/checkout pages, existing behavior)
Variant: B (express checkout above Add to Cart on PDP)
 HTML target selector: .add-to-cart-block (insert before the standard Add to Cart button)
 Variant DOM:
 <div class="express-checkout-row" data-variant="b" data-placement="pdp">
 <button class="apple-pay-button" id="apple-pay-button" data-variant="b">
 <svg>...</svg> Buy with Apple Pay
 </button>
 <button class="google-pay-button" id="google-pay-button" data-variant="b">
 <svg>...</svg> Buy with Google Pay
 </button>
 <button class="shop-pay-button" id="shop-pay-button" data-variant="b">
 <svg>...</svg> Shop Pay
 </button>
 <div class="express-divider">
 <span class="divider-line"></span>
 <span class="divider-text">or</span>
 <span class="divider-line"></span>
 </div>
 </div>
 <!-- Standard Add to Cart button follows -->
 Note: the actual Apple Pay / Google Pay / Shop Pay button rendering uses the platform's SDKs (e.g., Stripe Apple Pay button, Shopify Shop Pay button). The recipe shows the placement; the buttons themselves come from your payment provider's SDK.
Variant: C (express checkout in cart drawer)
 HTML target selector: .cart-drawer-actions (the action area at the bottom of the cart drawer)
 Variant DOM:
 <div class="express-checkout-row express-checkout-row--drawer" data-variant="c" data-placement="cart-drawer">
 <button class="apple-pay-button" id="apple-pay-button" data-variant="c">Buy with Apple Pay</button>
 <button class="google-pay-button" id="google-pay-button" data-variant="c">Buy with Google Pay</button>
 <button class="shop-pay-button" id="shop-pay-button" data-variant="c">Shop Pay</button>
 </div>
 <button class="standard-checkout-cta" id="cart-drawer-checkout">Continue to checkout</button>
Variant: D (combined: PDP + cart drawer)
 Both Variant B and Variant C DOM patches applied together. Standard checkout button still available alongside.
The Visual Editor allows the user to refine button order (Apple Pay first on iOS, Google Pay first on Android, etc.), styling, and divider design.
Taxonomy notes:
- REQUIRES PAYMENT-PROVIDER INTEGRATION: This recipe assumes the merchant has Apple Pay, Google Pay, and Shop Pay configured at the payment-provider level (Stripe, Shopify Payments, Braintree, etc.). Without these, the variant buttons render but don't function.
- Mobile users see the largest impact: express checkout on PDP can lift mobile conversion 15-30% by eliminating card-entry friction.
- iOS users prefer Apple Pay; Android users prefer Google Pay; Shopify users see Shop Pay. Show device-appropriate buttons; the buttons themselves auto-detect availability.
- Don't run this experiment alongside checkout-flow-length-test concurrently: checkout flow changes interact with express checkout placement. Run sequentially.
- Placed order.payment_method (or equivalent) must be populated to measure express-checkout share. If your order event doesn't track payment method, add it.
