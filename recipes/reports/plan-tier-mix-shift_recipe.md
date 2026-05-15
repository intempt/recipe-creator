---
name: plan-tier-mix-shift
description: |
  Use when a user mentions "plan-tier mix shift over time", or asks for related help. % of revenue and % of customers per plan over time, surfacing up-market vs down-market drift.
arguments: []
intempt:
  id: plan-tier-mix-shift
  version: 1.0.0
  slashCommand: /plan-tier-mix-shift
  group: Reports
  shortDescription: "% of revenue and % of customers per plan over time, surfacing up-market vs down-market drift."
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
        Create an Insights report called "Plan-Tier Mix Shift".

        Series A: Event "revenue_completed" filtered to recurring revenue type (or invoice_paid as fallback), aggregation: Sum of "amount", unit: $
        Series B: Count of users with an active subscription at month-end (active = has subscription_created with status in active states, no subsequent subscription_cancelled or subscription_expired before the month-end)
        Series C: Computed — Series A by plan / total Series A × 100, unit: %, label: "% of Revenue by Plan"
        Series D: Computed — Series B by plan / total Series B × 100, unit: %, label: "% of Customers by Plan"
        Time granularity: Monthly
        Breakdown: By plan_name (resolved from each user's most-recent active subscription_created.plan_name)
        Time range: Last 12 months
        Compare: Year-over-year
        Chart type: Two stacked area charts side-by-side — Series C (revenue mix) and Series D (customer mix)

        Annotations:
        - For each plan, label start-of-period and end-of-period share with the change in percentage points.
        - Flag any plan whose share of revenue shifted by >5 percentage points YoY.
        - Highlight any divergence between revenue mix and customer mix (e.g., higher tier growing as % of revenue but flat as % of customers = ARPA going up = pricing/positioning working).
        - Flag the opposite divergence (customer mix shifting up-market but revenue mix flat = discounting eroding the up-market thesis).

        This is one of the most consequential questions for SaaS pricing/positioning teams.

        Taxonomy notes:
        - plan_name is on subscription_created. Active subscription status is determined by absence of a later subscription_cancelled / subscription_expired for the same subscription_id.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Plan-Tier Mix Shift Over Time

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Plan-Tier Mix Shift".

   Series A: Event "revenue_completed" filtered to recurring revenue type (or invoice_paid as fallback), aggregation: Sum of "amount", unit: $
   Series B: Count of users with an active subscription at month-end (active = has subscription_created with status in active states, no subsequent subscription_cancelled or subscription_expired before the month-end)
   Series C: Computed — Series A by plan / total Series A × 100, unit: %, label: "% of Revenue by Plan"
   Series D: Computed — Series B by plan / total Series B × 100, unit: %, label: "% of Customers by Plan"
   Time granularity: Monthly
   Breakdown: By plan_name (resolved from each user's most-recent active subscription_created.plan_name)
   Time range: Last 12 months
   Compare: Year-over-year
   Chart type: Two stacked area charts side-by-side — Series C (revenue mix) and Series D (customer mix)

   Annotations:
   - For each plan, label start-of-period and end-of-period share with the change in percentage points.
   - Flag any plan whose share of revenue shifted by >5 percentage points YoY.
   - Highlight any divergence between revenue mix and customer mix (e.g., higher tier growing as % of revenue but flat as % of customers = ARPA going up = pricing/positioning working).
   - Flag the opposite divergence (customer mix shifting up-market but revenue mix flat = discounting eroding the up-market thesis).

   This is one of the most consequential questions for SaaS pricing/positioning teams.

   Taxonomy notes:
   - plan_name is on subscription_created. Active subscription status is determined by absence of a later subscription_cancelled / subscription_expired for the same subscription_id.
   ```
