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
        1. Event "View page" where the page URL contains "/pricing": "Viewed Pricing"
        2. Event "Click on" where the clicked element matches an upgrade CTA pattern (e.g. the element identifier contains "upgrade" or "checkout"): "Clicked Upgrade"
        3. Event "Checkout created": "Started Checkout"
        4. Event "Subscription updated" where the post-update plan indicates a higher-tier plan than prior (delta computation): "Upgraded"

        Conversion window: 30 days
        Breakdown: By plan: resolved from the plan the user was on BEFORE the upgrade (the plan they were upgrading from)
        Compare: Previous period (prior 30 days)

        For each step, also surface:
        - Median time-to-convert (days from previous step)
        - Drop-off rate vs. previous period

        Annotations:
        - Flag the largest drop-off step: this is the bottleneck to address first.
        - Flag any step where median time-to-convert exceeds 7 days.

        Identify which starting plan has the fastest expansion velocity.
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
