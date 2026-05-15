---
name: mrr-trend
description: |
  Use when a user mentions "mrr trend", or asks for related help. MRR over time by plan with month-over-month growth rate and net-new MRR overlay.
arguments: []
intempt:
  id: mrr-trend
  version: 1.0.0
  slashCommand: /mrr-trend
  group: Reports
  shortDescription: "MRR over time by plan with month-over-month growth rate and net-new MRR overlay."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [insights]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "Monthly Recurring Revenue Trend".

        Series A: Event "revenue_completed" where type indicates a recurring payment (or "invoice_paid" if invoice_paid is the canonical recurring revenue marker in this workspace), aggregation: Sum of "amount" property, unit: $, label: "MRR"
          - For revenue_completed, filter by type indicating subscription/recurring revenue.
          - For invoice_paid as fallback, aggregate amount_paid_cents and divide by 100 to get $.
        Series B: Computed — month-over-month MRR delta (current month MRR − previous month MRR), unit: $, label: "Net New MRR"
        Time granularity: Monthly
        Breakdown for Series A: By plan_name — for revenue_completed users, the plan_name comes from their subscription_created event (most recent active subscription). Render as stacked area.
        Time range: Last 12 months
        Compare: Year-over-year (same month previous year, dotted overlay)
        Chart type: Stacked area chart for Series A with Series B as a secondary line

        Annotations:
        - Add the absolute MRR figure for the most recent month as a callout.
        - Add the month-over-month growth rate (%) and the trailing 3-month average growth rate.
        - Flag any month where net new MRR went negative (contraction).
        - Highlight any plan tier whose share of MRR shifted by more than 5 percentage points YoY.

        Taxonomy notes:
        - revenue_completed has amount, customer_id, type, source — use type to filter for recurring revenue.
        - invoice_paid (Stripe) has amount_paid_cents — use as primary if revenue_completed type-discrimination is not configured.
        - plan_name comes from subscription_created — join to user's most-recent active subscription to attribute the MRR.
        - "subscription_payment" as an event does not exist in the canonical taxonomy.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# MRR Trend

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Monthly Recurring Revenue Trend".

   Series A: Event "revenue_completed" where type indicates a recurring payment (or "invoice_paid" if invoice_paid is the canonical recurring revenue marker in this workspace), aggregation: Sum of "amount" property, unit: $, label: "MRR"
     - For revenue_completed, filter by type indicating subscription/recurring revenue.
     - For invoice_paid as fallback, aggregate amount_paid_cents and divide by 100 to get $.
   Series B: Computed — month-over-month MRR delta (current month MRR − previous month MRR), unit: $, label: "Net New MRR"
   Time granularity: Monthly
   Breakdown for Series A: By plan_name — for revenue_completed users, the plan_name comes from their subscription_created event (most recent active subscription). Render as stacked area.
   Time range: Last 12 months
   Compare: Year-over-year (same month previous year, dotted overlay)
   Chart type: Stacked area chart for Series A with Series B as a secondary line

   Annotations:
   - Add the absolute MRR figure for the most recent month as a callout.
   - Add the month-over-month growth rate (%) and the trailing 3-month average growth rate.
   - Flag any month where net new MRR went negative (contraction).
   - Highlight any plan tier whose share of MRR shifted by more than 5 percentage points YoY.

   Taxonomy notes:
   - revenue_completed has amount, customer_id, type, source — use type to filter for recurring revenue.
   - invoice_paid (Stripe) has amount_paid_cents — use as primary if revenue_completed type-discrimination is not configured.
   - plan_name comes from subscription_created — join to user's most-recent active subscription to attribute the MRR.
   - "subscription_payment" as an event does not exist in the canonical taxonomy.
   ```
