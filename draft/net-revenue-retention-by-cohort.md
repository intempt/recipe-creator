---
description: Tracks monthly cohort retention rates over time to measure ongoing customer and user engagement.
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
  - finance
  - media
---

# Net revenue retention by cohort

Slash command: /net-revenue-retention-by-cohort

## Step 1: Track cohort revenue month by month

Create a Retention report called "Net Revenue Retention by Cohort".
Cohort: Monthly cohort defined by month of first paid Subscription started (trial_end is null OR a follow-on after-trial Subscription started) per user.
For each cohort and each month-after-cohort N (M, M+1, M+2, ... M+12), compute the dollar values for users in the cohort:
- Starting MRR (cohort's recurring revenue in month N-1) = Sum of Revenue completed.amount filtered to recurring type, for cohort users
- Expansion MRR = Sum of positive amount-deltas from Subscription updated events in month N for cohort users (where the post-event amount exceeds the prior amount on the same subscription_id)
- Reactivation MRR = Sum of subscription_resumed.amount in month N for cohort users who had a prior Subscription canceled
- Contraction MRR = Sum of negative amount-deltas from Subscription updated events (subtracted)
- Churned MRR = Sum of the prior subscription amount for each Subscription canceled in month N (subtracted)
- Ending MRR = Starting + Expansion + Reactivation − Contraction − Churn
- NRR for cohort at month N = Ending MRR / Original cohort revenue at month M × 100, unit: %
Time range: Last 12 cohort-months
Breakdown: By initial Plan (the Plan on the cohort-defining Subscription started)
Chart type: Multi-line chart: X axis is months-since-cohort, Y axis is NRR %; each cohort is a line. Plus a stacked bar showing the per-component decomposition for the most recent cohort.
Annotations:
- Add benchmarks: NRR ≥ 100% (cohort growing in revenue despite churn); ≥ 110% (top-quartile); ≥ 120% (best-in-class).
- Flag any cohort whose NRR at M+6 is below 90% (revenue erosion).
- Highlight the cohort with the highest M+12 NRR.
- Flag whether NRR is improving across cohorts over time (cohort-quality trend).
Surface the trailing 12-month blended NRR (a single headline number) and whether the cohort-level trend is improving.
Taxonomy notes:
- The canonical taxonomy does not have separate subscription_upgraded/_downgraded/_reactivated events. Expansion and Contraction are computed by Lovable from Subscription updated by comparing pre/post amount on the same subscription_id. Reactivation is computed as subscription_resumed (or subscription_activated) where the same customer_id had a recent Subscription canceled.
- This recipe depends on Subscription updated firing reliably with sufficient detail (changed_fields, plan_items) for the delta computation. If the integration emits sparse Subscription updated, the report degrades to logo-retention only.
