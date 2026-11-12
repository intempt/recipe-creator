---
frontmatter_id: marketing-attribution-dashboard
slash_command: /marketing-attribution-dashboard
description: Answers where revenue comes from across paid, organic, email and search. ROAS and CAC need an ad-spend integration and are not included.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows where revenue comes from across paid, organic, email and search, with channel LTV and funnel views on one
    attribution dashboard (ROAS and CAC excluded).
  parameters:
  - name: defaultDateRange
    type: duration
    label: Default date range
    default: 30 d
    required: false
  - name: emailUtmSource
    type: string
    label: UTM source value for email
    default: email
    required: false
  - name: paidUtmSources
    type: text
    label: UTM source values for paid channels
    default: paid_search, paid_social, paid_other
    required: false
  - name: organicUtmSources
    type: text
    label: UTM source values for organic channels
    default: organic, direct, organic_social
    required: false
  requirements:
  - slot: revenue_by_channel_recipe
    kind: segment
    meaning: Revenue by acquisition channel from placed orders, using the first-touch UTM source on users
  - slot: ltv_curve_recipe
    kind: segment
    meaning: First-purchase cohort lifetime value curve by acquisition channel
  - slot: email_purchase_funnel
    kind: segment
    meaning: Email-driven purchase conversion funnel
  - slot: search_conversion_funnel
    kind: segment
    meaning: Search-driven conversion funnel
  - slot: funnel_dropoff_by_source
    kind: segment
    meaning: Funnel drop-off stages broken down by acquisition source
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total price
      optional: false
  - slot: utm_source_attribute
    kind: attribute
    meaning: The first-touch UTM source recorded on the user
  steps:
  - id: s1
    builds: dashboard
    uses:
    - revenue_by_channel_recipe
    - ltv_curve_recipe
    - email_purchase_funnel
    - search_conversion_funnel
    - funnel_dropoff_by_source
    - placed_order_event
    - utm_source_attribute
    - defaultDateRange
    - emailUtmSource
    - paidUtmSources
    - organicUtmSources
    instruction: 'Create a 12-column dashboard titled "Marketing Attribution" with project visibility, default date range
      {defaultDateRange}, incomplete periods excluded, no board filters by default, and a board-wide breakdown by UTM source
      ({utm_source_attribute}) applied to all cards. Answers "Where is my revenue coming from across paid, organic, email,
      and search?" for Marketing Leads, Performance Marketers and Lifecycle Marketers. Row 1 (height 200 px): four metric
      cards at 3 columns each, all sourced from {revenue_by_channel_recipe} with metric visualization: "Revenue from Top Channel"
      (no filter); "Revenue from Email" filtered to UTM source = {emailUtmSource}; "Revenue from Paid" filtered to UTM source
      in {paidUtmSources}; "Revenue from Organic" filtered to UTM source in {organicUtmSources}. Row 2 (height 400 px): two
      cards at 6 columns each. Left: bar chart from {revenue_by_channel_recipe} showing the full channel breakdown with year-over-year
      comparison. Right: line chart from {ltv_curve_recipe} showing lifetime value by acquisition channel, the highest-leverage
      card for judging which channels acquire customers worth keeping. Row 3 (height 440 px): two funnel charts at 6 columns
      each: left from {email_purchase_funnel}, right from {search_conversion_funnel}. Row 4 (height 400 px): one full-width
      (12 column) small-multiples chart from {funnel_dropoff_by_source} showing funnel drop-off per source, revealing which
      channel leaks at which stage. Revenue is summed from {placed_order_event.total_price}. ROAS and CAC are not included
      because ad-spend data is outside this dashboard.'
---

# Revenue by marketing channel

Slash command: /marketing-attribution-dashboard

## Step 1: Build the attribution board

Create a Dash board (12-column composition canvas) titled "Marketing Attribution".
Persona: Marketing Lead, Performance Marketer, Lifecycle Marketer. Question answered: "Where is my revenue coming from across paid, organic, email, and search?"
IMPORTANT scoping note: the canonical Intempt V2.1 taxonomy does NOT include ad-spend events or ad-spend integration. Therefore this dashboard cannot natively compute ROAS or CAC. It tracks revenue and conversion attributed to channels using UTM source on the Users object, but spend-side metrics require a separate ad-spend integration beyond the scope of this dashboard.
Board-level configuration:
- defaultDateRange: last_30_days
- exclusionPeriod: incomplete_periods
- visibility: project
- boardFilters: none by default
- boardBreakdowns: UTM source: pushed down to all cards (the canonical channel attribution dimension)
Layout: 4 rows.
Row 1: Attribution KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: revenue-by-channel, vizType: metric, titleOverride: "Revenue from Top Channel"
- Card 2: Insights metric to source recipe: revenue-by-channel, vizType: metric, titleOverride: "Revenue from Email", filter: UTM source = email
- Card 3: Insights metric to source recipe: revenue-by-channel, vizType: metric, titleOverride: "Revenue from Paid", filter: UTM source IN (paid_search, paid_social, paid_other)
- Card 4: Insights metric to source recipe: revenue-by-channel, vizType: metric, titleOverride: "Revenue from Organic", filter: UTM source IN (organic, direct, organic_social)
Row 2: Channel revenue breakdown (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: revenue-by-channel, displayMode: chart, vizType: bar (full breakdown with YoY comparison)
- Card 2: Insights to source recipe: first-purchase-cohort-ltv-curve, displayMode: chart, vizType: line (LTV by acquisition channel: answers "which channels acquire customers worth keeping")
Row 3: Channel-specific conversion funnels (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Funnel to source recipe: email-purchase, displayMode: chart, vizType: funnel_steps
- Card 2: Funnel to source recipe: search-conversion, displayMode: chart, vizType: funnel_steps
Row 4: Cross-cutting attribution insight (heightPx: 400, full-width single card at widthUnits: 12):
- Card 1: Funnel to source recipe: funnel-dropoff-attribution-by-source, displayMode: chart (small-multiples per source: the canonical "which channel actually converts" view)
Annotations:
- Row 1's four channel KPIs are filtered views of the same revenue-by-channel recipe: Lovable's translation layer applies the UTM source filter and renders the metric vizType. Adjust the UTM source filters per Card 2/3/4 to match the workspace's actual UTM taxonomy.
- Row 2 Card 2 (LTV by channel) is the highest-leverage card on this dashboard. Channels can have similar revenue but very different LTV. The right channels to scale are those where LTV at month-6 exceeds CAC by a healthy multiple (LTV/CAC ≥ 3.0). Without ad-spend integration, this dashboard surfaces LTV; users must compute CAC externally and combine.
- Row 4's funnel-by-source small-multiples reveals which channels have leaks at which stage: different from "which channel produces revenue" (Row 2).
Taxonomy notes:
- Users.UTM source is the canonical channel attribution attribute (first-touch).
- All revenue computations use Placed order.total_price (Shopify-sourced) summed by channel.
- This dashboard does NOT include CAC or ROAS metrics because ad-spend events are not in canonical taxonomy V2.1.
