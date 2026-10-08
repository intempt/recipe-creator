---
description: Report active-user counts over time to monitor engagement trends.
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

# Daily, weekly and monthly stickiness

Slash command: /stickiness-ratios-dau-wau-mau

## Step 1: Track daily against monthly use

Create an Insights report called "DAU / WAU / MAU Stickiness".
Series A: Event "session_start", aggregation: Count Unique Users, time granularity: Daily, label: "DAU"
Series B: Event "session_start", aggregation: Count Unique Users, rolling 7-day window, label: "WAU"
Series C: Event "session_start", aggregation: Count Unique Users, rolling 28-day window, label: "MAU"
Series D: Computed: Series A / Series B × 100, unit: %, label: "DAU/WAU Stickiness"
Series E: Computed: Series A / Series C × 100, unit: %, label: "DAU/MAU Stickiness"
Time granularity: Daily (smooth Series D and E with 7-day rolling average to reduce noise)
Time range: Last 90 days
Breakdown: By plan_name: resolved from the user's most-recent active subscription
Compare: Year-over-year (same 90-day window prior year)
Chart type: Dual-axis: left axis user counts (A/B/C as lines), right axis stickiness % (D and E as lines)
Annotations:
- Add benchmarks: DAU/MAU ≥ 20% is "good" for B2B SaaS; ≥ 50% is best-in-class.
- Add benchmarks: DAU/WAU ≥ 50% indicates strong daily-habit usage.
- Flag any plan where DAU/MAU stickiness dropped >3 percentage points vs. previous period (engagement erosion: leading indicator of churn).
- Flag any plan where MAU is growing but DAU is flat (acquiring users who aren't engaging).
Stickiness leads retention by 1-2 quarters; it's the canary in the coal mine.
Taxonomy notes:
- session_start is the canonical "user is active" event. Alternative: identify, but session_start is more frequent and reliable.
- plan_tier as a User property does not exist; plan_name comes from the user's subscription_created.
