---
frontmatter_id: subscription-health-dashboard
slash_command: /subscription-health-dashboard
description: Review subscription revenue compounding or erosion using the subscription page's fixed NRR curve and MRR movement waterfall.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Gives a finance or revenue lead a monthly board view of whether subscription revenue is compounding or eroding,
    with MRR movements, cohort NRR, and leakage levers.
  parameters:
  - name: dateRange
    type: duration
    label: Default date range
    default: 90 d
    required: false
  - name: breakdownBy
    type: string
    label: Board breakdown
    default: Plan
    required: false
  - name: nrrHealthyThreshold
    type: number
    label: NRR top-quartile threshold (%)
    default: 110
    required: false
  - name: nrrErosionThreshold
    type: number
    label: NRR erosion threshold (%)
    default: 90
    required: false
  - name: dunningRecoveryTarget
    type: number
    label: Dunning recovery target (%)
    default: 70
    required: false
  - name: expansionShareTarget
    type: number
    label: Expansion share of new MRR target (%)
    default: 30
    required: false
  requirements:
  - slot: subscription_started
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: plan
      type: string
      meaning: Plan the subscription started on
      optional: false
  - slot: subscription_canceled
    kind: event
    meaning: A customer canceled a subscription
    properties:
    - name: plan
      type: string
      meaning: Plan that was canceled
      optional: false
  - slot: subscription_updated
    kind: event
    meaning: A customer's subscription was changed
    properties:
    - name: changed_fields
      type: text
      meaning: List of subscription fields that changed, used to split expansion from contraction
      optional: false
    - name: plan
      type: string
      meaning: Plan after the change
      optional: true
  - slot: subscription_resumed
    kind: event
    meaning: A customer resumed a paused subscription
    properties:
    - name: plan
      type: string
      meaning: Plan the subscription resumed on
      optional: true
  - slot: invoice_paid
    kind: event
    meaning: A customer's invoice was paid
    properties:
    - name: plan
      type: string
      meaning: Plan the invoice is for
      optional: true
    - name: amount
      type: number
      meaning: Amount paid on the invoice
      optional: false
  - slot: invoice_payment_failed
    kind: event
    meaning: A customer's invoice payment failed
    properties:
    - name: amount
      type: number
      meaning: Amount of the failed invoice
      optional: false
  - slot: revenue_completed
    kind: event
    meaning: A customer completed a revenue-generating purchase
    properties:
    - name: amount
      type: number
      meaning: Revenue amount of the purchase
      optional: false
  - slot: plan
    kind: attribute
    meaning: The subscription plan a customer is on
  - slot: mrr_trend_insight
    kind: knowledge
    meaning: An insights metric showing monthly recurring revenue over time
  - slot: mrr_movement_insight
    kind: knowledge
    meaning: An insights metric decomposing MRR movement into new, expansion, reactivation, contraction, churn and net new
  - slot: nrr_cohort_retention
    kind: knowledge
    meaning: A retention analysis of net revenue retention by signup cohort
  - slot: logo_retention_trend
    kind: knowledge
    meaning: An insights metric showing monthly logo retention trend
  - slot: paid_user_retention
    kind: knowledge
    meaning: A cohort retention grid of paid users over time
  - slot: payment_failure_recovery_funnel
    kind: knowledge
    meaning: A funnel showing failed payments moving through dunning recovery
  - slot: expansion_revenue_trend
    kind: knowledge
    meaning: An insights metric showing expansion revenue split by upgrade and seat expansion
  steps:
  - id: s1
    builds: dashboard
    instruction: 'Create a 12-column dashboard titled "Subscription Health" for a monthly subscription-business review by
      a finance, RevOps, or CRO audience, answering whether the subscription engine is compounding or eroding and where the
      leakage is. Set the default date range to {dateRange}, exclude incomplete periods, make it visible to the project, leave
      board filters empty, and set the board breakdown to {breakdownBy} pushed down where applicable. Use 4 rows. Row 1 (height
      200px): four metric cards at 3 units each, titled "MRR (Current)" from {mrr_trend_insight} as a metric, "Net New MRR
      (Last Month)" from {mrr_movement_insight} as a metric, "Trailing-12mo NRR" from {nrr_cohort_retention} as a metric,
      and "Logo Retention (Annualized)" from {logo_retention_trend} as a metric, where the annual implication of the monthly
      rate is shown directly (for example, 95% monthly equals 54% annual). Row 2 (height 480px): one full-width 12-unit stacked
      column chart from {mrr_movement_insight} showing New, Expansion, Reactivation, Contraction, Churn and Net New per month.
      Row 3 (height 440px): two 6-unit cards, a line chart of cohort NRR curves from {nrr_cohort_retention}, and a table from
      {paid_user_retention} showing logo retention vs revenue retention side by side. Row 4 (height 440px): two 6-unit cards,
      a funnel-steps chart from {payment_failure_recovery_funnel} showing revenue at risk and recovery rate, and a stacked
      bar chart from {expansion_revenue_trend} showing the upgrade vs seat-expansion mix.'
---

# Subscription revenue health

Slash command: /subscription-health-dashboard

## Step 1: Build the subscription board

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
- mrr-movement-decomposition and net-revenue-retention-by-cohort both depend on Subscription updated.changed_fields parsing for expansion/contraction split: see those recipes' notes.
- All other source recipes use canonical events: Subscription started, Subscription canceled, Subscription updated, subscription_resumed, Invoice paid, Invoice payment failed, Revenue completed.
- monthly-logo-retention-trend annualizes the monthly retention rate; surface the annual implication directly (e.g., "95% monthly = 54% annual retention").
