---
id: win-loss-analysis-report
title: Win loss analysis
slash_command: /win-loss-analysis-report
group: Reports
owner: intempt
summary: Breaks closed deals into won and lost by lead source, deal size and the stage they died at, so
  the pattern is visible.
description: >-
  Won vs. lost deals broken down by lead source, deal size, and stage at loss: surfaces patterns in what's
  working.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - b2b
  complexity: quick
  executionMode: live
  tags:
    - insights
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Break down wins against losses"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Break down wins against losses
    summary: >-
      Won and lost deal counts and revenue over the last 6 months with the win rate, split by lead source
      and by deal size (under 10k, 10k to 50k, over 50k), plus the stage each lost deal was sitting in
      when it died.
    builds: report
    description: |-
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
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Win loss analysis

Breaks closed deals into won and lost by lead source, deal size and the stage they died at, so the pattern is visible.

## Steps

1. **Break down wins against losses** (builds report)

   Won and lost deal counts and revenue over the last 6 months with the win rate, split by lead source and by deal size (under 10k, 10k to 50k, over 50k), plus the stage each lost deal was sitting in when it died.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Break down wins against losses"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
