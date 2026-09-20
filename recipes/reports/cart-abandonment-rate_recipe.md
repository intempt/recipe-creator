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
  title: "Cart abandonment rate"
  shortDescription: "Shows what share of shoppers who add to cart never order, week by week and by device, against the 70% industry line."
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
      title: "Track carts that never convert"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "A weekly abandonment rate over 8 weeks, calculated as carts created minus orders placed divided by carts created, split by desktop, mobile and tablet. Draws a benchmark line at 70% and flags weeks that worsened by 5 points or more."
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
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Cart abandonment rate

Shows what share of shoppers who add to cart never order, week by week and by device, against the 70% industry line.

## What it does

1. **Track carts that never convert** (`build_insights_report`)

   A weekly abandonment rate over 8 weeks, calculated as carts created minus orders placed divided by carts created, split by desktop, mobile and tablet. Draws a benchmark line at 70% and flags weeks that worsened by 5 points or more.

## What you end up with

- **report** (report): Report produced by this recipe.
