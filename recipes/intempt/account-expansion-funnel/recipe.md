---
frontmatter_id: account-expansion-funnel
slash_command: /account-expansion-funnel
description: Tracks subscription amount increases as a signal of account expansion. Uses subscription state changes and amount deltas to identify potential upgrades.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows where accounts drop off on the path from viewing pricing to upgrading a subscription, broken down by starting
    plan, with bottleneck and slow-step flags.
  parameters:
  - name: conversionWindow
    type: duration
    label: Conversion window
    default: 30 d
    required: false
  - name: comparisonWindow
    type: duration
    label: Comparison period
    default: 30 d
    required: false
  - name: slowStepThreshold
    type: duration
    label: Slow step threshold (median time-to-convert)
    default: 7 d
    required: false
  - name: pricingPageUrlContains
    type: string
    label: Pricing page URL contains
    default: /pricing
    required: false
  - name: upgradeCtaPattern
    type: string
    label: Upgrade CTA target_id pattern
    default: upgrade
    required: false
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A customer viewed a web page
    properties:
    - name: page_url
      type: string
      meaning: URL of the page viewed
      optional: false
  - slot: click_event
    kind: event
    meaning: A customer clicked an element on the page
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked element
      optional: false
  - slot: checkout_created_event
    kind: event
    meaning: A customer created a checkout session
  - slot: subscription_updated_event
    kind: event
    meaning: A customer's subscription was updated
    properties:
    - name: plan_items
      type: text
      meaning: Plan line items after the update, used to compare tier and amount
      optional: false
  - slot: subscription_started_plan_attribute
    kind: attribute
    meaning: The plan a customer's subscription started on
  steps:
  - id: s1
    builds: report
    uses:
    - page_view_event
    - click_event
    - checkout_created_event
    - subscription_updated_event
    - subscription_started_plan_attribute
    - conversionWindow
    - comparisonWindow
    - pricingPageUrlContains
    - upgradeCtaPattern
    - slowStepThreshold
    instruction: 'Create a funnel report named "Account Expansion Funnel" with these steps in order: (1) {page_view_event}
      where {page_view_event.page_url} contains {pricingPageUrlContains}, labeled "Viewed Pricing"; (2) {click_event} where
      {click_event.target_id} matches the upgrade CTA pattern {upgradeCtaPattern} (for example contains "upgrade" or "checkout"),
      labeled "Clicked Upgrade"; (3) {checkout_created_event}, labeled "Started Checkout"; (4) {subscription_updated_event}
      where the post-update {subscription_updated_event.plan_items} indicates a higher-tier plan than the prior plan (computed
      as a delta of plan amount), labeled "Upgraded". Set the conversion window to {conversionWindow}. Break down by starting
      plan, resolved from {subscription_started_plan_attribute} as of before the upgrade. Compare against the previous period
      of {comparisonWindow}. For each step, show median time-to-convert in days from the previous step and drop-off rate versus
      the previous period. Annotate the step with the largest drop-off as the bottleneck to address first. Annotate any step
      whose median time-to-convert exceeds {slowStepThreshold}. Identify which starting plan has the fastest expansion velocity.'
---

# Account expansion funnel

Slash command: /account-expansion-funnel

## Step 1: Chart the path to an upgrade

Create a Funnel report called "Account Expansion Funnel".
Steps:
1. Event "View page" where Page URL contains "/pricing": "Viewed Pricing"
2. Event "Click on" where target_id matches an upgrade CTA pattern (e.g. target_id contains "upgrade" or "checkout"): "Clicked Upgrade"
3. Event "Checkout created": "Started Checkout"
4. Event "Subscription updated" where the post-update plan_items indicates a higher-tier plan than prior (delta computation): "Upgraded"
Conversion window: 30 days
Breakdown: By Plan: resolved from the user's Subscription started.Plan BEFORE the upgrade (the plan they were upgrading from)
Compare: Previous period (prior 30 days)
For each step, also surface:
- Median time-to-convert (days from previous step)
- Drop-off rate vs. previous period
Annotations:
- Flag the largest drop-off step: this is the bottleneck to address first.
- Flag any step where median time-to-convert exceeds 7 days.
Identify which starting plan has the fastest expansion velocity.
Taxonomy notes:
- "rate_limit_hit" and "pricing_page_viewed" as standalone events do not exist. Pricing page views are derived from View page.Page URL. The first "Hit Plan Limit" step is intentionally omitted because it has no canonical event; if the workspace emits a custom event for limit hits, it can be substituted.
- "subscription_upgraded" does not exist; upgrades are derived from Subscription updated by comparing pre/post plan amount.
