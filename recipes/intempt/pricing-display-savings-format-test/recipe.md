---
frontmatter_id: pricing-display-savings-format-test
slash_command: /pricing-display-savings-format-test
description: Tests three ways of showing a discount (dollar amount, percentage, struck-through compare-at price) against the
  current savings display, scored on revenue from subscriptions and orders.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Tests three ways of showing a discount (dollar amount, percentage, struck-through compare-at price) against the
    current savings display, scored on revenue from subscriptions and orders.
  parameters:
  - name: experimentTitle
    type: string
    label: Experiment title
    default: Pricing Display Savings Format
    required: false
  - name: testDurationDays
    type: duration
    label: Test duration
    default: 21 d
    required: false
  - name: minUniqueVisitorsPerVariant
    type: number
    label: Minimum unique visitors per variant
    default: 1000
    required: false
  - name: trafficPerVariantPercent
    type: number
    label: Traffic share per variant (%)
    default: 25
    required: false
  - name: attributionWindow
    type: duration
    label: Revenue window after exposure
    default: 7 d
    required: false
  - name: dollarSavingsAmount
    type: string
    label: Dollar savings shown in Variant B
    default: $24
    required: false
  - name: percentOffValue
    type: string
    label: Percent off shown in Variant C
    default: 20%
    required: false
  - name: compareAtPrice
    type: string
    label: Struck-through compare-at price in Variant D
    default: $120
    required: false
  - name: currentPrice
    type: string
    label: Current price in Variant D
    default: $96
    required: false
  requirements:
  - slot: plan_select_click
    kind: event
    meaning: A visitor clicked a plan selection or add-to-cart button
  - slot: subscription_started
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: amount
      type: number
      meaning: Subscription amount
      optional: false
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total
      optional: false
  - slot: checkout_created
    kind: event
    meaning: A customer created a checkout
  steps:
  - id: s1
    builds: experiment
    uses:
    - plan_select_click
    - subscription_started
    - order_placed
    - checkout_created
    - experimentTitle
    - testDurationDays
    - minUniqueVisitorsPerVariant
    - trafficPerVariantPercent
    - attributionWindow
    - dollarSavingsAmount
    - percentOffValue
    - compareAtPrice
    - currentPrice
    instruction: 'Create a client-side experiment named "{experimentTitle}" for all visitors on all devices, on pages whose
      URL contains /pricing or /products/, shown always. Four variants at {trafficPerVariantPercent}% each: Control keeps
      the current savings display; Variant B shows "Save {dollarSavingsAmount}"; Variant C shows "{percentOffValue} off";
      Variant D shows {compareAtPrice} struck through next to {currentPrice}. Primary metric: revenue per visitor, the sum
      of {subscription_started.amount} and {order_placed.total_price} within {attributionWindow} of exposure. Secondary metrics:
      visitors who did {plan_select_click}; visitors who did {checkout_created} within {attributionWindow}; average {order_placed.total_price}.
      Run for {testDurationDays} and at least {minUniqueVisitorsPerVariant} unique visitors per variant.'
---

# Savings format test

Slash command: /pricing-display-savings-format-test

## Step 1: Set up the savings format test

Create a client-side experiment named "Pricing Display Savings Format" for all visitors on all devices, on pages whose URL contains /pricing or /products/, shown always. Four variants at 25% each: Control keeps the current savings display; Variant B shows "Save $24"; Variant C shows "20% off"; Variant D shows $120 struck through next to $96. Primary metric: revenue per visitor, the sum of amount and total price within 7 d of exposure. Secondary metrics: visitors who did plan select click; visitors who did checkout created within 7 d; average total price. Run for 21 d and at least 1000 unique visitors per variant.
