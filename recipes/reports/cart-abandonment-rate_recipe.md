---
name: cart-abandonment-rate
description: |
  Use when a user mentions "cart abandonment rate", or asks for related help. Cart abandonment rate by device with previous-period comparison and a 70% benchmark line.
arguments: []
intempt:
  id: cart-abandonment-rate
  version: 1.0.0
  slashCommand: /cart-abandonment-rate
  group: Reports
  shortDescription: "An Insights report named Cart Abandonment Rate showing weekly abandonment rate by device with prior-period comparison and a 70% benchmark line."
  availability: coming-soon
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
        Create an Insights report called "Cart Abandonment Rate".

        Series A: Event "cart_created", aggregation: Count Unique Users
        Series B: Event "order_created", aggregation: Count Unique Users
        Formula: ((A - B) / A) × 100, unit: %, label: "Abandonment Rate"
        Time granularity: Weekly
        Time range: Last 8 weeks
        Breakdown: By "device_type" attribute on the Users object (desktop, mobile, tablet)
        Compare: Previous period (previous 8 weeks)
        Chart type: Line chart with previous-period overlay

        Annotations:
        - Add a horizontal benchmark line at 70% (industry baseline; abandonment above this is losing material revenue).
        - Highlight any week where abandonment rate exceeded the previous period by 5 percentage points or more.

        Identify which device type has the highest abandonment rate and whether the gap between mobile and desktop is widening over time.

        Taxonomy notes:
        - "cart_created" and "order_created" are canonical events. cart_created carries cart_id and items.
        - Users object has device_type as an enum attribute.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Cart Abandonment Rate

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Cart Abandonment Rate".

   Series A: Event "cart_created", aggregation: Count Unique Users
   Series B: Event "order_created", aggregation: Count Unique Users
   Formula: ((A - B) / A) × 100, unit: %, label: "Abandonment Rate"
   Time granularity: Weekly
   Time range: Last 8 weeks
   Breakdown: By "device_type" attribute on the Users object (desktop, mobile, tablet)
   Compare: Previous period (previous 8 weeks)
   Chart type: Line chart with previous-period overlay

   Annotations:
   - Add a horizontal benchmark line at 70% (industry baseline; abandonment above this is losing material revenue).
   - Highlight any week where abandonment rate exceeded the previous period by 5 percentage points or more.

   Identify which device type has the highest abandonment rate and whether the gap between mobile and desktop is widening over time.

   Taxonomy notes:
   - "cart_created" and "order_created" are canonical events. cart_created carries cart_id and items.
   - Users object has device_type as an enum attribute.
   ```
