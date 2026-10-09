---
description: Shows weekly active users and monthly active users, plus the WAU to MAU ratio, to indicate engagement stickiness.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - media
---

# Weekly active users

Slash command: /weekly-active-users-trend

## Step 1: Track weekly users and stickiness

Create an Insights report called "Weekly Active Users Trend".
Series A: Event "Session start", aggregation: Count Unique Users, time granularity: Weekly, label: "WAU"
 (alternative: use "identify" if the workspace uses identify as the active-user signal)
Series B: Event "Session start", aggregation: Count Unique Users, rolling 28-day window, label: "MAU"
Series C: Computed: Series A (WAU) / Series B (MAU) × 100, unit: %, label: "Stickiness (WAU/MAU)"
Time granularity: Weekly
Time range: Last 12 weeks
Breakdown: By Plan: derive from each user's most-recent active Subscription started.Plan
Compare: Previous period (prior 12 weeks)
Chart type: Dual-axis: left axis user counts (WAU/MAU as lines), right axis stickiness % (line)
Annotations:
- Add a horizontal benchmark line at 20% stickiness (industry "good" for B2B SaaS).
- Add a horizontal benchmark at 50% (top-quartile, near-daily-use products).
- Highlight any plan where stickiness dropped >3 points vs. previous period.
- Flag any plan where WAU is growing but stickiness is falling (acquiring users but losing engagement).
Stickiness is the leading indicator of retention; raw WAU growth without stickiness growth is a vanity metric.
Taxonomy notes:
- Session start is canonical and carries device_type, country, UTM source. "user_active" as an event does not exist; Session start (or identify) is the active-user signal.
- plan_tier as a property does not exist; Plan on Subscription started is the canonical plan attribute.
