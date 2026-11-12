---
frontmatter_id: pipeline-value-snapshot
slash_command: /pipeline-value-snapshot
description: Shows the value of your open pipeline today by summing your deal events, broken out by stage.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows the value of your open pipeline today, summed from deal events and broken out by stage, with weighted forecast,
    concentration, and 30-day change callouts.
  parameters:
  - name: compare_window
    type: duration
    label: Comparison window for pipeline shift
    default: 30 d
    required: false
  - name: late_stage_threshold
    type: number
    label: Late-stage concentration flag threshold (%)
    default: 40
    required: false
  - name: early_stage_threshold
    type: number
    label: Early-stage concentration flag threshold (%)
    default: 40
    required: false
  - name: weighting_lookback
    type: duration
    label: Trailing window for historical stage win-rates
    default: 180 d
    required: false
  - name: min_closed_deals
    type: number
    label: Minimum closed deals needed to use historical win-rates
    default: 50
    required: false
  - name: fallback_early_weight
    type: number
    label: Fallback win weight for early stages (%)
    default: 10
    required: false
  - name: fallback_mid_weight
    type: number
    label: Fallback win weight for mid stages (%)
    default: 30
    required: false
  - name: fallback_late_weight
    type: number
    label: Fallback win weight for late stages (%)
    default: 70
    required: false
  requirements:
  - slot: deal_stage_event
    kind: event
    meaning: A deal's stage was changed in the CRM
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
    - name: amount
      type: number
      meaning: Deal value amount
      optional: false
    - name: new_stage
      type: string
      meaning: Stage the deal moved into
      optional: false
    - name: previous_stage
      type: string
      meaning: Stage the deal moved out of
      optional: false
    - name: currency
      type: string
      meaning: Currency of the deal amount
      optional: false
  - slot: deal_created_event
    kind: event
    meaning: A new deal was created in the CRM
    properties:
    - name: amount
      type: number
      meaning: Deal value amount at creation
      optional: false
  - slot: quota_target
    kind: attribute
    meaning: A sales quota target configured for the workspace
    optional: true
  - slot: open_stage_config
    kind: knowledge
    meaning: Project's deal stage configuration that classifies each stage as open or closed
  steps:
  - id: s1
    builds: report
    uses:
    - deal_stage_event
    - open_stage_config
    - compare_window
    - weighting_lookback
    - min_closed_deals
    - fallback_early_weight
    - fallback_mid_weight
    - fallback_late_weight
    - late_stage_threshold
    - early_stage_threshold
    instruction: 'Create an Insights report titled "Pipeline Value Snapshot". Series A: event {deal_stage_event}, scope the
      most recent state per {deal_stage_event.deal_id} where {deal_stage_event.new_stage} is an open stage according to {open_stage_config}
      (treat stages whose name matches won, lost, or closed as closed); aggregate as sum of {deal_stage_event.amount}, unit
      $, label "Open Pipeline Value". Series B: same as Series A, but multiply each open deal''s amount by the historical
      win-rate of its current stage, computed from deals closed within the trailing {weighting_lookback}; if fewer than {min_closed_deals}
      closed deals exist in that window, use fallback weights of {fallback_early_weight}% for early stages, {fallback_mid_weight}%
      for mid stages, and {fallback_late_weight}% for late stages and flag that the weighting is imprecise; label "Weighted
      Forecast". Series C: computed as Series A grouped by {deal_stage_event.new_stage}, divided by the Series A total, times
      100, unit %, label "Pipeline Concentration by Stage". Time range: current snapshot. Compare against the previous snapshot
      from {compare_window} ago. Chart: horizontal bar chart per stage with Series A as bar value, Series B as a secondary
      mark, and the previous-snapshot value as a dotted overlay. Annotations: if {quota_target} exists, show pipeline value
      to quota ratio; flag when late-stage (proposal/negotiation) share of Series A exceeds {late_stage_threshold}%; flag
      when early-stage (qualification/discovery) share exceeds {early_stage_threshold}%; highlight the largest single deal
      by {deal_created_event.amount}; add a callout stating the pipeline grew or shrank by $X (Y%) versus the comparison snapshot
      and name the primary driver as stage movement, new deals, or closed deals.'
---

# Pipeline value snapshot

Slash command: /pipeline-value-snapshot

## Step 1: Value open pipeline by stage

Create an Insights report called "Pipeline Value Snapshot".
Series A: Event "Deal stage changed", scope: most-recent state per deal_id where new_stage is in open stages (not in closed_won, closed_lost, or equivalent terminal stages), aggregation: Sum of "amount", unit: $, label: "Open Pipeline Value"
Series B: Same as A but with each deal's amount weighted by historical close-rate of its current stage (compute the historical win-rate per stage from trailing-180d closed deals, then multiply each open deal's amount by its current stage's win-rate), label: "Weighted Forecast"
Series C: Computed: Series A grouped by new_stage / Series A total × 100, unit: %, label: "Pipeline Concentration by Stage"
Time range: Current snapshot
Compare: Previous snapshot 30 days ago (point-in-time pipeline shift)
Breakdown for the chart view: By new_stage (current stage of each open deal)
Chart type: Horizontal bar chart per stage with Series A as the bar value, Series B as a secondary mark/line, and the previous-snapshot value as a dotted overlay
Annotations:
- Add the pipeline-value-to-quota ratio if the workspace has a quota target configured (otherwise skip).
- Flag if >40% of pipeline value is concentrated in late stages (proposal/negotiation): execution risk if any major deal slips.
- Flag if >40% of pipeline value is concentrated in early stages (qualification/discovery): pipeline thin on near-term close-able deals.
- Highlight the largest single deal in the pipeline (by Deal created.amount): single-deal concentration risk.
- Add a 30-day delta callout: "Pipeline grew/shrank by $X (Y%) vs. 30 days ago. Net change driven primarily by [stage_X movement / new deals / closed deals]."
Use case: the headline pipeline metric every sales VP and CRO looks at first thing each morning. Distinct from deal-velocity-by-stage (which is about how fast deals move): this is about how much money is currently in motion and where it sits.
Taxonomy notes:
- Deal stage changed carries amount, new_stage, previous_stage, deal_id, currency.
- "Open" vs "Closed" stage classification depends on the project's lead/deal stage configuration. Standard convention: closed stages are those whose name matches /won|lost|closed/i.
- Weighted forecast computation requires historical deal data; if trailing-180d closed-deal volume is insufficient (<50 deals), use a fallback weighting (early-stage 10%, mid 30%, late 70%) and flag the imprecision.
