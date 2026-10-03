---
id: weekly-active-users-trend
title: Weekly active users
slash_command: /weekly-active-users-trend
group: Reports
owner: intempt
summary: Shows weekly active users next to monthly, and the ratio between them, which tells you whether
  growth is real engagement or just signups.
description: >-
  WAU trend with WAU/MAU stickiness ratio: the standard PLG engagement view.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  complexity: quick
  executionMode: live
  tags:
    - insights
steps:
  - id: s1
    title: Track weekly users and stickiness
    summary: >-
      Weekly active users and a rolling 28 day figure over 12 weeks, with the ratio between them as a
      stickiness percentage split by plan. Benchmarks at 20% and 50% and flags plans where users grow
      but stickiness falls.
    builds: report
    description: |-
      Create an Insights report called "Weekly Active Users Trend".
      Series A: Event "session_start", aggregation: Count Unique Users, time granularity: Weekly, label: "WAU"
       (alternative: use "identify" if the workspace uses identify as the active-user signal)
      Series B: Event "session_start", aggregation: Count Unique Users, rolling 28-day window, label: "MAU"
      Series C: Computed: Series A (WAU) / Series B (MAU) × 100, unit: %, label: "Stickiness (WAU/MAU)"
      Time granularity: Weekly
      Time range: Last 12 weeks
      Breakdown: By plan_name: derive from each user's most-recent active subscription_created.plan_name
      Compare: Previous period (prior 12 weeks)
      Chart type: Dual-axis: left axis user counts (WAU/MAU as lines), right axis stickiness % (line)
      Annotations:
      - Add a horizontal benchmark line at 20% stickiness (industry "good" for B2B SaaS).
      - Add a horizontal benchmark at 50% (top-quartile, near-daily-use products).
      - Highlight any plan where stickiness dropped >3 points vs. previous period.
      - Flag any plan where WAU is growing but stickiness is falling (acquiring users but losing engagement).
      Stickiness is the leading indicator of retention; raw WAU growth without stickiness growth is a vanity metric.
      Taxonomy notes:
      - session_start is canonical and carries device_type, country, utm_source. "user_active" as an event does not exist; session_start (or identify) is the active-user signal.
      - plan_tier as a property does not exist; plan_name on subscription_created is the canonical plan attribute.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Weekly active users

Shows weekly active users next to monthly, and the ratio between them, which tells you whether growth is real engagement or just signups.

## Steps

1. **Track weekly users and stickiness** (builds report)

   Weekly active users and a rolling 28 day figure over 12 weeks, with the ratio between them as a stickiness percentage split by plan. Benchmarks at 20% and 50% and flags plans where users grow but stickiness falls.

## What you end up with

- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build report.
