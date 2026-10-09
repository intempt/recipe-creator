---
description: Shows how many trials go on to view pricing, start checkout and pay, and which plan loses people at which step.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - finance
  - media
---

# Free to paid conversion

Slash command: /free-paid-conversion-funnel

## Step 1: Follow trials through to payment

Create a Funnel report called "Free to Paid Conversion".
Steps:
1. Event "Subscription started" where trial_end is not null AND trial_start is not null: "Started Trial"
2. Event "View page" where Page URL contains "/pricing": "Viewed Pricing"
3. Event "Checkout created": "Started Checkout"
4. Event "Subscription started" filtered to non-trial conversions: "Subscribed Paid"
 (operationally: a follow-on Subscription started without trial fields, OR a Revenue completed/Invoice paid event after the trial_end of the original subscription)
Conversion window: 30 days
Breakdown: By Plan on the trial subscription (which plan they signed up to trial)
Compare: Previous period (prior 30 days)
For each step, also surface:
- Median and 75th-percentile time-to-convert from previous step
- Per-plan conversion rate at each stage
- For users who reached "Started Checkout" but did NOT reach "Subscribed Paid": time spent on the View page events between Step 3 and timeout (price-sensitivity proxy)
Annotations:
- Flag the largest drop-off step (typical largest drops: pricing to checkout, or checkout to subscribed).
- Flag any plan where pricing-to-checkout conversion is below 20% (price-objection signal).
- Flag any plan where checkout-to-subscribed conversion is below 60% (checkout friction).
- Highlight the plan with the highest end-to-end conversion AND volume.
Taxonomy notes:
- "pricing_page_viewed" and "checkout_started" as standalone events do not exist. Use View page.Page URL filters and Checkout created.
- "trial_started" does not exist; the trial-start cohort is derived from Subscription started with trial fields populated.
