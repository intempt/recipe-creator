---
id: campaign-performance-leaderboard
title: Campaign performance leaderboard
slash_command: /campaign-performance-leaderboard
group: Reports
owner: intempt
summary: Ranks every email and SMS campaign of the last 90 days by revenue, with sends, opens, clicks,
  conversions, open rate, click rate and revenue per send.
description: >-
  Per-campaign email/SMS performance: sent, opened, clicked, converted, revenue, revenue-per-send: the
  canonical Klaviyo-style view.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  complexity: quick
  executionMode: live
  tags:
    - insights
steps:
  - id: s1
    title: Rank campaigns by revenue
    summary: >-
      One row per campaign over the last 90 days: sends, opens, clicks, attributed orders and revenue,
      plus open rate, click rate, click to open rate, conversion rate and revenue per send. Orders are
      attributed on a 7 day window and rows sort by revenue.
    builds: report
    description: |-
      Create an Insights report called "Campaign Performance Leaderboard".
      Series A: Event "email_sent", aggregation: Count grouped by campaign_id, label: "Sends"
      Series B: Event "email_opened", aggregation: Count Unique users grouped by campaign_id (joined via the email's campaign_id), label: "Opens"
      Series C: Event "email_clicked", aggregation: Count Unique users grouped by campaign_id, label: "Clicks"
      Series D: Event "order_created" where the user previously emitted email_clicked or email_opened with that campaign_id within the attribution window, aggregation: Count Unique users grouped by campaign_id, label: "Conversions"
      Series E: Sum of order_created.total_price for those attributed orders, grouped by campaign_id, unit: $, label: "Attributed Revenue"
      Series F: Computed: Series B / Series A × 100, unit: %, label: "Open Rate"
      Series G: Computed: Series C / Series A × 100, unit: %, label: "Click Rate"
      Series H: Computed: Series C / Series B × 100, unit: %, label: "Click-to-Open Rate (CTOR)"
      Series I: Computed: Series D / Series A × 100, unit: %, label: "Conversion Rate"
      Series J: Computed: Series E / Series A, unit: $, label: "Revenue per Send (RPS)"
      Attribution window: 7 days (configurable; standard email attribution is 7-day click, 1-day view-through)
      Time range: Last 90 days of campaigns
      Breakdown: By campaign_id (each row = one campaign)
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
      Taxonomy notes:
      - email_sent has campaign_id, email, sent_at, subject: the campaign_id is the canonical campaign identifier.
      - email_opened and email_clicked do NOT carry campaign_id directly; attribution requires joining via email or masterID against the email_sent that matches the open/click. Lovable's translation layer must implement this join.
      - order_created attribution to a campaign requires a sequence: the user emitted email_clicked (with the matching campaign_id from join) within the attribution window, then order_created. Alternative: utm_campaign on order_created joined to the email's campaign_id (if emails inject utm_campaign into all links).
      - This recipe depends on the workspace's email integration (Klaviyo, Customer.io, Mailchimp, custom) populating campaign_id reliably on email_sent. If campaign_id is sparse, the report degrades to aggregate email performance without per-campaign breakdown.
      - For SMS-side analysis, substitute messaged_sms (which has template_id and journey_id) instead of email events.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Campaign performance leaderboard

Ranks every email and SMS campaign of the last 90 days by revenue, with sends, opens, clicks, conversions, open rate, click rate and revenue per send.

## Steps

1. **Rank campaigns by revenue** (builds report)

   One row per campaign over the last 90 days: sends, opens, clicks, attributed orders and revenue, plus open rate, click rate, click to open rate, conversion rate and revenue per send. Orders are attributed on a 7 day window and rows sort by revenue.

## What you end up with

- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build report.
