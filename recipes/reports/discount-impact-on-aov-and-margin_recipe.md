---
name: discount-impact-on-aov-and-margin
description: |
  Use when a user mentions "discount impact on aov and margin", or asks for related help. How discount usage affects AOV: surfaces whether discounts grow the basket or just shift demand to discounted moments.
arguments: []
intempt:
  id: discount-impact-on-aov-and-margin
  version: 1.0.0
  slashCommand: /discount-impact-on-aov-and-margin
  group: Reports
  title: "Discount impact on order value"
  shortDescription: "Shows whether your discount codes actually grow the basket or just hand money away, code by code."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: quick
    executionMode: live
    tags: [insights]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: shopify, severity: blocking }
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Test whether discounts grow baskets"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Average order value for discounted orders against orders with no code, weekly over 12 weeks for the top 10 codes, alongside the total discount cost and the net revenue effect. Flags any code where discounted baskets are smaller or the net effect is negative."
      prompt: |
        Create an Insights report called "Discount Impact on AOV".

        Series A: Event "Placed order" filtered to orders with a discount code applied (orders with a discount), aggregation: Average of the order total, label: "AOV with Discount"
        Series B: Event "Placed order" filtered to orders with NO discount code applied, aggregation: Average of the order total, label: "AOV without Discount"
        Series C: Computed: Series A − Series B, unit: $, label: "AOV Lift from Discount"
        Series D: Computed: Sum of the discount amount across all discounted orders, unit: $, label: "Total Discount Cost"
        Series E: Computed: (Sum of the order total for discounted orders − Series D) − (count of discounted orders × Series B), label: "Net Revenue Impact": answers: did discounts grow the pie or just shift it?

        Time granularity: Weekly
        Time range: Last 12 weeks
        Breakdown: By discount code (top 10 codes by usage volume)
        Compare: Previous period (prior 12 weeks)
        Chart type: Dual-axis: left axis AOV ($) showing Series A and Series B side-by-side bars per discount code, right axis Series E (net revenue impact) as a line

        Annotations:
        - Flag any discount code where AOV with discount is LOWER than AOV without (the discount is being used by lower-intent buyers: pure margin loss with no basket-growth benefit).
        - Flag any discount code with negative Series E (Net Revenue Impact): this code is cannibalizing full-price demand more than it's creating new orders.
        - Highlight discount codes where AOV with discount > AOV without (the discount actually grows the basket: keep these and scale).
        - Surface the trailing-12-week total discount cost as a % of total revenue (industry benchmark: <15% for healthy DTC; >20% indicates over-reliance on promotions).

        Use case: the cannibalization question is the most important and most-avoided ecommerce analysis. Most brands track discount usage but never measure whether discounts CREATE orders that wouldn't otherwise happen, vs. just SHIFTING demand to discounted moments. This recipe makes the distinction visible.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Discount impact on order value

Shows whether your discount codes actually grow the basket or just hand money away, code by code.

## Before you run it

- Connect shopify

## What it does

1. **Test whether discounts grow baskets** (`build_insights_report`)

   Average order value for discounted orders against orders with no code, weekly over 12 weeks for the top 10 codes, alongside the total discount cost and the net revenue effect. Flags any code where discounted baskets are smaller or the net effect is negative.

## What you end up with

- **report** (report): Report produced by this recipe.
