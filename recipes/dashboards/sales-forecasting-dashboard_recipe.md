---
name: sales-forecasting-dashboard
description: |
  Use when a user mentions "sales forecasting dashboard", asks for a sales vp / cro dashboard, or asks for related help. Sales VP / CRO forecasting view: pipeline coverage 3:1, weighted forecast, quota attainment, projected close, forecast accuracy.
arguments: []
intempt:
  id: sales-forecasting-dashboard
  version: 1.0.0
  slashCommand: /sales-forecasting-dashboard
  group: Dashboards
  shortDescription: "Sales VP / CRO forecasting view: pipeline coverage 3:1, weighted forecast, quota attainment, projected close, forecast accuracy."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [b2b]
    complexity: standard
    executionMode: live
    tags: [dashboard]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_dashboard
  procedure:
    - step: 1
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      description: "Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below."
      prompt: |
        Create a Dash board (12-column composition canvas) titled "Sales Forecasting".

        Persona: Sales VP, CRO, or Sales Manager doing forecast preparation. Question answered: "Will we hit number this period? What's the confidence level? Where's the risk?"

        Distinct from Sales Pipeline Dashboard (operational, current deals) and Revenue Operations (strategic GTM trends). Sales Forecasting is forward-looking commitment-level reporting — the report sales leadership submits to the CFO/board.

        Board-level configuration:
        - defaultDateRange: current quarter (or current quota period)
        - exclusionPeriod: none
        - visibility: project
        - boardFilters: none by default (each card scopes its own population)
        - boardBreakdowns: owner_id (per-rep) — pushed down for per-rep forecast visibility

        Layout: 4 rows.

        Row 1 — Forecast headline KPIs (heightPx: 200, four metric cards at widthUnits: 3):
        - Card 1: Insights metric → source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Quota Attainment (Period-to-Date)"
        - Card 2: Insights metric → source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Pipeline Coverage Ratio"
        - Card 3: Insights metric → source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Weighted Forecast"
        - Card 4: Insights metric → source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Projected Close (Next 30d)"

        Row 2 — Forecast vs. actual vs. quota (heightPx: 480, full-width single card at widthUnits: 12):
        - Card 1: Insights → source recipe: forecast-vs-actual-quota, displayMode: chart, vizType: column (combo chart — actual closed bars + weighted forecast bars + quota target line, broken down by owner_id and trended over the last 4 periods + current). The strategic centerpiece.

        Row 3 — Per-rep quota attainment (heightPx: 480, full-width single card at widthUnits: 12):
        - Card 1: Insights → source recipe: quota-attainment-by-rep, displayMode: table (the sortable per-rep leaderboard with attainment %, absolute revenue, pipeline coverage ratio, and trend sparkline)

        Row 4 — Pipeline composition (heightPx: 440, two cards at widthUnits: 6):
        - Card 1: Insights → source recipe: pipeline-value-snapshot, displayMode: chart, vizType: bar (pipeline by stage with weighted forecast)
        - Card 2: Insights → source recipe: deal-velocity-by-stage, displayMode: chart, vizType: bar (median time-in-stage — informs which deals will likely close in-period vs. slip)

        Annotations:
        - Row 1's Pipeline Coverage Ratio is the canonical sales-leadership health metric: <2:1 = acute risk for the period, 2-3:1 = warning, ≥3:1 = healthy, ≥5:1 = abundance (potentially over-forecasting).
        - Row 2 (Forecast vs Actual vs Quota, full-width) reads top-down: actual-period revenue should be approaching quota target; weighted forecast should be above quota by the end of the period; gap between forecast and quota = commit risk. Trailing-period accuracy (|forecast − actual|) should ideally stay within ±10% — that's top-quartile sales-team forecast accuracy.
        - Row 3 surfaces per-rep risk: any rep <50% attainment with <2:1 coverage is a yellow flag warranting manager intervention.
        - Row 4's velocity view answers a forecasting-specific question: of deals currently in negotiation/proposal, which are likely to actually close before period-end? Median time-in-stage tells you whether a deal at "negotiation" 3 days in is on track vs. behind.

        Taxonomy notes:
        - forecast-vs-actual-quota and quota-attainment-by-rep both depend on workspace-level quota target configuration. Without quota data, those cards degrade gracefully (Series C and D return null) and the report shows actual + weighted forecast only. Sales teams typically inject quota targets via HubSpot/Salesforce sync or manually as a workspace attribute.
        - All other source recipes use canonical events: deal_won, deal_lost, deal_stage_changed, deal_created.
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---

