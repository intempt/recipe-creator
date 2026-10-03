---
id: win-rate-trend
title: Win rate trend
slash_command: /win-rate-trend
group: Reports
owner: intempt
summary: Tracks win rate month by month with a 90 day rolling line, so you can see the direction without
  the noise of a single month.
description: >-
  Win rate over time as a single tracking metric: surfaces GTM health trajectory without the breakdown
  overhead of win-loss-analysis.
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
    - A new report, from step 1 "Track win rate over time"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Track win rate over time
    summary: >-
      Monthly win rate from won and lost deals over the last 18 months, with a 90 day rolling average
      and an optional line per lead source. Benchmarks 18 to 22% as median and 30% as top quartile, and
      flags three consecutive periods of decline.
    builds: report
    description: |-
      Create an Insights report called "Win Rate Trend".
      Series A: Event "deal_won", aggregation: Count
      Series B: Event "deal_lost", aggregation: Count
      Series C: Computed: Series A / (Series A + Series B) × 100, unit: %, label: "Win Rate"
      Series D: Trailing 90-day rolling win rate (smoother for trend reading), label: "Win Rate (90-day rolling)"
      Time granularity: Monthly (cohort by close month)
      Time range: Last 18 months (so two trailing-12-month windows can be compared)
      Breakdown: By Users.utm_source (lead source attribution via the deal's primary_user_id): top 5 sources, optional secondary line per source
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
      - deal_won and deal_lost are canonical events. Both carry amount, primary_user_id, owner_id, close_date, currency.
      - For workspaces using deal_closed_won / deal_closed_lost (alternative integration naming), substitute those.
      - Source attribution requires resolving primary_user_id to Users.utm_source.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Win rate trend

Tracks win rate month by month with a 90 day rolling line, so you can see the direction without the noise of a single month.

## Steps

1. **Track win rate over time** (builds report)

   Monthly win rate from won and lost deals over the last 18 months, with a 90 day rolling average and an optional line per lead source. Benchmarks 18 to 22% as median and 30% as top quartile, and flags three consecutive periods of decline.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Track win rate over time"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
