---
id: subscription-health-dashboard
title: Subscription revenue health
slash_command: /subscription-health-dashboard
group: Dashboards
owner: intempt
curator: sid
summary: >-
  Review subscription revenue compounding or erosion using the subscription page's fixed NRR curve and MRR
  movement waterfall.
description: >-
  Finance / RevOps view: the subscription page provides a fixed NRR curve and MRR movement waterfall. These
  are built-in features, not composable dashboard widgets.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  industry:
    - ai
    - b2b-saas
    - finance
    - media
    - social
  vertical: []
  complexity: standard
  executionMode: live
  tags:
    - dashboard
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new dashboard, from step 1 "Build the subscription board"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the subscription board
    summary: >-
      Monthly MRR movement as a waterfall, churn by cohort, net revenue retention, and revenue lost to
      failed payments then recovered.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "Subscription Health".
      Persona: Finance Lead, RevOps Lead, or CRO running monthly subscription-business review. Question answered: "Is the subscription engine compounding or eroding? Where is the leakage?"
      Distinct from SaaS Growth Command Center (founder daily/weekly view, mixed engagement + revenue) and Customer Success Dashboard (account-level operational save plays). Subscription Health is monthly board-review cadence, focused exclusively on subscription/revenue mechanics.
      Board-level configuration:
      - defaultDateRange: last_90_days
      - exclusionPeriod: incomplete_periods
      - visibility: project
      - boardFilters: none by default
      - boardBreakdowns: plan_name (pushed down where applicable)
      Layout: 4 rows.
      Row 1: Subscription health KPIs (heightPx: 200, four metric cards at widthUnits: 3):
      - Card 1: Insights metric to source recipe: mrr-trend, vizType: metric, titleOverride: "MRR (Current)"
      - Card 2: Insights metric to source recipe: mrr-movement-decomposition, vizType: metric, titleOverride: "Net New MRR (Last Month)"
      - Card 3: Retention metric to source recipe: net-revenue-retention-by-cohort, vizType: metric, titleOverride: "Trailing-12mo NRR"
      - Card 4: Insights metric to source recipe: monthly-logo-retention-trend, vizType: metric, titleOverride: "Logo Retention (Annualized)"
      Row 2: MRR movement waterfall (heightPx: 480, full-width single card at widthUnits: 12):
      - Card 1: Insights to source recipe: mrr-movement-decomposition, displayMode: chart, vizType: stacked_column (the canonical MRR waterfall: New, Expansion, Reactivation, Contraction, Churn, Net New per month). The strategic centerpiece of this dashboard.
      Row 3: Retention dynamics (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Retention to source recipe: net-revenue-retention-by-cohort, displayMode: chart, vizType: line (cohort NRR curves: answers "are recent cohorts compounding revenue or eroding?")
      - Card 2: Retention to source recipe: paid-user-retention, displayMode: table (cohort retention grid for logo retention vs revenue retention side-by-side)
      Row 4: Revenue leakage and recovery (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Funnel to source recipe: payment-failure-recovery-funnel, displayMode: chart, vizType: funnel_steps (dunning recovery: surfaces revenue at risk and the recovery rate)
      - Card 2: Insights to source recipe: expansion-revenue-trend, displayMode: chart, vizType: stacked_bar (upgrade vs. seat-expansion mix: quality of expansion revenue)
      Annotations:
      - This dashboard is meant for monthly review (e.g., the day before board meeting), not daily/weekly. The right cadence is reading it once per month and looking for inflection points.
      - Row 1 KPIs are the four numbers a CFO reports to the board. NRR ≥ 100% indicates the installed base is growing despite churn; NRR ≥ 110% is top-quartile; <90% indicates revenue erosion.
      - Row 2 (MRR movement waterfall, full-width) is the single most important view in subscription analytics. Reading it: green stacks (New + Expansion + Reactivation) should consistently outweigh red stacks (Contraction + Churn). Months where it doesn't are the moments to investigate.
      - Row 4 surfaces the operational levers: dunning recovery rate of 70% is healthy; expansion revenue ≥30% of new MRR is healthy; both can be operationally improved without changing the product.
      Taxonomy notes:
      - mrr-movement-decomposition and net-revenue-retention-by-cohort both depend on subscription_updated.changed_fields parsing for expansion/contraction split: see those recipes' notes.
      - All other source recipes use canonical events: subscription_created, subscription_cancelled, subscription_updated, subscription_resumed, invoice_paid, invoice_payment_failed, revenue_completed.
      - monthly-logo-retention-trend annualizes the monthly retention rate; surface the annual implication directly (e.g., "95% monthly = 54% annual retention").
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Subscription revenue health

Review subscription revenue compounding or erosion using the subscription page's fixed NRR curve and MRR movement waterfall.

## Steps

1. **Build the subscription board** (builds dashboard)

   Monthly MRR movement as a waterfall, churn by cohort, net revenue retention, and revenue lost to failed payments then recovered.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new dashboard, from step 1 "Build the subscription board"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
