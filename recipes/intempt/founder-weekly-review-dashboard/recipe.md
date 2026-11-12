---
frontmatter_id: founder-weekly-review-dashboard
slash_command: /founder-weekly-review-dashboard
description: Builds a compact one-page weekly scorecard for founders, CEOs and heads of operations to read before the Monday team meeting, then adds an automatic alert that flags weeks needing a conversation. It adapts to whether the business is SaaS, ecommerce or a mix of both.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
---

# Monday morning scorecard

## Step 1: Build the weekly scorecard

Create a Dash board (12-column composition canvas) titled "Founder Weekly Review".
Persona: a founder, CEO or head of operations running the weekly cadence. Question answered: what is the one page to read before the Monday team meeting.
This dashboard adapts to the workspace's primary mode, SaaS, ecommerce or mixed, and defaults each card to the configuration most relevant to that mode.
Board-level configuration:
- defaultDateRange: last_7_days, with cards also comparing against the prior week and the same week last year
- exclusionPeriod: incomplete_periods
- visibility: project
- boardFilters: none by default
- boardBreakdowns: none
Layout: 3 rows, intentionally compact as a one-pager.
Row 1: Headline scorecard (heightPx: 240, six metric cards at widthUnits: 2 each):
- Card 1: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "New Signups (Week over Week)"
- Card 2: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "New Paying Customers"
- Card 3: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Net New Customers"
- Card 4: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Revenue (Week over Week)"
- Card 5: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Active Users (7-day average)"
- Card 6: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Churned Customers"
Row 2: Trend strip (heightPx: 280, three cards at widthUnits: 4 each):
- Card 1: Insights to source recipe: weekly-business-review-summary, displayMode: chart, vizType: line, titleOverride: "Revenue 12-Week Trend"
- Card 2: Insights to source recipe: weekly-business-review-summary, displayMode: chart, vizType: line, titleOverride: "Net New Customers Trend"
- Card 3: Insights to source recipe: weekly-business-review-summary, displayMode: chart, vizType: line, titleOverride: "Engagement Trend (Daily Active Users)"
Row 3: Mode-specific anchor (heightPx: 360, full-width single card at widthUnits: 12):
- Workspace mode SaaS: Card 1: Insights to source recipe: mrr-movement-decomposition, displayMode: chart, vizType: stacked_column, the waterfall view
- Workspace mode ecommerce: Card 1: Insights to source recipe: customer-lifecycle-distribution, displayMode: chart, lifecycle distribution with migration view
- Workspace mode mixed: Card 1: Insights to source recipe: weekly-business-review-summary, displayMode: table, the full weekly business review table
Annotations:
- This dashboard is intentionally compact, 3 rows at roughly 880 pixels total height, so it fits on one screen for a Monday-morning scan.
- Each Row 1 card shows the current week's value, its week-over-week percent change, and its year-over-year percent change.
- Row 3 is the strategic anchor for the week: a SaaS founder reads the MRR waterfall there, an ecommerce founder reads the lifecycle migration view.
- Row 1 and Row 2 all draw from weekly-business-review-summary, a multi-series report built to power exactly this dashboard; each card pulls a different series from that same report.

## Step 2: Flag the week that needs a conversation

Create a workflow called "Founder Weekly Review Alert" that runs on the same weekly cadence the dashboard is read on. When Churned Customers for the week exceeds New Paying Customers, or when Revenue (Week over Week) is negative for 2 consecutive weeks, create a task for the founder titled "Review this week's scorecard" with the specific metrics that triggered it attached. When neither condition is met, no task is created. Use the result of "Build the weekly scorecard".
