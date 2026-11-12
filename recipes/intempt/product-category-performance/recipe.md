---
frontmatter_id: product-category-performance
slash_command: /product-category-performance
description: Shows revenue by product category using native bar or pie charts.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows revenue, units and average order value by product category in a treemap, flagging demand softening, price
    erosion and top momentum categories over the last 30 days.
  parameters:
  - name: window
    type: duration
    label: Analysis time range
    default: 30 d
    required: false
  - name: topCategories
    type: number
    label: Number of categories shown before grouping the rest as Other
    default: 12
    required: false
  - name: momentumMinShare
    type: number
    label: Minimum revenue share (%) for momentum highlight
    default: 5
    required: false
  - name: revenueChangeFlat
    type: number
    label: Change (%) treated as flat for price erosion flag
    default: 0
    required: false
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Total order price
      optional: false
    - name: items
      type: array
      meaning: Line items in the order, each with product_id, title, quantity, price and sku
      optional: false
  - slot: products_record
    kind: attribute
    meaning: Product records that map a product_id to its product category
    properties:
    - name: product_id
      type: string
      meaning: Unique product identifier
      optional: false
    - name: product_category
      type: string
      meaning: Category the product belongs to
      optional: false
  steps:
  - id: s1
    builds: report
    uses:
    - placed_order_event
    - products_record
    - window
    - topCategories
    - momentumMinShare
    - revenueChangeFlat
    instruction: 'Create an Insights report called "Category Performance". Series A: event {placed_order_event}, aggregation
      Sum of {placed_order_event.total_price}, unit $, label "Revenue". Series B: event {placed_order_event}, aggregation
      Sum of number of line items per order (count of {placed_order_event.items}), label "Units Sold". Series C: computed
      Series A divided by Series B, unit $, label "AOV per Category". Breakdown: by product category extracted from {placed_order_event.items},
      resolving each line item''s product_id to its category via {products_record}. Show the top {topCategories} categories
      and group the remainder as "Other". Time range: last {window}. Compare to the previous period (prior {window}) and to
      the same period last year. Chart type: treemap sized by Series A revenue, colored by year-over-year % change (green
      for growing, red for declining). Annotations: for each category, label revenue, % share of total, MoM change and YoY
      change. Flag categories where revenue and units both decline (demand softening). Flag categories where units rise but
      revenue is flat within {revenueChangeFlat}% (price or discount erosion). Highlight the top 3 momentum categories, ranked
      by highest YoY growth among those with at least {momentumMinShare}% revenue share.'
---

# Category performance

Slash command: /product-category-performance

## Step 1: Compare categories on revenue

Create an Insights report called "Category Performance".
Series A: Event "Placed order", aggregation: Sum of "total_price", unit: $, label: "Revenue"
Series B: Event "Placed order", aggregation: Sum of items count (number of line items per order), label: "Units Sold"
Series C: Computed: Series A / Series B, unit: $, label: "AOV per Category"
Breakdown: By product category: extracted from Placed order.items (each line item carries product_id; resolve to category via the Products record-object). Top 12 categories, group remainder as "Other".
Time range: Last 30 days
Compare: Previous period (prior 30 days) AND year-over-year (same 30 days last year)
Chart type: Treemap sized by Series A revenue, color-coded by YoY % change (green = growing, red = declining)
Annotations:
- For each category, label with: revenue, % share of total, MoM change, YoY change.
- Flag categories with declining revenue AND declining units (true demand softening).
- Flag categories with rising units but flat revenue (price/discount erosion).
- Highlight the top 3 momentum categories (highest YoY growth combined with >5% share).
Taxonomy notes:
- Placed order.items is flattened (product_id, title, quantity, price, sku). Category lookup goes through the Products record-object.
- "product_category" is not a property on Placed order: it's a derived join.
