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
  shortDescription: "Revenue + units by category with period comparison and category-level momentum scoring."
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
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "Category Performance".

        Series A: Event "order_created", aggregation: Sum of "total_price", unit: $, label: "Revenue"
        Series B: Event "order_created", aggregation: Sum of items count (number of line items per order), label: "Units Sold"
        Series C: Computed — Series A / Series B, unit: $, label: "AOV per Category"
        Breakdown: By product category — extracted from order_created.items (each line item carries product_id; resolve to category via the Products record-object). Top 12 categories, group remainder as "Other".
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
        - "product_category" is not a property on order_created — it's a derived join.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Product Category Performance

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Category Performance".

   Series A: Event "order_created", aggregation: Sum of "total_price", unit: $, label: "Revenue"
   Series B: Event "order_created", aggregation: Sum of items count (number of line items per order), label: "Units Sold"
   Series C: Computed — Series A / Series B, unit: $, label: "AOV per Category"
   Breakdown: By product category — extracted from order_created.items (each line item carries product_id; resolve to category via the Products record-object). Top 12 categories, group remainder as "Other".
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
   - "product_category" is not a property on order_created — it's a derived join.
   ```
