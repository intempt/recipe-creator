---
frontmatter_id: free-paid-conversion-funnel
slash_command: /free-paid-conversion-funnel
description: Builds a segment of trial users who viewed pricing but never started checkout, and emails a weekly digest of
  trial to pricing to checkout to paid conversion by plan.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Builds the trial users who viewed pricing segment and emails a weekly digest of how trial users move to pricing,
    checkout and payment, by plan, with drop-off flags.
  parameters:
  - name: conversionWindow
    type: duration
    label: Conversion window
    default: 30 d
    required: false
  - name: comparisonPeriod
    type: duration
    label: Window analyzed and compared with the one before
    default: 30 d
    required: false
  - name: pricingToCheckoutThreshold
    type: number
    label: Pricing to checkout rate below which it is flagged (%)
    default: 20
    required: false
  - name: checkoutToSubscribedThreshold
    type: number
    label: Checkout to paid rate below which it is flagged (%)
    default: 60
    required: false
  - name: pricingPageUrlFilter
    type: string
    label: Text in the pricing page URL
    default: /pricing
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
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
    meaning: A customer converted from trial to a paid subscription or paid an invoice
  steps:
  - id: s1
    builds: segment
    uses:
    - trial_subscription_event
    - page_view_event
    - checkout_created_event
    - paid_conversion_event
    - pricingPageUrlFilter
    - conversionWindow
    instruction: 'Build a new segment of users named "Trial Users Who Viewed Pricing": users whose latest {trial_subscription_event}
      has {trial_subscription_event.trial_end} in the future, who have not done {paid_conversion_event}, who did {page_view_event}
      with {page_view_event.page_url} containing {pricingPageUrlFilter} in the last {conversionWindow}, and who did not do
      {checkout_created_event} in the last {conversionWindow}.'
  - id: s2
    builds: automation
    uses:
    - s1
    - trial_subscription_event
    - page_view_event
    - checkout_created_event
    - paid_conversion_event
    - conversionWindow
    - comparisonPeriod
    - pricingToCheckoutThreshold
    - checkoutToSubscribedThreshold
    - pricingPageUrlFilter
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {trial_subscription_event}
      with {trial_subscription_event.trial_start} set in the last {comparisonPeriod} and writes these figures: how many then
      did {page_view_event} with {page_view_event.page_url} containing {pricingPageUrlFilter}, then {checkout_created_event},
      then {paid_conversion_event}, each within {conversionWindow}, with the conversion rate of each step, next to the {comparisonPeriod}
      before; the same rates split by {trial_subscription_event.plan}; the plan and step with the largest drop-off; the number
      of users in the segment from "Find trial users stuck at pricing". When pricing to checkout is below {pricingToCheckoutThreshold}%
      or checkout to paid is below {checkoutToSubscribedThreshold}%, the email''s first line says so. Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Free to paid conversion

Slash command: /free-paid-conversion-funnel

## Step 1: Find trial users stuck at pricing

Build a new segment of users named "Trial Users Who Viewed Pricing": users whose latest trial subscription event has trial end in the future, who have not done paid conversion event, who did page view event with page url containing /pricing in the last 30 d, and who did not do checkout created event in the last 30 d.

## Step 2: Email the weekly free-to-paid digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did trial subscription event with trial start set in the last 30 d and writes these figures: how many then did page view event with page url containing /pricing, then checkout created event, then paid conversion event, each within 30 d, with the conversion rate of each step, next to the 30 d before; the same rates split by plan; the plan and step with the largest drop-off; the number of users in the segment from "Find trial users stuck at pricing". When pricing to checkout is below 20% or checkout to paid is below 60%, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
