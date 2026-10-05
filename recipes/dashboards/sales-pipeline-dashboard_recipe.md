---
name: sales-pipeline-dashboard
description: |
  Use when a user mentions "sales pipeline dashboard", asks for a account executive / sales manager dashboard, or asks for related help. AE / Sales Manager operational view: open pipeline, deal velocity, multi-threading risk, and account engagement on active deals.
arguments: []
intempt:
  id: sales-pipeline-dashboard
  version: 1.0.0
  slashCommand: /sales-pipeline-dashboard
  group: Dashboards
  shortDescription: "A Sales Pipeline dashboard canvas with linked cards for open deals, deal velocity, multi-threading risk, and account engagement."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [b2b]
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
      title: "Build Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      description: "Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below."
      prompt: |
        Create a Dash board (12-column composition canvas) titled "Sales Pipeline".

        Persona: Account Executive or Sales Manager. Question answered: "What deals do I work this week?" — current-state operational view, this-quarter horizon, per-deal/per-rep granularity.

        This dashboard is intentionally distinct from the Revenue Operations Dashboard. Sales Pipeline is operational (deals to work now); Revenue Operations is strategic (GTM trends and health).

        Board-level configuration:
        - defaultDateRange: last_30_days (rolling, since open deals are point-in-time)
        - exclusionPeriod: none
        - visibility: project
        - boardFilters: none by default (each card scopes its own population per recipe definition)
        - boardBreakdowns: owner_id (rep) — pushed down so each card decomposes by rep where applicable

        Layout: 4 rows.

        Row 1 — Operational KPIs (heightPx: 200, four metric cards at widthUnits: 3):
        - Card 1: Insights metric → source recipe: pipeline-value-snapshot, vizType: metric, titleOverride: "Open Pipeline Value"
        - Card 2: Insights metric → source recipe: multi-threading-coverage-by-deal, vizType: metric, titleOverride: "Single-threaded Deals"
        - Card 3: Insights metric → source recipe: accounts-at-risk-count, vizType: metric, titleOverride: "Accounts at Risk"
        - Card 4: Insights metric → source recipe: deal-velocity-by-stage, vizType: metric, titleOverride: "Median Sales Cycle (days)"

        Row 2 — Deal health (heightPx: 440, two cards at widthUnits: 6):
        - Card 1: Insights → source recipe: deal-velocity-by-stage, displayMode: chart, vizType: bar (horizontal bar per stage with median time-in-stage)
        - Card 2: Insights → source recipe: multi-threading-coverage-by-deal, displayMode: chart, vizType: stacked_bar (threading distribution per stage)

        Row 3 — Account-level intelligence (heightPx: 400, full-width single card at widthUnits: 12):
        - Card 1: Insights → source recipe: account-engagement-score-trend, displayMode: table (top 30 accounts ranked by current engagement, with trend sparkline; sortable by week-over-week change)

        Row 4 — Behavioral signals (heightPx: 400, two cards at widthUnits: 6):
        - Card 1: Funnel → source recipe: lead-customer-sales, displayMode: chart, vizType: funnel_steps (high-level pipeline progression)
        - Card 2: Insights → source recipe: pipeline-value-snapshot, displayMode: chart, vizType: bar (full pipeline-value-by-stage view from the recipe)

        Annotations:
        - Row 1's four KPIs are the daily-check numbers: what's in pipeline, what's at risk (single-threaded), what accounts need saving, and how fast we move.
        - Row 3 (the full-width account table) is the key actionable artifact: sorted by week-over-week engagement change, it surfaces both expansion candidates (rising) and churn-risk accounts (falling).

        Taxonomy notes:
        - All source recipes use canonical Intempt events: deal_stage_changed, deal_won, deal_lost, deal_created, meeting_scheduled, session_start, click_on, ticket_created.
        - pipeline-value-snapshot includes weighted-forecast computation (each deal's amount × historical close-rate of its current stage).
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---

# Sales Pipeline Dashboard

## Procedure

1. **Build Dashboard** [`create_dashboard`] — Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below. → produces: dashboard

   ```text
   Create a Dash board (12-column composition canvas) titled "Sales Pipeline".

   Persona: Account Executive or Sales Manager. Question answered: "What deals do I work this week?" — current-state operational view, this-quarter horizon, per-deal/per-rep granularity.

   This dashboard is intentionally distinct from the Revenue Operations Dashboard. Sales Pipeline is operational (deals to work now); Revenue Operations is strategic (GTM trends and health).

   Board-level configuration:
   - defaultDateRange: last_30_days (rolling, since open deals are point-in-time)
   - exclusionPeriod: none
   - visibility: project
   - boardFilters: none by default (each card scopes its own population per recipe definition)
   - boardBreakdowns: owner_id (rep) — pushed down so each card decomposes by rep where applicable

   Layout: 4 rows.

   Row 1 — Operational KPIs (heightPx: 200, four metric cards at widthUnits: 3):
   - Card 1: Insights metric → source recipe: pipeline-value-snapshot, vizType: metric, titleOverride: "Open Pipeline Value"
   - Card 2: Insights metric → source recipe: multi-threading-coverage-by-deal, vizType: metric, titleOverride: "Single-threaded Deals"
   - Card 3: Insights metric → source recipe: accounts-at-risk-count, vizType: metric, titleOverride: "Accounts at Risk"
   - Card 4: Insights metric → source recipe: deal-velocity-by-stage, vizType: metric, titleOverride: "Median Sales Cycle (days)"

   Row 2 — Deal health (heightPx: 440, two cards at widthUnits: 6):
   - Card 1: Insights → source recipe: deal-velocity-by-stage, displayMode: chart, vizType: bar (horizontal bar per stage with median time-in-stage)
   - Card 2: Insights → source recipe: multi-threading-coverage-by-deal, displayMode: chart, vizType: stacked_bar (threading distribution per stage)

   Row 3 — Account-level intelligence (heightPx: 400, full-width single card at widthUnits: 12):
   - Card 1: Insights → source recipe: account-engagement-score-trend, displayMode: table (top 30 accounts ranked by current engagement, with trend sparkline; sortable by week-over-week change)

   Row 4 — Behavioral signals (heightPx: 400, two cards at widthUnits: 6):
   - Card 1: Funnel → source recipe: lead-customer-sales, displayMode: chart, vizType: funnel_steps (high-level pipeline progression)
   - Card 2: Insights → source recipe: pipeline-value-snapshot, displayMode: chart, vizType: bar (full pipeline-value-by-stage view from the recipe)

   Annotations:
   - Row 1's four KPIs are the daily-check numbers: what's in pipeline, what's at risk (single-threaded), what accounts need saving, and how fast we move.
   - Row 3 (the full-width account table) is the key actionable artifact: sorted by week-over-week engagement change, it surfaces both expansion candidates (rising) and churn-risk accounts (falling).

   Taxonomy notes:
   - All source recipes use canonical Intempt events: deal_stage_changed, deal_won, deal_lost, deal_created, meeting_scheduled, session_start, click_on, ticket_created.
   - pipeline-value-snapshot includes weighted-forecast computation (each deal's amount × historical close-rate of its current stage).
   ```
