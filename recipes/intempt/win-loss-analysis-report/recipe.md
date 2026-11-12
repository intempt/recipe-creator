---
frontmatter_id: win-loss-analysis-report
slash_command: /win-loss-analysis-report
description: Breaks closed deals into won and lost by lead source, deal size and the stage they died at, so the pattern is visible.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Splits closed deals into won and lost by lead source, deal size and stage at loss, with win rate, revenue and flags
    showing where to scale or fix the sales process.
  parameters:
  - name: lookback_period
    type: duration
    label: Analysis window for closed deals
    default: 6 m
    required: false
  - name: win_rate_alert_threshold
    type: number
    label: Deal-size win rate alert threshold (%)
    default: 25
    required: false
  - name: deal_size_small_max
    type: number
    label: Small deal upper bound (amount)
    default: 10000
    required: false
  - name: deal_size_enterprise_min
    type: number
    label: Enterprise deal lower bound (amount)
    default: 50000
    required: false
  requirements:
  - slot: deal_won_event
    kind: event
    meaning: A deal was marked as won (closed-won)
    properties:
    - name: amount
      type: number
      meaning: Deal amount
      optional: false
    - name: primary_user_id
      type: string
      meaning: ID of the primary user linked to the deal
      optional: false
    - name: stage
      type: string
      meaning: Deal stage at close
      optional: true
    - name: close_date
      type: date
      meaning: Date the deal closed
      optional: true
    - name: owner_id
      type: string
      meaning: Deal owner ID
      optional: true
    - name: currency
      type: string
      meaning: Deal currency
      optional: true
  - slot: deal_lost_event
    kind: event
    meaning: A deal was marked as lost (closed-lost)
    properties:
    - name: amount
      type: number
      meaning: Deal amount
      optional: false
    - name: primary_user_id
      type: string
      meaning: ID of the primary user linked to the deal
      optional: false
    - name: stage
      type: string
      meaning: Deal stage at close
      optional: true
    - name: previous_stage
      type: string
      meaning: Deal stage immediately before it was lost
      optional: false
    - name: close_date
      type: date
      meaning: Date the deal closed
      optional: true
    - name: owner_id
      type: string
      meaning: Deal owner ID
      optional: true
    - name: currency
      type: string
      meaning: Deal currency
      optional: true
  - slot: user_utm_source
    kind: attribute
    meaning: The UTM source recorded on a user, used as lead source attribution
  steps:
  - id: s1
    builds: report
    uses:
    - deal_won_event
    - deal_lost_event
    - user_utm_source
    - lookback_period
    instruction: 'Create an Insights report titled "Win-Loss Analysis". Series A: count of {deal_won_event}, label "Won".
      Series B: count of {deal_lost_event}, label "Lost". Series C: computed as Series A divided by (Series A plus Series
      B) multiplied by 100, unit %, label "Win Rate". Series D: sum of {deal_won_event.amount}, label "Revenue Won". Series
      E: sum of {deal_lost_event.amount}, label "Revenue Lost". Break down by {user_utm_source} (lead source via the deal''s
      {deal_won_event.primary_user_id} or {deal_lost_event.primary_user_id}). Time range: last {lookback_period} of closed
      deals. Compare against the previous period of equal length. Chart: side-by-side bars for Won vs Lost counts with Win
      Rate % annotations.'
---

# Win loss analysis

Slash command: /win-loss-analysis-report

## Step 1: Break down wins against losses

Create an Insights report called "Win-Loss Analysis".
Series A: Event "Deal won", aggregation: Count, label: "Won"
Series B: Event "Deal lost", aggregation: Count, label: "Lost"
Series C: Computed: Series A / (Series A + Series B) × 100, unit: %, label: "Win Rate"
Series D: Sum of deal amount for won deals (revenue won)
Series E: Sum of deal amount for lost deals (revenue lost)
Breakdown: By Users.UTM source (lead source attribution via the deal's primary_user_id)
Time range: Last 6 months of closed deals
Compare: Previous period (prior 6 months)
Chart type: Side-by-side bar chart for won vs. lost counts with win-rate % annotations, plus a separate breakdown by deal-size bucket (small <$10K, mid $10K-$50K, enterprise >$50K)
Also include a parallel "stage-at-loss" view:
- For Deal lost events, what was the previous_stage just before loss? Distribution shows whether deals die early (qualification mismatch) or late (close-stage objections)
Annotations:
- Flag the source with the highest win rate AND volume: the channel to scale.
- Flag the source with the lowest win rate but high volume: the channel with leakage; investigate ICP fit.
- Flag any deal-size bucket where win rate is below 25% (typically signals a sweet-spot mismatch: deals too big or too small for current sales motion).
- Highlight the dominant "stage at loss": late-stage losses suggest closing/competition issues; early-stage losses suggest qualification/ICP issues.
- Surface the average deal size of won vs. lost deals: if won deals are systematically smaller, the team is winning easy ones and losing hard ones (qualification or pricing strategy issue).
Use case: the canonical sales-team retro report. Most teams track pipeline and revenue but rarely systematically analyze why deals died. This recipe makes loss patterns visible.
Taxonomy notes:
- Deal won and Deal lost both have amount, primary_user_id, stage, close_date, owner_id, currency.
- Deal lost.previous_stage (or the last Deal stage changed before Deal lost) gives stage-at-loss.
- Source attribution via the user's UTM source on the Users object linked through primary_user_id.
