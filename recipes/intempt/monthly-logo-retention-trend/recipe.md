---
frontmatter_id: monthly-logo-retention-trend
slash_command: /monthly-logo-retention-trend
description: This recipe builds a monthly report on how many paying customers you keep, then sets up an automatic check that alerts your customer success team when retention slips. It is meant for SaaS and subscription teams that want to catch churn early.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# Monthly logo retention

## Step 1: Track monthly customer retention

Create an Insights report called "Monthly Logo Retention Trend".
Series A: For each calendar month M, count the unique customers who had an active subscription at the start of month M (no Subscription canceled or subscription_expired before M-start)
Series B: For the same cohort, count those who still have an active subscription at the end of month M (no Subscription canceled or subscription_expired during M)
Series C: Computed: Series B divided by Series A, times 100, unit: percent, label: "Monthly Logo Retention Rate"
Series D: Trailing 3-month rolling average of Series C, label: "Logo Retention (3-month rolling)"
Time granularity: Monthly
Time range: Last 12 months
Breakdown: By Plan (resolved from each user's Subscription started.Plan at the start of month M)
Compare: Year-over-year (same month previous year, dotted overlay)
Chart type: Line chart with Series C and Series D as primary lines, plus a small-multiple of Series C per plan tier
Annotations:
- Flag any month where Series C dropped more than 2 percentage points versus the trailing 3-month average.
- Flag if Series D has been declining for 3 or more consecutive months.
- Highlight the plan tier with the highest retention and the one with the lowest.
- Surface the implied annualized retention rate (Series C compounded over 12 months) as a single callout.
Taxonomy notes:
- Subscription started marks active subscription start (with Plan, amount, trial_end). Filter for trial_end null to scope to paid, not trial, subscriptions.
- Subscription canceled and subscription_expired mark subscription end. subscription_paused is not counted as churn, since paused subscriptions can resume.
- "Active at start of month" is computed as: Subscription started exists prior to month-start, with no terminal event before month-start.

## Step 2: Open a save review when retention drops

Create a workflow called "Logo Retention Drop Review" that runs on the same monthly schedule as "Track monthly customer retention". When Series C drops more than 2 percentage points versus its trailing 3-month average, or Series D has declined for 3 or more consecutive months, create a task assigned to the customer success owner, titled with the calendar month and the words "Logo retention drop", listing the affected plan tier, the percentage-point drop, and a link to the report. Post the month's retention rate and 3-month rolling average to the customer success Slack channel every month regardless of outcome. Use the result of "Track monthly customer retention".
