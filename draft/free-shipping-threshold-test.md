---
description: Finds which free shipping threshold (50, 75, 99 dollars, or none) earns the most revenue per session, served as a server-side flag.
author:
  first_name: V
  last_name: Ranadheer
  job_title: Design Engineer
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
  - finance
---

# Free shipping threshold test

Slash command: /free-shipping-threshold-test

## Step 1: Set up the threshold test

Create a SERVER EXPERIMENT on /experiences titled "Free Shipping Threshold".
═══ PATH 1: Top-level configuration (Setup tab) ═══
Experience type: server_experiment (Flag Key + JSON payload, no per-variant targeting)
Flag Key: free_shipping_threshold
Variants:
- Control (25%): free shipping at $75
- Variant B (25%): free shipping at $50
- Variant C (25%): free shipping at $99
- Variant D (25%): no free shipping (flat $5.99)
Targeting:
- Pages: any page where the free-shipping threshold logic applies: typically cart, checkout, and shipping-info banners on PDPs (whatever pages call getFlag for this experiment)
- Devices: any (server experiments are device-agnostic; the cart logic runs the same regardless of client device)
- Audience: all visitors except wholesale accounts (segment exclusion: account_type = "wholesale")
- Display frequency: always (sticky assignment: every cart calculation for a given userId uses the same variant for the experiment's duration)
Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue per session: sum of Placed order.total_price attributed via exposed_to_experience)
Secondary metrics:
- Placed order.total_price (AOV per variant)
- Placed order count per session (conversion rate)
- items_count on Placed order (units per order: does free shipping inflate cart size?)
Guardrail: Abandoned cart rate must not increase >5% in lower-threshold variants (some shoppers may abandon when realizing they don't qualify)
Schedule: 21 days. Track new vs. returning visitors separately (returning visitors may have shipping expectations from prior orders).
═══ PATH 2: Variant JSON payload (loaded as code via SDK) ═══
For SERVER experiments, each variant ships a JSON payload that the application loads via getFlag() and renders accordingly. The application code reads the payload and applies the threshold dynamically.
Variant: Control (75)
 JSON payload:
 {
 "threshold_cents": 7500,
 "threshold_display": "$75",
 "fallback_shipping_cents": 599,
 "fallback_shipping_display": "$5.99",
 "messaging": "Free shipping on orders over $75!"
 }
Variant: B (50)
 {
 "threshold_cents": 5000,
 "threshold_display": "$50",
 "fallback_shipping_cents": 599,
 "fallback_shipping_display": "$5.99",
 "messaging": "Free shipping on orders over $50!"
 }
Variant: C (99)
 {
 "threshold_cents": 9900,
 "threshold_display": "$99",
 "fallback_shipping_cents": 599,
 "fallback_shipping_display": "$5.99",
 "messaging": "Free shipping on orders over $99!"
 }
Variant: D (no free shipping)
 {
 "threshold_cents": null,
 "threshold_display": null,
 "fallback_shipping_cents": 599,
 "fallback_shipping_display": "$5.99",
 "messaging": "Standard shipping: $5.99"
 }
SDK integration example (JavaScript):
 const config = await intempt.getFlag('free_shipping_threshold', userId);
 // config.threshold_cents to number or null
 // applies in cart logic, displays in shipping banner
Taxonomy notes:
- Placed order.total_price is the canonical order value. items_count derives from Placed order.items length.
- exposed_to_experience fires when getFlag() is first called for the user; goal_completed_in_experience fires when the configured goal (Placed order within session) is reached.
- Server experiments do not have a Visual Editor: there is no DOM change. The variant's effect is purely via the JSON payload's effect on application logic.
- "Display frequency: always" for server experiments means the same variant returns on every getFlag call for a given userId (sticky assignment): this is what makes the experiment statistically valid. A user assigned to Variant B sees the $50 threshold consistently across sessions.
