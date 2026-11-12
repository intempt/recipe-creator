---
frontmatter_id: ecommerce-revenue-dashboard
slash_command: /ecommerce-revenue-dashboard
description: Answers how much you are making, which channels drive it, and whether the trend is holding.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows how much revenue you are making, which channels drive it, and whether the trend is holding, on one weekly
    dashboard for founders and CMOs.
  parameters:
  - name: date_range
    type: duration
    label: Default date range
    default: 30 d
    required: false
  - name: breakdown_property
    type: string
    label: Breakdown property pushed down to cards
    default: device_type
    required: false
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: channel
      type: string
      meaning: Acquisition channel of the order
      optional: false
    - name: device_type
      type: string
      meaning: Device the customer used to order
      optional: true
    - name: order_value
      type: number
      meaning: Total value of the order
      optional: false
    - name: units
      type: number
      meaning: Number of units in the order
      optional: false
    - name: product_category
      type: string
      meaning: Category of the purchased product
      optional: true
  - slot: cart_created_event
    kind: event
    meaning: A customer created a shopping cart
    properties:
    - name: device_type
      type: string
      meaning: Device the customer used
      optional: true
  - slot: view_page_event
    kind: event
    meaning: A customer viewed a page
    properties:
    - name: device_type
      type: string
      meaning: Device the customer used
      optional: true
  - slot: checkout_created_event
    kind: event
    meaning: A customer started checkout
    properties:
    - name: device_type
      type: string
      meaning: Device the customer used
      optional: true
  steps:
  - id: s1
    builds: dashboard
    uses:
    - date_range
    - breakdown_property
    - placed_order_event
    - cart_created_event
    - checkout_created_event
    - view_page_event
    instruction: 'Create a 12-column composition dashboard titled "E-commerce Revenue" with default date range {date_range},
      incomplete periods excluded, visible to the whole project, no board filters by default, and breakdown by {breakdown_property}
      pushed down to applicable cards. Lay it out in four rows. Row 1 (height 200px, four metric cards each 3 columns wide):
      "Total Revenue (30d)" from {placed_order_event} grouped by {placed_order_event.channel}; "AOV" from {placed_order_event.order_value}
      averaged per order; "Cart Abandonment Rate" from {cart_created_event} and {checkout_created_event}; "Top Category Revenue
      Share" from {placed_order_event.product_category}. Row 2 (height 400px, two cards each 6 columns wide): horizontal bar
      chart of revenue by {placed_order_event.channel} with year-over-year comparison; multi-line chart of AOV, units per
      order ({placed_order_event.units}) and price per unit decomposition. Row 3 (height 400px, two cards each 6 columns wide):
      funnel steps chart across {view_page_event}, {cart_created_event}, {checkout_created_event} and {placed_order_event}
      with device breakdown; line chart of cart abandonment rate with previous-period overlay. Row 4 (height 440px, two cards
      each 6 columns wide): treemap of revenue by {placed_order_event.product_category}; retention curve for repeat purchases
      of {placed_order_event}.'
---

# Ecommerce revenue overview

Slash command: /ecommerce-revenue-dashboard

## Step 1: Build the revenue board

Create a Dash board (12-column composition canvas) titled "E-commerce Revenue".
Persona: Founder or CMO. Question answered: "How much money are we making, where is it coming from, and is the trend healthy?"
Board-level configuration:
- defaultDateRange: last_30_days
- exclusionPeriod: incomplete_periods
- visibility: project
- boardFilters: none by default
- boardBreakdowns: device_type: pushed down to applicable cards
Layout: 4 rows.
Row 1: Revenue KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: revenue-by-channel, vizType: metric, titleOverride: "Total Revenue (30d)"
- Card 2: Insights metric to source recipe: average-order-value-trend, vizType: metric, titleOverride: "AOV"
- Card 3: Insights metric to source recipe: cart-abandonment-rate, vizType: metric, titleOverride: "Cart Abandonment Rate"
- Card 4: Insights metric to source recipe: product-category-performance, vizType: metric, titleOverride: "Top Category Revenue Share"
Row 2: Revenue trends (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: revenue-by-channel, displayMode: chart, vizType: bar (horizontal, with YoY comparison)
- Card 2: Insights to source recipe: average-order-value-trend, displayMode: chart, vizType: line (multi-line: AOV, units/order, price/unit decomposition)
Row 3: Conversion behavior (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Funnel to source recipe: browse-purchase-funnel, displayMode: chart, vizType: funnel_steps (with device breakdown)
- Card 2: Insights to source recipe: cart-abandonment-rate, displayMode: chart, vizType: line (trend with previous-period overlay)
Row 4: Category and retention (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: product-category-performance, displayMode: chart, vizType: treemap
- Card 2: Retention to source recipe: purchase-retention, displayMode: chart, vizType: retention_curve
Annotations:
- This is the canonical CMO/Founder weekly-check dashboard for ecommerce. Row 1 is the headline; Row 2 surfaces channel mix shifts; Row 3 surfaces conversion bottlenecks; Row 4 surfaces inventory/retention strategy.
- The AOV decomposition in Row 2 Card 2 (units/order vs price/unit) is the diagnostic: AOV moving via price = merchandising/pricing impact; AOV moving via units = bundling/cross-sell impact.
Taxonomy notes:
- All source recipes use canonical events: Placed order, Cart created, View page, Checkout created.
