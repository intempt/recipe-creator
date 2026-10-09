---
name: marketing-attribution-dashboard
description: |
  Use when a user mentions "marketing attribution dashboard", asks for a marketing lead dashboard, or asks for related help. Marketing Lead view: revenue by channel, email-driven revenue, search-driven revenue, and category-level marketing performance. Note: ROAS/CAC require ad-spend integration not in canonical taxonomy.
arguments: []
intempt:
  id: marketing-attribution-dashboard
  version: 1.0.0
  slashCommand: /marketing-attribution-dashboard
  group: Dashboards
  title: "Revenue by marketing channel"
  shortDescription: "Answers where revenue comes from across paid, organic, email and search. Return on ad spend and cost per acquisition need an ad-spend integration and are not included."
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
  prerequisites:
    integrations:
      - { value: shopify, severity: blocking }
  invokesCommands:
    - create_dashboard
  procedure:
    - step: 1
      title: "Build the attribution board"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      description: "Revenue split by channel with email-driven and search-driven revenue broken out, per-channel conversion funnels, and performance by product category."
      prompt: |
        Create a Dash board (12-column composition canvas) titled "Marketing Attribution".

        Persona: Marketing Lead, Performance Marketer, Lifecycle Marketer. Question answered: "Where is my revenue coming from across paid, organic, email, and search?"

        IMPORTANT scoping note: this dashboard has no ad-spend data, so it cannot natively compute ROAS or CAC. It tracks revenue and conversion attributed to channels using the UTM source on the user, but spend-side metrics require a separate ad-spend integration beyond the scope of this dashboard.

        Board-level configuration:
        - defaultDateRange: last_30_days
        - exclusionPeriod: incomplete_periods
        - visibility: project
        - boardFilters: none by default
        - boardBreakdowns: UTM source: pushed down to all cards (the channel attribution dimension)

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
        - Card 1: Funnel to source recipe: funnel-dropoff-attribution-by-source, displayMode: chart (small-multiples per source: the "which channel actually converts" view)

        Annotations:
        - Row 1's four channel KPIs are filtered views of the same revenue-by-channel recipe: Lovable's translation layer applies the UTM source filter and renders the metric vizType. Adjust the UTM source filters per Card 2/3/4 to match the workspace's actual UTM values.
        - Row 2 Card 2 (LTV by channel) is the highest-leverage card on this dashboard. Channels can have similar revenue but very different LTV. The right channels to scale are those where LTV at month-6 exceeds CAC by a healthy multiple (LTV/CAC ≥ 3.0). Without ad-spend integration, this dashboard surfaces LTV; users must compute CAC externally and combine.
        - Row 4's funnel-by-source small-multiples reveals which channels have leaks at which stage: different from "which channel produces revenue" (Row 2).
        - Channel attribution is first-touch, using the UTM source on the user.
        - All revenue computations use the order total (Shopify-sourced) from Placed order, summed by channel.
        - This dashboard does NOT include CAC or ROAS metrics because there is no ad-spend data.
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Revenue by marketing channel

Answers where revenue comes from across paid, organic, email and search. Return on ad spend and cost per acquisition need an ad-spend integration and are not included.

## Before you run it

- Connect shopify

## What it does

1. **Build the attribution board** (`create_dashboard`)

   Revenue split by channel with email-driven and search-driven revenue broken out, per-channel conversion funnels, and performance by product category.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.
