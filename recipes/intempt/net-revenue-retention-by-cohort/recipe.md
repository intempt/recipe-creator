---
frontmatter_id: net-revenue-retention-by-cohort
slash_command: /net-revenue-retention-by-cohort
description: This recipe builds a monthly view of how much recurring revenue each signup cohort keeps and grows over its first year, then turns weak results into follow-up work. It is for revenue, finance and growth teams who watch subscription health.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# Net revenue retention by cohort

## Step 1: Track cohort revenue month by month

Create a Retention report called "Net Revenue Retention by Cohort".
Cohort: Monthly cohort defined by month of first paid Subscription started (trial_end is null, or a follow-on Subscription started after a trial) per user.
For each cohort and each month-after-cohort N (M, M+1, M+2, through M+12), compute the dollar values for users in the cohort:
- Starting MRR (cohort's recurring revenue in month N-1) = Sum of Revenue completed.amount filtered to recurring type, for cohort users
- Expansion MRR = Sum of positive amount deltas from Subscription updated events in month N for cohort users (where the post-event amount exceeds the prior amount on the same subscription_id)
- Reactivation MRR = Sum of subscription_resumed.amount in month N for cohort users who had a prior Subscription canceled
- Contraction MRR = Sum of negative amount deltas from Subscription updated events (subtracted)
- Churned MRR = Sum of the prior subscription amount for each Subscription canceled in month N (subtracted)
- Ending MRR = Starting plus Expansion plus Reactivation minus Contraction minus Churn
- Net Revenue Retention for the cohort at month N = Ending MRR divided by the cohort's original revenue at month M, times 100, unit: percent
Time range: Last 12 cohort-months
Breakdown: By initial Plan (the Plan on the cohort-defining Subscription started)
Chart type: Multi-line chart: X axis is months-since-cohort, Y axis is Net Revenue Retention percent; each cohort is a line. Plus a stacked bar showing the per-component decomposition for the most recent cohort.
Annotations:
- Flag any cohort whose Net Revenue Retention at M+6 is below 90 percent.
- Highlight the cohort with the highest M+12 Net Revenue Retention.
- Surface the trailing 12-month blended Net Revenue Retention as a single headline number.
Taxonomy notes:
- The canonical taxonomy does not have separate subscription_upgraded, subscription_downgraded, or subscription_reactivated events. Expansion and Contraction are computed from Subscription updated by comparing pre- and post-event amount on the same subscription_id. Reactivation is computed as subscription_resumed (or subscription_activated) where the same customer_id had a recent Subscription canceled.
- This report depends on Subscription updated firing reliably with changed_fields and plan_items for the delta computation. If the integration emits sparse Subscription updated, the report degrades to logo-retention only.

## Step 2: Flag cohorts eroding below the retention bar

Create a workflow called "Cohort Net Revenue Retention Review" that runs on the same monthly schedule as "Track cohort revenue month by month". For any cohort whose Net Revenue Retention at M+6 falls below 90 percent, create a task assigned to the revenue owner, titled with the cohort's start month and the words "Net Revenue Retention below 90 percent at M+6", listing the cohort's starting MRR, the components driving the shortfall, and a link to the report. Post a monthly summary of all tracked cohorts' current Net Revenue Retention to the revenue team Slack channel regardless of outcome. Use the result of "Track cohort revenue month by month".
