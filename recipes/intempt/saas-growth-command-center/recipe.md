---
id: saas-growth-command-center
title: SaaS growth command center
slash_command: /saas-growth-command-center
group: Dashboards
owner: intempt
curator: sid
summary: >-
  Shows whether you are growing and whether growth is healthy on one dashboard: weekly actives, MRR, trial
  conversion, activation, retention and feature adoption.
description: >-
  Founder-level SaaS growth dashboard: WAU, MRR, trial conversion, retention, activation, and feature adoption
  on one canvas.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  complexity: standard
  executionMode: live
  tags:
    - dashboard
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new dashboard, from step 1 "Build the growth board"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the growth board
    summary: >-
      Weekly active users, MRR, trial conversion and retention, plus activation depth and feature adoption
      over time.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "SaaS Growth Command Center".
      Persona: SaaS founder or GM. Question answered: "Are we growing, and is the growth healthy?"
      Board-level configuration:
      - defaultDateRange: last_30_days
      - exclusionPeriod: incomplete_periods
      - visibility: project
      - boardFilters: none by default (allow user to add plan_tier filter at runtime)
      - boardBreakdowns: none
      Layout: 4 rows × variable cards per row. All cards isLinked: true (live-mirror the source recipe). Widths sum to 12 per row.
      Row 1: Headline KPIs (heightPx: 200, four metric cards at widthUnits: 3 each):
      - Card 1: Insights metric card to source recipe: weekly-active-users-trend, displayMode: chart, vizType: metric, titleOverride: "Weekly Active Users"
      - Card 2: Insights metric card to source recipe: mrr-trend, displayMode: chart, vizType: metric, titleOverride: "MRR"
      - Card 3: Insights metric card to source recipe: trial-to-paid-conversion-rate, displayMode: chart, vizType: metric, titleOverride: "Trial to Paid"
      - Card 4: Insights metric card to source recipe: stickiness-ratios-dau-wau-mau, displayMode: chart, vizType: metric, titleOverride: "Stickiness (DAU/MAU)"
      Row 2: Growth trends (heightPx: 400, two cards at widthUnits: 6 each):
      - Card 1: Insights trend to source recipe: mrr-trend, displayMode: chart, vizType: stacked_area
      - Card 2: Funnel to source recipe: signup-activation-funnel, displayMode: chart, vizType: funnel_steps
      Row 3: Activation depth (heightPx: 400, two cards at widthUnits: 6 each):
      - Card 1: Insights to source recipe: feature-adoption-by-plan, displayMode: chart, vizType: bar
      - Card 2: Insights to source recipe: stickiness-ratios-dau-wau-mau, displayMode: chart, vizType: line (full trend, not just metric)
      Row 4: Retention and behavior (heightPx: 440, two cards at widthUnits: 6 each):
      - Card 1: Retention to source recipe: user-retention-weekly, displayMode: table (cohort grid)
      - Card 2: Path to source recipe: first-session-paths-after-signup, displayMode: chart, vizType: sankey-style path
      Annotations:
      - The four KPIs in Row 1 should be reviewed alongside the stickiness ratio (Row 1 Card 4): high WAU/MRR with falling stickiness is a leading indicator of churn.
      - All cards respect the board-level date range; users can override per-card if needed.
      Taxonomy notes:
      - All 7 source recipes are taxonomy-grounded against Intempt V2.1.
      - Cards reference recipe slugs by id; when isLinked: true the card is a live mirror of the source recipe's configuration.
      - KPI cards use the metric vizType applied to the source chart-recipe: Lovable renders the recipe's headline metric as a single number.
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# SaaS growth command center

Shows whether you are growing and whether growth is healthy on one dashboard: weekly actives, MRR, trial conversion, activation, retention and feature adoption.

## Steps

1. **Build the growth board** (builds dashboard)

   Weekly active users, MRR, trial conversion and retention, plus activation depth and feature adoption over time.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new dashboard, from step 1 "Build the growth board"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
