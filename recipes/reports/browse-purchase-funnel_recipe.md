---
name: browse-purchase-funnel
description: |
  Use when a user mentions "browse to purchase funnel", or asks for related help. Browse-to-purchase funnel using page views, cart and order events with device-comparison conversion.
arguments: []
intempt:
  id: browse-purchase-funnel
  version: 1.0.0
  slashCommand: /browse-purchase-funnel
  group: Reports
  title: "Browse to purchase funnel"
  shortDescription: "Shows how many shoppers move from a category page to a product page, cart, checkout and a completed order, and where you lose them on each device."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: quick
    executionMode: live
    tags: [funnel]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_funnel_report
  procedure:
    - step: 1
      title: "Trace category page to order"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "A five step funnel from a category page view to a product page, cart, checkout and order, inside a 7 day window, split by desktop, mobile and tablet. Flags the biggest drop and any step where mobile trails desktop by more than 10 points."
      prompt: |
        Create a Funnel report called "Browse to Purchase".

        Steps:
        1. Event "View page" where the content type indicates a category/listing page (or the page URL contains /collections/ or /category/): "Browsed Category"
        2. Event "View page" where the page URL indicates a product detail page (e.g. contains /products/): "Viewed Product Detail"
        3. Event "Cart created": "Added to Cart"
        4. Event "Checkout created": "Started Checkout"
        5. Event "Placed order": "Completed Purchase"

        Conversion window: 7 days
        Breakdown: By the user's device type (desktop, mobile, tablet)
        Compare: Previous period (prior 7 days)

        For each step, also surface:
        - Median time-to-convert from previous step
        - Per-device conversion rate at each step

        Annotations:
        - Flag the step with the largest drop-off (the primary bottleneck).
        - Flag any step where mobile conversion lags desktop by >10 percentage points (mobile UX issue).
        - Highlight any step where overall drop-off worsened by >3 percentage points vs. previous period.

        Industry benchmarks: 2-3% browse-to-buy for fashion, 4-6% for electronics.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Browse to purchase funnel

Shows how many shoppers move from a category page to a product page, cart, checkout and a completed order, and where you lose them on each device.

## What it does

1. **Trace category page to order** (`build_funnel_report`)

   A five step funnel from a category page view to a product page, cart, checkout and order, inside a 7 day window, split by desktop, mobile and tablet. Flags the biggest drop and any step where mobile trails desktop by more than 10 points.

## What you end up with

- **report** (report): Report produced by this recipe.
