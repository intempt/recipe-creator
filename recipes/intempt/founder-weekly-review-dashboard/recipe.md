---
frontmatter_id: founder-weekly-review-dashboard
slash_command: /founder-weekly-review-dashboard
description: 'The one page to read before the Monday team meeting: new customers, churn, revenue, retention and engagement, each against last week and last year.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Gives a founder one Monday page with new customers, churn, revenue, retention and engagement, each compared with
    last week and last year.
  parameters:
  - name: defaultDateRange
    type: enum
    label: Default date range for the board
    default: last_7_days
    options:
    - last_7_days
    - last_30_days
    - last_90_days
  - name: primaryMode
    type: enum
    label: Workspace primary mode
    default: mixed
    options:
    - saas
    - ecommerce
    - mixed
  - name: exclusionPeriod
    type: enum
    label: Exclude periods
    default: incomplete_periods
    options:
    - incomplete_periods
    - none
  requirements:
  - slot: weekly_business_review_report
    kind: knowledge
    meaning: A weekly business review summary report with multiple metric series for signups, paying customers, churn, revenue,
      and active users
  - slot: mrr_movement_report
    kind: knowledge
    meaning: A monthly recurring revenue movement report showing new, expansion, contraction and churned revenue
    optional: true
  - slot: customer_lifecycle_report
    kind: knowledge
    meaning: A customer lifecycle distribution report showing customers moving between lifecycle stages
    optional: true
  steps:
  - id: s1
    builds: dashboard
    uses:
    - weekly_business_review_report
    - mrr_movement_report
    - customer_lifecycle_report
    - defaultDateRange
    - primaryMode
    - exclusionPeriod
    instruction: 'Create a dashboard titled "Founder Weekly Review" on a 12-column canvas with 3 rows, default date range
      {defaultDateRange}, exclusion of {exclusionPeriod}, project visibility, and no board filters or breakdowns. Row 1 (height
      240 px): six metric cards, each 2 columns wide, sourced from {weekly_business_review_report} as metric visualizations
      titled "New Signups (WoW)", "New Paying Customers", "Net New Customers", "Revenue (WoW)", "Active Users (DAU 7d avg)",
      and "Churned Customers". Each card shows the current week value with week-over-week and year-over-year percentage change.
      Row 2 (height 280 px): three cards, each 4 columns wide, sourced from {weekly_business_review_report} as line charts
      titled "Revenue 12-Week Trend", "Net New Customers Trend", and "Engagement Trend (DAU)". Row 3 (height 360 px): one
      full-width card (12 columns) whose content depends on {primaryMode}: for saas, a stacked column waterfall chart from
      {mrr_movement_report}; for ecommerce, a lifecycle distribution chart with migration view from {customer_lifecycle_report};
      for mixed, a full table from {weekly_business_review_report}.'
---

# Monday morning scorecard

Slash command: /founder-weekly-review-dashboard

## Step 1: Build the weekly scorecard

Create a Dash board (12-column composition canvas) titled "Founder Weekly Review".
Persona: Founder, CEO, or Head-of-Operations running the weekly cadence. Question answered: "What's the one-pager I look at every Monday before my team meeting?"
This dashboard is mode-agnostic: it auto-adapts to the workspace's primary mode (saas, ecommerce, or mixed). The cards default to the most relevant configuration per mode.
Board-level configuration:
- defaultDateRange: last_7_days (this-week view): but cards default to comparing against prior week and YoY
- exclusionPeriod: incomplete_periods
- visibility: project
- boardFilters: none by default
- boardBreakdowns: none
Layout: 3 rows (intentionally compact: this is a one-pager).
Row 1: Headline scorecard (heightPx: 240, six metric cards at widthUnits: 2 each):
- Card 1: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "New Signups (WoW)"
- Card 2: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "New Paying Customers"
- Card 3: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Net New Customers"
- Card 4: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Revenue (WoW)"
- Card 5: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Active Users (DAU 7d avg)"
- Card 6: Insights metric to source recipe: weekly-business-review-summary, vizType: metric, titleOverride: "Churned Customers"
Row 2: Trend strip (heightPx: 280, three cards at widthUnits: 4 each):
- Card 1: Insights to source recipe: weekly-business-review-summary, displayMode: chart, vizType: line, titleOverride: "Revenue 12-Week Trend"
- Card 2: Insights to source recipe: weekly-business-review-summary, displayMode: chart, vizType: line, titleOverride: "Net New Customers Trend"
- Card 3: Insights to source recipe: weekly-business-review-summary, displayMode: chart, vizType: line, titleOverride: "Engagement Trend (DAU)"
Row 3: Mode-specific anchor (heightPx: 360, full-width single card at widthUnits: 12):
- Mode = saas: Card 1: Insights to source recipe: mrr-movement-decomposition, displayMode: chart, vizType: stacked_column (waterfall view)
- Mode = ecommerce: Card 1: Insights to source recipe: customer-lifecycle-distribution, displayMode: chart (lifecycle distribution with migration view)
- Mode = all (mixed): Card 1: Insights to source recipe: weekly-business-review-summary, displayMode: table (the full WBR scorecard table)
Annotations:
- This dashboard is intentionally compact (3 rows, ~880px total height) so it fits on a single screen for a Monday-morning scan.
- Row 1's six metric cards each show: current week value, week-over-week % change, year-over-year % change.
- Row 3 is the strategic anchor for the week. SaaS founders watch the MRR waterfall; ecommerce founders watch lifecycle migration.
- Row 1 and Row 2 cards are intentionally all sourced from weekly-business-review-summary: that recipe is a multi-series report designed to power exactly this dashboard. Each card pulls a different series (Series A through Series F) of the same report.
Taxonomy notes:
- weekly-business-review-summary is mode-aware and adapts its underlying queries based on the workspace's primary mode.
- All cards reference canonical events through their source recipes.
