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
  - slot: experiment_platform
    kind: integration
    meaning: A client-side experimentation tool that can run variant tests on web pages with a visual editor
    channel: email
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
  - slot: high_intent_pages
    kind: segment
    meaning: Visitors viewing pricing, checkout, key product, or signup pages
  - slot: page_bounce_metric
    kind: attribute
    meaning: Page bounce rate measured per page for the experiment audience
    optional: true
  steps:
  - id: s1
    builds: experiment
    uses:
    - experiment_platform
    - high_intent_pages
    - goal_completed_event
    - primary_cta_click_event
    - experimentTitle
    - controlWeight
    - variantBWeight
    - variantCWeight
    - variantDWeight
    - placement
    - experimentWindow
    instruction: 'Create a client-side experiment titled "{experimentTitle}" on the experiences page. Target high-intent pages
      (pricing, checkout, key product pages, signup pages) for all devices and all visitors, with display frequency set to
      always. Define four variants: Control at {controlWeight}% with no trust badges (existing state); Variant B at {variantBWeight}%
      showing security badges only (SSL, Secure Checkout, payment encryption icons); Variant C at {variantCWeight}% showing
      guarantee badges only (30-day money-back guarantee, Free returns, Cancel anytime); Variant D at {variantDWeight}% showing
      a combined row of security, guarantee, and payment method badges (Visa, Mastercard, AmEx, Apple Pay). Place the badges
      {placement} relative to the primary CTA button, inside the primary CTA block. Only display badges for certifications,
      guarantees, and payment methods the merchant actually offers. Run for {experimentWindow}.'
---

# Trust badges near the CTA

Slash command: /trust-badges-near-cta-test

## Step 1: Set up the trust badge test

Create a CLIENT EXPERIMENT on /experiences titled "Trust Badges Near CTA".
═══ PATH 1: Top-level configuration ═══
Experience type: client_experiment
Variants:
- Control (25%): no trust badges near the primary CTA (existing state for many pages)
- Variant B (25%): security badges only: SSL, "Secure Checkout", payment encryption icons
- Variant C (25%): guarantee badges only: "30-day money-back guarantee", "Free returns", "Cancel anytime"
- Variant D (25%): combined: small row showing security + guarantee + payment methods (Visa/MC/AmEx/Apple Pay icons)
Targeting:
- Pages: high-intent pages: /pricing, /checkout, key product pages, signup pages
- Devices: any
- Audience: all visitors
- Display frequency: always
Primary metric: goal_completed_in_experience where experience_id = <this> (goal: Subscription started OR Placed order within 24 hours of exposure)
Secondary metrics:
- Click on on the primary CTA (target_id matches the page's primary CTA)
- Checkout completed within session
- Subscription started or Placed order within 24 hours
Guardrail: page-bounce rate must not increase >5% (badges shouldn't add visual clutter that drives users off the page)
Schedule: 21 days
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (no DOM changes: no trust badges)
Variant: B (security badges)
 HTML target selector: .primary-cta-block (insert after the CTA button)
 Variant DOM:
 <div class="trust-badges trust-badges--security" data-variant="b" data-badges="security">
 <span class="trust-item"><svg>...</svg> SSL Secure</span>
 <span class="trust-item"><svg>...</svg> 256-bit encryption</span>
 <span class="trust-item"><svg>...</svg> PCI compliant</span>
 </div>
Variant: C (guarantee badges)
 HTML target selector: .primary-cta-block (insert after the CTA button)
 Variant DOM:
 <div class="trust-badges trust-badges--guarantee" data-variant="c" data-badges="guarantee">
 <span class="trust-item"><svg>...</svg> 30-day money-back</span>
 <span class="trust-item"><svg>...</svg> Cancel anytime</span>
 <span class="trust-item"><svg>...</svg> Free returns</span>
 </div>
Variant: D (combined)
 HTML target selector: .primary-cta-block (insert after the CTA button)
 Variant DOM:
 <div class="trust-badges trust-badges--combined" data-variant="d" data-badges="combined">
 <div class="trust-row trust-row--security">
 <span class="trust-item">🔒 Secure Checkout</span>
 <span class="trust-item">30-day guarantee</span>
 </div>
 <div class="trust-row trust-row--payment">
 <img src="/badges/visa.svg" alt="Visa" />
 <img src="/badges/mastercard.svg" alt="Mastercard" />
 <img src="/badges/amex.svg" alt="AmEx" />
 <img src="/badges/apple-pay.svg" alt="Apple Pay" />
 </div>
 </div>
The Visual Editor allows the user to swap badges, adjust placement (inline-after-CTA vs. below-button vs. floating-near-CTA), and refine typography. Badges should look authentic: only display certifications the merchant actually has.
Taxonomy notes:
- Only display trust badges that reflect real certifications, guarantees, or payment methods the merchant actually offers. Fake or aspirational badges erode trust.
- For SaaS pages, "guarantee" framing tends to outperform "security" framing; for ecommerce checkout, both matter.
- Build Grow Scale's 2026 data: badges placed directly below or beside the Add to Cart button increase purchase confidence by 42%.
