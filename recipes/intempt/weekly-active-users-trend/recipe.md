---
frontmatter_id: weekly-active-users-trend
slash_command: /weekly-active-users-trend
description: Builds a segment of monthly users who skipped this week, and emails a weekly digest of weekly and monthly active
  users and their ratio, by plan, to see whether users come back often enough.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds the monthly-but-not-weekly users segment and emails a weekly digest of weekly and monthly active users and
    stickiness by plan, with drop flags.
  parameters:
  - name: wau_window
    type: duration
    label: Weekly active window
    default: 7 d
    required: false
  - name: mau_window
    type: duration
    label: Monthly active window
    default: 28 d
    required: false
  - name: report_range
    type: duration
    label: Weeks of history in the digest
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
    label: Stickiness drop in a plan that gets flagged (points)
    default: 3
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: active_user_event
    kind: event
    meaning: A user started a session in the product
  - slot: plan_attribute
    kind: attribute
    meaning: The plan of a user's most recent active subscription
  steps:
  - id: s1
    builds: segment
    uses:
    - active_user_event
    - wau_window
    - mau_window
    instruction: 'Build a new segment of users named "Monthly Active, Not Weekly Active": users who did {active_user_event}
      in the last {mau_window} and did not do {active_user_event} in the last {wau_window}.'
  - id: s2
    builds: automation
    uses:
    - s1
    - active_user_event
    - plan_attribute
    - wau_window
    - mau_window
    - report_range
    - benchmark_low
    - benchmark_high
    - drop_threshold
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes {active_user_event}
      and writes these figures: weekly active users (unique users in the last {wau_window}), monthly active users (unique
      users in the last {mau_window}) and stickiness, weekly divided by monthly as a %, next to the values a week ago and
      {report_range} ago; the weekly values over the last {report_range}; the same three figures by {plan_attribute}; where
      stickiness sits against {benchmark_low}% and {benchmark_high}%; the number of users in the segment from "Find monthly
      users who skipped this week". When a plan''s stickiness dropped more than {drop_threshold} points against {report_range}
      ago, or a plan''s weekly users grew while its stickiness fell, the email''s first line says so. Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Weekly active users

Slash command: /weekly-active-users-trend

## Step 1: Find monthly users who skipped this week

Build a new segment of users named "Monthly Active, Not Weekly Active": users who did active user event in the last 28 d and did not do active user event in the last 7 d.

## Step 2: Email the weekly active users digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes active user event and writes these figures: weekly active users (unique users in the last 7 d), monthly active users (unique users in the last 28 d) and stickiness, weekly divided by monthly as a %, next to the values a week ago and 12 w ago; the weekly values over the last 12 w; the same three figures by plan attribute; where stickiness sits against 20% and 50%; the number of users in the segment from "Find monthly users who skipped this week". When a plan's stickiness dropped more than 3 points against 12 w ago, or a plan's weekly users grew while its stickiness fell, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
