---
frontmatter_id: forecast-vs-actual-quota
slash_command: /forecast-vs-actual-quota
description: Shows period closed-won revenue alongside pipeline coverage.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows each rep's closed-won revenue against forecast and quota, with pipeline coverage, projected near-term closes,
    and forecast accuracy flags.
  parameters:
  - name: trailing_periods
    type: number
    label: Trailing quota periods to show
    default: 4
    required: false
  - name: coverage_minimum
    type: number
    label: Minimum pipeline coverage ratio (x)
    default: 3
    required: false
  - name: coverage_risk_threshold
    type: number
    label: Acute pipeline coverage risk threshold (x)
    default: 2
    required: false
  - name: projection_window
    type: duration
    label: Projected close window
    default: 30 d
    required: false
  - name: forecast_accuracy_band
    type: number
    label: Forecast accuracy tolerance (%)
    default: 20
    required: false
  - name: low_attainment_streak
    type: number
    label: Consecutive periods below quota to flag
    default: 4
    required: false
  requirements:
  - slot: closed_won_deal
    kind: event
    meaning: A deal was marked closed-won
    properties:
    - name: amount
      type: number
      meaning: Value of the won deal
      optional: false
    - name: close_date
      type: date
      meaning: Date the deal closed
      optional: false
    - name: owner_id
      type: string
      meaning: Rep who owns the deal
      optional: false
  - slot: deal_stage_change
    kind: event
    meaning: A deal moved to a new pipeline stage with its amount at that time
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
    - name: new_stage
      type: string
      meaning: Stage the deal moved into
      optional: false
    - name: amount
      type: number
      meaning: Deal amount at this stage change
      optional: false
    - name: close_date
      type: date
      meaning: Expected close date of the deal
      optional: true
    - name: owner_id
      type: string
      meaning: Rep who owns the deal
      optional: false
  - slot: quota_target
    kind: attribute
    meaning: Per-period dollar quota target for a rep or the workspace
    optional: true
  - slot: late_stage_definition
    kind: attribute
    meaning: The set of deal stages treated as late-stage (negotiation, proposal, contract) in the project's deal-stage configuration
  - slot: rep_user
    kind: attribute
    meaning: Sales rep user records used for per-rep breakdown
  steps:
  - id: s1
    builds: report
    uses:
    - closed_won_deal
    - deal_stage_change
    - quota_target
    - late_stage_definition
    - rep_user
    - trailing_periods
    - coverage_minimum
    - coverage_risk_threshold
    - projection_window
    - forecast_accuracy_band
    - low_attainment_streak
    instruction: 'Create an Insights report titled "Forecast vs Actual vs Quota" with monthly granularity over the trailing
      {trailing_periods} quota periods plus the current and next period, broken down by owner. Series A: sum of {closed_won_deal.amount}
      per period, labeled "Actual Closed-Won" in dollars. Series B: sum of the most recent open-deal amount per {deal_stage_change.deal_id}
      (from {deal_stage_change.amount}) multiplied by the historical close rate of its current stage, for deals whose {deal_stage_change.close_date}
      falls in the period, labeled "Weighted Forecast" in dollars. Series C: the quota target for the period from {quota_target},
      labeled "Quota Target" in dollars; if {quota_target} is not configured, omit Series C and Series D and show only Series
      A and B. Series D: Series A divided by Series C times 100, labeled "Quota Attainment" in percent. Series E: sum of all
      open-deal amounts divided by Series C, labeled "Pipeline Coverage Ratio". Series F: sum of deal amount where {deal_stage_change.close_date}
      is within the next {projection_window} and the stage is in {late_stage_definition}, labeled "Projected Close (Next 30d)"
      in dollars. Chart: combo chart with Series A and B as bars, Series C as a horizontal target line, Series D as a secondary-axis
      callout, Series E as a separate KPI tile. Compare each period with the previous period and the same period last year.
      Annotate the {coverage_minimum}:1 minimum coverage benchmark (healthy at 4 to 5:1, shortfall below 2:1). Flag any period
      where Series B significantly exceeds Series A as a forecast-accuracy issue. Flag any rep whose pipeline coverage ratio
      is below {coverage_risk_threshold}:1. Highlight any run of {low_attainment_streak} or more consecutive periods below
      100% attainment. Add a forecast accuracy metric: absolute value of (Series A minus Series B) divided by Series A times
      100, over the trailing {trailing_periods} periods, flagged when it exceeds {forecast_accuracy_band}%.'
