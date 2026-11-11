---
frontmatter_id: customer-success-dashboard
slash_command: /customer-success-dashboard
description: This recipe sets up a Customer Success board that shows which accounts need attention this week and whether the overall customer base is healthy. It then adds a weekly routine that sends the most at-risk and most promising accounts to the right people. It is built for customer success leads and managers.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
---

# Account health and churn risk

## Step 1: Build the account health board

Create a Dash board (12-column composition canvas) titled "Customer Success".
Persona: a customer success lead or an individual customer success manager. Question answered: which accounts need attention this week, and is the customer base healthy overall.
Board-level configuration:
- defaultDateRange: last_30_days
- exclusionPeriod: incomplete_periods
- visibility: project
- boardFilters: none by default; a customer success manager typically adds an owner filter at runtime to see their own book of business
- boardBreakdowns: none
Layout: 4 rows.
Row 1: Health KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: accounts-at-risk-count, vizType: metric, titleOverride: "Accounts at Risk"
- Card 2: Insights metric to source recipe: monthly-logo-retention-trend, vizType: metric, titleOverride: "Monthly Logo Retention"
- Card 3: Retention metric to source recipe: net-revenue-retention-by-cohort, vizType: metric, titleOverride: "Trailing 12-Month Net Revenue Retention"
- Card 4: Insights metric to source recipe: nps-tracking, vizType: metric, titleOverride: "NPS Score"
Row 2: Account-level intelligence (heightPx: 440, full-width single card at widthUnits: 12):
- Card 1: Insights to source recipe: account-engagement-score-trend, displayMode: table, the top 30 accounts by current engagement score, sortable by week-over-week change: sorted by decline for save plays, sorted by rise for expansion outreach.
Row 3: Revenue retention dynamics (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Retention to source recipe: net-revenue-retention-by-cohort, displayMode: chart, vizType: line, cohort Net Revenue Retention curves
- Card 2: Insights to source recipe: expansion-revenue-trend, displayMode: chart, vizType: stacked_bar, upgrade versus seat-expansion mix
Row 4: Churn early-warning (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: support-tickets-vs-churn-correlation, displayMode: chart, vizType: line, dual-axis support tickets versus churns
- Card 2: Retention to source recipe: predictive-churn-tiered-intervention, displayMode: chart, the weekly distribution of accounts across churn_risk_score tiers
Annotations:
- Row 1's four KPIs answer the health question from four angles: how many accounts are slipping, is the base being retained, is it paying more, and how does it feel, by NPS.
- Row 2 is the centerpiece a customer success manager works weekly: the decline sort is the save-plays list, the rise sort is the expansion-outreach list.
- Row 4 is leading-indicator territory: a support-ticket spike and a rising share of accounts in the high or critical churn_risk_score tier both typically precede the retention erosion that later shows up in Row 3's Net Revenue Retention curves.
Taxonomy notes:
- All source recipes use canonical events: Session start, Click on, Ticket created, Subscription canceled, Subscription updated, Feedback submitted.
- Account-level rollups use the account each user belongs to.

## Step 2: Route the weekly save list to its owners

Create a workflow called "Customer Success Weekly Routing" that runs weekly, on the same cadence the dashboard is read on. For each account in the top 10 of Row 2's decline sort, create a task for that account's customer success manager, titled with the account's name and the words "Save play", with the account's engagement-score trend and current churn_risk_score tier attached. For each account in the top 10 of the rise sort, create a separate task for the assigned account executive, titled with the account's name and the words "Expansion outreach". Use the result of "Build the account health board".
