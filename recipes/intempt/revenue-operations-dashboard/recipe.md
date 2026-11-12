---
frontmatter_id: revenue-operations-dashboard
slash_command: /revenue-operations-dashboard
description: This recipe builds a Revenue Operations dashboard that shows whether the go-to-market engine is healthy, where revenue is leaking, and where spend should shift. It also sets up a monthly check that alerts the RevOps lead when a key indicator keeps getting worse. It suits RevOps leads and CROs preparing for quarterly business reviews.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# GTM health and revenue leakage

## Step 1: Build the RevOps board

Create a Dash board (12-column composition canvas) titled "Revenue Operations".
Persona: RevOps lead or CRO. Question answered: is the go-to-market machine healthy, where is the leakage, and where should spend be re-allocated. Strategic horizon: trailing 90 days plus cohort views, at segment, source and cohort granularity rather than per-rep.
Board-level configuration:
- defaultDateRange: last_90_days
- exclusionPeriod: incomplete_periods
- visibility: project
- boardFilters: none by default
- boardBreakdowns: UTM source (lead source): pushed down so cards decompose by acquisition channel where applicable
Layout: 4 rows.
Row 1: Strategic KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: win-rate-trend, vizType: metric, titleOverride: "Trailing-90d Win Rate"
- Card 2: Insights metric to source recipe: deal-velocity-by-stage, vizType: metric, titleOverride: "Median Sales Cycle (Closed Deals)"
- Card 3: Funnel metric to source recipe: lead-to-mql-to-sql-funnel, vizType: metric, titleOverride: "MQL to Closed-Won Rate"
- Card 4: Retention metric to source recipe: net-revenue-retention-by-cohort, vizType: metric, titleOverride: "Trailing 12-Month Blended Net Revenue Retention"
Row 2: Funnel health (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Funnel to source recipe: lead-to-mql-to-sql-funnel, displayMode: chart, vizType: funnel_steps (the full qualification funnel)
- Card 2: Funnel to source recipe: funnel-dropoff-attribution-by-source, displayMode: chart, vizType: funnel_steps (small-multiples by source)
Row 3: Win-loss intelligence (heightPx: 400, full-width single card at widthUnits: 12):
- Card 1: Insights to source recipe: win-loss-analysis, displayMode: chart, vizType: bar (won versus lost by source, with stage-at-loss decomposition view)
Row 4: Trend and revenue retention (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: win-rate-trend, displayMode: chart, vizType: line (trailing win-rate trend with rolling 90-day smoothing)
- Card 2: Retention to source recipe: net-revenue-retention-by-cohort, displayMode: chart (multi-line cohort Net Revenue Retention curves)
Annotations:
- This board is read monthly, for the QBR cadence, not daily or weekly.
- Row 1's four KPIs are leading indicators: a declining win rate, a lengthening sales cycle, a falling MQL-to-Won rate, or Net Revenue Retention dipping below 100 percent each warrant review.
- Row 3's breakdown by source shows where to invest more or less; the breakdown by stage-at-loss shows whether losses come from qualification or from closing.
Taxonomy notes:
- All source recipes use canonical events: Deal won, Deal lost, Deal stage changed, Lead stage changed, User created, Subscription started, Subscription updated, Subscription canceled.
- net-revenue-retention-by-cohort depends on Subscription updated.changed_fields parsing for the expansion and contraction split.

## Step 2: Escalate when a leading indicator breaks

Create a workflow called "RevOps Monthly Leading-Indicator Check" that runs monthly, on the same cadence as the board's QBR review. Read the four Row 1 KPIs: Trailing-90d Win Rate, Median Sales Cycle, MQL to Closed-Won Rate, and Trailing 12-Month Blended Net Revenue Retention. When any of them has moved against the business for two consecutive months (win rate down, sales cycle up, MQL-to-Won down, or Net Revenue Retention below 100 percent), create a task assigned to the RevOps lead, titled with the name of the indicator that declined, with the two months of values and a link to the dashboard. Post the full set of four KPI values to the RevOps Slack channel every month regardless of outcome. Use the result of "Build the RevOps board".
