---
frontmatter_id: win-rate-trend
slash_command: /win-rate-trend
description: Tracks win rate month by month with a 90 day rolling line, so you can see the direction without the noise of a single month.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tracks monthly win rate with a 90-day rolling trend line, year-over-year comparison, per-source breakdown, and
    alerts for sharp drops or sustained decline.
  parameters:
  - name: time_range
    type: duration
    label: Time range to chart
    default: 18 mo
    required: false
  - name: rolling_window
    type: duration
    label: Rolling window for trend line
    default: 90 d
    required: false
  - name: top_sources
    type: number
    label: Number of top sources to break down
    default: 5
    required: false
  - name: benchmark_median
    type: number
    label: Median benchmark win rate (%)
    default: 18
    required: false
  - name: benchmark_top_quartile
    type: number
    label: Top-quartile benchmark win rate (%)
    default: 30
    required: false
  - name: benchmark_low
    type: number
    label: Low-performance threshold win rate (%)
    default: 15
    required: false
  - name: acute_drop_points
    type: number
    label: Acute monthly drop threshold (percentage points)
    default: 5
    required: false
  - name: comparison_months
    type: number
    label: Trailing months for drop baseline
    default: 3
    required: false
  - name: decline_periods
    type: number
    label: Consecutive declining periods that flag a durable trend
    default: 3
    required: false
  - name: source_divergence_points
    type: number
    label: Source divergence threshold (percentage points)
    default: 10
    required: false
  requirements:
  - slot: deal_won_event
    kind: event
    meaning: A deal was marked as won
    properties:
    - name: amount
      type: number
      meaning: Deal amount
      optional: true
    - name: primary_user_id
      type: string
      meaning: Primary user linked to the deal
      optional: false
    - name: owner_id
      type: string
      meaning: Deal owner
      optional: true
    - name: close_date
      type: date
      meaning: Date the deal closed
      optional: false
    - name: currency
      type: string
      meaning: Deal currency
      optional: true
  - slot: deal_lost_event
    kind: event
    meaning: A deal was marked as lost
    properties:
    - name: amount
      type: number
      meaning: Deal amount
      optional: true
    - name: primary_user_id
      type: string
      meaning: Primary user linked to the deal
      optional: false
    - name: owner_id
      type: string
      meaning: Deal owner
      optional: true
    - name: close_date
      type: date
      meaning: Date the deal closed
      optional: false
    - name: currency
      type: string
      meaning: Deal currency
      optional: true
  - slot: user_utm_source
    kind: attribute
    meaning: The UTM source attribute on users used for lead source attribution
  steps:
  - id: s1
    builds: report
    uses:
    - deal_won_event
    - deal_lost_event
    - user_utm_source
    - time_range
    - rolling_window
    - top_sources
    - benchmark_median
    - benchmark_top_quartile
    - benchmark_low
    - acute_drop_points
    - comparison_months
    - decline_periods
    - source_divergence_points
    instruction: 'Track win rate over time. Create an Insights report called "Win Rate Trend". Series A: event {deal_won_event},
      aggregation Count. Series B: event {deal_lost_event}, aggregation Count. Series C: computed as Series A / (Series A
      + Series B) × 100, unit %, label "Win Rate". Series D: trailing {rolling_window} rolling win rate as a smoother, label
      "Win Rate ({rolling_window} rolling)". Time granularity: monthly, cohorted by close month. Time range: last {time_range},
      so two trailing-12-month windows can be compared. Breakdown: by {user_utm_source} via the deal''s primary_user_id (lead
      source attribution), top {top_sources} sources, with an optional secondary line per source. Compare: year-over-year
      (same month previous year) as a dotted overlay. Chart type: line chart with Series C (monthly) and Series D (rolling)
      as primary lines, plus optional per-source overlay lines. Annotations: add benchmark lines at {benchmark_median}% (median
      B2B SaaS win rate, cited as Gartner 18-22%), {benchmark_top_quartile}%+ (top quartile), and {benchmark_low}% (below
      this indicates lead-quality or ICP issues). Flag any month where Series C dropped more than {acute_drop_points} percentage
      points versus the trailing {comparison_months}-month average. Flag when Series D has declined for {decline_periods}
      or more consecutive periods. Show the trailing-12-month win rate versus the prior 12 months as a single before/after
      callout. Highlight any source whose per-source win rate differs from the blended average by more than {source_divergence_points}
      percentage points.'
---

# Win rate trend

Slash command: /win-rate-trend

## Step 1: Track win rate over time

Create an Insights report called "Win Rate Trend".
Series A: Event "Deal won", aggregation: Count
Series B: Event "Deal lost", aggregation: Count
Series C: Computed: Series A / (Series A + Series B) × 100, unit: %, label: "Win Rate"
Series D: Trailing 90-day rolling win rate (smoother for trend reading), label: "Win Rate (90-day rolling)"
Time granularity: Monthly (cohort by close month)
Time range: Last 18 months (so two trailing-12-month windows can be compared)
Breakdown: By Users.UTM source (lead source attribution via the deal's primary_user_id): top 5 sources, optional secondary line per source
Compare: Year-over-year (same month previous year, dotted overlay)
Chart type: Line chart with Series C (monthly) and Series D (rolling) as primary lines, plus optional per-source overlay lines
Annotations:
- Add benchmark lines: median B2B SaaS win rate is 18: 22% (Gartner); top-quartile is 30%+; below 15% indicates either lead-quality or ICP issues.
- Flag any month where Series C dropped >5 percentage points vs. the trailing-3-month average (acute decline: investigate that month's sales activity, comp changes, market events).
- Flag if Series D (90-day rolling) has been declining for 3+ consecutive periods (durable downward trend, not noise).
- Surface the trailing-12-month win rate vs. the prior 12 months as a single before/after callout: the headline number for board reporting.
- Highlight any source whose per-source win rate diverges materially (>10pts) from the blended average: outlier channels deserve investigation.
Use case: the win-rate trend that goes on the RevOps dashboard's headline KPI strip. Distinct from win-loss-analysis (which is a bar chart with breakdowns by source/reason); this is the single metric over time.
Taxonomy notes:
- Deal won and Deal lost are canonical events. Both carry amount, primary_user_id, owner_id, close_date, currency.
- For workspaces using deal_closed_won / deal_closed_lost (alternative integration naming), substitute those.
- Source attribution requires resolving primary_user_id to Users.UTM source.
