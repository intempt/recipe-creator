---
description: Shows account health and customer base health using return-rate retention and NPS.
author:
  first_name: Sid
  last_name: Chaudhary
  job_title: Founder & CEO
  avatar: https://cdn.intempt.com/assets/author-profile-pics/sid.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - media
  - social
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
