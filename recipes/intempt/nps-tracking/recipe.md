---
id: nps-tracking
title: NPS tracking
slash_command: /nps-tracking
group: Reports
owner: intempt
curator: aman
summary: Tracks your Net Promoter Score month by month with the promoter, passive and detractor split
  behind it.
description: >-
  NPS score over time from feedback_submitted with promoter/passive/detractor decomposition and trend.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - all
  complexity: quick
  executionMode: live
  tags:
    - insights
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Score NPS each month"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Score NPS each month
    summary: >-
      Monthly counts of promoters scoring 9 or 10, passives on 7 or 8 and detractors at 6 or below from
      NPS survey responses, with the resulting score, a 90 day rolling average, a year over year overlay
      and industry benchmarks.
    builds: report
    description: |-
      Create an Insights report called "NPS Tracking".
      Series A: Event "feedback_submitted" where survey_type = "nps", aggregation: Count where score >= 9 (promoters), label: "Promoters"
      Series B: Event "feedback_submitted" where survey_type = "nps", aggregation: Count where score is between 7 and 8 (passives), label: "Passives"
      Series C: Event "feedback_submitted" where survey_type = "nps", aggregation: Count where score <= 6 (detractors), label: "Detractors"
      Series D: Computed NPS: (Series A − Series C) / (Series A + Series B + Series C) × 100, unit: # (NPS is reported as a score from -100 to +100), label: "NPS Score"
      Series E: Trailing 90-day rolling NPS for trend smoothing, label: "NPS (90-day rolling)"
      Time granularity: Monthly
      Time range: Last 12 months
      Breakdown for the trend chart: optional plan_name (saas) or first-purchase product category (ecommerce)
      Compare: Year-over-year
      Chart type: Stacked bar chart for Series A/B/C distribution per month, with Series D (NPS) as a line on a secondary axis. Use color: Promoters green, Passives gray, Detractors red.
      Annotations:
      - Add benchmarks per industry: B2B SaaS median NPS is 30; top-quartile 50+; SaaS world-class 70+. eCommerce DTC median 30: 40; top-quartile 60+. Below 0 indicates a serious problem (more detractors than promoters).
      - Flag any month where Series D dropped >10 points vs. trailing-3-month average.
      - Highlight the % of detractors who left feedback_text: these are the highest-leverage voice-of-customer signals (act on the qualitative comments, not just the score).
      - Highlight any plan/segment whose NPS is significantly below the blended average (>15 points lower): these are the audiences where product-market fit is weakest.
      - Surface response volume per month: a falling NPS from a small sample (<30 responses/month) may not be statistically meaningful. Add a "low confidence" flag when monthly sample size <30.
      Use case: every business tracks NPS but most never visualize the underlying promoter/passive/detractor distribution shifts that drive the score. A score of 30 with rising detractors is very different from a score of 30 with falling passives: same headline number, opposite direction.
      Taxonomy notes:
      - feedback_submitted has score, sentiment, survey_type, feedback_text, masterID, submitted_at: all canonical.
      - This recipe assumes the workspace uses survey_type = "nps" to discriminate NPS surveys from other feedback. If the project uses a different value (e.g. "net_promoter"), adjust the filter.
      - score is expected to be 0: 10 numeric. Workspaces emitting feedback_submitted from custom surveys may need to validate score range matches NPS convention.
      - If the workspace doesn't have feedback_submitted events flowing reliably from their NPS tool (Delighted, AskNicely, Wootric, custom in-app surveys), this recipe degrades to "no data." Recommend ensuring NPS-survey integration is configured.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# NPS tracking

Tracks your Net Promoter Score month by month with the promoter, passive and detractor split behind it.

## Steps

1. **Score NPS each month** (builds report)

   Monthly counts of promoters scoring 9 or 10, passives on 7 or 8 and detractors at 6 or below from NPS survey responses, with the resulting score, a 90 day rolling average, a year over year overlay and industry benchmarks.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Score NPS each month"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
