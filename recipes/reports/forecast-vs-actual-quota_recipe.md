---
name: forecast-vs-actual-quota
description: |
  Use when a user mentions "forecast vs actual vs quota", or asks for related help. Period-level revenue forecast vs. actual closed-won vs. quota target with pipeline coverage ratio and projected close.
arguments: []
intempt:
  id: forecast-vs-actual-quota
  version: 1.0.0
  slashCommand: /forecast-vs-actual-quota
  group: Reports
  shortDescription: "Period-level revenue forecast vs. actual closed-won vs. quota target with pipeline coverage ratio and projected close."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [b2b]
    complexity: quick
    executionMode: live
    tags: [insights]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: hubspot, severity: blocking }
      - { value: salesforce, severity: blocking }
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "Forecast vs Actual vs Quota".

        Series A: Sum of deal_won.amount per period (closed-won revenue), unit: $, label: "Actual Closed-Won"
        Series B: Sum of (open-deal amount × historical close-rate of current stage) for deals with close_date in the period — the weighted forecast, unit: $, label: "Weighted Forecast"
        Series C: Workspace-configured quota target for the period, unit: $, label: "Quota Target"
          - Default: pulled from a workspace-level quota attribute (per-period dollar target). If unconfigured, recipe degrades gracefully and surfaces just A and B.
        Series D: Computed — Series A / Series C × 100, unit: %, label: "Quota Attainment"
        Series E: Computed — (Sum of all open-deal amounts) / Series C, label: "Pipeline Coverage Ratio"
          - The canonical 3:1 ratio benchmark — pipeline-to-quota of 3x is the industry minimum for reliable close.
        Series F: Computed — Sum of deal amount where close_date IS within next 30 days AND stage is in late-stage (negotiation/proposal/contract), unit: $, label: "Projected Close (Next 30d)"

        Time granularity: Monthly (or per quota period — quarterly for most B2B teams)
        Time range: Trailing 4 quota periods + current + next period (forward-looking forecast)
        Breakdown: By owner_id (per-rep) — pushed down so each rep's forecast/actual/quota is visible
        Compare: Previous period AND year-over-year same-period
        Chart type: Combo chart — Series A (actual) and B (forecast) as bars, Series C (quota) as a horizontal target line, Series D (attainment %) on a secondary axis as a callout, Series E (coverage ratio) as a separate KPI tile

        Annotations:
        - Add the canonical pipeline coverage benchmark: 3:1 minimum, 4-5:1 healthy, <2:1 indicates pipeline shortfall.
        - Flag any period where forecast (Series B) significantly exceeded actual (Series A) — forecast-accuracy issue, investigate which deals slipped.
        - Flag any rep whose pipeline coverage ratio fell below 2:1 (acute risk for next period).
        - Highlight the period attainment trend: 4+ consecutive periods below 100% attainment indicates either quota is set too aggressively or systematic execution issues.
        - Surface forecast accuracy as an explicit metric: |Actual − Forecast| / Actual × 100 over trailing 4 periods. Top-quartile sales orgs forecast within ±10%; below ±20% accuracy indicates the forecasting process needs refinement.

        Use case: the canonical sales VP / CRO weekly report. Pipeline coverage ratio (Series E) is the most-cited B2B sales KPI; forecast accuracy is the leading indicator of sales-process maturity.

        Taxonomy notes:
        - deal_won.amount and deal_won.close_date are canonical properties.
        - deal_stage_changed has new_stage and amount per state change; "current open-deal amount" comes from the most-recent deal_stage_changed.amount per deal_id.
        - owner_id is a canonical property on deal_created and deal_stage_changed; also on Users object.
        - IMPORTANT — quota target dependency: this recipe assumes the workspace has quota targets configured per period per rep, OR a workspace-level aggregate quota. If neither is configured, Series C and Series D return null and the report renders Series A, B, E, F only. Sales teams typically inject quota targets via HubSpot/Salesforce sync or as a manual workspace-level attribute.
        - "Late-stage" classification for Series F (Projected Close) follows the project's deal-stage configuration; standard convention is the final 2-3 stages before deal_won/deal_lost.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Forecast vs Actual vs Quota

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Forecast vs Actual vs Quota".

   Series A: Sum of deal_won.amount per period (closed-won revenue), unit: $, label: "Actual Closed-Won"
   Series B: Sum of (open-deal amount × historical close-rate of current stage) for deals with close_date in the period — the weighted forecast, unit: $, label: "Weighted Forecast"
   Series C: Workspace-configured quota target for the period, unit: $, label: "Quota Target"
     - Default: pulled from a workspace-level quota attribute (per-period dollar target). If unconfigured, recipe degrades gracefully and surfaces just A and B.
   Series D: Computed — Series A / Series C × 100, unit: %, label: "Quota Attainment"
   Series E: Computed — (Sum of all open-deal amounts) / Series C, label: "Pipeline Coverage Ratio"
     - The canonical 3:1 ratio benchmark — pipeline-to-quota of 3x is the industry minimum for reliable close.
   Series F: Computed — Sum of deal amount where close_date IS within next 30 days AND stage is in late-stage (negotiation/proposal/contract), unit: $, label: "Projected Close (Next 30d)"

   Time granularity: Monthly (or per quota period — quarterly for most B2B teams)
   Time range: Trailing 4 quota periods + current + next period (forward-looking forecast)
   Breakdown: By owner_id (per-rep) — pushed down so each rep's forecast/actual/quota is visible
   Compare: Previous period AND year-over-year same-period
   Chart type: Combo chart — Series A (actual) and B (forecast) as bars, Series C (quota) as a horizontal target line, Series D (attainment %) on a secondary axis as a callout, Series E (coverage ratio) as a separate KPI tile

   Annotations:
   - Add the canonical pipeline coverage benchmark: 3:1 minimum, 4-5:1 healthy, <2:1 indicates pipeline shortfall.
   - Flag any period where forecast (Series B) significantly exceeded actual (Series A) — forecast-accuracy issue, investigate which deals slipped.
   - Flag any rep whose pipeline coverage ratio fell below 2:1 (acute risk for next period).
   - Highlight the period attainment trend: 4+ consecutive periods below 100% attainment indicates either quota is set too aggressively or systematic execution issues.
   - Surface forecast accuracy as an explicit metric: |Actual − Forecast| / Actual × 100 over trailing 4 periods. Top-quartile sales orgs forecast within ±10%; below ±20% accuracy indicates the forecasting process needs refinement.

   Use case: the canonical sales VP / CRO weekly report. Pipeline coverage ratio (Series E) is the most-cited B2B sales KPI; forecast accuracy is the leading indicator of sales-process maturity.

   Taxonomy notes:
   - deal_won.amount and deal_won.close_date are canonical properties.
   - deal_stage_changed has new_stage and amount per state change; "current open-deal amount" comes from the most-recent deal_stage_changed.amount per deal_id.
   - owner_id is a canonical property on deal_created and deal_stage_changed; also on Users object.
   - IMPORTANT — quota target dependency: this recipe assumes the workspace has quota targets configured per period per rep, OR a workspace-level aggregate quota. If neither is configured, Series C and Series D return null and the report renders Series A, B, E, F only. Sales teams typically inject quota targets via HubSpot/Salesforce sync or as a manual workspace-level attribute.
   - "Late-stage" classification for Series F (Projected Close) follows the project's deal-stage configuration; standard convention is the final 2-3 stages before deal_won/deal_lost.
   ```
