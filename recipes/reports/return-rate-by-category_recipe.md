---
name: return-rate-by-category
description: |
  Use when a user mentions "return rate by category", or asks for related help. Return rate by product category with previous-period comparison and rising-rate flagging.
arguments: []
intempt:
  id: return-rate-by-category
  version: 1.0.0
  slashCommand: /return-rate-by-category
  group: Reports
  title: "Return rate by category"
  shortDescription: "Shows which product categories get returned most, and which ones have got worse since last quarter."
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
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Rank categories by returns"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Return requests as a percentage of fulfilled orders by product category over the last 90 days, compared with the prior 90. Flags any category up more than 5 points and lists the top 5 by volume and the top 5 by rate."
      prompt: |
        Create an Insights report called "Return Rate by Category".

        Series A: Event "Order fulfilled", aggregation: Count
        Series B: Event "Return requested", aggregation: Count
        Formula: (B / A) × 100, unit: %, label: "Return Rate"
        Breakdown: By product category: derive the category from the items on each return, or from the items on the order it belongs to.
        Time range: Last 90 days
        Compare: Previous period (prior 90 days)
        Chart type: Bar chart sorted by total return rate descending

        Annotations:
        - Flag any category where return rate jumped >5 percentage points vs. prior period.
        - Surface top 5 categories by absolute return volume and top 5 by return rate (the lists are usually different and both matter).

        Return reason is not captured on the return itself. To analyze why items come back, join to the refund, which carries a reason, for returns that were refunded.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Return rate by category

Shows which product categories get returned most, and which ones have got worse since last quarter.

## What it does

1. **Rank categories by returns** (`build_insights_report`)

   Return requests as a percentage of fulfilled orders by product category over the last 90 days, compared with the prior 90. Flags any category up more than 5 points and lists the top 5 by volume and the top 5 by rate.

## What you end up with

- **report** (report): Report produced by this recipe.
