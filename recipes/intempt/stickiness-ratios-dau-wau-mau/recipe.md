---
frontmatter_id: stickiness-ratios-dau-wau-mau
slash_command: /stickiness-ratios-dau-wau-mau
description: Report active-user counts over time to monitor engagement trends.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds a dashboard report tracking daily, weekly and monthly active users and their stickiness ratios over time,
    broken down by plan, with benchmark and warning flags.
  parameters:
  - name: reportName
    type: string
    label: Report name
    default: DAU / WAU / MAU Stickiness
    required: false
  - name: trendWindow
    type: duration
    label: Time range to show
    default: 90 d
    required: false
  - name: smoothingWindow
    type: duration
    label: Rolling average window for stickiness lines
    default: 7 d
    required: false
  - name: weeklyWindow
    type: duration
    label: Weekly active rolling window
    default: 7 d
    required: false
  - name: monthlyWindow
    type: duration
    label: Monthly active rolling window
    default: 28 d
    required: false
  - name: dauMauGoodThreshold
    type: number
    label: DAU/MAU 'good' benchmark (%)
    default: 20
    required: false
  - name: dauMauBestThreshold
    type: number
    label: DAU/MAU best-in-class benchmark (%)
    default: 50
    required: false
  - name: dauWauStrongThreshold
    type: number
    label: DAU/WAU strong habit benchmark (%)
    default: 50
    required: false
  - name: erosionThreshold
    type: number
    label: Stickiness drop that triggers an erosion flag (percentage points)
    default: 3
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product (marks the user as active)
    properties:
    - name: plan
      type: string
      meaning: Plan of the user's most recent active subscription at the time of the session
      optional: false
  - slot: subscription_plan_attribute
    kind: attribute
    meaning: The plan name on a user's most recent active subscription, used to break down activity by plan
  - slot: at_risk_plan_segment
    kind: segment
    meaning: Plans flagged for stickiness erosion or MAU growth without DAU growth
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - session_start_event
    - subscription_plan_attribute
    - reportName
    - trendWindow
    - smoothingWindow
    - weeklyWindow
    - monthlyWindow
    - dauMauGoodThreshold
    - dauMauBestThreshold
    - dauWauStrongThreshold
    - erosionThreshold
    instruction: 'Create an Insights report named "{reportName}". Add Series A: count unique users of {session_start_event}
      with daily time granularity, labeled "DAU". Add Series B: count unique users of {session_start_event} over a rolling
      {weeklyWindow} window, labeled "WAU". Add Series C: count unique users of {session_start_event} over a rolling {monthlyWindow}
      window, labeled "MAU". Add Series D: Series A divided by Series B times 100, unit %, labeled "DAU/WAU Stickiness". Add
      Series E: Series A divided by Series C times 100, unit %, labeled "DAU/MAU Stickiness". Use daily granularity and show
      the last {trendWindow}; smooth Series D and E with a {smoothingWindow} rolling average. Break down all series by {subscription_plan_attribute.plan},
      resolved from each user''s most recent active subscription. Compare with the same window one year earlier. Chart type:
      dual-axis, with user counts (A, B, C) as lines on the left axis and stickiness percentages (D, E) as lines on the right
      axis. Annotate benchmarks: DAU/MAU at or above {dauMauGoodThreshold}% is good for B2B SaaS and at or above {dauMauBestThreshold}%
      is best-in-class; DAU/WAU at or above {dauWauStrongThreshold}% indicates strong daily-habit usage. Flag any plan whose
      DAU/MAU stickiness dropped by more than {erosionThreshold} percentage points versus the previous period as engagement
      erosion. Flag any plan where MAU is rising while DAU is flat as acquiring users who are not engaging.'
---

# Daily, weekly and monthly stickiness

Slash command: /stickiness-ratios-dau-wau-mau

## Step 1: Track daily against monthly use

Create an Insights report called "DAU / WAU / MAU Stickiness".
Series A: Event "Session start", aggregation: Count Unique Users, time granularity: Daily, label: "DAU"
Series B: Event "Session start", aggregation: Count Unique Users, rolling 7-day window, label: "WAU"
Series C: Event "Session start", aggregation: Count Unique Users, rolling 28-day window, label: "MAU"
Series D: Computed: Series A / Series B × 100, unit: %, label: "DAU/WAU Stickiness"
Series E: Computed: Series A / Series C × 100, unit: %, label: "DAU/MAU Stickiness"
Time granularity: Daily (smooth Series D and E with 7-day rolling average to reduce noise)
Time range: Last 90 days
Breakdown: By Plan: resolved from the user's most-recent active subscription
Compare: Year-over-year (same 90-day window prior year)
Chart type: Dual-axis: left axis user counts (A/B/C as lines), right axis stickiness % (D and E as lines)
Annotations:
- Add benchmarks: DAU/MAU ≥ 20% is "good" for B2B SaaS; ≥ 50% is best-in-class.
- Add benchmarks: DAU/WAU ≥ 50% indicates strong daily-habit usage.
- Flag any plan where DAU/MAU stickiness dropped >3 percentage points vs. previous period (engagement erosion: leading indicator of churn).
- Flag any plan where MAU is growing but DAU is flat (acquiring users who aren't engaging).
Stickiness leads retention by 1-2 quarters; it's the canary in the coal mine.
Taxonomy notes:
- Session start is the canonical "user is active" event. Alternative: identify, but Session start is more frequent and reliable.
- plan_tier as a User property does not exist; Plan comes from the user's Subscription started.
