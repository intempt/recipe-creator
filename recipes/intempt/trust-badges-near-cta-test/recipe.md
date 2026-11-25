---
frontmatter_id: trust-badges-near-cta-test
slash_command: /trust-badges-near-cta-test
description: Compares no badges, security badges, guarantee badges and all of them together beside your main call to action.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tests whether showing security, guarantee, or combined trust badges beside the main call to action lifts subscriptions
    and orders versus no badges.
  parameters:
  - name: experimentTitle
    type: string
    label: Experiment title
    default: Trust Badges Near CTA
    required: false
  - name: controlWeight
    type: number
    label: Control variant traffic share (%)
    default: 25
    required: false
  - name: variantBWeight
    type: number
    label: Security badges variant traffic share (%)
    default: 25
    required: false
  - name: variantCWeight
    type: number
    label: Guarantee badges variant traffic share (%)
    default: 25
    required: false
  - name: variantDWeight
    type: number
    label: Combined badges variant traffic share (%)
    default: 25
    required: false
  - name: experimentWindow
    type: duration
    label: Experiment run length
    default: 21 d
    required: false
  - name: attributionWindow
    type: duration
    label: Conversion attribution window after exposure
    default: 24 h
    required: false
  - name: bounceGuardrailIncrease
    type: number
    label: Maximum allowed page-bounce rate increase (%)
    default: 5
    required: false
  - name: placement
    type: enum
    label: Badge placement relative to the CTA
    default: inline_after_cta
    required: false
    options:
    - inline_after_cta
    - below_button
    - floating_near_cta
  requirements:
  - slot: goal_completed_event
    kind: event
    meaning: A customer started a subscription or placed an order on the site
    properties:
    - name: experiment_id
      type: string
      meaning: Identifier of the experiment the goal was attributed to
      optional: false
  - slot: checkout_completed_event
    kind: event
    meaning: A customer completed checkout during a session
  - slot: primary_cta_click_event
    kind: event
    meaning: A visitor clicked the primary call-to-action button on a page
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the element clicked
      optional: false
  steps:
  - id: s1
    builds: experiment
    uses:
    - attributionWindow
    - bounceGuardrailIncrease
    - checkout_completed_event
    - controlWeight
    - experimentTitle
    - experimentWindow
    - goal_completed_event
    - placement
    - primary_cta_click_event
    - variantBWeight
    - variantCWeight
    - variantDWeight
    instruction: 'Create a client-side experiment titled "{experimentTitle}" on the experiences page. Target pricing, checkout,
      key product and signup pages, all devices, all visitors, display frequency always. Variants: Control at {controlWeight}%
      with no trust badges; Variant B at {variantBWeight}% with security badges only (SSL, secure checkout, payment encryption);
      Variant C at {variantCWeight}% with guarantee badges only (30-day money-back guarantee, free returns, cancel anytime);
      Variant D at {variantDWeight}% with one row of security, guarantee and payment method badges. Place the badges {placement}
      relative to the primary call to action button, inside its block. Show only certifications, guarantees and payment methods
      the merchant really offers. Primary metric: {goal_completed_event} (subscription started or order placed) within {attributionWindow}
      of exposure. Secondary metrics: {primary_cta_click_event} click rate; {checkout_completed_event} rate. Guardrail: page
      bounce rate must not rise by more than {bounceGuardrailIncrease}%. Run for {experimentWindow}.'
---

# Trust badges near the CTA

Slash command: /trust-badges-near-cta-test

## Step 1: Set up the trust badge test

Create a client-side experiment titled "Trust Badges Near CTA" on the experiences page. Target pricing, checkout, key product and signup pages, all devices, all visitors, display frequency always. Variants: Control at 25% with no trust badges; Variant B at 25% with security badges only (SSL, secure checkout, payment encryption); Variant C at 25% with guarantee badges only (30-day money-back guarantee, free returns, cancel anytime); Variant D at 25% with one row of security, guarantee and payment method badges. Place the badges inline_after_cta relative to the primary call to action button, inside its block. Show only certifications, guarantees and payment methods the merchant really offers. Primary metric: goal completed event (subscription started or order placed) within 24 h of exposure. Secondary metrics: primary cta click event click rate; checkout completed event rate. Guardrail: page bounce rate must not rise by more than 5%. Run for 21 d.
