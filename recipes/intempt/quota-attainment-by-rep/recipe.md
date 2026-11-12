---
frontmatter_id: quota-attainment-by-rep
slash_command: /quota-attainment-by-rep
description: See revenue by rep to compare each rep's closed revenue over the selected period.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows each sales rep's closed revenue against their assigned quota by quarter, with attainment %, pipeline coverage,
    trends, and risk flags.
  parameters:
  - name: time_granularity
    type: enum
    label: Time granularity
    default: quarter
    required: false
    options:
    - month
    - quarter
    - year
  - name: lookback_quarters
    type: number
    label: Quarters of history to show
    default: 4
    required: false
  - name: attainment_green_pct
    type: number
    label: Green threshold (attainment %)
    default: 100
    required: false
  - name: attainment_yellow_pct
    type: number
    label: Yellow threshold (attainment %)
    default: 80
    required: false
  - name: acute_risk_attainment_pct
    type: number
    label: Acute risk attainment threshold (%)
    default: 50
    required: false
  - name: acute_risk_coverage_ratio
    type: number
    label: Acute risk pipeline coverage ratio
    default: 2
    required: false
  - name: top_bottom_gap_multiple
    type: number
    label: Top-to-median gap multiple that triggers a flag
    default: 3
    required: false
  - name: ramp_quarters
    type: number
    label: Quarters a rep is treated as ramping
    default: 2
    required: false
  - name: top_revenue_reps_count
    type: number
    label: Number of top reps by absolute revenue to highlight
    default: 3
    required: false
  requirements:
  - slot: deal_won_event
    kind: event
    meaning: A deal was marked won (closed-won) by a sales rep
    properties:
    - name: owner_id
      type: string
      meaning: The rep who owns the won deal
      optional: false
    - name: amount
      type: number
      meaning: Dollar amount of the won deal
      optional: false
  - slot: deal_stage_changed_event
    kind: event
    meaning: A deal's stage was changed, recording its new stage and amount
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
    - name: new_stage
      type: string
      meaning: The stage the deal moved into
      optional: false
    - name: amount
      type: number
      meaning: Deal amount at the time of the stage change
      optional: false
  - slot: rep_quota_attribute
    kind: attribute
    meaning: A per-rep quota target amount for each period, stored on the user record or synced from a CRM
  - slot: crm_quota_integration
    kind: integration
    meaning: A connected CRM (such as HubSpot or Salesforce) that syncs per-rep quota targets
    optional: true
    channel: hubspot
  - slot: ramping_reps_segment
    kind: segment
    meaning: Reps who are in their first quarters of selling and not yet expected to hit full quota
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - deal_won_event
    - rep_quota_attribute
    - crm_quota_integration
    - deal_stage_changed_event
    - ramping_reps_segment
    - time_granularity
    - lookback_quarters
    - attainment_green_pct
    - attainment_yellow_pct
    - acute_risk_attainment_pct
    - acute_risk_coverage_ratio
    - top_bottom_gap_multiple
    - ramp_quarters
    - top_revenue_reps_count
    instruction: 'Create an Insights report titled "Quota Attainment by Rep". Use these series: (A) Revenue Closed by Rep:
      sum of {deal_won_event.amount} per period, grouped by {deal_won_event.owner_id}, unit dollars. (B) Quota Target: the
      per-rep quota for each period taken from {rep_quota_attribute} or from {crm_quota_integration}, unit dollars. (C) Quota
      Attainment %: Series A divided by Series B multiplied by 100, unit percent. (D) Pipeline Coverage Ratio per Rep: the
      sum of open-deal amounts per rep divided by Series B, where open-deal amount is the most recent {deal_stage_changed_event.amount}
      per {deal_stage_changed_event.deal_id} whose {deal_stage_changed_event.new_stage} is not a closed stage. (E) Rolling
      12-month attainment: trailing twelve-month average of Series C per rep. Time granularity is {time_granularity}, covering
      the last {lookback_quarters} quarters plus the current period. Break down by rep (owner). Compare against the previous
      quarter and the same quarter of the prior year. Chart: sortable horizontal bar chart per rep with bar = Series C and
      a 100% target line, with labels showing absolute closed revenue and quota; secondary view is a per-rep trend chart over
      the lookback window. Provide three sort modes: by Quota Attainment descending ("Top Performers"), by Pipeline Coverage
      Ratio ascending ("At-Risk Reps"), and by rolling 12-month attainment trend ("Consistent Performers"). Color-code Series
      C: green at or above {attainment_green_pct}%, yellow from {attainment_yellow_pct}% up to but excluding {attainment_green_pct}%,
      red below {attainment_yellow_pct}%. Flag any rep below {acute_risk_attainment_pct}% attainment whose pipeline coverage
      is below {acute_risk_coverage_ratio}:1 as acute performance risk requiring immediate manager intervention. Flag when
      the top performer''s attainment is at least {top_bottom_gap_multiple} times the median rep''s attainment, as a sign
      of skill or territory imbalance. Separate reps in their first {ramp_quarters} quarters (from {ramping_reps_segment})
      into their own group and exclude them from the team attainment percentage. Highlight the top {top_revenue_reps_count}
      reps by absolute Revenue Closed regardless of quota.'
