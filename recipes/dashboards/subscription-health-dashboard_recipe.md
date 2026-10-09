---
name: subscription-health-dashboard
description: |
  Use when a user mentions "subscription health dashboard", asks for a finance / revops dashboard, or asks for related help. Finance / RevOps view: MRR movement, churn cohorts, payment recovery, NRR: the monthly board-review subscription metrics.
arguments: []
intempt:
  id: subscription-health-dashboard
  version: 1.0.0
  slashCommand: /subscription-health-dashboard
  group: Dashboards
  title: "Subscription revenue health"
  shortDescription: "Answers whether subscription revenue is compounding or eroding each month and where the leakage is: MRR movement, churn cohorts, failed payments and NRR."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: standard
    executionMode: live
    tags: [dashboard]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_dashboard
  procedure:
    - step: 1
      title: "Build the subscription board"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      description: "Monthly MRR movement as a waterfall, churn by cohort, net revenue retention, and revenue lost to failed payments then recovered."
      prompt: |
        Create a Dash board (12-column composition canvas) titled "Subscription Health".

        Persona: Finance Lead, RevOps Lead, or CRO running monthly subscription-business review. Question answered: "Is the subscription engine compounding or eroding? Where is the leakage?"

        Distinct from SaaS Growth Command Center (founder daily/weekly view, mixed engagement + revenue) and Customer Success Dashboard (account-level operational save plays). Subscription Health is monthly board-review cadence, focused exclusively on subscription/revenue mechanics.

        Board-level configuration:
        - defaultDateRange: last_90_days
        - exclusionPeriod: incomplete_periods
        - visibility: project
        - boardFilters: none by default
        - boardBreakdowns: Plan (pushed down where applicable)

        Layout: 4 rows.

        Row 1: Subscription health KPIs (heightPx: 200, four metric cards at widthUnits: 3):
        - Card 1: Insights metric to source recipe: mrr-trend, vizType: metric, titleOverride: "MRR (Current)"
        - Card 2: Insights metric to source recipe: mrr-movement-decomposition, vizType: metric, titleOverride: "Net New MRR (Last Month)"
        - Card 3: Retention metric to source recipe: net-revenue-retention-by-cohort, vizType: metric, titleOverride: "Trailing-12mo NRR"
        - Card 4: Insights metric to source recipe: monthly-logo-retention-trend, vizType: metric, titleOverride: "Logo Retention (Annualized)"

        Row 2: MRR movement waterfall (heightPx: 480, full-width single card at widthUnits: 12):
        - Card 1: Insights to source recipe: mrr-movement-decomposition, displayMode: chart, vizType: stacked_column (the standard MRR waterfall: New, Expansion, Reactivation, Contraction, Churn, Net New per month). The strategic centerpiece of this dashboard.

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
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Subscription revenue health

Answers whether subscription revenue is compounding or eroding each month and where the leakage is: MRR movement, churn cohorts, failed payments and NRR.

## What it does

1. **Build the subscription board** (`create_dashboard`)

   Monthly MRR movement as a waterfall, churn by cohort, net revenue retention, and revenue lost to failed payments then recovered.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.
