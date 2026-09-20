---
name: account-expansion-funnel
description: |
  Use when a user mentions "account expansion funnel", or asks for related help. Plan-limit-to-upgrade funnel built from real subscription state-change events with per-step time-to-convert.
arguments: []
intempt:
  id: account-expansion-funnel
  version: 1.0.0
  slashCommand: /account-expansion-funnel
  group: Reports
  title: "Account expansion funnel"
  shortDescription: "Tracks how many customers go from viewing pricing to clicking upgrade, starting checkout and landing on a higher plan, and how long each step takes."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [b2b]
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
      title: "Chart the path to an upgrade"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "A four step funnel from a pricing page view to an upgrade click, a started checkout and a completed plan change, inside a 30 day window, split by the plan they were upgrading from. Shows median time to convert per step and flags any step over 7 days."
      prompt: |
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
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Account expansion funnel

Tracks how many customers go from viewing pricing to clicking upgrade, starting checkout and landing on a higher plan, and how long each step takes.

## What it does

1. **Chart the path to an upgrade** (`build_funnel_report`)

   A four step funnel from a pricing page view to an upgrade click, a started checkout and a completed plan change, inside a 30 day window, split by the plan they were upgrading from. Shows median time to convert per step and flags any step over 7 days.

## What you end up with

- **report** (report): Report produced by this recipe.
