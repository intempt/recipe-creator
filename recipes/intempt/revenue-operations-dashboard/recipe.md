---
id: revenue-operations-dashboard
title: GTM health and revenue leakage
slash_command: /revenue-operations-dashboard
group: Dashboards
owner: intempt
curator: sid
summary: Answers where the go-to-market machine leaks over a trailing 90 days, by source and cohort rather
  than by rep, so you can move spend and fix process.
description: >-
  RevOps / CRO strategic view: trailing GTM health, funnel attribution by source, win-loss patterns, and
  NRR trends.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - b2b
  complexity: standard
  executionMode: live
  tags:
    - dashboard
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new dashboard, from step 1 "Build the RevOps board"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the RevOps board
    summary: >-
      Trailing 90-day funnel conversion by source, win and loss patterns, and net revenue retention trends
      at segment and cohort level.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "Revenue Operations".
      Persona: RevOps lead or CRO. Question answered: "Is the GTM machine healthy? Where's the leakage and where do we re-allocate?": strategic horizon (trailing 90 days + cohort views), aggregate granularity (segment/source/cohort, not per-rep), drives spend re-allocation and process changes.
      This dashboard is intentionally distinct from the Sales Pipeline Dashboard. RevOps is strategic and trend-oriented (is the funnel getting healthier?); Sales Pipeline is operational (which deals to work now). Zero card overlap between the two.
      Board-level configuration:
      - defaultDateRange: last_90_days
      - exclusionPeriod: incomplete_periods
      - visibility: project
      - boardFilters: none by default
      - boardBreakdowns: utm_source (lead source): pushed down so cards decompose by acquisition channel where applicable
      Layout: 4 rows.
      Row 1: Strategic KPIs (heightPx: 200, four metric cards at widthUnits: 3):
      - Card 1: Insights metric to source recipe: win-rate-trend, vizType: metric, titleOverride: "Trailing-90d Win Rate"
      - Card 2: Insights metric to source recipe: deal-velocity-by-stage, vizType: metric, titleOverride: "Median Sales Cycle (Closed Deals)"
      - Card 3: Funnel metric to source recipe: lead-to-mql-to-sql-funnel, vizType: metric, titleOverride: "MQL to Closed-Won Rate"
      - Card 4: Retention metric to source recipe: net-revenue-retention-by-cohort, vizType: metric, titleOverride: "Trailing 12-Month Blended NRR"
      Row 2: Funnel health (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Funnel to source recipe: lead-to-mql-to-sql-funnel, displayMode: chart, vizType: funnel_steps (the full qualification funnel)
      - Card 2: Funnel to source recipe: funnel-dropoff-attribution-by-source, displayMode: chart, vizType: funnel_steps (small-multiples by source)
      Row 3: Win-loss intelligence (heightPx: 400, full-width single card at widthUnits: 12):
      - Card 1: Insights to source recipe: win-loss-analysis, displayMode: chart, vizType: bar (won vs. lost by source, with stage-at-loss decomposition view)
      Row 4: Trend and revenue retention (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: win-rate-trend, displayMode: chart, vizType: line (trailing win-rate trend with rolling-90d smoothing)
      - Card 2: Retention to source recipe: net-revenue-retention-by-cohort, displayMode: chart (multi-line cohort NRR curves)
      Annotations:
      - This board is meant for monthly QBR review, not daily/weekly. The right cadence is reading it once per month, looking for inflection points.
      - Row 1 KPIs are 4 leading indicators: declining win rate, lengthening sales cycle, falling MQL to Won, or NRR dipping below 100% are all early-warning signs that warrant strategic intervention.
      - Row 3 (full-width win-loss) is the strategic centerpiece: the breakdown by source shows where to invest more vs. less; the breakdown by stage-at-loss shows whether losses come from qualification (top-funnel ICP issue) or closing (late-funnel competition/pricing issue).
      Taxonomy notes:
      - All source recipes use canonical events: deal_won, deal_lost, deal_stage_changed, lead_stage_changed, user_created, subscription_created, subscription_updated, subscription_cancelled.
      - net-revenue-retention-by-cohort depends on subscription_updated.changed_fields parsing for expansion/contraction split.
      - win-rate-trend (new in v5) is the single-metric tracking version of win-loss-analysis.
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# GTM health and revenue leakage

Answers where the go-to-market machine leaks over a trailing 90 days, by source and cohort rather than by rep, so you can move spend and fix process.

## Steps

1. **Build the RevOps board** (builds dashboard)

   Trailing 90-day funnel conversion by source, win and loss patterns, and net revenue retention trends at segment and cohort level.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new dashboard, from step 1 "Build the RevOps board"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
