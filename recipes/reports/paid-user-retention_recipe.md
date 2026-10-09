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
  title: "Paid user retention"
  shortDescription: "Shows whether paying customers keep logging in and keep paying, tracked separately, month by month and by plan."
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
      title: "Split logo and revenue retention"
      command: build_retention_report
      produces: report
      bindsAs: report
      description: "Monthly cohorts of paid non trial signups over 6 months, shown twice: the share still starting sessions, and the revenue they generate as a percentage of month zero. Split by plan, with a 95% benchmark and a flag below 80% at month 3."
      prompt: |
        Create a Retention report called "Paid User Monthly Retention".

        Anchor event: Subscription started where trial end is empty (paid signup, not trial)
        Return event: Session start (logo retention) AND Revenue completed (revenue retention): render as two views

        Cohort granularity: Monthly
        Time range: Last 6 months
        Breakdown: By Plan (from the Subscription started event)
        Compare: Previous period (prior 6 months of cohorts)
        Chart type: Retention curve plus cohort table with M1 through M6 columns

        Logo Retention view:
        - Cell value = % of cohort users who emitted at least one Session start in month N

        Revenue Retention view:
        - Cell value = Sum of the Revenue completed amount in month N from cohort users / Sum of the Revenue completed amount in month 0 from cohort users × 100, unit: %
        - This separates "do users stay?" from "do they pay the same or more?"

        Annotations:
        - Add benchmarks: 95% monthly logo retention is industry-good for self-serve SaaS; 85% is below par.
        - Flag any plan tier where M3 logo retention is below 80%.
        - Flag any cohort where revenue retention exceeded logo retention by 10+ percentage points (expansion offsetting churn: good).
        - Highlight the highest-retaining plan tier.

        Surface whether enterprise tiers retain materially better than starter tiers.

        For logo retention, use Session start as the active-user signal: it is the most reliable active marker.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Paid user retention

Shows whether paying customers keep logging in and keep paying, tracked separately, month by month and by plan.

## What it does

1. **Split logo and revenue retention** (`build_retention_report`)

   Monthly cohorts of paid non trial signups over 6 months, shown twice: the share still starting sessions, and the revenue they generate as a percentage of month zero. Split by plan, with a 95% benchmark and a flag below 80% at month 3.

## What you end up with

- **report** (report): Report produced by this recipe.
