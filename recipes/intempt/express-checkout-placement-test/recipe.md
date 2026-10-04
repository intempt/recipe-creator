---
id: express-checkout-placement-test
title: Express checkout placement test
slash_command: /express-checkout-placement-test
group: Experiments
owner: intempt
curator: rana
summary: Compares showing Apple Pay, Google Pay and Shop Pay on the product page, in the cart drawer,
  in both, or only at checkout.
description: >-
  Test express-checkout button placement on PDP, cart, and checkout. "Highest-impact payment additions"
  eliminating card-entry friction; major mobile conversion factor.
version: 2.0.0
classification:
  product:
    - experiences
  agent: experiment-strategist
  mode:
    - ecommerce
  complexity: standard
  executionMode: live
  tags:
    - experiment
    - client
  experimentType: a-b
prerequisites:
  integrations:
    - value: shopify
      severity: blocking
      group: checkout-source
    - value: stripe
      severity: blocking
      group: checkout-source
touches:
  reads:
    - Your Shopify connection
    - Your Stripe connection
  writes:
    - A new A/B experiment, from step 1 "Set up the placement test"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Set up the placement test
    summary: >-
      Splits traffic four ways: express checkout only in cart and checkout (the usual setup), added above
      Add to Cart on the product page, added in the cart drawer, or all three at once. The winner is the
      variant with the most order revenue in the same session.
    builds: experiment
    description: |-
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
       - Variant C: any page where the cart drawer opens (triggered by cart_created event)
       - Variant D: all pages where the buttons are visible per their placement
      - Devices: any (mobile is where express checkout has the largest impact, but desktop also benefits)
      - Audience: all visitors
      - Display frequency: always
      Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from order_created within session of exposure)
      Secondary metrics:
      - click_on where target_id = "apple-pay-button" OR "google-pay-button" OR "shop-pay-button" (express-checkout engagement rate)
      - order_created where payment_method IN ("apple_pay", "google_pay", "shop_pay"): share of express orders per variant
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
      - order_created.payment_method (or equivalent) must be populated to measure express-checkout share. If your order event doesn't track payment method, add it.
outputs:
  - key: experiment
    producedByStep: s1
    type: experiment
    description: Website experiment created on /experiences.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Express checkout placement test

Compares showing Apple Pay, Google Pay and Shop Pay on the product page, in the cart drawer, in both, or only at checkout.

## Steps

1. **Set up the placement test** (builds experiment)

   Splits traffic four ways: express checkout only in cart and checkout (the usual setup), added above Add to Cart on the product page, added in the cart drawer, or all three at once. The winner is the variant with the most order revenue in the same session.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.

## What this recipe touches

Reads:

- Your Shopify connection
- Your Stripe connection

Writes:

- A new A/B experiment, from step 1 "Set up the placement test"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build experiment.
