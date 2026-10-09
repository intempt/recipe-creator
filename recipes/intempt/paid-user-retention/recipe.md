---
description: See whether paying customers continue logging in, tracked month by month and compared by plan.
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

# Paid user retention

Slash command: /paid-user-retention

## Step 1: Split logo and revenue retention

Create a Retention report called "Paid User Monthly Retention".
Anchor event: Subscription started where trial_end is null (paid signup, not trial)
Return event: Session start (logo retention) AND Revenue completed (revenue retention): render as two views
Cohort granularity: Monthly
Time range: Last 6 months
Breakdown: By Plan (from Subscription started.Plan)
Compare: Previous period (prior 6 months of cohorts)
Chart type: Retention curve plus cohort table with M1 through M6 columns
Logo Retention view:
- Cell value = % of cohort users who emitted at least one Session start in month N
Revenue Retention view:
- Cell value = Sum of Revenue completed.amount in month N from cohort users / Sum of Revenue completed.amount in month 0 from cohort users × 100, unit: %
- This separates "do users stay?" from "do they pay the same or more?"
Annotations:
- Add benchmarks: 95% monthly logo retention is industry-good for self-serve SaaS; 85% is below par.
- Flag any plan tier where M3 logo retention is below 80%.
- Flag any cohort where revenue retention exceeded logo retention by 10+ percentage points (expansion offsetting churn: good).
- Highlight the highest-retaining plan tier.
Surface whether enterprise tiers retain materially better than starter tiers.
Taxonomy notes:
- Subscription started with trial_end=null marks paid (non-trial) starts.
- Revenue completed has amount, customer_id, type: the canonical recurring revenue marker.
- "any_active_event" as a return signal can be substituted with Session start (most reliable active marker).
