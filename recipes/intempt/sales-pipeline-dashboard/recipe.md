---
frontmatter_id: sales-pipeline-dashboard
slash_command: /sales-pipeline-dashboard
description: Answers which open deals need attention now using weighted forecast and risk or engagement scores on active pipeline.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows which open deals and accounts need attention this week, using weighted pipeline value, deal threading, stage
    velocity, and account engagement trends on one dashboard.
  parameters:
  - name: defaultDateRange
    type: enum
    label: Default date range
    default: last_30_days
    required: false
    options:
    - last_30_days
  - name: dashboardTitle
    type: string
    label: Dashboard title
    default: Sales Pipeline
    required: false
  - name: tableTopN
    type: number
    label: Accounts shown in engagement table
    default: 30
    required: false
  requirements:
  - slot: deal_stage_changed_event
    kind: event
    meaning: A deal moved to a different pipeline stage
    properties:
    - name: owner_id
      type: string
      meaning: Rep who owns the deal
      optional: false
    - name: stage
      type: string
      meaning: Stage the deal moved to
      optional: false
  - slot: deal_won_event
    kind: event
    meaning: A customer closed a deal as won
    properties:
    - name: amount
      type: number
      meaning: Value of the won deal
      optional: false
    - name: owner_id
      type: string
      meaning: Rep who owns the deal
      optional: false
  - slot: deal_lost_event
    kind: event
    meaning: A deal was closed as lost
    properties:
    - name: owner_id
      type: string
      meaning: Rep who owns the deal
      optional: false
  - slot: deal_created_event
    kind: event
    meaning: A new deal was created
    properties:
    - name: amount
      type: number
      meaning: Deal amount
      optional: false
    - name: owner_id
      type: string
      meaning: Rep who owns the deal
      optional: false
  - slot: meeting_scheduled_event
    kind: event
    meaning: A customer meeting was scheduled with a deal contact
    properties:
    - name: owner_id
      type: string
      meaning: Rep who owns the deal
      optional: false
  - slot: session_start_event
    kind: event
    meaning: A customer started a product session
    properties:
    - name: account_id
      type: string
      meaning: Account the session belongs to
      optional: false
  - slot: click_on_event
    kind: event
    meaning: A customer clicked on a tracked element
    properties:
    - name: account_id
      type: string
      meaning: Account the click belongs to
      optional: false
  - slot: ticket_created_event
    kind: event
    meaning: A customer support ticket was created
    properties:
    - name: account_id
      type: string
      meaning: Account the ticket belongs to
      optional: false
  - slot: owner_id_attribute
    kind: attribute
    meaning: The sales rep who owns a deal or account
  - slot: deal_amount_attribute
    kind: attribute
    meaning: The monetary amount of a deal
  - slot: sales_pipeline_stage_close_rate
    kind: attribute
    meaning: Historical close rate for each pipeline stage, used to weight open deals
  steps:
  - id: s1
    builds: dashboard
    uses:
    - deal_stage_changed_event
    - deal_won_event
    - deal_lost_event
    - deal_created_event
    - meeting_scheduled_event
    - session_start_event
    - click_on_event
    - ticket_created_event
    - owner_id_attribute
    - deal_amount_attribute
    - sales_pipeline_stage_close_rate
    - defaultDateRange
    - dashboardTitle
    - tableTopN
    instruction: 'Create a 12-column dashboard titled "{dashboardTitle}" for account executives and sales managers to see
      which deals to work this week. Set the default date range to {defaultDateRange} (rolling), no exclusion period, project
      visibility, and no board-level filters; each card scopes its own population. Push the owner_id breakdown down so each
      card can split by rep where applicable. Use 4 rows. Row 1 (height 200 px): four metric cards, each 3 units wide: "Open
      Pipeline Value" (metric from the pipeline value snapshot, which weights each open deal''s amount by the historical close
      rate of its current stage), "Single-threaded Deals" (metric from multi-threading coverage by deal), "Accounts at Risk"
      (metric from the accounts-at-risk count), and "Median Sales Cycle (days)" (metric from deal velocity by stage). Row
      2 (height 440 px): two cards, each 6 units wide: a horizontal bar chart of median time-in-stage per stage from deal
      velocity by stage, and a stacked bar chart of threading distribution per stage from multi-threading coverage by deal.
      Row 3 (height 400 px): one full-width table of the top {tableTopN} accounts ranked by current engagement from the account
      engagement score trend, with a trend sparkline, sortable by week-over-week change. Row 4 (height 400 px): two cards,
      each 6 units wide: a funnel-steps chart of pipeline progression from the lead-to-customer-sales funnel, and a bar chart
      of pipeline value by stage from the pipeline value snapshot. Annotation: row 1 is the daily check; row 3 is the key
      actionable artifact, since sorting by week-over-week engagement change surfaces both expansion candidates (rising) and
      churn-risk accounts (falling).'
