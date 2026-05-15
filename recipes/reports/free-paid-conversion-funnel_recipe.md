---
name: free-paid-conversion-funnel
description: |
  Use when a user mentions "free → paid conversion funnel", or asks for related help. Trial-to-paid funnel using subscription_created (trial mode), pricing page views, and checkout_created.
arguments: []
intempt:
  id: free-paid-conversion-funnel
  version: 1.0.0
  slashCommand: /free-paid-conversion-funnel
  group: Reports
  shortDescription: "Trial-to-paid funnel using subscription_created (trial mode), pricing page views, and checkout_created."
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
      title: "Build Funnel Report"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Funnel report called "Free to Paid Conversion".

        Steps:
        1. Event "subscription_created" where trial_end is not null AND trial_start is not null — "Started Trial"
        2. Event "page_viewed" where page_url contains "/pricing" — "Viewed Pricing"
        3. Event "checkout_created" — "Started Checkout"
        4. Event "subscription_created" filtered to non-trial conversions — "Subscribed Paid"
           (operationally: a follow-on subscription_created without trial fields, OR a revenue_completed/invoice_paid event after the trial_end of the original subscription)

        Conversion window: 30 days
        Breakdown: By plan_name on the trial subscription (which plan they signed up to trial)
        Compare: Previous period (prior 30 days)

        For each step, also surface:
        - Median and 75th-percentile time-to-convert from previous step
        - Per-plan conversion rate at each stage
        - For users who reached "Started Checkout" but did NOT reach "Subscribed Paid": time spent on the page_viewed events between Step 3 and timeout (price-sensitivity proxy)

        Annotations:
        - Flag the largest drop-off step (typical largest drops: pricing → checkout, or checkout → subscribed).
        - Flag any plan where pricing-to-checkout conversion is below 20% (price-objection signal).
        - Flag any plan where checkout-to-subscribed conversion is below 60% (checkout friction).
        - Highlight the plan with the highest end-to-end conversion AND volume.

        Taxonomy notes:
        - "pricing_page_viewed" and "checkout_started" as standalone events do not exist. Use page_viewed.page_url filters and checkout_created.
        - "trial_started" does not exist; the trial-start cohort is derived from subscription_created with trial fields populated.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Free → Paid Conversion Funnel

## Procedure

1. **Build Funnel Report** [`build_funnel_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Funnel report called "Free to Paid Conversion".

   Steps:
   1. Event "subscription_created" where trial_end is not null AND trial_start is not null — "Started Trial"
   2. Event "page_viewed" where page_url contains "/pricing" — "Viewed Pricing"
   3. Event "checkout_created" — "Started Checkout"
   4. Event "subscription_created" filtered to non-trial conversions — "Subscribed Paid"
      (operationally: a follow-on subscription_created without trial fields, OR a revenue_completed/invoice_paid event after the trial_end of the original subscription)

   Conversion window: 30 days
   Breakdown: By plan_name on the trial subscription (which plan they signed up to trial)
   Compare: Previous period (prior 30 days)

   For each step, also surface:
   - Median and 75th-percentile time-to-convert from previous step
   - Per-plan conversion rate at each stage
   - For users who reached "Started Checkout" but did NOT reach "Subscribed Paid": time spent on the page_viewed events between Step 3 and timeout (price-sensitivity proxy)

   Annotations:
   - Flag the largest drop-off step (typical largest drops: pricing → checkout, or checkout → subscribed).
   - Flag any plan where pricing-to-checkout conversion is below 20% (price-objection signal).
   - Flag any plan where checkout-to-subscribed conversion is below 60% (checkout friction).
   - Highlight the plan with the highest end-to-end conversion AND volume.

   Taxonomy notes:
   - "pricing_page_viewed" and "checkout_started" as standalone events do not exist. Use page_viewed.page_url filters and checkout_created.
   - "trial_started" does not exist; the trial-start cohort is derived from subscription_created with trial fields populated.
   ```
