---
id: founder-weekly-review-dashboard
title: Monday morning scorecard
slash_command: /founder-weekly-review-dashboard
group: Dashboards
owner: intempt
curator: sid
summary: 'The one page to read before the Monday team meeting: new customers, churn, revenue, retention
  and engagement, each against last week and last year.'
description: >-
  The single scorecard a founder/operator wants every Monday: new customers, churn, revenue, retention,
  engagement, with WoW and YoY comparison.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - all
  complexity: standard
  executionMode: live
  tags:
    - dashboard
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new dashboard, from step 1 "Build the weekly scorecard"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the weekly scorecard
    summary: >-
      Six headline numbers (new customers, churn, revenue, retention, engagement) each with week-over-week
      and year-over-year change, plus trend lines.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "Founder Weekly Review".
      Persona: Founder, CEO, or Head-of-Operations running the weekly cadence. Question answered: "What's the one-pager I look at every Monday before my team meeting?"
      This dashboard is mode-agnostic: it auto-adapts to the workspace's primary mode (saas, ecommerce, or mixed). The cards default to the most relevant configuration per mode.
      Board-level configuration:
      - defaultDateRange: last_7_days (this-week view): but cards default to comparing against prior week and YoY
      - exclusionPeriod: incomplete_periods
      - visibility: project
      - boardFilters: none by default
      - boardBreakdowns: none
      Layout: 3 rows (intentionally compact: this is a one-pager).
      Row 1: Headline scorecard (heightPx: 240, six metric cards at widthUnits: 2 each):
      - Card 1: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "New Signups (WoW)"
      - Card 2: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "New Paying Customers"
      - Card 3: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Net New Customers"
      - Card 4: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Revenue (WoW)"
      - Card 5: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Active Users (DAU 7d avg)"
      - Card 6: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Churned Customers"
      Row 2: Trend strip (heightPx: 280, three cards at widthUnits: 4 each):
      - Card 1: Insights to source recipe: weekly-business-review-summary, displayMode: chart, vizType: line, titleOverride: "Revenue 12-Week Trend"
      - Card 2: Insights to source recipe: weekly-business-review-summary, displayMode: chart, vizType: line, titleOverride: "Net New Customers Trend"
      - Card 3: Insights to source recipe: weekly-business-review-summary, displayMode: chart, vizType: line, titleOverride: "Engagement Trend (DAU)"
      Row 3: Mode-specific anchor (heightPx: 360, full-width single card at widthUnits: 12):
      - Mode = saas: Card 1: Insights to source recipe: mrr-movement-decomposition, displayMode: chart, vizType: stacked_column (waterfall view)
      - Mode = ecommerce: Card 1: Insights to source recipe: customer-lifecycle-distribution, displayMode: chart (lifecycle distribution with migration view)
      - Mode = all (mixed): Card 1: Insights to source recipe: weekly-business-review-summary, displayMode: table (the full WBR scorecard table)
      Annotations:
      - This dashboard is intentionally compact (3 rows, ~880px total height) so it fits on a single screen for a Monday-morning scan.
      - Row 1's six metric cards each show: current week value, week-over-week % change, year-over-year % change.
      - Row 3 is the strategic anchor for the week. SaaS founders watch the MRR waterfall; ecommerce founders watch lifecycle migration.
      - Row 1 and Row 2 cards are intentionally all sourced from weekly-business-review-summary: that recipe is a multi-series report designed to power exactly this dashboard. Each card pulls a different series (Series A through Series F) of the same report.
      Taxonomy notes:
      - weekly-business-review-summary is mode-aware and adapts its underlying queries based on the workspace's primary mode.
      - All cards reference canonical events through their source recipes.
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Monday morning scorecard

The one page to read before the Monday team meeting: new customers, churn, revenue, retention and engagement, each against last week and last year.

## Steps

1. **Build the weekly scorecard** (builds dashboard)

   Six headline numbers (new customers, churn, revenue, retention, engagement) each with week-over-week and year-over-year change, plus trend lines.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new dashboard, from step 1 "Build the weekly scorecard"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
