---
id: free-paid-conversion-funnel
title: Free to paid conversion
slash_command: /free-paid-conversion-funnel
group: Reports
owner: intempt
curator: aman
summary: Shows how many trials go on to view pricing, start checkout and pay, and which plan loses people
  at which step.
description: >-
  Trial-to-paid funnel using subscription_created (trial mode), pricing page views, and checkout_created.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  industry:
    - ai
    - b2b-saas
    - ecommerce
    - finance
    - media
  vertical:
    - subscription
  complexity: quick
  executionMode: live
  tags:
    - funnel
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Follow trials through to payment"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Follow trials through to payment
    summary: >-
      A four step funnel over 30 days from a trial subscription to a pricing page view, a started checkout
      and a paid subscription, split by the plan they trialled. Adds median and 75th percentile time per
      step and flags plans under 20% from pricing to checkout.
    builds: report
    description: |-
      Create a Funnel report called "Free to Paid Conversion".
      Steps:
      1. Event "subscription_created" where trial_end is not null AND trial_start is not null: "Started Trial"
      2. Event "page_viewed" where page_url contains "/pricing": "Viewed Pricing"
      3. Event "checkout_created": "Started Checkout"
      4. Event "subscription_created" filtered to non-trial conversions: "Subscribed Paid"
       (operationally: a follow-on subscription_created without trial fields, OR a revenue_completed/invoice_paid event after the trial_end of the original subscription)
      Conversion window: 30 days
      Breakdown: By plan_name on the trial subscription (which plan they signed up to trial)
      Compare: Previous period (prior 30 days)
      For each step, also surface:
      - Median and 75th-percentile time-to-convert from previous step
      - Per-plan conversion rate at each stage
      - For users who reached "Started Checkout" but did NOT reach "Subscribed Paid": time spent on the page_viewed events between Step 3 and timeout (price-sensitivity proxy)
      Annotations:
      - Flag the largest drop-off step (typical largest drops: pricing to checkout, or checkout to subscribed).
      - Flag any plan where pricing-to-checkout conversion is below 20% (price-objection signal).
      - Flag any plan where checkout-to-subscribed conversion is below 60% (checkout friction).
      - Highlight the plan with the highest end-to-end conversion AND volume.
      Taxonomy notes:
      - "pricing_page_viewed" and "checkout_started" as standalone events do not exist. Use page_viewed.page_url filters and checkout_created.
      - "trial_started" does not exist; the trial-start cohort is derived from subscription_created with trial fields populated.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Free to paid conversion

Shows how many trials go on to view pricing, start checkout and pay, and which plan loses people at which step.

## Steps

1. **Follow trials through to payment** (builds report)

   A four step funnel over 30 days from a trial subscription to a pricing page view, a started checkout and a paid subscription, split by the plan they trialled. Adds median and 75th percentile time per step and flags plans under 20% from pricing to checkout.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Follow trials through to payment"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
