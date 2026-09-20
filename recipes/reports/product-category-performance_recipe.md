---
name: product-category-performance
description: |
  Use when a user mentions "product category performance", or asks for related help. Revenue + units by category with period comparison and category-level momentum scoring.
arguments: []
intempt:
  id: product-category-performance
  version: 1.0.0
  slashCommand: /product-category-performance
  group: Reports
  title: "Category performance"
  shortDescription: "Shows revenue and units by product category for the last 30 days, against both the previous month and the same month last year."
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
      title: "Compare categories on revenue"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Revenue, units sold and average order value for the top 12 categories over 30 days, drawn as a treemap sized by revenue and coloured by year on year change. Flags categories where revenue and units are both falling, and where units rise but revenue does not."
      prompt: |
        Create an Insights report called "Category Performance".

        Series A: Event "order_created", aggregation: Sum of "total_price", unit: $, label: "Revenue"
        Series B: Event "order_created", aggregation: Sum of items count (number of line items per order), label: "Units Sold"
        Series C: Computed: Series A / Series B, unit: $, label: "AOV per Category"
        Breakdown: By product category: extracted from order_created.items (each line item carries product_id; resolve to category via the Products record-object). Top 12 categories, group remainder as "Other".
        Time range: Last 30 days
        Compare: Previous period (prior 30 days) AND year-over-year (same 30 days last year)
        Chart type: Treemap sized by Series A revenue, color-coded by YoY % change (green = growing, red = declining)

        Annotations:
        - For each category, label with: revenue, % share of total, MoM change, YoY change.
        - Flag categories with declining revenue AND declining units (true demand softening).
        - Flag categories with rising units but flat revenue (price/discount erosion).
        - Highlight the top 3 momentum categories (highest YoY growth combined with >5% share).

        Taxonomy notes:
        - order_created.items is flattened (product_id, title, quantity, price, sku). Category lookup goes through the Products record-object.
        - "product_category" is not a property on order_created: it's a derived join.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Category performance

Shows revenue and units by product category for the last 30 days, against both the previous month and the same month last year.

## What it does

1. **Compare categories on revenue** (`build_insights_report`)

   Revenue, units sold and average order value for the top 12 categories over 30 days, drawn as a treemap sized by revenue and coloured by year on year change. Flags categories where revenue and units are both falling, and where units rise but revenue does not.

## What you end up with

- **report** (report): Report produced by this recipe.
