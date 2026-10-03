---
id: sales-pipeline-dashboard
title: Deals to work this week
slash_command: /sales-pipeline-dashboard
group: Dashboards
owner: intempt
summary: Answers which open deals need attention now, flagging the ones that have stalled and the ones
  where only a single contact is engaged.
description: >-
  AE / Sales Manager operational view: open pipeline, deal velocity, multi-threading risk, and account
  engagement on active deals.
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
steps:
  - id: s1
    title: Build the pipeline board
    summary: >-
      Open pipeline and deal velocity for the current quarter, per deal and per rep, with single-threading
      risk and buyer engagement signals.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "Sales Pipeline".
      Persona: Account Executive or Sales Manager. Question answered: "What deals do I work this week?": current-state operational view, this-quarter horizon, per-deal/per-rep granularity.
      This dashboard is intentionally distinct from the Revenue Operations Dashboard. Sales Pipeline is operational (deals to work now); Revenue Operations is strategic (GTM trends and health).
      Board-level configuration:
      - defaultDateRange: last_30_days (rolling, since open deals are point-in-time)
      - exclusionPeriod: none
      - visibility: project
      - boardFilters: none by default (each card scopes its own population per recipe definition)
      - boardBreakdowns: owner_id (rep): pushed down so each card decomposes by rep where applicable
      Layout: 4 rows.
      Row 1: Operational KPIs (heightPx: 200, four metric cards at widthUnits: 3):
      - Card 1: Insights metric to source recipe: pipeline-value-snapshot, vizType: metric, titleOverride: "Open Pipeline Value"
      - Card 2: Insights metric to source recipe: multi-threading-coverage-by-deal, vizType: metric, titleOverride: "Single-threaded Deals"
      - Card 3: Insights metric to source recipe: accounts-at-risk-count, vizType: metric, titleOverride: "Accounts at Risk"
      - Card 4: Insights metric to source recipe: deal-velocity-by-stage, vizType: metric, titleOverride: "Median Sales Cycle (days)"
      Row 2: Deal health (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: deal-velocity-by-stage, displayMode: chart, vizType: bar (horizontal bar per stage with median time-in-stage)
      - Card 2: Insights to source recipe: multi-threading-coverage-by-deal, displayMode: chart, vizType: stacked_bar (threading distribution per stage)
      Row 3: Account-level intelligence (heightPx: 400, full-width single card at widthUnits: 12):
      - Card 1: Insights to source recipe: account-engagement-score-trend, displayMode: table (top 30 accounts ranked by current engagement, with trend sparkline; sortable by week-over-week change)
      Row 4: Behavioral signals (heightPx: 400, two cards at widthUnits: 6):
      - Card 1: Funnel to source recipe: lead-customer-sales, displayMode: chart, vizType: funnel_steps (high-level pipeline progression)
      - Card 2: Insights to source recipe: pipeline-value-snapshot, displayMode: chart, vizType: bar (full pipeline-value-by-stage view from the recipe)
      Annotations:
      - Row 1's four KPIs are the daily-check numbers: what's in pipeline, what's at risk (single-threaded), what accounts need saving, and how fast we move.
      - Row 3 (the full-width account table) is the key actionable artifact: sorted by week-over-week engagement change, it surfaces both expansion candidates (rising) and churn-risk accounts (falling).
      Taxonomy notes:
      - All source recipes use canonical Intempt events: deal_stage_changed, deal_won, deal_lost, deal_created, meeting_scheduled, session_start, click_on, ticket_created.
      - pipeline-value-snapshot includes weighted-forecast computation (each deal's amount × historical close-rate of its current stage).
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Deals to work this week

Answers which open deals need attention now, flagging the ones that have stalled and the ones where only a single contact is engaged.

## Steps

1. **Build the pipeline board** (builds dashboard)

   Open pipeline and deal velocity for the current quarter, per deal and per rep, with single-threading risk and buyer engagement signals.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Availability

Coming soon: waiting on the engine to build dashboard.
