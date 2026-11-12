---
frontmatter_id: campaign-performance-leaderboard
slash_command: /campaign-performance-leaderboard
description: Reports on email and SMS campaign performance over the last 90 days, ranking campaigns by attributed revenue alongside sends, clicks, and conversions.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Ranks email and SMS campaigns over the last 90 days by attributed revenue, alongside sends, opens, clicks, conversions
    and rate metrics, with benchmark flags.
  parameters:
  - name: attribution_window
    type: duration
    label: Attribution window
    default: 7 d
  - name: time_range
    type: duration
    label: Campaign time range
    default: 90 d
  - name: top_n
    type: number
    label: Number of campaigns shown in leaderboard
    default: 30
  - name: top_highlight_count
    type: number
    label: Number of top campaigns by revenue per send to highlight
    default: 3
  - name: open_rate_flag_threshold
    type: number
    label: High open rate threshold (%)
    default: 40
  - name: ctor_low_threshold
    type: number
    label: Low click-to-open rate threshold (%)
    default: 10
  - name: ctor_high_threshold
    type: number
    label: High click-to-open rate threshold (%)
    default: 20
  - name: conversion_low_threshold
    type: number
    label: Low conversion rate threshold (%)
    default: 0.5
  - name: trailing_campaign_count
    type: number
    label: Trailing campaigns used for trend average
    default: 4
  requirements:
  - slot: email_sent_event
    kind: event
    meaning: A marketing email was sent to a customer
    properties:
    - name: campaign_id
      type: string
      meaning: Identifier of the campaign the email belongs to
      optional: false
    - name: email
      type: string
      meaning: Recipient email address
      optional: false
    - name: sent_at
      type: date
      meaning: Time the email was sent
      optional: false
    - name: subject
      type: string
      meaning: Subject line of the email
      optional: true
  - slot: email_opened_event
    kind: event
    meaning: A customer opened a marketing email
    properties:
    - name: email
      type: string
      meaning: Recipient email address used to join back to the sent email
      optional: false
  - slot: email_clicked_event
    kind: event
    meaning: A customer clicked a link in a marketing email
    properties:
    - name: email
      type: string
      meaning: Recipient email address used to join back to the sent email
      optional: false
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Total value of the order
      optional: false
  steps:
  - id: s1
    builds: report
    uses:
    - email_sent_event
    - email_opened_event
    - email_clicked_event
    - placed_order_event
    - attribution_window
    - time_range
    - top_n
    - top_highlight_count
    - open_rate_flag_threshold
    - ctor_low_threshold
    - ctor_high_threshold
    - conversion_low_threshold
    - trailing_campaign_count
    instruction: 'Create an insights report named "Campaign Performance Leaderboard" covering the last {time_range} of campaigns,
      with one row per campaign_id from {email_sent_event.campaign_id}. Series: (A) Sends = count of {email_sent_event} grouped
      by campaign_id. (B) Opens = unique users with {email_opened_event} joined to {email_sent_event} on the email address,
      grouped by campaign_id. (C) Clicks = unique users with {email_clicked_event} joined to {email_sent_event} on the email
      address, grouped by campaign_id. (D) Conversions = unique users with {placed_order_event} who had a prior {email_clicked_event}
      or {email_opened_event} for the same campaign_id within {attribution_window}, grouped by campaign_id. (E) Attributed
      Revenue = sum of {placed_order_event.total_price} for those attributed orders, grouped by campaign_id, in dollars. Computed:
      Open Rate = B/A x 100 (%); Click Rate = C/A x 100 (%); Click-to-Open Rate (CTOR) = C/B x 100 (%); Conversion Rate =
      D/A x 100 (%); Revenue per Send = E/A (dollars). Sort by Attributed Revenue descending and show the top {top_n} campaigns
      as a sortable table. Add a scatter plot with x = Click Rate, y = Conversion Rate, bubble size = Revenue per Send. Provide
      sort toggles: Highest Earners (Attributed Revenue), Most Efficient (Revenue per Send), Best Subject Lines (Open Rate),
      Best Email Content (CTOR), Best Landing Page Match (Conversion Rate), all descending.'
---

# Campaign performance leaderboard

Slash command: /campaign-performance-leaderboard

## Step 1: Rank campaigns by revenue

Create an Insights report called "Campaign Performance Leaderboard".
Series A: Event "Email sent", aggregation: Count grouped by campaign_id, label: "Sends"
Series B: Event "Email opened", aggregation: Count Unique users grouped by campaign_id (joined via the email's campaign_id), label: "Opens"
Series C: Event "Email clicked", aggregation: Count Unique users grouped by campaign_id, label: "Clicks"
Series D: Event "Placed order" where the user previously emitted Email clicked or Email opened with that campaign_id within the attribution window, aggregation: Count Unique users grouped by campaign_id, label: "Conversions"
Series E: Sum of Placed order.total_price for those attributed orders, grouped by campaign_id, unit: $, label: "Attributed Revenue"
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
- Email sent has campaign_id, email, sent_at, subject: the campaign_id is the canonical campaign identifier.
- Email opened and Email clicked do NOT carry campaign_id directly; attribution requires joining via email or masterID against the Email sent that matches the open/click. Lovable's translation layer must implement this join.
- Placed order attribution to a campaign requires a sequence: the user emitted Email clicked (with the matching campaign_id from join) within the attribution window, then Placed order. Alternative: UTM campaign on Placed order joined to the email's campaign_id (if emails inject UTM campaign into all links).
- This recipe depends on the workspace's email integration (Klaviyo, Customer.io, Mailchimp, custom) populating campaign_id reliably on Email sent. If campaign_id is sparse, the report degrades to aggregate email performance without per-campaign breakdown.
- For SMS-side analysis, substitute messaged_sms (which has template_id and journey_id) instead of email events.