---

# Deals to work this week

Slash command: /sales-pipeline-dashboard

## Step 1: Build the pipeline board

Create a Dash board (12-column composition canvas) titled "Sales Pipeline".
Persona: Account Executive or Sales Manager. Question answered: "What deals do I work this week?": current-state operational view, this-quarter horizon, per-deal/per-rep granularity.
This dashboard is intentionally distinct from the Revenue Operations Dashboard. Sales Pipeline is operational (deals to work now); Revenue Operations is strategic (GTM trends and health).
Board-level configuration:
- defaultDateRange: last_30_days (rolling, since open deals are point-in-time)
- exclusionPeriod: none
- visibility: project
- boardFilters: none by default (each card scopes its own population per recipe definition)
- boardBreakdowns: owner_id (rep): pushed down so each card decomposes by rep where applicable
Layout: 4 rows.
Row 1: Operational KPIs (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: pipeline-value-snapshot, vizType: metric, titleOverride: "Open Pipeline Value"
- Card 2: Insights metric to source recipe: multi-threading-coverage-by-deal, vizType: metric, titleOverride: "Single-threaded Deals"
- Card 3: Insights metric to source recipe: accounts-at-risk-count, vizType: metric, titleOverride: "Accounts at Risk"
- Card 4: Insights metric to source recipe: deal-velocity-by-stage, vizType: metric, titleOverride: "Median Sales Cycle (days)"
Row 2: Deal health (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: deal-velocity-by-stage, displayMode: chart, vizType: bar (horizontal bar per stage with median time-in-stage)
- Card 2: Insights to source recipe: multi-threading-coverage-by-deal, displayMode: chart, vizType: stacked_bar (threading distribution per stage)
Row 3: Account-level intelligence (heightPx: 400, full-width single card at widthUnits: 12):
- Card 1: Insights to source recipe: account-engagement-score-trend, displayMode: table (top 30 accounts ranked by current engagement, with trend sparkline; sortable by week-over-week change)
Row 4: Behavioral signals (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Funnel to source recipe: lead-customer-sales, displayMode: chart, vizType: funnel_steps (high-level pipeline progression)
- Card 2: Insights to source recipe: pipeline-value-snapshot, displayMode: chart, vizType: bar (full pipeline-value-by-stage view from the recipe)
Annotations:
- Row 1's four KPIs are the daily-check numbers: what's in pipeline, what's at risk (single-threaded), what accounts need saving, and how fast we move.
- Row 3 (the full-width account table) is the key actionable artifact: sorted by week-over-week engagement change, it surfaces both expansion candidates (rising) and churn-risk accounts (falling).
Taxonomy notes:
- All source recipes use canonical Intempt events: Deal stage changed, Deal won, Deal lost, Deal created, Meeting scheduled, Session start, Click on, Ticket created.
- pipeline-value-snapshot includes weighted-forecast computation (each deal's amount × historical close-rate of its current stage).
