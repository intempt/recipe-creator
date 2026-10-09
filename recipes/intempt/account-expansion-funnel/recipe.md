---
description: Tracks subscription amount increases as a signal of account expansion. Uses subscription state changes and amount deltas to identify potential upgrades.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - b2b-saas
  - finance
  - media
---

# Account expansion funnel

Slash command: /account-expansion-funnel

## Step 1: Chart the path to an upgrade

Create a Funnel report called "Account Expansion Funnel".
Steps:
1. Event "page_viewed" where page_url contains "/pricing": "Viewed Pricing"
2. Event "click_on" where target_id matches an upgrade CTA pattern (e.g. target_id contains "upgrade" or "checkout"): "Clicked Upgrade"
3. Event "checkout_created": "Started Checkout"
4. Event "subscription_updated" where the post-update plan_items indicates a higher-tier plan than prior (delta computation): "Upgraded"
Conversion window: 30 days
Breakdown: By plan_name: resolved from the user's subscription_created.plan_name BEFORE the upgrade (the plan they were upgrading from)
Compare: Previous period (prior 30 days)
For each step, also surface:
- Median time-to-convert (days from previous step)
- Drop-off rate vs. previous period
Annotations:
- Flag the largest drop-off step: this is the bottleneck to address first.
- Flag any step where median time-to-convert exceeds 7 days.
Identify which starting plan has the fastest expansion velocity.
Taxonomy notes:
- "rate_limit_hit" and "pricing_page_viewed" as standalone events do not exist. Pricing page views are derived from page_viewed.page_url. The first "Hit Plan Limit" step is intentionally omitted because it has no canonical event; if the workspace emits a custom event for limit hits, it can be substituted.
- "subscription_upgraded" does not exist; upgrades are derived from subscription_updated by comparing pre/post plan amount.
