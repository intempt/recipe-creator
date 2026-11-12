---
frontmatter_id: pricing-display-savings-format-test
slash_command: /pricing-display-savings-format-test
description: Compares showing a discount as a dollar amount, as a percentage, or as a struck-through compare-at price, scored on revenue.
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
    label: Traffic per variant (%)
    default: 25
    required: false
  - name: attributionWindow
    type: duration
    label: Conversion attribution window
    default: 7 d
    required: false
  - name: bounceRateIncreaseLimitPercent
    type: number
    label: Maximum allowed bounce rate increase (%)
    default: 5
    required: false
  - name: dollarSavingsAmount
    type: string
    label: Dollar savings shown in Variant B
    default: $24
    required: false
  - name: percentOffValue
    type: string
    label: Percentage off shown in Variant C
    default: 20%
    required: false
  - name: compareAtPrice
    type: string
    label: Struck-through compare-at price in Variant D
    default: $120
    required: false
  - name: currentPrice
    type: string
    label: Current price shown in Variant D
    default: $96
    required: false
  requirements:
  - slot: pricing_page
    kind: event
    meaning: A visitor viewed a pricing page or a product detail page where discounts are shown
  - slot: plan_select_click
    kind: event
    meaning: A visitor clicked a plan selection or add-to-cart button
    properties:
    - name: target_id
      type: text
      meaning: Identifier of the clicked element, starting with plan-select- or add-to-cart-button
      optional: false
  - slot: subscription_started
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: amount
      type: number
      meaning: Subscription amount in dollars
      optional: false
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total price in dollars
      optional: false
  - slot: checkout_created
    kind: event
    meaning: A customer created a checkout
  - slot: experiment_exposure
    kind: event
    meaning: A visitor was exposed to a variant of an experience, with the variant name recorded
    properties:
    - name: experience_id
      type: text
      meaning: Identifier of the experience the visitor saw
      optional: false
    - name: variant
      type: text
      meaning: Name of the variant the visitor saw
      optional: false
  - slot: page_bounce_rate
    kind: attribute
    meaning: Bounce rate of the pricing page per variant
  - slot: experiment_platform
    kind: integration
    meaning: The client-side experimentation platform used to run variant tests and visual editor changes
    channel: email
  steps:
  - id: s1
    builds: experiment
    instruction: 'Create a client experiment titled "{experimentTitle}" on the experiences surface. Type: client experiment.
      Variants: Control at {trafficPerVariantPercent}% traffic showing the existing savings display unchanged; Variant B at
      {trafficPerVariantPercent}% traffic showing dollar-amount framing with the headline "Save {dollarSavingsAmount}"; Variant
      C at {trafficPerVariantPercent}% traffic showing percentage framing with the headline "{percentOffValue} off"; Variant
      D at {trafficPerVariantPercent}% traffic showing compare-at framing with "{compareAtPrice}" struck through and "{currentPrice}"
      displayed prominently. Targeting: pages whose URL contains "/pricing" or product detail pages where discounts are shown;
      all devices; all visitors; display always. Primary metric: revenue per variant, counted as goal completions in the experience
      with value above zero, from a subscription started or an order placed within {attributionWindow} of exposure. Secondary
      metrics: click-through on plan selection or add-to-cart buttons per variant; checkouts created within {attributionWindow};
      average order value of orders attributed to each variant. Guardrail: bounce rate on the page must not increase by more
      than {bounceRateIncreaseLimitPercent}%. Schedule: run for {testDurationDays} and require at least {minUniqueVisitorsPerVariant}
      unique visitors per variant.'
---

# Savings format test

Slash command: /pricing-display-savings-format-test

## Step 1: Set up the savings format test

Create a CLIENT EXPERIMENT on /experiences titled "Pricing Display Savings Format".
═══ PATH 1: Top-level configuration (Setup tab) ═══
Experience type: client_experiment
Variants:
- Control (25% traffic): existing savings display (whatever the current page shows)
- Variant B (25%): dollar-amount framing: "Save $24" with the discount value as the headline
- Variant C (25%): percentage framing: "20% off" with the percentage as the headline
- Variant D (25%): compare-at framing: "$120" struck through with "$96" displayed prominently
Targeting (experience-wide):
- Pages: page URL contains "/pricing" OR product detail pages where discounts are shown
- Devices: any
- Audience: all visitors
- Display frequency: always
Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from Subscription started OR Placed order within 7 days of exposure)
Secondary metrics:
- Click on where target_id starts with "plan-select-" or "add-to-cart-button" (CTA click-through per variant)
- Checkout created within 7 days
- AOV: average value of orders attributed to the variant
Guardrail: bounce rate on the page must not increase >5%
Schedule: 21 days, require 1,000 unique visitors per variant minimum
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (no DOM changes)
Variant: B (dollar-amount framing)
 HTML target selector: .pricing-savings-display (or whatever wraps the existing savings text)
 Replacement HTML:
 <div class="savings-display" data-variant="b" data-format="dollar-amount">
 <span class="savings-headline">Save $24</span>
 <span class="savings-context">on annual billing</span>
 </div>
Variant: C (percentage framing)
 HTML target selector: .pricing-savings-display
 Replacement HTML:
 <div class="savings-display" data-variant="c" data-format="percentage">
 <span class="savings-headline">20% off</span>
 <span class="savings-context">with annual billing</span>
 </div>
Variant: D (compare-at framing)
 HTML target selector: .pricing-savings-display
 Replacement HTML:
 <div class="savings-display" data-variant="d" data-format="compare-at">
 <span class="original-price"><s>$120</s></span>
 <span class="current-price">$96</span>
 <span class="savings-context">/year</span>
 </div>
The Visual Editor allows the user to refine typography, color (red vs. green for savings), and exact dollar/percentage values to match their actual pricing.
Taxonomy notes:
- The actual savings amounts ($24, 20%, $120 to $96) must reflect the merchant's real pricing: these are placeholders that the user adjusts in the Visual Editor.
- For ecommerce, the goal fires on Placed order.total_price; for saas, on Subscription started.amount.
- Compare-at pricing requires the merchant's actual original price to be available; if pricing varies dynamically, the recipe assumes a stable comparison baseline.
