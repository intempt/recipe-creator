---
frontmatter_id: pricing-page-layout-test
slash_command: /pricing-page-layout-test
description: Compares your current pricing layout against side-by-side cards with a recommended plan and an interactive usage slider.
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
    label: Pricing page URL path
    default: /pricing
    required: false
  - name: minDurationDays
    type: duration
    label: Minimum run length
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
    label: Variant B traffic share (%)
    default: 33
    required: false
  - name: variantCTrafficPercent
    type: number
    label: Variant C traffic share (%)
    default: 33
    required: false
  - name: revenueWindow
    type: duration
    label: Revenue attribution window after exposure
    default: 7 d
    required: false
  - name: checkoutWindow
    type: duration
    label: Checkout attribution window after exposure
    default: 7 d
    required: false
  - name: subscriptionWindow
    type: duration
    label: Subscription attribution window
    default: 14 d
    required: false
  - name: bounceRateGuardrailPercent
    type: number
    label: Maximum allowed bounce rate increase (%)
    default: 5
    required: false
  requirements:
  - slot: pricing_experiment_event
    kind: event
    meaning: A visitor was exposed to a page experience variant
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experience the visitor was shown
      optional: false
    - name: value
      type: number
      meaning: Revenue value recorded when a downstream subscription started
      optional: true
    - name: target_id
      type: string
      meaning: Identifier of the element clicked, such as a plan select button
      optional: true
  - slot: plan_click_event
    kind: event
    meaning: A visitor clicked a plan selection button on the pricing page
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked plan button, starting with plan-select-
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
      meaning: Subscription amount captured at start
      optional: false
  - slot: goal_completed_event
    kind: event
    meaning: A visitor completed a goal inside an experience, with value set when a subscription started
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experience the goal belongs to
      optional: false
    - name: value
      type: number
      meaning: Revenue value attributed to the goal
      optional: false
  - slot: pricing_page_bounce_metric
    kind: attribute
    meaning: Bounce rate of visitors on the pricing page
  - slot: pricing_page_visitors
    kind: segment
    meaning: Visitors who viewed the pricing page
  steps:
  - id: s1
    builds: experiment
    instruction: 'Create a client experiment titled "{experimentTitle}" on the experiences page. Targeting: page URL equals
      "{pricingPagePath}" (or "{pricingPagePath}/*" for nested routes); devices any; audience all visitors; display frequency
      always. Variants: Control at {controlTrafficPercent}% showing the existing pricing layout with no DOM changes; Variant
      B at {variantBTrafficPercent}% showing side-by-side plan cards with a "Recommended" badge on the middle plan; Variant
      C at {variantCTrafficPercent}% showing an interactive usage slider with dynamic plan recommendation. Primary metric:
      goal_completed in this experience where experience_id equals this experiment and value is greater than 0 (revenue from
      subscription started within {revenueWindow} of exposure), using {goal_completed_event}. Secondary metrics: click where
      target_id starts with "plan-select-" (per-plan click-through) using {plan_click_event}; checkout created within {checkoutWindow}
      of exposure using {checkout_created_event}; subscription started within {subscriptionWindow} using {subscription_started_event}.
      Guardrail: bounce rate on the pricing page must not increase by more than {bounceRateGuardrailPercent}% using {pricing_page_bounce_metric}.
      Schedule: run for at least {minDurationDays} and require at least {minVisitorsPerVariant} unique visitors per variant
      from {pricing_page_visitors}.'
---

# Pricing page layout test

Slash command: /pricing-page-layout-test

## Step 1: Set up the pricing layout test

Create a CLIENT EXPERIMENT on /experiences titled "Pricing Page Layout Test".
═══ PATH 1: Top-level configuration (Setup tab) ═══
Experience type: client_experiment
Variants:
- Control (34%): existing pricing layout
- Variant B (33%): side-by-side cards with "Recommended" badge on the middle plan
- Variant C (33%): interactive usage slider with dynamic plan recommendation
Targeting:
- Pages: page URL equals "/pricing" (or "/pricing/*" for nested routes)
- Devices: any
- Audience: all visitors
- Display frequency: always
Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from Subscription started within 7 days of exposure)
Secondary metrics:
- Click on where target_id starts with "plan-select-" (per-plan click-through)
- Checkout created within 7 days of exposed_to_experience
- Subscription started within 14 days
Guardrail: bounce rate on /pricing must not increase >5%
Schedule: 21 days minimum, require 1,000 unique visitors per variant
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control
 No DOM changes: measures the existing pricing page.
Variant: B (side-by-side cards)
 HTML target selector: .pricing-section (or whatever wraps the existing plan grid)
 Replacement HTML:
 <section class="pricing-cards-grid">
 <article class="plan-card" data-plan="starter">
 <h3>Starter</h3>
 <div class="plan-price">$X/mo</div>
 <ul class="plan-features"><!-- features --></ul>
 <button class="plan-select" id="plan-select-starter" data-variant="b">Choose Starter</button>
 </article>
 <article class="plan-card plan-card--recommended" data-plan="pro">
 <span class="recommended-badge">Recommended</span>
 <h3>Pro</h3>
 <div class="plan-price">$Y/mo</div>
 <ul class="plan-features"><!-- features --></ul>
 <button class="plan-select" id="plan-select-pro" data-variant="b">Choose Pro</button>
 </article>
 <article class="plan-card" data-plan="enterprise">
 <h3>Enterprise</h3>
 <div class="plan-price">Contact us</div>
 <ul class="plan-features"><!-- features --></ul>
 <button class="plan-select" id="plan-select-enterprise" data-variant="b">Contact Sales</button>
 </article>
 </section>
Variant: C (interactive slider)
 HTML target selector: .pricing-section
 Replacement HTML:
 <section class="pricing-slider-layout">
 <div class="usage-slider">
 <label for="usage-input">How many users do you have?</label>
 <input type="range" id="usage-input" min="1" max="500" value="10" />
 <output class="usage-value">10 users</output>
 </div>
 <div class="dynamic-plan-display">
 <h3 class="recommended-plan-name">Pro</h3>
 <div class="dynamic-price">$Y/mo</div>
 <button class="plan-select" id="plan-select-dynamic" data-variant="c">Get Started</button>
 </div>
 <!-- include lightweight JS to update the displayed plan as the slider moves -->
 </section>
The Visual Editor renders the variant HTML with the user's existing site styles applied; the user refines copy, color, and spacing in the canvas before publishing.
Taxonomy notes:
- All Click on target_id values starting with "plan-select-" are tracked uniformly so per-plan click rates can be compared across variants.
- value on goal_completed_in_experience is set by the platform when the downstream Subscription started.amount is captured.
