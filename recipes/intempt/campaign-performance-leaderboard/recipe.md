---
description: Reports on email and SMS campaign performance over the last 90 days, ranking campaigns by attributed revenue alongside sends, clicks, and conversions.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce
  - finance
---

# Campaign performance leaderboard

Slash command: /campaign-performance-leaderboard

## Step 1: Rank campaigns by revenue

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
