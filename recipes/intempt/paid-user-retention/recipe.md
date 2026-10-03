---
id: paid-user-retention
title: Paid user retention
slash_command: /paid-user-retention
group: Reports
owner: intempt
summary: Shows whether paying customers keep logging in and keep paying, tracked separately, month by
  month and by plan.
description: >-
  Monthly paid retention with logo and revenue retention separately, plus plan-tier comparison.
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
    - retention
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Split logo and revenue retention"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Split logo and revenue retention
    summary: >-
      Monthly cohorts of paid non trial signups over 6 months, shown twice: the share still starting sessions,
      and the revenue they generate as a percentage of month zero. Split by plan, with a 95% benchmark
      and a flag below 80% at month 3.
    builds: report
    description: |-
      Create a Retention report called "Paid User Monthly Retention".
      Anchor event: subscription_created where trial_end is null (paid signup, not trial)
      Return event: session_start (logo retention) AND revenue_completed (revenue retention): render as two views
      Cohort granularity: Monthly
      Time range: Last 6 months
      Breakdown: By plan_name (from subscription_created.plan_name)
      Compare: Previous period (prior 6 months of cohorts)
      Chart type: Retention curve plus cohort table with M1 through M6 columns
      Logo Retention view:
      - Cell value = % of cohort users who emitted at least one session_start in month N
      Revenue Retention view:
      - Cell value = Sum of revenue_completed.amount in month N from cohort users / Sum of revenue_completed.amount in month 0 from cohort users × 100, unit: %
      - This separates "do users stay?" from "do they pay the same or more?"
      Annotations:
      - Add benchmarks: 95% monthly logo retention is industry-good for self-serve SaaS; 85% is below par.
      - Flag any plan tier where M3 logo retention is below 80%.
      - Flag any cohort where revenue retention exceeded logo retention by 10+ percentage points (expansion offsetting churn: good).
      - Highlight the highest-retaining plan tier.
      Surface whether enterprise tiers retain materially better than starter tiers.
      Taxonomy notes:
      - subscription_created with trial_end=null marks paid (non-trial) starts.
      - revenue_completed has amount, customer_id, type: the canonical recurring revenue marker.
      - "any_active_event" as a return signal can be substituted with session_start (most reliable active marker).
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Paid user retention

Shows whether paying customers keep logging in and keep paying, tracked separately, month by month and by plan.

## Steps

1. **Split logo and revenue retention** (builds report)

   Monthly cohorts of paid non trial signups over 6 months, shown twice: the share still starting sessions, and the revenue they generate as a percentage of month zero. Split by plan, with a 95% benchmark and a flag below 80% at month 3.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Split logo and revenue retention"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
