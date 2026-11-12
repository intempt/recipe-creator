---
frontmatter_id: weekly-active-users-trend
slash_command: /weekly-active-users-trend
description: Shows weekly active users and monthly active users, plus the WAU to MAU ratio, to indicate engagement stickiness.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows weekly and monthly active users plus their ratio, so you can see whether users come back often enough to
    stay engaged, broken down by plan.
  parameters:
  - name: wau_window
    type: duration
    label: Weekly active window
    default: 7 d
    required: false
  - name: mau_window
    type: duration
    label: Monthly active window (rolling)
    default: 28 d
    required: false
  - name: report_range
    type: duration
    label: Time range of report
    default: 12 w
    required: false
  - name: benchmark_low
    type: number
    label: Low stickiness benchmark (%)
    default: 20
    required: false
  - name: benchmark_high
    type: number
    label: High stickiness benchmark (%)
    default: 50
    required: false
  - name: drop_threshold
    type: number
    label: Stickiness drop alert threshold (points)
    default: 3
    required: false
  requirements:
  - slot: active_user_event
    kind: event
    meaning: A user started a session in the product
    properties:
    - name: device_type
      type: string
      meaning: Device the session ran on
      optional: true
    - name: country
      type: string
      meaning: Country of the session
      optional: true
    - name: utm_source
      type: string
      meaning: Marketing source of the session
      optional: true
  - slot: plan_attribute
    kind: attribute
    meaning: The plan of a user's most recent active subscription, taken from the subscription start record
  - slot: active_user_identify
    kind: event
    meaning: A user was identified in the product, used as an alternative active-user signal if the workspace uses identify
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - active_user_event
    - active_user_identify
    - plan_attribute
    - wau_window
    - mau_window
    - report_range
    - benchmark_low
    - benchmark_high
    - drop_threshold
    instruction: 'Create an Insights report called "Weekly Active Users Trend". Series A: event {active_user_event}, aggregation
      Count Unique Users, time granularity weekly, label "WAU" (alternative: use {active_user_identify} if the workspace uses
      identify as the active-user signal). Series B: event {active_user_event}, aggregation Count Unique Users, rolling {mau_window}
      window, label "MAU". Series C: computed Series A (WAU) divided by Series B (MAU) multiplied by 100, unit %, label "Stickiness
      (WAU/MAU)". Time granularity weekly. Time range last {report_range}. Breakdown by {plan_attribute}, derived from each
      user''s most recent active subscription start record. Compare to previous period (prior {report_range}). Chart type:
      dual-axis, left axis user counts (WAU and MAU as lines), right axis stickiness % as a line. Annotations: add a horizontal
      benchmark line at {benchmark_low}% stickiness; add a horizontal benchmark line at {benchmark_high}% stickiness; highlight
      any plan where stickiness dropped more than {drop_threshold} points versus the previous period; flag any plan where
      WAU is growing but stickiness is falling.'
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
