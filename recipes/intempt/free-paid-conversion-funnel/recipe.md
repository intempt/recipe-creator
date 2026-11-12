---
frontmatter_id: free-paid-conversion-funnel
slash_command: /free-paid-conversion-funnel
description: Shows how many trials go on to view pricing, start checkout and pay, and which plan loses people at which step.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows how many trial users go on to view pricing, start checkout, and pay, by plan, and flags the plan and step
    where people drop off most.
  parameters:
  - name: conversionWindow
    type: duration
    label: Conversion window
    default: 30 d
    required: false
  - name: comparisonPeriod
    type: duration
    label: Comparison period (previous period)
    default: 30 d
    required: false
  - name: pricingToCheckoutThreshold
    type: number
    label: 'Price-objection flag: pricing-to-checkout conversion below (%)'
    default: 20
    required: false
  - name: checkoutToSubscribedThreshold
    type: number
    label: 'Checkout friction flag: checkout-to-subscribed conversion below (%)'
    default: 60
    required: false
  - name: pricingPageUrlFilter
    type: string
    label: Pricing page URL contains
    default: /pricing
    required: false
  requirements:
  - slot: trial_subscription_event
    kind: event
    meaning: A customer started a subscription, including trial start and trial end dates
    properties:
    - name: trial_start
      type: date
      meaning: Date the trial began
      optional: false
    - name: trial_end
      type: date
      meaning: Date the trial ends
      optional: false
    - name: plan
      type: string
      meaning: Plan the customer signed up to trial
      optional: false
  - slot: page_view_event
    kind: event
    meaning: A customer viewed a web page
    properties:
    - name: page_url
      type: string
      meaning: URL of the page viewed
      optional: false
  - slot: checkout_created_event
    kind: event
    meaning: A customer created a checkout session
  - slot: paid_conversion_event
    kind: event
    meaning: A customer converted from trial to a paid subscription or paid invoice
    properties:
    - name: trial_end
      type: date
      meaning: Trial end date of the original subscription
      optional: true
  steps:
  - id: s1
    builds: report
    instruction: 'Create a Funnel report called "Free to Paid Conversion" with these steps in order: 1) {trial_subscription_event}
      where trial_start and trial_end are both not null, labeled "Started Trial"; 2) {page_view_event} where page_url contains
      {pricingPageUrlFilter}, labeled "Viewed Pricing"; 3) {checkout_created_event}, labeled "Started Checkout"; 4) a follow-on
      {trial_subscription_event} without trial fields, or a Revenue completed or Invoice paid event after the trial_end of
      the original subscription, labeled "Subscribed Paid". Set the conversion window to {conversionWindow}. Break down by
      plan on the trial subscription (the plan they signed up to trial). Compare against the previous {comparisonPeriod}.'
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
