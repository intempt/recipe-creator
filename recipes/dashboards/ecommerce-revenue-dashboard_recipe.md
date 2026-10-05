---
name: ecommerce-revenue-dashboard
description: |
  Use when a user mentions "e-commerce revenue dashboard", asks for a founder / cmo dashboard, or asks for related help. Founder / CMO revenue overview: top-line revenue, AOV, channel, conversion, and category performance.
arguments: []
intempt:
  id: ecommerce-revenue-dashboard
  version: 1.0.0
  slashCommand: /ecommerce-revenue-dashboard
  group: Dashboards
  shortDescription: "Creates a 12-column e-commerce revenue dashboard with linked cards for revenue, AOV, channel, conversion, and category performance."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: standard
    executionMode: live
    tags: [dashboard]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_dashboard
  procedure:
    - step: 1
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      description: "Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below."
      prompt: |
        Create a Dash board (12-column composition canvas) titled "E-commerce Revenue".

        Persona: Founder or CMO. Question answered: "How much money are we making, where is it coming from, and is the trend healthy?"

        Board-level configuration:
        - defaultDateRange: last_30_days
        - exclusionPeriod: incomplete_periods
        - visibility: project
        - boardFilters: none by default
        - boardBreakdowns: device_type — pushed down to applicable cards

        Layout: 4 rows.

        Row 1 — Revenue KPIs (heightPx: 200, four metric cards at widthUnits: 3):
        - Card 1: Insights metric → source recipe: revenue-by-channel, vizType: metric, titleOverride: "Total Revenue (30d)"
        - Card 2: Insights metric → source recipe: average-order-value-trend, vizType: metric, titleOverride: "AOV"
        - Card 3: Insights metric → source recipe: cart-abandonment-rate, vizType: metric, titleOverride: "Cart Abandonment Rate"
        - Card 4: Insights metric → source recipe: product-category-performance, vizType: metric, titleOverride: "Top Category Revenue Share"

        Row 2 — Revenue trends (heightPx: 400, two cards at widthUnits: 6):
        - Card 1: Insights → source recipe: revenue-by-channel, displayMode: chart, vizType: bar (horizontal, with YoY comparison)
        - Card 2: Insights → source recipe: average-order-value-trend, displayMode: chart, vizType: line (multi-line: AOV, units/order, price/unit decomposition)

        Row 3 — Conversion behavior (heightPx: 400, two cards at widthUnits: 6):
        - Card 1: Funnel → source recipe: browse-purchase-funnel, displayMode: chart, vizType: funnel_steps (with device breakdown)
        - Card 2: Insights → source recipe: cart-abandonment-rate, displayMode: chart, vizType: line (trend with previous-period overlay)

        Row 4 — Category and retention (heightPx: 440, two cards at widthUnits: 6):
        - Card 1: Insights → source recipe: product-category-performance, displayMode: chart, vizType: treemap
        - Card 2: Retention → source recipe: purchase-retention, displayMode: chart, vizType: retention_curve

        Annotations:
        - This is the canonical CMO/Founder weekly-check dashboard for ecommerce. Row 1 is the headline; Row 2 surfaces channel mix shifts; Row 3 surfaces conversion bottlenecks; Row 4 surfaces inventory/retention strategy.
        - The AOV decomposition in Row 2 Card 2 (units/order vs price/unit) is the diagnostic: AOV moving via price = merchandising/pricing impact; AOV moving via units = bundling/cross-sell impact.

        Taxonomy notes:
        - All source recipes use canonical events: order_created, cart_created, page_viewed, checkout_created.
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---

# E-commerce Revenue Dashboard

## Procedure

1. **Build Dashboard** [`create_dashboard`] — Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below. → produces: dashboard

   ```text
   Create a Dash board (12-column composition canvas) titled "E-commerce Revenue".

   Persona: Founder or CMO. Question answered: "How much money are we making, where is it coming from, and is the trend healthy?"

   Board-level configuration:
   - defaultDateRange: last_30_days
   - exclusionPeriod: incomplete_periods
   - visibility: project
   - boardFilters: none by default
   - boardBreakdowns: device_type — pushed down to applicable cards

   Layout: 4 rows.

   Row 1 — Revenue KPIs (heightPx: 200, four metric cards at widthUnits: 3):
   - Card 1: Insights metric → source recipe: revenue-by-channel, vizType: metric, titleOverride: "Total Revenue (30d)"
   - Card 2: Insights metric → source recipe: average-order-value-trend, vizType: metric, titleOverride: "AOV"
   - Card 3: Insights metric → source recipe: cart-abandonment-rate, vizType: metric, titleOverride: "Cart Abandonment Rate"
   - Card 4: Insights metric → source recipe: product-category-performance, vizType: metric, titleOverride: "Top Category Revenue Share"

   Row 2 — Revenue trends (heightPx: 400, two cards at widthUnits: 6):
   - Card 1: Insights → source recipe: revenue-by-channel, displayMode: chart, vizType: bar (horizontal, with YoY comparison)
   - Card 2: Insights → source recipe: average-order-value-trend, displayMode: chart, vizType: line (multi-line: AOV, units/order, price/unit decomposition)

   Row 3 — Conversion behavior (heightPx: 400, two cards at widthUnits: 6):
   - Card 1: Funnel → source recipe: browse-purchase-funnel, displayMode: chart, vizType: funnel_steps (with device breakdown)
   - Card 2: Insights → source recipe: cart-abandonment-rate, displayMode: chart, vizType: line (trend with previous-period overlay)

   Row 4 — Category and retention (heightPx: 440, two cards at widthUnits: 6):
   - Card 1: Insights → source recipe: product-category-performance, displayMode: chart, vizType: treemap
   - Card 2: Retention → source recipe: purchase-retention, displayMode: chart, vizType: retention_curve

   Annotations:
   - This is the canonical CMO/Founder weekly-check dashboard for ecommerce. Row 1 is the headline; Row 2 surfaces channel mix shifts; Row 3 surfaces conversion bottlenecks; Row 4 surfaces inventory/retention strategy.
   - The AOV decomposition in Row 2 Card 2 (units/order vs price/unit) is the diagnostic: AOV moving via price = merchandising/pricing impact; AOV moving via units = bundling/cross-sell impact.

   Taxonomy notes:
   - All source recipes use canonical events: order_created, cart_created, page_viewed, checkout_created.
   ```
