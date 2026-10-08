---
id: customer-success-dashboard
title: Account health and churn risk
slash_command: /customer-success-dashboard
group: Dashboards
owner: intempt
curator: sid
summary: >-
  Shows account health and customer base health using return-rate retention and NPS.
description: >-
  CS Lead / CSM view: return-rate retention and NPS for account health checks.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - b2b
    - saas
  industry:
    - ai
    - b2b-saas
    - media
    - social
  vertical: []
  complexity: standard
  executionMode: live
  tags:
    - dashboard
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new dashboard, from step 1 "Build the account health board"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the account health board
    summary: >-
      Accounts at risk, logo retention, trailing 12-month net revenue retention and NPS, plus a sortable
      table of the top 30 accounts by engagement score and week-over-week change.
    builds: dashboard
    description: |-
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
      - All source recipes use canonical events: session_start, click_on, ticket_created, subscription_cancelled, subscription_updated, feedback_submitted.
      - Account-level rollups via Users.primary_account_id.
      - accounts-at-risk-count, monthly-logo-retention-trend, and nps-tracking are new v5 recipes designed to fill the headline-KPI slots cleanly.
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Account health and churn risk

Shows account health and customer base health using return-rate retention and NPS.

## Steps

1. **Build the account health board** (builds dashboard)

   Accounts at risk, logo retention, trailing 12-month net revenue retention and NPS, plus a sortable table of the top 30 accounts by engagement score and week-over-week change.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new dashboard, from step 1 "Build the account health board"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
