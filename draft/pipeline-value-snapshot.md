---
description: Shows the value of your open pipeline today by summing your deal events, broken out by stage.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - b2b-saas
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
