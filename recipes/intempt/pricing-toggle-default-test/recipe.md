---
frontmatter_id: pricing-toggle-default-test
slash_command: /pricing-toggle-default-test
description: Tests whether defaulting the pricing page billing toggle to annual instead of monthly increases revenue, counting
  annual plans at their full annual value.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Tests whether defaulting the pricing page billing toggle to annual instead of monthly increases revenue, counting
    annual plans at their full annual value.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Pricing Toggle Default
    required: false
  - name: pricing_page_url_contains
    type: string
    label: Pricing page URL contains
    default: /pricing
    required: false
  - name: test_duration
    type: duration
    label: Test duration
    default: 21 d
    required: false
  - name: min_visitors_per_variant
    type: number
    label: Minimum visitors per variant
    default: 1000
    required: false
  - name: guardrail_max_drop_pct
    type: number
    label: Max drop in subscription rate (%)
    default: 3
    required: false
  - name: revenue_window
    type: duration
    label: Revenue window after exposure
    default: 7 d
    required: false
  - name: savings_badge_copy
    type: string
    label: Savings badge on the annual option
    default: Save 20% with annual
    required: false
  requirements:
  - slot: billing_toggle_click
    kind: event
    meaning: A visitor clicked an element on the website
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked element
      optional: false
  - slot: subscription_started
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: billing_period
      type: string
      meaning: Billing period, annual or monthly
      optional: false
    - name: value
      type: number
      meaning: Subscription value for the full billing period
      optional: false
  steps:
  - id: s1
    builds: experiment
    uses:
    - billing_toggle_click
    - subscription_started
    - experiment_title
    - pricing_page_url_contains
    - test_duration
    - min_visitors_per_variant
    - guardrail_max_drop_pct
    - revenue_window
    - savings_badge_copy
    instruction: 'Create a client-side experiment named "{experiment_title}" for all visitors on all devices, on pages whose
      URL contains {pricing_page_url_contains}, shown always. Variants: Control (34%) keeps the current toggle default; Variant
      B (33%) sets the billing toggle to annual on page load, shows annual prices and the badge "{savings_badge_copy}" on
      the annual option; Variant C (33%) sets the toggle to monthly on page load. Clicks on the toggle record {billing_toggle_click}
      with target_id pricing-toggle in every variant. Primary metric: sum of {subscription_started.value} from {subscription_started}
      within {revenue_window} of exposure, annual plans at their full annual value. Secondary metrics: {subscription_started}
      rate split by {subscription_started.billing_period}; {billing_toggle_click} where {billing_toggle_click.target_id} is
      pricing-toggle. Guardrail: the {subscription_started} rate must not drop more than {guardrail_max_drop_pct}% below Control.
      Run for {test_duration} and at least {min_visitors_per_variant} visitors per variant.'
---

# Billing toggle default test

Slash command: /pricing-toggle-default-test

## Step 1: Set up the toggle default test

Create a client-side experiment named "Pricing Toggle Default" for all visitors on all devices, on pages whose URL contains /pricing, shown always. Variants: Control (34%) keeps the current toggle default; Variant B (33%) sets the billing toggle to annual on page load, shows annual prices and the badge "Save 20% with annual" on the annual option; Variant C (33%) sets the toggle to monthly on page load. Clicks on the toggle record billing toggle click with target_id pricing-toggle in every variant. Primary metric: sum of value from subscription started within 7 d of exposure, annual plans at their full annual value. Secondary metrics: subscription started rate split by billing period; billing toggle click where target id is pricing-toggle. Guardrail: the subscription started rate must not drop more than 3% below Control. Run for 21 d and at least 1000 visitors per variant.
