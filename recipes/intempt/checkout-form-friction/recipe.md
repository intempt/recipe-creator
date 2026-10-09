---
description: Shows which checkout step loses you orders, how long shoppers sit on each one, and where mobile is worse than desktop.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
  - finance
---

# Checkout friction

Slash command: /checkout-form-friction

## Step 1: Find the stalling checkout step

Create a Funnel report called "Checkout Form Friction".
Steps:
1. Event "Checkout created": "Started Checkout"
2. Event "View page" where Page URL contains "/checkout/shipping" or equivalent shipping step: "Reached Shipping"
3. Event "View page" where Page URL contains "/checkout/payment" or equivalent payment step: "Reached Payment"
4. Event "View page" where Page URL contains "/checkout/review" or equivalent review step: "Reached Review"
5. Event "Checkout completed" OR "Placed order": "Completed Order"
Conversion window: 1 hour (in-session checkout completion)
Breakdown: By "device_type" attribute on the Users object (mobile checkout typically 30% lower conversion than desktop)
Compare: Previous period (prior 30 days)
For each step, also surface:
- Median and 75th-percentile time on the step page (long times suggest friction)
- Drop-off rate vs. previous period
- For users who reached but didn't pass each step: what was their last in-checkout action (helps identify the specific field/element that caused exit)
Annotations:
- Flag the step with the largest drop-off (the primary checkout bottleneck).
- Flag any step where median time-on-page exceeds 90 seconds (typically signals form complexity, validation issues, or payment-method confusion).
- Flag if mobile drop-off at any step is >15 percentage points worse than desktop (mobile-specific UX issue at that step).
- Highlight the Abandoned checkout volume in the same period: these are recoverable users; pair this report with abandoned-cart recovery.
Industry benchmarks: average ecommerce checkout completion rate is ~50%; top-quartile is 70%+. Step-level: shipping to payment typically 80%+ of the drop-off.
Use case: every ecommerce team optimizes the checkout but most see only the top-line drop-off, not the per-step diagnosis. This recipe surfaces exactly where the friction lives.
Taxonomy notes:
- Checkout created and Checkout completed are canonical (Stripe-sourced).
- Abandoned checkout (Shopify) is canonical and complementary.
- Per-step pages are derived from View page.Page URL patterns since separate canonical events for each checkout substep don't exist.
