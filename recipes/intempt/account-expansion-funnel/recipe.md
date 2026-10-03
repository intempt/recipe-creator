---
id: account-expansion-funnel
title: Account expansion funnel
slash_command: /account-expansion-funnel
group: Reports
owner: intempt
summary: Tracks how many customers go from viewing pricing to clicking upgrade, starting checkout and
  landing on a higher plan, and how long each step takes.
description: >-
  Plan-limit-to-upgrade funnel built from real subscription state-change events with per-step time-to-convert.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - b2b
  complexity: quick
  executionMode: live
  tags:
    - funnel
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Chart the path to an upgrade"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Chart the path to an upgrade
    summary: >-
      A four step funnel from a pricing page view to an upgrade click, a started checkout and a completed
      plan change, inside a 30 day window, split by the plan they were upgrading from. Shows median time
      to convert per step and flags any step over 7 days.
    builds: report
    description: |-
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
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Account expansion funnel

Tracks how many customers go from viewing pricing to clicking upgrade, starting checkout and landing on a higher plan, and how long each step takes.

## Steps

1. **Chart the path to an upgrade** (builds report)

   A four step funnel from a pricing page view to an upgrade click, a started checkout and a completed plan change, inside a 30 day window, split by the plan they were upgrading from. Shows median time to convert per step and flags any step over 7 days.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Chart the path to an upgrade"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
