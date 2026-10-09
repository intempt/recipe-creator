---
name: email-sms-campaign-performance-dashboard
description: |
  Use when a user mentions "email/sms campaign performance dashboard", asks for a lifecycle marketer / email manager dashboard, or asks for related help. Lifecycle marketer view: campaign-level leaderboard with sends, opens, clicks, conversions, revenue per send: the canonical Klaviyo-style view.
arguments: []
intempt:
  id: email-sms-campaign-performance-dashboard
  version: 1.0.0
  slashCommand: /email-sms-campaign-performance-dashboard
  group: Dashboards
  title: "Email and SMS campaign results"
  shortDescription: "Ranks every email and SMS send by the revenue it produced, so you can see which subject lines, offers and content earn their place."
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
  invokesCommands:
    - create_dashboard
  procedure:
    - step: 1
      title: "Build the campaign leaderboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      description: "Sends, opens, clicks, conversions and revenue per send for every campaign, ranked, with a conversion funnel and channel context."
      prompt: |
        Create a Dash board (12-column composition canvas) titled "Email/SMS Campaign Performance".

        Persona: Lifecycle Marketer, Email Manager, or CRM Lead running campaigns through Klaviyo, Customer.io, or similar. Question answered: "Which campaigns are working? Which subject lines, content, and offers drive revenue?"

        Distinct from Marketing Attribution Dashboard (channel-level revenue, mostly paid acquisition) and Ecommerce Lifecycle Dashboard (lifecycle stage migration). Campaign Performance is operational per-send: the dashboard an email marketer opens after every campaign deploy.

        Board-level configuration:
        - defaultDateRange: last_30_days
        - exclusionPeriod: today (most campaign attribution windows extend 7 days; today's data is incomplete)
        - visibility: project
        - boardFilters: none by default; marketers can filter to specific campaign ID patterns (e.g., flow vs. broadcast) at runtime
        - boardBreakdowns: Campaign ID

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
        - Card 2: Funnel to source recipe: email-purchase, displayMode: chart, vizType: funnel_steps (the email-to-purchase journey, with per-campaign breakdown showing where in the funnel campaigns leak)

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
        - The leaderboard depends on the campaign ID being reliably recorded on each Email sent by the workspace's email integration (Klaviyo, Customer.io, Mailchimp). If the campaign ID is sparse, the report degrades to aggregate email performance without per-campaign breakdown.
        - Attribution from Email clicked to Placed order uses a 7-day window, matched on the person's identity and the campaign that sent the email.
        - For SMS-side analysis, use Messaged SMS (which carries a template and a journey) in place of Email sent: the recipe handles both channels.
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Email and SMS campaign results

Ranks every email and SMS send by the revenue it produced, so you can see which subject lines, offers and content earn their place.

## What it does

1. **Build the campaign leaderboard** (`create_dashboard`)

   Sends, opens, clicks, conversions and revenue per send for every campaign, ranked, with a conversion funnel and channel context.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.
