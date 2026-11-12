---
frontmatter_id: email-sms-campaign-performance-dashboard
slash_command: /email-sms-campaign-performance-dashboard
description: Ranks every email and SMS send by the revenue it produced, so you can see which subject lines, offers and content earn their place.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Ranks every email and SMS send by the revenue it produced, showing which subject lines, offers and content earn
    their place.
  parameters:
  - name: defaultDateRange
    type: enum
    label: Default date range
    default: last_30_days
    required: false
    options:
    - last_7_days
    - last_30_days
    - last_90_days
  - name: exclusionPeriod
    type: enum
    label: Exclude recent period
    default: today
    required: false
    options:
    - today
    - last_3_days
    - last_7_days
  - name: attributionWindowDays
    type: number
    label: Attribution window (days after click or send)
    default: 7
    required: false
  - name: leaderboardRowLimit
    type: number
    label: Leaderboard row limit
    default: 30
    required: false
  - name: leaderboardSortMetric
    type: enum
    label: Default leaderboard sort metric
    default: revenue_per_send
    required: false
    options:
    - revenue
    - revenue_per_send
    - open_rate
    - click_rate
    - ctor
    - conversion_rate
  requirements:
  - slot: campaign_performance_leaderboard
    kind: segment
    meaning: Per-campaign send, open, click, conversion and revenue metrics for email and SMS sends
  - slot: email_sent
    kind: event
    meaning: A customer was sent an email
    properties:
    - name: campaign_id
      type: string
      meaning: Identifier of the email campaign that produced the send
      optional: false
  - slot: email_opened
    kind: event
    meaning: A customer opened an email
  - slot: email_clicked
    kind: event
    meaning: A customer clicked a link in an email
  - slot: placed_order
    kind: event
    meaning: A customer placed an order
  - slot: view_page
    kind: event
    meaning: A customer viewed a web page
  - slot: messaged_sms
    kind: event
    meaning: A customer was sent an SMS message
    properties:
    - name: template_id
      type: string
      meaning: Identifier of the SMS template used
      optional: false
    - name: journey_id
      type: string
      meaning: Identifier of the journey that sent the SMS
      optional: true
    optional: true
  - slot: email_purchase
    kind: segment
    meaning: Customers who were sent an email, clicked it and then purchased, for the email-to-purchase funnel
  - slot: revenue_by_channel
    kind: segment
    meaning: Revenue broken down by acquisition channel, including UTM source
  - slot: customer_lifecycle_distribution
    kind: segment
    meaning: Distribution of customers across lifecycle stages such as New, Active, At Risk and Champions
  - slot: sms_connection
    kind: integration
    channel: sms
    meaning: The SMS sender the text goes out from
  steps:
  - id: s1
    builds: dashboard
    uses:
    - campaign_performance_leaderboard
    - email_sent
    - email_opened
    - email_clicked
    - placed_order
    - view_page
    - messaged_sms
    - email_purchase
    - revenue_by_channel
    - customer_lifecycle_distribution
    - defaultDateRange
    - exclusionPeriod
    - attributionWindowDays
    - leaderboardRowLimit
    - leaderboardSortMetric
    instruction: 'Create a dashboard titled "Email/SMS Campaign Performance" on a 12-column canvas, project visibility, default
      date range {defaultDateRange}, excluding the most recent {exclusionPeriod} of data. Add no board filters by default;
      allow runtime filtering by campaign_id pattern. Break down by campaign_id. Lay it out in four rows. Row 1 (height 200
      px): four metric cards, each 3 columns wide, all sourced from {campaign_performance_leaderboard} as metric visualizations:
      ''Total Sends (30d)'', ''Average Open Rate'', ''Total Email Revenue (30d)'', and ''Average Revenue per Send''. Row 2
      (height 520 px): one full-width 12-column table sourced from {campaign_performance_leaderboard}, showing the top {leaderboardRowLimit}
      campaigns sortable by revenue, revenue per send, open rate, click rate, CTOR and conversion rate, sorted by default
      on {leaderboardSortMetric}. Row 3 (height 440 px): two 6-column cards. Left: a scatter from {campaign_performance_leaderboard}
      with X = click rate, Y = conversion rate, bubble size = revenue per send. Right: a funnel_steps chart from {email_purchase}
      broken down per campaign. Row 4 (height 400 px): two 6-column cards. Left: a bar chart from {revenue_by_channel} filtered
      to UTM source = email. Right: a chart from {customer_lifecycle_distribution} showing lifecycle stage distribution of
      email-engaged users. Interpretation: in the scatter, top-right is replicate-worthy, top-left means fix the landing page,
      bottom-right means A/B test creative, bottom-left means retire the audience or rethink the offer. Use revenue per send
      as the benchmark: $0.10 to $0.50 is typical for DTC, above $1.00 is best-in-class. In the funnel, open-to-click drop
      points to subject line or preheader, click-to-product-page points to landing page, product-page-to-purchase points to
      price or offer. If campaign_id is sparse in {email_sent}, the leaderboard reduces to aggregate email performance without
      per-campaign rows. SMS reporting uses {messaged_sms} with template_id and journey_id in place of the email campaign
      identifier.'
---

# Email and SMS campaign results

Slash command: /email-sms-campaign-performance-dashboard

## Step 1: Build the campaign leaderboard

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
- Card 1: Insights to source recipe: revenue-by-channel, displayMode: chart, vizType: bar (filter: UTM source = email; shows email's contribution to total channel revenue)
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
- campaign-performance-leaderboard depends on Email sent.campaign_id being reliably populated by the workspace's email integration (Klaviyo, Customer.io, Mailchimp). If campaign_id is sparse, the report degrades to aggregate email performance without per-campaign breakdown.
- Attribution from Email clicked to Placed order uses a 7-day window joined via masterID/email matching the Email sent.campaign_id.
- For SMS-side analysis, substitute messaged_sms (which has template_id and journey_id): the recipe handles both channels.
- All other source recipes use canonical events: Email sent, Email opened, Email clicked, Placed order, View page.
