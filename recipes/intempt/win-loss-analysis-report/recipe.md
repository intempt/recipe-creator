---
description: Breaks closed deals into won and lost by lead source, deal size and the stage they died at, so the pattern is visible.
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

# Win loss analysis

Slash command: /win-loss-analysis-report

## Step 1: Break down wins against losses

Create an Insights report called "Win-Loss Analysis".
Series A: Event "deal_won", aggregation: Count, label: "Won"
Series B: Event "deal_lost", aggregation: Count, label: "Lost"
Series C: Computed: Series A / (Series A + Series B) × 100, unit: %, label: "Win Rate"
Series D: Sum of deal amount for won deals (revenue won)
Series E: Sum of deal amount for lost deals (revenue lost)
Breakdown: By Users.utm_source (lead source attribution via the deal's primary_user_id)
Time range: Last 6 months of closed deals
Compare: Previous period (prior 6 months)
Chart type: Side-by-side bar chart for won vs. lost counts with win-rate % annotations, plus a separate breakdown by deal-size bucket (small <$10K, mid $10K-$50K, enterprise >$50K)
Also include a parallel "stage-at-loss" view:
- For deal_lost events, what was the previous_stage just before loss? Distribution shows whether deals die early (qualification mismatch) or late (close-stage objections)
Annotations:
- Flag the source with the highest win rate AND volume: the channel to scale.
- Flag the source with the lowest win rate but high volume: the channel with leakage; investigate ICP fit.
- Flag any deal-size bucket where win rate is below 25% (typically signals a sweet-spot mismatch: deals too big or too small for current sales motion).
- Highlight the dominant "stage at loss": late-stage losses suggest closing/competition issues; early-stage losses suggest qualification/ICP issues.
- Surface the average deal size of won vs. lost deals: if won deals are systematically smaller, the team is winning easy ones and losing hard ones (qualification or pricing strategy issue).
Use case: the canonical sales-team retro report. Most teams track pipeline and revenue but rarely systematically analyze why deals died. This recipe makes loss patterns visible.
Taxonomy notes:
- deal_won and deal_lost both have amount, primary_user_id, stage, close_date, owner_id, currency.
- deal_lost.previous_stage (or the last deal_stage_changed before deal_lost) gives stage-at-loss.
- Source attribution via the user's utm_source on the Users object linked through primary_user_id.
