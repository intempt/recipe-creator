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
  title: "Expansion revenue trend"
  shortDescription: "Shows how much new revenue comes from existing customers upgrading or adding seats each month, and how that compares with revenue from new customers."
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
      title: "Split upgrades from seat growth"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Monthly expansion revenue over 12 months, separated into plan upgrades and seat or quantity increases, each taken from the amount change on a subscription update. Shown as a share of new monthly revenue, split by plan and compared year over year."
      prompt: |
        Create an Insights report called "Expansion Revenue Trend".

        Series A: Event "subscription_updated" where changed_fields indicates a plan upgrade (parsed from the changed_fields text property: e.g. contains "plan_id" or "plan_items" with a higher-priced target), aggregation: Sum of the resulting subscription amount delta
          Computation: for each subscription_updated event, compare new amount vs. prior amount on the same subscription_id. Positive delta with plan change = upgrade. Sum positive deltas, unit: $, label: "Upgrade Revenue".
        Series B: Event "subscription_updated" where changed_fields indicates seat/quantity increase (e.g. plan_items quantity went up), aggregation: Sum of positive amount delta, unit: $, label: "Seat / Quantity Expansion Revenue"
        Series C: Computed: (A + B) / new_mrr_in_period × 100, unit: %, label: "Expansion as % of New MRR"
          where new_mrr = sum of subscription_created.amount in the period
        Time granularity: Monthly
        Breakdown: By plan_name: show which starting plan tiers produce the most expansion
        Time range: Last 12 months
        Compare: Year-over-year
        Chart type: Stacked bar for A and B with Series C as a line on a secondary axis

        Annotations:
        - Add benchmarks: expansion as % of new MRR ≥ 30% is healthy; ≥ 50% is best-in-class.
        - Flag any month where total expansion revenue declined MoM by more than 15% (expansion engine stalling).
        - Highlight whether upgrade-driven expansion or seat-driven expansion dominates, and whether the mix is shifting.

        Taxonomy notes:
        - The canonical taxonomy has subscription_updated with a changed_fields text property and a plan_items property (flattenable to price_id, quantity, product). It does NOT have separate subscription_upgraded / subscription_downgraded events.
        - Computing upgrade vs downgrade requires comparing new vs prior subscription state: operationally this means: when subscription_updated fires, look up the prior subscription_created.amount and compute the delta. Positive delta = expansion, negative = contraction.
        - "subscription_payment" is not a canonical event. Use revenue_completed or invoice_paid for actual revenue capture.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Expansion revenue trend

Shows how much new revenue comes from existing customers upgrading or adding seats each month, and how that compares with revenue from new customers.

## What it does

1. **Split upgrades from seat growth** (`build_insights_report`)

   Monthly expansion revenue over 12 months, separated into plan upgrades and seat or quantity increases, each taken from the amount change on a subscription update. Shown as a share of new monthly revenue, split by plan and compared year over year.

## What you end up with

- **report** (report): Report produced by this recipe.