# Sales Forecasting Dashboard

## Procedure

1. **Build Dashboard** [`create_dashboard`] — Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below. → produces: dashboard

   ```text
   Create a Dash board (12-column composition canvas) titled "Sales Forecasting".

   Persona: Sales VP, CRO, or Sales Manager doing forecast preparation. Question answered: "Will we hit number this period? What's the confidence level? Where's the risk?"

   Distinct from Sales Pipeline Dashboard (operational, current deals) and Revenue Operations (strategic GTM trends). Sales Forecasting is forward-looking commitment-level reporting — the report sales leadership submits to the CFO/board.

   Board-level configuration:
   - defaultDateRange: current quarter (or current quota period)
   - exclusionPeriod: none
   - visibility: project
   - boardFilters: none by default (each card scopes its own population)
   - boardBreakdowns: owner_id (per-rep) — pushed down for per-rep forecast visibility

   Layout: 4 rows.

   Row 1 — Forecast headline KPIs (heightPx: 200, four metric cards at widthUnits: 3):
   - Card 1: Insights metric → source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Quota Attainment (Period-to-Date)"
   - Card 2: Insights metric → source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Pipeline Coverage Ratio"
   - Card 3: Insights metric → source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Weighted Forecast"
   - Card 4: Insights metric → source recipe: forecast-vs-actual-quota, vizType: metric, titleOverride: "Projected Close (Next 30d)"

   Row 2 — Forecast vs. actual vs. quota (heightPx: 480, full-width single card at widthUnits: 12):
   - Card 1: Insights → source recipe: forecast-vs-actual-quota, displayMode: chart, vizType: column (combo chart — actual closed bars + weighted forecast bars + quota target line, broken down by owner_id and trended over the last 4 periods + current). The strategic centerpiece.

   Row 3 — Per-rep quota attainment (heightPx: 480, full-width single card at widthUnits: 12):
   - Card 1: Insights → source recipe: quota-attainment-by-rep, displayMode: table (the sortable per-rep leaderboard with attainment %, absolute revenue, pipeline coverage ratio, and trend sparkline)

   Row 4 — Pipeline composition (heightPx: 440, two cards at widthUnits: 6):
   - Card 1: Insights → source recipe: pipeline-value-snapshot, displayMode: chart, vizType: bar (pipeline by stage with weighted forecast)
   - Card 2: Insights → source recipe: deal-velocity-by-stage, displayMode: chart, vizType: bar (median time-in-stage — informs which deals will likely close in-period vs. slip)

   Annotations:
   - Row 1's Pipeline Coverage Ratio is the canonical sales-leadership health metric: <2:1 = acute risk for the period, 2-3:1 = warning, ≥3:1 = healthy, ≥5:1 = abundance (potentially over-forecasting).
   - Row 2 (Forecast vs Actual vs Quota, full-width) reads top-down: actual-period revenue should be approaching quota target; weighted forecast should be above quota by the end of the period; gap between forecast and quota = commit risk. Trailing-period accuracy (|forecast − actual|) should ideally stay within ±10% — that's top-quartile sales-team forecast accuracy.
   - Row 3 surfaces per-rep risk: any rep <50% attainment with <2:1 coverage is a yellow flag warranting manager intervention.
   - Row 4's velocity view answers a forecasting-specific question: of deals currently in negotiation/proposal, which are likely to actually close before period-end? Median time-in-stage tells you whether a deal at "negotiation" 3 days in is on track vs. behind.

   Taxonomy notes:
   - forecast-vs-actual-quota and quota-attainment-by-rep both depend on workspace-level quota target configuration. Without quota data, those cards degrade gracefully (Series C and D return null) and the report shows actual + weighted forecast only. Sales teams typically inject quota targets via HubSpot/Salesforce sync or manually as a workspace attribute.
   - All other source recipes use canonical events: deal_won, deal_lost, deal_stage_changed, deal_created.
   ```
