---
frontmatter_id: checkout-flow-length-test
slash_command: /checkout-flow-length-test
description: Compares a one-page checkout against a three-step checkout, scored on orders completed within an hour of starting.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Tests a one-page checkout against a three-step checkout and reports which one gets more orders placed within an
    hour of starting, with guardrails on card declines and abandonment.
  parameters:
  - name: experimentName
    type: string
    label: Experiment name
    default: Checkout Flow Length
    required: false
  - name: checkoutPath
    type: string
    label: Checkout page URL fragment
    default: /checkout
    required: false
  - name: controlTrafficPercent
    type: number
    label: One-page (control) traffic share (%)
    default: 50
    required: false
  - name: variantTrafficPercent
    type: number
    label: Three-step traffic share (%)
    default: 50
    required: false
  - name: testDuration
    type: duration
    label: Test duration
    default: 14 d
    required: false
  - name: minCheckoutsPerVariant
    type: number
    label: Minimum checkouts per variant
    default: 3000
    required: false
  - name: orderWindow
    type: duration
    label: Order completion window after checkout starts
    default: 1 h
    required: false
  - name: declineIncreaseLimit
    type: number
    label: Maximum allowed increase in card decline rate (percentage points)
    default: 2
    required: false
  - name: abandonIncreaseLimit
    type: number
    label: Maximum allowed increase in checkout abandonment (percentage points)
    default: 5
    required: false
  requirements:
  - slot: checkout_created_event
    kind: event
    meaning: A customer started a checkout
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
  - slot: payment_failed_event
    kind: event
    meaning: A customer's payment attempt failed
  - slot: abandoned_checkout_event
    kind: event
    meaning: A customer abandoned a checkout before placing an order
  - slot: view_page_event
    kind: event
    meaning: A customer viewed a page
    properties:
    - name: checkout_step
      type: string
      meaning: Checkout step shown on the page
      optional: true
  steps:
  - id: s1
    builds: experiment
    uses:
    - checkout_created_event
    - order_placed_event
    - payment_failed_event
    - abandoned_checkout_event
    - view_page_event
    - experimentName
    - checkoutPath
    - controlTrafficPercent
    - variantTrafficPercent
    - testDuration
    - minCheckoutsPerVariant
    - orderWindow
    - declineIncreaseLimit
    - abandonIncreaseLimit
    instruction: 'Create a website experiment named "{experimentName}" on pages whose URL contains "{checkoutPath}", for all
      visitors who reach checkout, all devices with results split by desktop and mobile, shown always. Control ({controlTrafficPercent}%):
      the current one-page checkout, unchanged. Variant B ({variantTrafficPercent}%): a three-step checkout, Shipping, then
      Payment, then Review. Primary goal: {order_placed_event} within {orderWindow} of {checkout_created_event}. Secondary:
      median time from {checkout_created_event} to {order_placed_event}, and for Variant B the share of visitors leaving at
      each {view_page_event.checkout_step}. Guardrails: the {payment_failed_event} rate must not rise more than {declineIncreaseLimit}
      percentage points and the {abandoned_checkout_event} rate not more than {abandonIncreaseLimit} percentage points. Run
      {testDuration} and until each variant has {minCheckoutsPerVariant} checkouts.'
---

# Checkout flow length test

Slash command: /checkout-flow-length-test

## Step 1: Set up the checkout length test

Create a website experiment named "Checkout Flow Length" on pages whose URL contains "/checkout", for all visitors who reach checkout, all devices with results split by desktop and mobile, shown always. Control (50%): the current one-page checkout, unchanged. Variant B (50%): a three-step checkout, Shipping, then Payment, then Review. Primary goal: order placed event within 1 h of checkout created event. Secondary: median time from checkout created event to order placed event, and for Variant B the share of visitors leaving at each checkout step. Guardrails: the payment failed event rate must not rise more than 2 percentage points and the abandoned checkout event rate not more than 5 percentage points. Run 14 d and until each variant has 3000 checkouts.
