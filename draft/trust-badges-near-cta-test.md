---
description: Compares no badges, security badges, guarantee badges and all of them together beside your main call to action.
author:
  first_name: V
  last_name: Ranadheer
  job_title: Design Engineer
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - finance
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
Primary metric: goal_completed_in_experience where experience_id = <this> (goal: subscription_created OR order_created within 24 hours of exposure)
Secondary metrics:
- click_on on the primary CTA (target_id matches the page's primary CTA)
- checkout_completed within session
- subscription_created or order_created within 24 hours
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
