---
frontmatter_id: customer-success-dashboard
slash_command: /customer-success-dashboard
description: Shows account health and customer base health using return-rate retention and NPS.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Gives customer success teams one dashboard showing which accounts are at risk, retention, expansion revenue, NPS,
    and early churn signals to act on weekly.
  parameters:
  - name: dateRange
    type: enum
    label: Default date range
    default: last_30_days
    required: false
    options:
    - last_7_days
    - last_30_days
    - last_90_days
  - name: visibility
    type: enum
    label: Board visibility
    default: project
    required: false
    options:
    - private
    - project
  requirements:
  - slot: accounts_at_risk_metric
    kind: segment
    meaning: A count of accounts showing declining engagement or health, used as the at-risk indicator
  - slot: logo_retention_trend
    kind: segment
    meaning: A monthly trend of customer logo retention rate
  - slot: net_revenue_retention
    kind: segment
    meaning: Net revenue retention by customer cohort over time
  - slot: nps_tracking
    kind: segment
    meaning: Net Promoter Score tracking from customer feedback
  - slot: account_engagement_score
    kind: segment
    meaning: Account-level engagement score trend with week-over-week change
  - slot: expansion_revenue
    kind: segment
    meaning: Expansion revenue trend split by upgrades and seat additions
  - slot: support_tickets_vs_churn
    kind: segment
    meaning: Correlation of support ticket volume with subscription churn over time
  - slot: pre_churn_signals
    kind: segment
    meaning: Behavioral events that precede customer churn, ranked by lift over baseline
  - slot: session_start_event
    kind: event
    meaning: A customer started a session in the product
    properties:
    - name: account
      type: string
      meaning: The account the user belongs to
      optional: false
  - slot: ticket_created_event
    kind: event
    meaning: A customer created a support ticket
    properties:
    - name: account
      type: string
      meaning: The account the user belongs to
      optional: false
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
    properties:
    - name: account
      type: string
      meaning: The account the user belongs to
      optional: false
  - slot: feedback_submitted_event
    kind: event
    meaning: A customer submitted feedback, including an NPS rating
    properties:
    - name: account
      type: string
      meaning: The account the user belongs to
      optional: false
  steps:
  - id: s1
    builds: dashboard
    uses:
    - accounts_at_risk_metric
    - logo_retention_trend
    - net_revenue_retention
    - nps_tracking
    - account_engagement_score
    - expansion_revenue
    - support_tickets_vs_churn
    - pre_churn_signals
    - dateRange
    - visibility
    instruction: 'Create a Dash board (12-column composition canvas) titled "Customer Success" with default date range {dateRange}
      and exclusion period set to incomplete periods. Set visibility to {visibility}. Add no board filters and no breakdowns
      by default; users may add an owner filter at runtime to view their own accounts. Layout in four rows. Row 1 (height
      200 px): four metric cards, each 3 units wide: ''Accounts at Risk'' from {accounts_at_risk_metric} shown as a metric;
      ''Monthly Logo Retention'' from {logo_retention_trend} shown as a metric; ''Trailing-12mo NRR'' from {net_revenue_retention}
      shown as a metric; ''NPS Score'' from {nps_tracking} shown as a metric. Row 2 (height 440 px): one full-width card (12
      units) showing {account_engagement_score} as a table of the top 30 accounts by current engagement score, sortable by
      week-over-week change. Row 3 (height 400 px): two 6-unit cards: a line chart of cohort NRR curves from {net_revenue_retention},
      and a stacked bar chart of the upgrade versus seat expansion mix from {expansion_revenue}. Row 4 (height 440 px): two
      6-unit cards: a dual-axis line chart of support tickets versus churns from {support_tickets_vs_churn}, and a chart ranking
      precursor behavioral signals by lift over baseline from {pre_churn_signals}.'
---

# Account health and churn risk

Slash command: /customer-success-dashboard

## Step 1: Build the account health board

Create a Dash board (12-column composition canvas) titled "Customer Success".
Persona: Customer Success Lead or individual CSM. Question answered: "Which accounts need my attention this week, and is the customer base healthy overall?"
Board-level configuration:
- defaultDateRange: last_30_days
- exclusionPeriod: incomplete_periods
- visibility: project
- boardFilters: none by default; CSMs typically add a filter on owner_id at runtime to view their book of business
- boardBreakdowns: none
Layout: 4 rows.
Row 1: Health KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: accounts-at-risk-count, vizType: metric, titleOverride: "Accounts at Risk"
- Card 2: Insights metric to source recipe: monthly-logo-retention-trend, vizType: metric, titleOverride: "Monthly Logo Retention"
- Card 3: Retention metric to source recipe: net-revenue-retention-by-cohort, vizType: metric, titleOverride: "Trailing-12mo NRR"
- Card 4: Insights metric to source recipe: nps-tracking, vizType: metric, titleOverride: "NPS Score"
Row 2: Account-level intelligence (heightPx: 440, full-width single card at widthUnits: 12):
- Card 1: Insights to source recipe: account-engagement-score-trend, displayMode: table (top 30 accounts by current engagement score, sortable by week-over-week change). The two key sort modes: sort by score-decline (descending) to "accounts to save"; sort by score-rise (descending) to "accounts to expand"
Row 3: Revenue retention dynamics (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Retention to source recipe: net-revenue-retention-by-cohort, displayMode: chart, vizType: line (cohort NRR curves)
- Card 2: Insights to source recipe: expansion-revenue-trend, displayMode: chart, vizType: stacked_bar (upgrade vs. seat expansion mix)
Row 4: Churn early-warning (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: support-tickets-vs-churn-correlation, displayMode: chart, vizType: line (dual-axis tickets vs churns)
- Card 2: Path to source recipe: pre-churn-behavioral-signals, displayMode: chart (precursor-event ranking by lift over baseline)
Annotations:
- Row 1's four KPIs together answer "how is the customer base health" from four angles: how many are slipping (Accounts at Risk), are we keeping them (Logo Retention), are they paying more (NRR), and how do they feel (NPS).
- Row 2 (the full-width account table) is the centerpiece. CSMs work this list weekly: top of the "decline" sort = save plays; top of the "rise" sort = expansion outreach.
- Row 4 is leading-indicator territory: support spikes precede churn by 2-4 weeks, and pre-churn behavioral signals surface 30 days out. Use these to fire intervention before retention erosion shows up in Row 3's NRR curves.
Taxonomy notes:
- All source recipes use canonical events: Session start, Click on, Ticket created, Subscription canceled, Subscription updated, Feedback submitted.
- Account-level rollups via Users.the account the user belongs to.
- accounts-at-risk-count, monthly-logo-retention-trend, and nps-tracking are new v5 recipes designed to fill the headline-KPI slots cleanly.
