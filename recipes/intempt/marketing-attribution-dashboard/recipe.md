---
id: marketing-attribution-dashboard
title: Revenue by marketing channel
slash_command: /marketing-attribution-dashboard
group: Dashboards
owner: intempt
curator: sid
summary: Answers where revenue comes from across paid, organic, email and search. Return on ad spend and
  cost per acquisition need an ad-spend integration and are not included.
description: >-
  Marketing Lead view: revenue by channel, email-driven revenue, search-driven revenue, and category-level
  marketing performance. Note: ROAS/CAC require ad-spend integration not in canonical taxonomy.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  complexity: standard
  executionMode: live
  tags:
    - dashboard
prerequisites:
  integrations:
    - value: shopify
      severity: blocking
touches:
  reads:
    - Your Shopify connection
  writes:
    - A new dashboard, from step 1 "Build the attribution board"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the attribution board
    summary: >-
      Revenue split by channel with email-driven and search-driven revenue broken out, per-channel conversion
      funnels, and performance by product category.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "Marketing Attribution".
      Persona: Marketing Lead, Performance Marketer, Lifecycle Marketer. Question answered: "Where is my revenue coming from across paid, organic, email, and search?"
      IMPORTANT scoping note: the canonical Intempt V2.1 taxonomy does NOT include ad-spend events or ad-spend integration. Therefore this dashboard cannot natively compute ROAS or CAC. It tracks revenue and conversion attributed to channels using utm_source on the Users object, but spend-side metrics require a separate ad-spend integration beyond the scope of this dashboard.
      Board-level configuration:
      - defaultDateRange: last_30_days
      - exclusionPeriod: incomplete_periods
      - visibility: project
      - boardFilters: none by default
      - boardBreakdowns: utm_source: pushed down to all cards (the canonical channel attribution dimension)
      Layout: 4 rows.
      Row 1: Attribution KPIs (heightPx: 200, four metric cards at widthUnits: 3):
      - Card 1: Insights metric to source recipe: revenue-by-channel, vizType: metric, titleOverride: "Revenue from Top Channel"
      - Card 2: Insights metric to source recipe: revenue-by-channel, vizType: metric, titleOverride: "Revenue from Email", filter: utm_source = email
      - Card 3: Insights metric to source recipe: revenue-by-channel, vizType: metric, titleOverride: "Revenue from Paid", filter: utm_source IN (paid_search, paid_social, paid_other)
      - Card 4: Insights metric to source recipe: revenue-by-channel, vizType: metric, titleOverride: "Revenue from Organic", filter: utm_source IN (organic, direct, organic_social)
      Row 2: Channel revenue breakdown (heightPx: 400, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: revenue-by-channel, displayMode: chart, vizType: bar (full breakdown with YoY comparison)
      - Card 2: Insights to source recipe: first-purchase-cohort-ltv-curve, displayMode: chart, vizType: line (LTV by acquisition channel: answers "which channels acquire customers worth keeping")
      Row 3: Channel-specific conversion funnels (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Funnel to source recipe: email-purchase, displayMode: chart, vizType: funnel_steps
      - Card 2: Funnel to source recipe: search-conversion, displayMode: chart, vizType: funnel_steps
      Row 4: Cross-cutting attribution insight (heightPx: 400, full-width single card at widthUnits: 12):
      - Card 1: Funnel to source recipe: funnel-dropoff-attribution-by-source, displayMode: chart (small-multiples per source: the canonical "which channel actually converts" view)
      Annotations:
      - Row 1's four channel KPIs are filtered views of the same revenue-by-channel recipe: Lovable's translation layer applies the utm_source filter and renders the metric vizType. Adjust the utm_source filters per Card 2/3/4 to match the workspace's actual UTM taxonomy.
      - Row 2 Card 2 (LTV by channel) is the highest-leverage card on this dashboard. Channels can have similar revenue but very different LTV. The right channels to scale are those where LTV at month-6 exceeds CAC by a healthy multiple (LTV/CAC ≥ 3.0). Without ad-spend integration, this dashboard surfaces LTV; users must compute CAC externally and combine.
      - Row 4's funnel-by-source small-multiples reveals which channels have leaks at which stage: different from "which channel produces revenue" (Row 2).
      Taxonomy notes:
      - Users.utm_source is the canonical channel attribution attribute (first-touch).
      - All revenue computations use order_created.total_price (Shopify-sourced) summed by channel.
      - This dashboard does NOT include CAC or ROAS metrics because ad-spend events are not in canonical taxonomy V2.1.
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Revenue by marketing channel

Answers where revenue comes from across paid, organic, email and search. Return on ad spend and cost per acquisition need an ad-spend integration and are not included.

## Steps

1. **Build the attribution board** (builds dashboard)

   Revenue split by channel with email-driven and search-driven revenue broken out, per-channel conversion funnels, and performance by product category.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Your Shopify connection

Writes:

- A new dashboard, from step 1 "Build the attribution board"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
