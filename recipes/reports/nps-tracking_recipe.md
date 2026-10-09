---
name: nps-tracking
description: |
  Use when a user mentions "nps tracking", or asks for related help. NPS score over time from survey responses with promoter/passive/detractor decomposition and trend.
arguments: []
intempt:
  id: nps-tracking
  version: 1.0.0
  slashCommand: /nps-tracking
  group: Reports
  title: "NPS tracking"
  shortDescription: "Tracks your Net Promoter Score month by month with the promoter, passive and detractor split behind it."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [all]
    complexity: quick
    executionMode: live
    tags: [insights]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Score NPS each month"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Monthly counts of promoters scoring 9 or 10, passives on 7 or 8 and detractors at 6 or below from NPS survey responses, with the resulting score, a 90 day rolling average, a year over year overlay and industry benchmarks."
      prompt: |
        Create an Insights report called "NPS Tracking".

        Series A: Feedback submitted events where survey type is "nps", aggregation: Count where score >= 9 (promoters), label: "Promoters"
        Series B: Feedback submitted events where survey type is "nps", aggregation: Count where score is between 7 and 8 (passives), label: "Passives"
        Series C: Feedback submitted events where survey type is "nps", aggregation: Count where score <= 6 (detractors), label: "Detractors"
        Series D: Computed NPS: (Series A − Series C) / (Series A + Series B + Series C) × 100, unit: # (NPS is reported as a score from -100 to +100), label: "NPS Score"
        Series E: Trailing 90-day rolling NPS for trend smoothing, label: "NPS (90-day rolling)"

        Time granularity: Monthly
        Time range: Last 12 months
        Breakdown for the trend chart: optional Plan (saas) or first-purchase product category (ecommerce)
        Compare: Year-over-year
        Chart type: Stacked bar chart for Series A/B/C distribution per month, with Series D (NPS) as a line on a secondary axis. Use color: Promoters green, Passives gray, Detractors red.

        Annotations:
        - Add benchmarks per industry: B2B SaaS median NPS is 30; top-quartile 50+; SaaS world-class 70+. eCommerce DTC median 30: 40; top-quartile 60+. Below 0 indicates a serious problem (more detractors than promoters).
        - Flag any month where Series D dropped >10 points vs. trailing-3-month average.
        - Highlight the % of detractors who left feedback text: these are the highest-leverage voice-of-customer signals (act on the qualitative comments, not just the score).
        - Highlight any plan/segment whose NPS is significantly below the blended average (>15 points lower): these are the audiences where product-market fit is weakest.
        - Surface response volume per month: a falling NPS from a small sample (<30 responses/month) may not be statistically meaningful. Add a "low confidence" flag when monthly sample size <30.

        Use case: every business tracks NPS but most never visualize the underlying promoter/passive/detractor distribution shifts that drive the score. A score of 30 with rising detractors is very different from a score of 30 with falling passives: same headline number, opposite direction.

        Survey assumptions:
        - This recipe assumes the workspace marks NPS responses with a survey type of "nps". If the project uses a different value (e.g. "net_promoter"), adjust the filter.
        - The score is expected to be numeric from 0 to 10. Responses from custom surveys may need their score range validated against the NPS convention.
        - If NPS survey responses are not flowing reliably from the NPS tool (Delighted, AskNicely, Wootric, custom in-app surveys), this recipe degrades to "no data." Recommend ensuring the NPS-survey integration is configured.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# NPS tracking

Tracks your Net Promoter Score month by month with the promoter, passive and detractor split behind it.

## What it does

1. **Score NPS each month** (`build_insights_report`)

   Monthly counts of promoters scoring 9 or 10, passives on 7 or 8 and detractors at 6 or below from NPS survey responses, with the resulting score, a 90 day rolling average, a year over year overlay and industry benchmarks.

## What you end up with

- **report** (report): Report produced by this recipe.
