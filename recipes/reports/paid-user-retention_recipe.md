---
name: paid-user-retention
description: |
  Use when a user mentions "paid user retention", or asks for related help. Monthly paid retention with logo and revenue retention separately, plus plan-tier comparison.
arguments: []
intempt:
  id: paid-user-retention
  version: 1.0.0
  slashCommand: /paid-user-retention
  group: Reports
  shortDescription: "Produce a monthly cohort retention report for paid signups showing logo vs revenue retention curves broken down by plan_name over the last 6 months."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [retention]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_retention_report
  procedure:
    - step: 1
      title: "Build Retention Report"
      command: build_retention_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Retention report called "Paid User Monthly Retention".

        Anchor event: subscription_created where trial_end is null (paid signup, not trial)
        Return event: session_start (logo retention) AND revenue_completed (revenue retention) — render as two views

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
        - Flag any cohort where revenue retention exceeded logo retention by 10+ percentage points (expansion offsetting churn — good).
        - Highlight the highest-retaining plan tier.

        Surface whether enterprise tiers retain materially better than starter tiers.

        Taxonomy notes:
        - subscription_created with trial_end=null marks paid (non-trial) starts.
        - revenue_completed has amount, customer_id, type — the canonical recurring revenue marker.
        - "any_active_event" as a return signal can be substituted with session_start (most reliable active marker).
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Paid User Retention

## Procedure

1. **Build Retention Report** [`build_retention_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Retention report called "Paid User Monthly Retention".

   Anchor event: subscription_created where trial_end is null (paid signup, not trial)
   Return event: session_start (logo retention) AND revenue_completed (revenue retention) — render as two views

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
   - Flag any cohort where revenue retention exceeded logo retention by 10+ percentage points (expansion offsetting churn — good).
   - Highlight the highest-retaining plan tier.

   Surface whether enterprise tiers retain materially better than starter tiers.

   Taxonomy notes:
   - subscription_created with trial_end=null marks paid (non-trial) starts.
   - revenue_completed has amount, customer_id, type — the canonical recurring revenue marker.
   - "any_active_event" as a return signal can be substituted with session_start (most reliable active marker).
   ```
