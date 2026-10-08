---
id: product-category-performance
title: Category performance
slash_command: /product-category-performance
group: Reports
owner: intempt
curator: aman
summary: >-
  Shows revenue by product category using native bar or pie charts.
description: >-
  Revenue by product category displayed as native bar or pie charts.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  industry:
    - ecommerce
    - finance
  vertical: []
  complexity: quick
  executionMode: live
  tags:
    - insights
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Compare categories on revenue"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Compare categories on revenue
    summary: >-
      Revenue, units sold and average order value for the top 12 categories over 30 days, drawn as a treemap
      sized by revenue and coloured by year on year change. Flags categories where revenue and units are
      both falling, and where units rise but revenue does not.
    builds: report
    description: |-
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
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Category performance

Shows revenue by product category using native bar or pie charts.

## Steps

1. **Compare categories on revenue** (builds report)

   Revenue, units sold and average order value for the top 12 categories over 30 days, drawn as a treemap sized by revenue and coloured by year on year change. Flags categories where revenue and units are both falling, and where units rise but revenue does not.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Compare categories on revenue"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
