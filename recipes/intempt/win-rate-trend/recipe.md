---
description: Tracks win rate month by month with a 90 day rolling line, so you can see the direction without the noise of a single month.
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

# Win rate trend

Slash command: /win-rate-trend

## Step 1: Track win rate over time

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
