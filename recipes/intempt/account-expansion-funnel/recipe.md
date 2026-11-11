---
frontmatter_id: account-expansion-funnel
slash_command: /account-expansion-funnel
description: This recipe maps how existing customers move from viewing pricing to upgrading their plan, then finds the ones who stalled at checkout and automatically nudges them to finish. It suits growth and lifecycle teams who want to increase account expansion revenue.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
---

# Account expansion funnel

## Step 1: Chart the path to an upgrade

Create a Funnel report called "Account Expansion Funnel".
Steps:
1. Event "View page" where Page URL contains "/pricing": "Viewed Pricing"
2. Event "Click on" where target_id matches an upgrade CTA pattern (target_id contains "upgrade" or "checkout"): "Clicked Upgrade"
3. Event "Checkout created": "Started Checkout"
4. Event "Subscription updated" where the post-update plan_items indicates a higher-tier plan than prior: "Upgraded"
Conversion window: 30 days
Breakdown: By Plan, resolved from the user's Subscription started.Plan before the upgrade
Compare: Previous period (prior 30 days)
For each step, also surface:
- Median time-to-convert (days from previous step)
- Drop-off rate versus previous period
Annotations:
- Flag the largest drop-off step.
- Flag any step where median time-to-convert exceeds 7 days.
Taxonomy notes:
- "rate_limit_hit" and "pricing_page_viewed" as standalone events do not exist. Pricing page views are derived from View page.Page URL.
- "subscription_upgraded" does not exist; upgrades are derived from Subscription updated by comparing pre- and post-upgrade plan amount.

## Step 2: Catch users stuck at checkout

Build a segment of users named "Expansion Checkout Abandoners". A user is in the segment only when all of these are true: they did the "Checkout created" event in the last 7 days; they did not do a "Subscription updated" event indicating an upgrade in the same 7 days; their account has an active subscription. Use the result of "Chart the path to an upgrade".

## Step 3: Recover the abandoned upgrade

Build a journey for the users in "Expansion Checkout Abandoners". On entry, send an email reminding the user their plan upgrade was not completed, with a direct link back to checkout. If the user has not completed the upgrade 72 hours after entry, create a task for the account owner with the plan they started upgrading to and the date they abandoned checkout. Exit the journey when the user completes the upgrade or 14 days pass without completion. Use the result of "Chart the path to an upgrade", "Catch users stuck at checkout".