---

# Quota attainment by rep

Slash command: /quota-attainment-by-rep

## Step 1: Rank reps on quota hit

Create an Insights report called "Quota Attainment by Rep".
Series A: Sum of Deal won.amount per period, grouped by owner_id, unit: $, label: "Revenue Closed by Rep"
Series B: Workspace-configured quota per rep per period, unit: $, label: "Quota Target"
 - Sourced from a per-rep quota attribute on the Users object OR from an external integration (HubSpot/Salesforce typically syncs this).
Series C: Computed: Series A / Series B × 100, unit: %, label: "Quota Attainment %"
Series D: Sum of all open-deal amounts (current pipeline) per rep / Series B = "Pipeline Coverage Ratio per Rep"
Series E: Trailing-12-month rolling Series C per rep: the durable performance signal vs. period noise
Time granularity: Quarterly (the standard quota period for B2B)
Time range: Last 4 quarters + current quarter
Breakdown: By owner_id (per-rep)
Compare: Previous quarter AND same quarter prior year
Chart type: Sortable horizontal bar chart per rep: bar = Series C (attainment %), with target line at 100%, annotation showing absolute closed revenue and quota; secondary view: trend chart per rep over last 4 quarters
Sort modes:
- By Quota Attainment (descending) to "Top Performers"
- By Pipeline Coverage Ratio (ascending) to "At-Risk Reps" (low coverage = next-quarter shortfall)
- By Revenue Trend (rolling-12mo) to "Consistent Performers"
Annotations:
- Color-code attainment: green ≥100%, yellow 80-99%, red <80%. Industry benchmark: top-quartile sales orgs have 60%+ of reps at ≥100% attainment; struggling teams have <40%.
- Flag any rep at <50% quota attainment with <2:1 coverage ratio: acute performance risk; needs immediate manager intervention.
- Flag the gap between top-performer and median: a 3x+ gap indicates skill/territory imbalance worth rebalancing.
- Surface "ramp" reps (in their first 2 quarters) separately: they're not expected to hit full quota and shouldn't dilute the team-attainment percentage.
- Highlight the top 3 reps by absolute revenue (not just %): these are the deal-making heavyweights regardless of quota assignment.
Use case: distinct from rep-activity-leaderboard (which is calls/emails leading indicators): this is the lagging revenue outcome compared to assigned quota. Sales VPs use these together: activity diagnoses, attainment evaluates.
Taxonomy notes:
- Deal won.owner_id and Deal won.amount are canonical properties.
- IMPORTANT (quota dependency: same caveat as forecast-vs-actual-quota) quota targets must be configured. Without quota data, Series B/C return null and the report degrades to absolute revenue-by-rep ranking only.
- "Open deal amount" for Series D comes from the most-recent Deal stage changed.amount per deal_id where new_stage is not in closed states.
