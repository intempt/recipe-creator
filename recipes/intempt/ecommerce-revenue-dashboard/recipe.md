---
description: Answers how much you are making, which channels drive it, and whether the trend is holding.
author:
  first_name: Sid
  last_name: Chaudhary
  job_title: Founder & CEO
  avatar: https://cdn.intempt.com/assets/author-profile-pics/sid.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
  - finance
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
- All source recipes use canonical events: order_created, cart_created, page_viewed, checkout_created.
