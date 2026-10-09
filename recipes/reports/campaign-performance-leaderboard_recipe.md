---
name: campaign-performance-leaderboard
description: |
  Use when a user mentions "campaign performance leaderboard", or asks for related help. Per-campaign email/SMS performance: sent, opened, clicked, converted, revenue, revenue-per-send: the canonical Klaviyo-style view.
arguments: []
intempt:
  id: campaign-performance-leaderboard
  version: 1.0.0
  slashCommand: /campaign-performance-leaderboard
  group: Reports
  title: "Campaign performance leaderboard"
  shortDescription: "Ranks every email and SMS campaign of the last 90 days by revenue, with sends, opens, clicks, conversions, open rate, click rate and revenue per send."
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
      title: "Rank campaigns by revenue"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "One row per campaign over the last 90 days: sends, opens, clicks, attributed orders and revenue, plus open rate, click rate, click to open rate, conversion rate and revenue per send. Orders are attributed on a 7 day window and rows sort by revenue."
      prompt: |
        Create an Insights report called "Campaign Performance Leaderboard".

        Series A: Event "Email sent", aggregation: Count grouped by campaign, label: "Sends"
        Series B: Event "Email opened", aggregation: Count Unique users grouped by campaign (joined via the email's campaign), label: "Opens"
        Series C: Event "Email clicked", aggregation: Count Unique users grouped by campaign, label: "Clicks"
        Series D: Event "Placed order" where the user previously emitted Email clicked or Email opened for that campaign within the attribution window, aggregation: Count Unique users grouped by campaign, label: "Conversions"
        Series E: Sum of the order total for those attributed orders, grouped by campaign, unit: $, label: "Attributed Revenue"
        Series F: Computed: Series B / Series A × 100, unit: %, label: "Open Rate"
        Series G: Computed: Series C / Series A × 100, unit: %, label: "Click Rate"
        Series H: Computed: Series C / Series B × 100, unit: %, label: "Click-to-Open Rate (CTOR)"
        Series I: Computed: Series D / Series A × 100, unit: %, label: "Conversion Rate"
        Series J: Computed: Series E / Series A, unit: $, label: "Revenue per Send (RPS)"

        Attribution window: 7 days (configurable; standard email attribution is 7-day click, 1-day view-through)
        Time range: Last 90 days of campaigns
        Breakdown: By campaign (each row = one campaign)
        Sort: By Series E (Revenue) descending by default
        Chart type: Sortable table (the leaderboard: top 30 campaigns), with secondary scatter plot: x-axis = Click Rate, y-axis = Conversion Rate, bubble size = Revenue per Send. Top-right quadrant = highest-performing campaigns on both engagement and conversion.

        Sort modes (toggle):
        - By Attributed Revenue (descending) to "Highest Earners"
        - By Revenue per Send (descending) to "Most Efficient"
        - By Open Rate (descending) to "Best Subject Lines"
        - By Click-to-Open Rate (descending) to "Best Email Content"
        - By Conversion Rate (descending) to "Best Landing Page Match"

        Annotations:
        - Add benchmarks: typical DTC ecommerce email open rates 20-30%, click rates 2-5%, conversion rates 0.5-2%, revenue per send $0.10-$0.50 (varies by AOV).
        - Flag campaigns with high open rate but low CTOR (>40% open, <10% CTOR): subject line worked but email content disappointed.
        - Flag campaigns with high CTOR but low conversion (>20% CTOR, <0.5% conversion): landing page or offer mismatch.
        - Highlight the top 3 by Revenue per Send: these are the templates worth replicating.
        - Flag campaigns with negative trend: open rate or CTOR declining vs. trailing 4-campaign average for that audience (subscriber fatigue or list quality erosion).
        - Surface the cumulative revenue from email vs. total store revenue in the period: context for whether the email channel is over- or under-invested.

        Use case: the canonical Klaviyo/Customer.io campaign performance view. Replaces the per-tool campaign reports most ecommerce teams maintain manually, and ties every campaign directly to attributed revenue (the metric that matters).
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Campaign performance leaderboard

Ranks every email and SMS campaign of the last 90 days by revenue, with sends, opens, clicks, conversions, open rate, click rate and revenue per send.

## What it does

1. **Rank campaigns by revenue** (`build_insights_report`)

   One row per campaign over the last 90 days: sends, opens, clicks, attributed orders and revenue, plus open rate, click rate, click to open rate, conversion rate and revenue per send. Orders are attributed on a 7 day window and rows sort by revenue.

## What you end up with

- **report** (report): Report produced by this recipe.
