---
name: free-paid-conversion-funnel
description: |
  Use when a user mentions "free to paid conversion funnel", or asks for related help. Trial-to-paid funnel using subscription_created (trial mode), pricing page views, and checkout_created.
arguments: []
intempt:
  id: free-paid-conversion-funnel
  version: 1.0.0
  slashCommand: /free-paid-conversion-funnel
  group: Reports
  title: "Free to paid conversion"
  shortDescription: "Shows how many trials go on to view pricing, start checkout and pay, and which plan loses people at which step."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [funnel]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_funnel_report
  procedure:
    - step: 1
      title: "Follow trials through to payment"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "A four step funnel over 30 days from a trial subscription to a pricing page view, a started checkout and a paid subscription, split by the plan they trialled. Adds median and 75th percentile time per step and flags plans under 20% from pricing to checkout."
      prompt: |
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
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Free to paid conversion

Shows how many trials go on to view pricing, start checkout and pay, and which plan loses people at which step.

## What it does

1. **Follow trials through to payment** (`build_funnel_report`)

   A four step funnel over 30 days from a trial subscription to a pricing page view, a started checkout and a paid subscription, split by the plan they trialled. Adds median and 75th percentile time per step and flags plans under 20% from pricing to checkout.

## What you end up with

- **report** (report): Report produced by this recipe.