---

# Forecast versus quota

Slash command: /forecast-vs-actual-quota

## Step 1: Compare closed, forecast and quota

Create an Insights report called "Forecast vs Actual vs Quota".
Series A: Sum of Deal won.amount per period (closed-won revenue), unit: $, label: "Actual Closed-Won"
Series B: Sum of (open-deal amount × historical close-rate of current stage) for deals with close_date in the period: the weighted forecast, unit: $, label: "Weighted Forecast"
Series C: Workspace-configured quota target for the period, unit: $, label: "Quota Target"
 - Default: pulled from a workspace-level quota attribute (per-period dollar target). If unconfigured, recipe degrades gracefully and surfaces just A and B.
Series D: Computed: Series A / Series C × 100, unit: %, label: "Quota Attainment"
Series E: Computed: (Sum of all open-deal amounts) / Series C, label: "Pipeline Coverage Ratio"
 - The canonical 3:1 ratio benchmark: pipeline-to-quota of 3x is the industry minimum for reliable close.
Series F: Computed: Sum of deal amount where close_date IS within next 30 days AND stage is in late-stage (negotiation/proposal/contract), unit: $, label: "Projected Close (Next 30d)"
Time granularity: Monthly (or per quota period: quarterly for most B2B teams)
Time range: Trailing 4 quota periods + current + next period (forward-looking forecast)
Breakdown: By owner_id (per-rep): pushed down so each rep's forecast/actual/quota is visible
Compare: Previous period AND year-over-year same-period
Chart type: Combo chart: Series A (actual) and B (forecast) as bars, Series C (quota) as a horizontal target line, Series D (attainment %) on a secondary axis as a callout, Series E (coverage ratio) as a separate KPI tile
Annotations:
- Add the canonical pipeline coverage benchmark: 3:1 minimum, 4-5:1 healthy, <2:1 indicates pipeline shortfall.
- Flag any period where forecast (Series B) significantly exceeded actual (Series A): forecast-accuracy issue, investigate which deals slipped.
- Flag any rep whose pipeline coverage ratio fell below 2:1 (acute risk for next period).
- Highlight the period attainment trend: 4+ consecutive periods below 100% attainment indicates either quota is set too aggressively or systematic execution issues.
- Surface forecast accuracy as an explicit metric: |Actual − Forecast| / Actual × 100 over trailing 4 periods. Top-quartile sales orgs forecast within ±10%; below ±20% accuracy indicates the forecasting process needs refinement.
Use case: the canonical sales VP / CRO weekly report. Pipeline coverage ratio (Series E) is the most-cited B2B sales KPI; forecast accuracy is the leading indicator of sales-process maturity.
Taxonomy notes:
- Deal won.amount and Deal won.close_date are canonical properties.
- Deal stage changed has new_stage and amount per state change; "current open-deal amount" comes from the most-recent Deal stage changed.amount per deal_id.
- owner_id is a canonical property on Deal created and Deal stage changed; also on Users object.
- IMPORTANT: quota target dependency: this recipe assumes the workspace has quota targets configured per period per rep, OR a workspace-level aggregate quota. If neither is configured, Series C and Series D return null and the report renders Series A, B, E, F only. Sales teams typically inject quota targets via HubSpot/Salesforce sync or as a manual workspace-level attribute.
- "Late-stage" classification for Series F (Projected Close) follows the project's deal-stage configuration; standard convention is the final 2-3 stages before Deal won/Deal lost.
