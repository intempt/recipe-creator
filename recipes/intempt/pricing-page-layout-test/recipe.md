---
frontmatter_id: pricing-page-layout-test
slash_command: /pricing-page-layout-test
description: Tests your current pricing page against side-by-side plan cards and an interactive usage slider, tracking plan
  clicks, checkouts and subscriptions to show which layout earns more.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tests your current pricing page against side-by-side plan cards and an interactive usage slider, tracking plan
    clicks, checkouts, and subscriptions to show which layout earns more.
  parameters:
  - name: experimentTitle
    type: string
    label: Experiment title
    default: Pricing Page Layout Test
    required: false
  - name: pricingPagePath
    type: string
    label: Pricing page path
    default: /pricing
    required: false
  - name: minDurationDays
    type: duration
    label: Minimum test duration
    default: 21 d
    required: false
  - name: minVisitorsPerVariant
    type: number
    label: Minimum unique visitors per variant
    default: 1000
    required: false
  - name: controlTrafficPercent
    type: number
    label: Control traffic share (%)
    default: 34
    required: false
  - name: variantBTrafficPercent
    type: number
    label: Plan cards traffic share (%)
    default: 33
    required: false
  - name: variantCTrafficPercent
    type: number
    label: Usage slider traffic share (%)
    default: 33
    required: false
  - name: checkoutWindow
    type: duration
    label: Checkout window after exposure
    default: 7 d
    required: false
  - name: subscriptionWindow
    type: duration
    label: Subscription window after exposure
    default: 14 d
    required: false
  requirements:
  - slot: plan_click_event
    kind: event
    meaning: A visitor clicked a plan selection button on the pricing page
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked plan button, e.g. plan-select-pro
      optional: false
  - slot: checkout_created_event
    kind: event
    meaning: A customer created a checkout
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: amount
      type: number
      meaning: Subscription amount
      optional: false
  steps:
  - id: s1
    builds: experiment
    uses:
    - plan_click_event
    - checkout_created_event
    - subscription_started_event
    - experimentTitle
    - pricingPagePath
    - minDurationDays
    - minVisitorsPerVariant
    - controlTrafficPercent
    - variantBTrafficPercent
    - variantCTrafficPercent
    - checkoutWindow
    - subscriptionWindow
    instruction: 'Create a client-side experiment named "{experimentTitle}" for all visitors on all devices, on pages whose
      URL starts with {pricingPagePath}, shown always. Variants: Control ({controlTrafficPercent}%) keeps the current pricing
      layout; Variant B ({variantBTrafficPercent}%) shows side-by-side plan cards with a "Recommended" badge on the middle
      plan; Variant C ({variantCTrafficPercent}%) shows an interactive usage slider that recommends a plan. Primary metric:
      sum of {subscription_started_event.amount} from {subscription_started_event} within {subscriptionWindow} of exposure.
      Secondary metrics: {plan_click_event} per {plan_click_event.target_id} starting with plan-select-; visitors who did
      {checkout_created_event} within {checkoutWindow}; visitors who did {subscription_started_event} within {subscriptionWindow}.
      Run for at least {minDurationDays} and {minVisitorsPerVariant} unique visitors per variant.'
---

# Pricing page layout test

Slash command: /pricing-page-layout-test

## Step 1: Set up the pricing layout test

Create a client-side experiment named "Pricing Page Layout Test" for all visitors on all devices, on pages whose URL starts with /pricing, shown always. Variants: Control (34%) keeps the current pricing layout; Variant B (33%) shows side-by-side plan cards with a "Recommended" badge on the middle plan; Variant C (33%) shows an interactive usage slider that recommends a plan. Primary metric: sum of amount from subscription started event within 14 d of exposure. Secondary metrics: plan click event per target id starting with plan-select-; visitors who did checkout created event within 7 d; visitors who did subscription started event within 14 d. Run for at least 21 d and 1000 unique visitors per variant.
