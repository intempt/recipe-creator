---
frontmatter_id: revenue-operations-dashboard
slash_command: /revenue-operations-dashboard
description: Answers where the go-to-market machine leaks over a trailing 90 days, by source and cohort rather than by rep, so you can move spend and fix process.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows where the go-to-market engine leaks over a trailing 90 days by source and cohort, so leaders can re-allocate
    spend and fix process.
  parameters:
  - name: defaultDateRange
    type: string
    label: Default date range
    default: last_90_days
  - name: exclusionPeriod
    type: enum
    label: Exclusion period
    default: incomplete_periods
    options:
    - incomplete_periods
    - none
  - name: boardVisibility
    type: enum
    label: Board visibility
    default: project
    options:
    - project
    - private
  - name: boardBreakdown
    type: enum
    label: Board breakdown
    default: utm_source
    options:
    - utm_source
    - none
  - name: boardTitle
    type: string
    label: Board title
    default: Revenue Operations
  requirements:
  - slot: deal_won_event
    kind: event
    meaning: A customer closed a deal as won
    properties:
    - name: utm_source
      type: string
      meaning: Lead acquisition source
      optional: true
    - name: stage_at_loss
      type: string
      meaning: Stage where the deal was lost
      optional: true
  - slot: deal_lost_event
    kind: event
    meaning: A deal was closed as lost
    properties:
    - name: utm_source
      type: string
      meaning: Lead acquisition source
      optional: true
    - name: stage_at_loss
      type: string
      meaning: Stage where the deal was lost
      optional: false
  - slot: deal_stage_changed_event
    kind: event
    meaning: A deal moved from one sales stage to another
    properties:
    - name: stage
      type: string
      meaning: Sales stage the deal moved to
      optional: false
  - slot: lead_stage_changed_event
    kind: event
    meaning: A lead moved to a new qualification stage such as MQL or SQL
    properties:
    - name: stage
      type: string
      meaning: Qualification stage the lead moved to
      optional: false
    - name: utm_source
      type: string
      meaning: Lead acquisition source
      optional: true
  - slot: user_created_event
    kind: event
    meaning: A new user account was created
    properties:
    - name: utm_source
      type: string
      meaning: Lead acquisition source
      optional: true
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: cohort
      type: string
      meaning: Customer acquisition cohort
      optional: true
  - slot: subscription_updated_event
    kind: event
    meaning: A customer subscription was changed
    properties:
    - name: changed_fields
      type: text
      meaning: Fields changed on the subscription, used to split expansion from contraction
      optional: false
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
    properties:
    - name: cohort
      type: string
      meaning: Customer acquisition cohort
      optional: true
  steps:
  - id: s1
    builds: dashboard
    uses:
    - deal_won_event
    - deal_lost_event
    - deal_stage_changed_event
    - lead_stage_changed_event
    - user_created_event
    - subscription_started_event
    - subscription_updated_event
    - subscription_canceled_event
    - defaultDateRange
    - exclusionPeriod
    - boardVisibility
    - boardBreakdown
    - boardTitle
    instruction: 'Create a 12-column dashboard titled "{boardTitle}" for RevOps leads and CROs to review monthly. Set default
      date range to {defaultDateRange}, exclusion period to {exclusionPeriod}, visibility to {boardVisibility}, and no board
      filters by default. Push the {boardBreakdown} breakdown down so cards split by acquisition channel where applicable.
      Use 4 rows. Row 1 (height 200px): four metric cards at 3 width units each, titled "Trailing-90d Win Rate" (win-rate
      trend metric), "Median Sales Cycle (Closed Deals)" (deal velocity by stage metric), "MQL to Closed-Won Rate" (lead-to-MQL-to-SQL
      funnel metric), and "Trailing 12-Month Blended NRR" (net revenue retention by cohort metric). Row 2 (height 440px):
      two cards at 6 width units each: the full qualification funnel as funnel steps chart, and funnel drop-off attribution
      by source as small-multiple funnel steps. Row 3 (height 400px): one full-width card at 12 width units showing won versus
      lost by source as a bar chart with stage-at-loss decomposition (win-loss analysis). Row 4 (height 440px): two cards
      at 6 width units each: a line chart of trailing win rate with rolling 90-day smoothing, and a multi-line chart of cohort
      NRR curves. Add these annotations: the board is for monthly QBR review, read once per month for inflection points; Row
      1 KPIs are early-warning signs (declining win rate, lengthening sales cycle, falling MQL to Won, NRR below 100%); Row
      3 is the strategic centerpiece, where the source breakdown shows where to invest more or less and the stage-at-loss
      breakdown shows whether losses come from qualification (top-funnel ICP issue) or closing (late-funnel competition or
      pricing issue). Keep this board''s cards distinct from any sales pipeline board with zero card overlap.'
---

# GTM health and revenue leakage

Slash command: /revenue-operations-dashboard

## Step 1: Build the RevOps board

Create a Dash board (12-column composition canvas) titled "Revenue Operations".
Persona: RevOps lead or CRO. Question answered: "Is the GTM machine healthy? Where's the leakage and where do we re-allocate?": strategic horizon (trailing 90 days + cohort views), aggregate granularity (segment/source/cohort, not per-rep), drives spend re-allocation and process changes.
This dashboard is intentionally distinct from the Sales Pipeline Dashboard. RevOps is strategic and trend-oriented (is the funnel getting healthier?); Sales Pipeline is operational (which deals to work now). Zero card overlap between the two.
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
- Card 4: Retention metric to source recipe: net-revenue-retention-by-cohort, vizType: metric, titleOverride: "Trailing 12-Month Blended NRR"
Row 2: Funnel health (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Funnel to source recipe: lead-to-mql-to-sql-funnel, displayMode: chart, vizType: funnel_steps (the full qualification funnel)
- Card 2: Funnel to source recipe: funnel-dropoff-attribution-by-source, displayMode: chart, vizType: funnel_steps (small-multiples by source)
Row 3: Win-loss intelligence (heightPx: 400, full-width single card at widthUnits: 12):
- Card 1: Insights to source recipe: win-loss-analysis, displayMode: chart, vizType: bar (won vs. lost by source, with stage-at-loss decomposition view)
Row 4: Trend and revenue retention (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: win-rate-trend, displayMode: chart, vizType: line (trailing win-rate trend with rolling-90d smoothing)
- Card 2: Retention to source recipe: net-revenue-retention-by-cohort, displayMode: chart (multi-line cohort NRR curves)
Annotations:
- This board is meant for monthly QBR review, not daily/weekly. The right cadence is reading it once per month, looking for inflection points.
- Row 1 KPIs are 4 leading indicators: declining win rate, lengthening sales cycle, falling MQL to Won, or NRR dipping below 100% are all early-warning signs that warrant strategic intervention.
- Row 3 (full-width win-loss) is the strategic centerpiece: the breakdown by source shows where to invest more vs. less; the breakdown by stage-at-loss shows whether losses come from qualification (top-funnel ICP issue) or closing (late-funnel competition/pricing issue).
Taxonomy notes:
- All source recipes use canonical events: Deal won, Deal lost, Deal stage changed, Lead stage changed, User created, Subscription started, Subscription updated, Subscription canceled.
- net-revenue-retention-by-cohort depends on Subscription updated.changed_fields parsing for expansion/contraction split.
- win-rate-trend (new in v5) is the single-metric tracking version of win-loss-analysis.
