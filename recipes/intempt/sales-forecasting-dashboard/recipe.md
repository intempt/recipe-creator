---
id: sales-forecasting-dashboard
title: Will we hit the number
slash_command: /sales-forecasting-dashboard
group: Dashboards
owner: intempt
curator: sid
summary: 'Answers whether the period will close on target and where the risk sits: pipeline coverage,
  weighted forecast, quota attainment per rep, and past forecast accuracy.'
description: >-
  Sales VP / CRO forecasting view: pipeline coverage 3:1, weighted forecast, quota attainment, projected
  close, forecast accuracy.
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
prerequisites:
  integrations:
    - value: hubspot
      severity: blocking
      group: crm
    - value: salesforce
      severity: blocking
      group: crm
touches:
  reads:
    - Your HubSpot connection
    - Your Salesforce connection
  writes:
    - A new dashboard, from step 1 "Build the forecast board"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the forecast board
    summary: >-
      Pipeline coverage against the 3:1 benchmark, weighted forecast versus quota, per-rep attainment,
      and how accurate past forecasts turned out.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "Sales Forecasting".
      Persona: Sales VP, CRO, or Sales Manager doing forecast preparation. Question answered: "Will we hit number this period? What's the confidence level? Where's the risk?"
      Distinct from Sales Pipeline Dashboard (operational, current deals) and Revenue Operations (strategic GTM trends). Sales Forecasting is forward-looking commitment-level reporting: the report sales leadership submits to the CFO/board.
      Board-level configuration:
      - defaultDateRange: current quarter (or current quota period)
      - exclusionPeriod: none
      - visibility: project
      - boardFilters: none by default (each card scopes its own population)
      - boardBreakdowns: owner_id (per-rep): pushed down for per-rep forecast visibility
      Layout: 4 rows.
      Row 1: Forecast headline KPIs (heightPx: 200, four metric cards at widthUnits: 3):
      - Card 1: Insights metric to source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Quota Attainment (Period-to-Date)"
      - Card 2: Insights metric to source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Pipeline Coverage Ratio"
      - Card 3: Insights metric to source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Weighted Forecast"
      - Card 4: Insights metric to source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Projected Close (Next 30d)"
      Row 2: Forecast vs. actual vs. quota (heightPx: 480, full-width single card at widthUnits: 12):
      - Card 1: Insights to source recipe: forecast-vs-actual-quota, displayMode: chart, vizType: column (combo chart: actual closed bars + weighted forecast bars + quota target line, broken down by owner_id and trended over the last 4 periods + current). The strategic centerpiece.
      Row 3: Per-rep quota attainment (heightPx: 480, full-width single card at widthUnits: 12):
      - Card 1: Insights to source recipe: quota-attainment-by-rep, displayMode: table (the sortable per-rep leaderboard with attainment %, absolute revenue, pipeline coverage ratio, and trend sparkline)
      Row 4: Pipeline composition (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: pipeline-value-snapshot, displayMode: chart, vizType: bar (pipeline by stage with weighted forecast)
      - Card 2: Insights to source recipe: deal-velocity-by-stage, displayMode: chart, vizType: bar (median time-in-stage: informs which deals will likely close in-period vs. slip)
      Annotations:
      - Row 1's Pipeline Coverage Ratio is the canonical sales-leadership health metric: <2:1 = acute risk for the period, 2-3:1 = warning, ≥3:1 = healthy, ≥5:1 = abundance (potentially over-forecasting).
      - Row 2 (Forecast vs Actual vs Quota, full-width) reads top-down: actual-period revenue should be approaching quota target; weighted forecast should be above quota by the end of the period; gap between forecast and quota = commit risk. Trailing-period accuracy (|forecast − actual|) should ideally stay within ±10%: that's top-quartile sales-team forecast accuracy.
      - Row 3 surfaces per-rep risk: any rep <50% attainment with <2:1 coverage is a yellow flag warranting manager intervention.
      - Row 4's velocity view answers a forecasting-specific question: of deals currently in negotiation/proposal, which are likely to actually close before period-end? Median time-in-stage tells you whether a deal at "negotiation" 3 days in is on track vs. behind.
      Taxonomy notes:
      - forecast-vs-actual-quota and quota-attainment-by-rep both depend on workspace-level quota target configuration. Without quota data, those cards degrade gracefully (Series C and D return null) and the report shows actual + weighted forecast only. Sales teams typically inject quota targets via HubSpot/Salesforce sync or manually as a workspace attribute.
      - All other source recipes use canonical events: deal_won, deal_lost, deal_stage_changed, deal_created.
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Will we hit the number

Answers whether the period will close on target and where the risk sits: pipeline coverage, weighted forecast, quota attainment per rep, and past forecast accuracy.

## Steps

1. **Build the forecast board** (builds dashboard)

   Pipeline coverage against the 3:1 benchmark, weighted forecast versus quota, per-rep attainment, and how accurate past forecasts turned out.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Your HubSpot connection
- Your Salesforce connection

Writes:

- A new dashboard, from step 1 "Build the forecast board"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
