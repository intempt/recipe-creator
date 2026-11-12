---
frontmatter_id: pricing-toggle-default-test
slash_command: /pricing-toggle-default-test
description: Tests whether defaulting the pricing toggle to annual rather than monthly earns more, counting annual plans at full annual value.
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
    label: Maximum allowed drop in total subscription rate (%)
    default: 3
    required: false
  - name: revenue_window
    type: duration
    label: Revenue measurement window after subscription start
    default: 7 d
    required: false
  - name: savings_badge_copy
    type: string
    label: Savings badge copy for annual option
    default: Save 20% with annual
    required: false
  requirements:
  - slot: experiment_surface
    kind: integration
    meaning: A client-side experimentation tool that can run a page experiment with variants on the pricing page and a visual
      editor
    channel: email
  - slot: pricing_page
    kind: destination
    meaning: The pricing page on the website where the billing toggle appears
    channel: email
  - slot: billing_toggle_click
    kind: event
    meaning: A visitor clicked an element on the website
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked element, such as pricing-toggle
      optional: false
  - slot: subscription_started
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: billing_period
      type: enum
      meaning: 'Billing period chosen for the subscription: annual or monthly'
      optional: false
    - name: value
      type: number
      meaning: First-payment value of the subscription, with annual plans at full annual value
      optional: false
    - name: experience_id
      type: string
      meaning: Identifier of the experiment experience the visitor was exposed to
      optional: true
  - slot: pricing_toggle_element
    kind: attribute
    meaning: The monthly and annual billing toggle component on the pricing page
  steps:
  - id: s1
    builds: experiment
    uses:
    - experiment_surface
    - pricing_page
    - billing_toggle_click
    - subscription_started
    - pricing_toggle_element
    - experiment_title
    - pricing_page_url_contains
    - test_duration
    - min_visitors_per_variant
    - guardrail_max_drop_pct
    - revenue_window
    - savings_badge_copy
    instruction: 'Create a client-side experiment on {experiment_surface} titled "{experiment_title}" targeting pages whose
      URL contains "{pricing_page_url_contains}" on any device, for all visitors, shown always. Variants: Control (33%) keeps
      the existing default toggle state with no DOM changes. Variant B (33%) sets the default billing toggle to annual on
      {pricing_toggle_element} and shows the savings highlight "{savings_badge_copy}". Variant C (34%) sets the default billing
      toggle to monthly explicitly as a baseline. In Variant B, on page load set the toggle to the annual position, update
      displayed prices to annual values, and set a data attribute billing-default=annual on the body for analytics. Replace
      the {pricing_toggle_element} HTML in each variant with a toggle block containing monthly and annual buttons, with the
      annual button active in Variant B and the monthly button active in Variant C, keeping the Save 20% badge on the annual
      option. Ensure click events on the toggle buttons fire so {billing_toggle_click} with target_id pricing-toggle is recorded
      in every variant. Primary metric: revenue from {subscription_started} with value above 0 within {revenue_window} of
      the subscription start, annual plans counted at full annual value, attributed to this experience. Secondary metrics:
      {subscription_started} rate by billing_period annual and monthly per variant, toggle interaction rate from {billing_toggle_click},
      and average order value per signup. Guardrail: total {subscription_started} rate must not drop by more than {guardrail_max_drop_pct}
      percent. Run for {test_duration} with at least {min_visitors_per_variant} visitors per variant.'
---

# Billing toggle default test

Slash command: /pricing-toggle-default-test

## Step 1: Set up the toggle default test

Create a CLIENT EXPERIMENT on /experiences titled "Pricing Toggle Default".
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants:
- Control (33%): existing default state (whatever the page currently shows: most often monthly)
- Variant B (33%): default to ANNUAL billing toggle position with savings highlight ("Save 20% with annual")
- Variant C (34%): default to MONTHLY billing toggle position (most-likely current state, but explicit)
Targeting:
- Pages: page URL contains "/pricing"
- Devices: any
- Audience: all visitors
- Display frequency: always
Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from Subscription started within 7 days, weighted by billing-period: annual subscriptions count for full annual value)
Secondary metrics:
- Subscription started where billing_period = "annual" (annual conversion rate per variant)
- Subscription started where billing_period = "monthly" (monthly conversion rate per variant)
- Toggle-interaction rate (Click on where target_id = "pricing-toggle")
- AOV per signup (annual signups have ~12x higher first-payment value than monthly)
Guardrail: total Subscription started rate must not drop >3% (the test shouldn't suppress overall conversion; it should shift mix toward annual)
Schedule: 21 days, 1,000 visitors per variant minimum
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (no DOM changes)
Variant: B (annual default + savings highlight)
 HTML target selector: .pricing-toggle (the toggle UI between monthly and annual)
 Replacement HTML:
 <div class="pricing-toggle" data-variant="b" data-default="annual">
 <div class="toggle-buttons">
 <button class="toggle-option" data-period="monthly" id="pricing-toggle-monthly">Monthly</button>
 <button class="toggle-option toggle-option--active" data-period="annual" id="pricing-toggle-annual">
 Annual
 <span class="savings-badge">Save 20%</span>
 </button>
 </div>
 </div>
 Lightweight JS:
 - On page load, programmatically set the toggle to "annual" position
 - Update all displayed prices to annual values
 - Add a `data-billing-default="annual"` attribute on body for analytics
Variant: C (monthly default: explicit baseline for comparison)
 HTML target selector: .pricing-toggle
 Replacement HTML:
 <div class="pricing-toggle" data-variant="c" data-default="monthly">
 <div class="toggle-buttons">
 <button class="toggle-option toggle-option--active" data-period="monthly" id="pricing-toggle-monthly">Monthly</button>
 <button class="toggle-option" data-period="annual" id="pricing-toggle-annual">
 Annual
 <span class="savings-badge">Save 20%</span>
 </button>
 </div>
 </div>
The Visual Editor allows the user to refine the savings-badge copy, toggle styling, and animation. Ensure the toggle-button Click on events fire properly in both variants so the toggle-interaction rate metric works.
Taxonomy notes:
- Most modern SaaS pricing pages already have a monthly/annual toggle: this experiment changes the *default* state on page load.
- Subscription started.billing_period (or equivalent) must be populated to measure the annual-vs-monthly mix shift. If your subscription event doesn't track billing period, add it.
- Annual default tends to lift annual conversion rate by 30-50% with little impact on overall conversion: the savings come almost entirely from mix shift, not from new conversions.
- For trial signups (which usually start as a free trial then convert to paid), this experiment is more impactful at the trial to paid step than at the trial-signup step. Plan your downstream measurement window accordingly.
