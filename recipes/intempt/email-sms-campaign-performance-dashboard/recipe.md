---
id: email-sms-campaign-performance-dashboard
title: Email and SMS campaign results
slash_command: /email-sms-campaign-performance-dashboard
group: Dashboards
owner: intempt
curator: sid
summary: Ranks every email and SMS send by the revenue it produced, so you can see which subject lines,
  offers and content earn their place.
description: >-
  Lifecycle marketer view: campaign-level leaderboard with sends, opens, clicks, conversions, revenue
  per send: the canonical Klaviyo-style view.
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
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new dashboard, from step 1 "Build the campaign leaderboard"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the campaign leaderboard
    summary: >-
      Sends, opens, clicks, conversions and revenue per send for every campaign, ranked, with a conversion
      funnel and channel context.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "Email/SMS Campaign Performance".
      Persona: Lifecycle Marketer, Email Manager, or CRM Lead running campaigns through Klaviyo, Customer.io, or similar. Question answered: "Which campaigns are working? Which subject lines, content, and offers drive revenue?"
      Distinct from Marketing Attribution Dashboard (channel-level revenue, mostly paid acquisition) and Ecommerce Lifecycle Dashboard (lifecycle stage migration). Campaign Performance is operational per-send: the dashboard an email marketer opens after every campaign deploy.
      Board-level configuration:
      - defaultDateRange: last_30_days
      - exclusionPeriod: today (most campaign attribution windows extend 7 days; today's data is incomplete)
      - visibility: project
      - boardFilters: none by default; marketers can filter to specific campaign_id patterns (e.g., flow vs. broadcast) at runtime
      - boardBreakdowns: campaign_id
      Layout: 4 rows.
      Row 1: Campaign performance KPIs (heightPx: 200, four metric cards at widthUnits: 3):
      - Card 1: Insights metric to source recipe: campaign-performance-leaderboard, vizType: metric, titleOverride: "Total Sends (30d)"
      - Card 2: Insights metric to source recipe: campaign-performance-leaderboard, vizType: metric, titleOverride: "Average Open Rate"
      - Card 3: Insights metric to source recipe: campaign-performance-leaderboard, vizType: metric, titleOverride: "Total Email Revenue (30d)"
      - Card 4: Insights metric to source recipe: campaign-performance-leaderboard, vizType: metric, titleOverride: "Average Revenue per Send"
      Row 2: The leaderboard (heightPx: 520, full-width single card at widthUnits: 12):
      - Card 1: Insights to source recipe: campaign-performance-leaderboard, displayMode: table (sortable top 30 campaigns by Revenue / Revenue per Send / Open Rate / Click Rate / CTOR / Conversion Rate). The strategic centerpiece: every email marketer's morning view.
      Row 3: Performance scatter and funnel (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: campaign-performance-leaderboard, displayMode: chart, vizType: scatter (X-axis: Click Rate, Y-axis: Conversion Rate, bubble size: Revenue per Send: the four-quadrant performance matrix)
      - Card 2: Funnel to source recipe: email-purchase, displayMode: chart, vizType: funnel_steps (the canonical email-to-purchase journey, with per-campaign breakdown showing where in the funnel campaigns leak)
      Row 4: Channel context (heightPx: 400, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: revenue-by-channel, displayMode: chart, vizType: bar (filter: utm_source = email; shows email's contribution to total channel revenue)
      - Card 2: Insights to source recipe: customer-lifecycle-distribution, displayMode: chart (lifecycle stage distribution of email-engaged users: answers "are emails reaching Champions or At Risk?")
      Annotations:
      - Row 2 (the leaderboard, full-width) is the centerpiece. Default sort is Revenue per Send (RPS): the metric that ties every campaign directly to dollar contribution. Industry benchmarks: $0.10-$0.50 RPS for typical DTC; >$1.00 RPS is best-in-class.
      - Row 3 Card 1 (scatter quadrant) tells you what to copy and what to fix:
       - Top-right quadrant (high CTR + high CR) = your best campaigns; replicate their subject lines, content, and offer structure
       - Top-left (high CTR + low CR) = great email but landing-page mismatch; fix the post-click experience
       - Bottom-right (low CTR + high CR) = great offer but email content underperformed; A/B test creative
       - Bottom-left (low CTR + low CR) = the campaign didn't connect; either retire the audience segment or rethink the offer
      - Row 3 Card 2 (email-purchase funnel) surfaces where in the email-to-purchase journey campaigns leak: open to click drop = subject line/preheader; click to product page = landing page; product page to purchase = price/offer.
      - Row 4 provides context: how big is email as a % of total revenue (Card 1)? And are emails reaching the right lifecycle segments (Card 2)? Emails reaching mostly At Risk customers signal great win-back work; emails reaching mostly New customers signal acquisition-funnel email.
      Taxonomy notes:
      - campaign-performance-leaderboard depends on email_sent.campaign_id being reliably populated by the workspace's email integration (Klaviyo, Customer.io, Mailchimp). If campaign_id is sparse, the report degrades to aggregate email performance without per-campaign breakdown.
      - Attribution from email_clicked to order_created uses a 7-day window joined via masterID/email matching the email_sent.campaign_id.
      - For SMS-side analysis, substitute messaged_sms (which has template_id and journey_id): the recipe handles both channels.
      - All other source recipes use canonical events: email_sent, email_opened, email_clicked, order_created, page_viewed.
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Email and SMS campaign results

Ranks every email and SMS send by the revenue it produced, so you can see which subject lines, offers and content earn their place.

## Steps

1. **Build the campaign leaderboard** (builds dashboard)

   Sends, opens, clicks, conversions and revenue per send for every campaign, ranked, with a conversion funnel and channel context.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new dashboard, from step 1 "Build the campaign leaderboard"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
