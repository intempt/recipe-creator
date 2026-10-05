---
name: expansion-revenue-trend
description: |
  Use when a user mentions "expansion revenue trend", or asks for related help. Expansion revenue derived from subscription_updated change-events with quality-of-MRR-growth surfacing.
arguments: []
intempt:
  id: expansion-revenue-trend
  version: 1.0.0
  slashCommand: /expansion-revenue-trend
  group: Reports
  shortDescription: "Produce an 'Expansion Revenue Trend' Insights report summing positive subscription_updated amount deltas for plan upgrades per subscription_id."
  availability: coming-soon
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
        Create an Insights report called "Expansion Revenue Trend".

        Series A: Event "subscription_updated" where changed_fields indicates a plan upgrade (parsed from the changed_fields text property — e.g. contains "plan_id" or "plan_items" with a higher-priced target), aggregation: Sum of the resulting subscription amount delta
          Computation: for each subscription_updated event, compare new amount vs. prior amount on the same subscription_id. Positive delta with plan change = upgrade. Sum positive deltas, unit: $, label: "Upgrade Revenue".
        Series B: Event "subscription_updated" where changed_fields indicates seat/quantity increase (e.g. plan_items quantity went up), aggregation: Sum of positive amount delta, unit: $, label: "Seat / Quantity Expansion Revenue"
        Series C: Computed — (A + B) / new_mrr_in_period × 100, unit: %, label: "Expansion as % of New MRR"
          where new_mrr = sum of subscription_created.amount in the period
        Time granularity: Monthly
        Breakdown: By plan_name — show which starting plan tiers produce the most expansion
        Time range: Last 12 months
        Compare: Year-over-year
        Chart type: Stacked bar for A and B with Series C as a line on a secondary axis

        Annotations:
        - Add benchmarks: expansion as % of new MRR ≥ 30% is healthy; ≥ 50% is best-in-class.
        - Flag any month where total expansion revenue declined MoM by more than 15% (expansion engine stalling).
        - Highlight whether upgrade-driven expansion or seat-driven expansion dominates, and whether the mix is shifting.

        Taxonomy notes:
        - The canonical taxonomy has subscription_updated with a changed_fields text property and a plan_items property (flattenable to price_id, quantity, product). It does NOT have separate subscription_upgraded / subscription_downgraded events.
        - Computing upgrade vs downgrade requires comparing new vs prior subscription state — operationally this means: when subscription_updated fires, look up the prior subscription_created.amount and compute the delta. Positive delta = expansion, negative = contraction.
        - "subscription_payment" is not a canonical event. Use revenue_completed or invoice_paid for actual revenue capture.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Expansion revenue trend

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Expansion Revenue Trend".

   Series A: Event "subscription_updated" where changed_fields indicates a plan upgrade (parsed from the changed_fields text property — e.g. contains "plan_id" or "plan_items" with a higher-priced target), aggregation: Sum of the resulting subscription amount delta
     Computation: for each subscription_updated event, compare new amount vs. prior amount on the same subscription_id. Positive delta with plan change = upgrade. Sum positive deltas, unit: $, label: "Upgrade Revenue".
   Series B: Event "subscription_updated" where changed_fields indicates seat/quantity increase (e.g. plan_items quantity went up), aggregation: Sum of positive amount delta, unit: $, label: "Seat / Quantity Expansion Revenue"
   Series C: Computed — (A + B) / new_mrr_in_period × 100, unit: %, label: "Expansion as % of New MRR"
     where new_mrr = sum of subscription_created.amount in the period
   Time granularity: Monthly
   Breakdown: By plan_name — show which starting plan tiers produce the most expansion
   Time range: Last 12 months
   Compare: Year-over-year
   Chart type: Stacked bar for A and B with Series C as a line on a secondary axis

   Annotations:
   - Add benchmarks: expansion as % of new MRR ≥ 30% is healthy; ≥ 50% is best-in-class.
   - Flag any month where total expansion revenue declined MoM by more than 15% (expansion engine stalling).
   - Highlight whether upgrade-driven expansion or seat-driven expansion dominates, and whether the mix is shifting.

   Taxonomy notes:
   - The canonical taxonomy has subscription_updated with a changed_fields text property and a plan_items property (flattenable to price_id, quantity, product). It does NOT have separate subscription_upgraded / subscription_downgraded events.
   - Computing upgrade vs downgrade requires comparing new vs prior subscription state — operationally this means: when subscription_updated fires, look up the prior subscription_created.amount and compute the delta. Positive delta = expansion, negative = contraction.
   - "subscription_payment" is not a canonical event. Use revenue_completed or invoice_paid for actual revenue capture.
   ```
