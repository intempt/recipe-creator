---
name: revenue-by-channel
description: |
  Use when a user mentions "revenue by channel", or asks for related help. Revenue by acquisition channel with share-of-revenue, period comparison, and channel mix shift.
arguments: []
intempt:
  id: revenue-by-channel
  version: 1.0.0
  slashCommand: /revenue-by-channel
  group: Reports
  title: "Revenue by acquisition channel"
  shortDescription: "Shows which channels brought in revenue over the last 30 days, each channel's share, and how the mix has shifted since last year."
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
  prerequisites:
    integrations:
      - { value: shopify, severity: blocking }
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Split revenue by channel"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Order revenue for the top 8 acquisition sources over 30 days with the rest grouped as Other, compared with the prior 30 days and the same period last year, plus a share of revenue trend. Flags any channel whose share moved 5 points or more."
      prompt: |
        Create an Insights report called "Revenue by Acquisition Channel".

        Series A: Event "order_created", aggregation: Sum of "total_price" property, unit: $, label: "Revenue"
        Series B: Computed: Series A / total revenue × 100, unit: %, label: "Share of Revenue"
        Breakdown: By utm_source: use the User.utm_source attribute (Users object has utm_source as a User-scope text attribute) to attribute each order to a channel. Top 8 by revenue, group remainder as "Other".
        Time range: Last 30 days
        Compare: Previous period (prior 30 days) AND year-over-year (same 30 days last year)
        Chart type: Horizontal bar chart for Series A with overlaid period comparison; separate small-multiple area chart for share-of-revenue over time

        Annotations:
        - Add absolute revenue and YoY % change next to each channel bar.
        - Flag any channel whose share of revenue shifted by 5+ percentage points YoY (mix shift).
        - Highlight channels with revenue growth but declining share (growing slower than overall) and channels with declining revenue but stable share (overall slowdown, not channel-specific).

        The mix-shift view is what reveals whether the business is becoming more or less channel-concentrated.

        Taxonomy notes:
        - Users.utm_source is a real text attribute; per-order channel attribution uses the User's first-touch utm_source as authored on the user record.
        - order_created.total_price is the order value (Shopify-sourced). "order_total" is not a real property.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Revenue by acquisition channel

Shows which channels brought in revenue over the last 30 days, each channel's share, and how the mix has shifted since last year.

## Before you run it

- Connect shopify

## What it does

1. **Split revenue by channel** (`build_insights_report`)

   Order revenue for the top 8 acquisition sources over 30 days with the rest grouped as Other, compared with the prior 30 days and the same period last year, plus a share of revenue trend. Flags any channel whose share moved 5 points or more.

## What you end up with

- **report** (report): Report produced by this recipe.
