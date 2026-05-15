---
name: saas-growth-command-center
description: |
  Use when a user mentions "saas growth command center", asks for a founder dashboard, or asks for related help. Founder-level SaaS growth view: WAU, MRR, trial conversion, retention, activation, and feature adoption on one canvas.
arguments: []
intempt:
  id: saas-growth-command-center
  version: 1.0.0
  slashCommand: /saas-growth-command-center
  group: Dashboards
  shortDescription: "Founder-level SaaS growth view: WAU, MRR, trial conversion, retention, activation, and feature adoption on one canvas."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
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
        Create a Dash board (12-column composition canvas) titled "SaaS Growth Command Center".

        Persona: SaaS founder or GM. Question answered: "Are we growing, and is the growth healthy?"

        Board-level configuration:
        - defaultDateRange: last_30_days
        - exclusionPeriod: incomplete_periods
        - visibility: project
        - boardFilters: none by default (allow user to add plan_tier filter at runtime)
        - boardBreakdowns: none

        Layout: 4 rows × variable cards per row. All cards isLinked: true (live-mirror the source recipe). Widths sum to 12 per row.

        Row 1 — Headline KPIs (heightPx: 200, four metric cards at widthUnits: 3 each):
        - Card 1: Insights metric card → source recipe: weekly-active-users-trend, displayMode: chart, vizType: metric, titleOverride: "Weekly Active Users"
        - Card 2: Insights metric card → source recipe: mrr-trend, displayMode: chart, vizType: metric, titleOverride: "MRR"
        - Card 3: Insights metric card → source recipe: trial-to-paid-conversion-rate, displayMode: chart, vizType: metric, titleOverride: "Trial → Paid"
        - Card 4: Insights metric card → source recipe: stickiness-ratios-dau-wau-mau, displayMode: chart, vizType: metric, titleOverride: "Stickiness (DAU/MAU)"

        Row 2 — Growth trends (heightPx: 400, two cards at widthUnits: 6 each):
        - Card 1: Insights trend → source recipe: mrr-trend, displayMode: chart, vizType: stacked_area
        - Card 2: Funnel → source recipe: signup-activation-funnel, displayMode: chart, vizType: funnel_steps

        Row 3 — Activation depth (heightPx: 400, two cards at widthUnits: 6 each):
        - Card 1: Insights → source recipe: feature-adoption-by-plan, displayMode: chart, vizType: bar
        - Card 2: Insights → source recipe: stickiness-ratios-dau-wau-mau, displayMode: chart, vizType: line (full trend, not just metric)

        Row 4 — Retention and behavior (heightPx: 440, two cards at widthUnits: 6 each):
        - Card 1: Retention → source recipe: user-retention-weekly, displayMode: table (cohort grid)
        - Card 2: Path → source recipe: first-session-paths-after-signup, displayMode: chart, vizType: sankey-style path

        Annotations:
        - The four KPIs in Row 1 should be reviewed alongside the stickiness ratio (Row 1 Card 4) — high WAU/MRR with falling stickiness is a leading indicator of churn.
        - All cards respect the board-level date range; users can override per-card if needed.

        Taxonomy notes:
        - All 7 source recipes are taxonomy-grounded against Intempt V2.1.
        - Cards reference recipe slugs by id; when isLinked: true the card is a live mirror of the source recipe's configuration.
        - KPI cards use the metric vizType applied to the source chart-recipe — Lovable renders the recipe's headline metric as a single number.
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---

# SaaS Growth Command Center

## Procedure

1. **Build Dashboard** [`create_dashboard`] — Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below. → produces: dashboard

   ```text
   Create a Dash board (12-column composition canvas) titled "SaaS Growth Command Center".

   Persona: SaaS founder or GM. Question answered: "Are we growing, and is the growth healthy?"

   Board-level configuration:
   - defaultDateRange: last_30_days
   - exclusionPeriod: incomplete_periods
   - visibility: project
   - boardFilters: none by default (allow user to add plan_tier filter at runtime)
   - boardBreakdowns: none

   Layout: 4 rows × variable cards per row. All cards isLinked: true (live-mirror the source recipe). Widths sum to 12 per row.

   Row 1 — Headline KPIs (heightPx: 200, four metric cards at widthUnits: 3 each):
   - Card 1: Insights metric card → source recipe: weekly-active-users-trend, displayMode: chart, vizType: metric, titleOverride: "Weekly Active Users"
   - Card 2: Insights metric card → source recipe: mrr-trend, displayMode: chart, vizType: metric, titleOverride: "MRR"
   - Card 3: Insights metric card → source recipe: trial-to-paid-conversion-rate, displayMode: chart, vizType: metric, titleOverride: "Trial → Paid"
   - Card 4: Insights metric card → source recipe: stickiness-ratios-dau-wau-mau, displayMode: chart, vizType: metric, titleOverride: "Stickiness (DAU/MAU)"

   Row 2 — Growth trends (heightPx: 400, two cards at widthUnits: 6 each):
   - Card 1: Insights trend → source recipe: mrr-trend, displayMode: chart, vizType: stacked_area
   - Card 2: Funnel → source recipe: signup-activation-funnel, displayMode: chart, vizType: funnel_steps

   Row 3 — Activation depth (heightPx: 400, two cards at widthUnits: 6 each):
   - Card 1: Insights → source recipe: feature-adoption-by-plan, displayMode: chart, vizType: bar
   - Card 2: Insights → source recipe: stickiness-ratios-dau-wau-mau, displayMode: chart, vizType: line (full trend, not just metric)

   Row 4 — Retention and behavior (heightPx: 440, two cards at widthUnits: 6 each):
   - Card 1: Retention → source recipe: user-retention-weekly, displayMode: table (cohort grid)
   - Card 2: Path → source recipe: first-session-paths-after-signup, displayMode: chart, vizType: sankey-style path

   Annotations:
   - The four KPIs in Row 1 should be reviewed alongside the stickiness ratio (Row 1 Card 4) — high WAU/MRR with falling stickiness is a leading indicator of churn.
   - All cards respect the board-level date range; users can override per-card if needed.

   Taxonomy notes:
   - All 7 source recipes are taxonomy-grounded against Intempt V2.1.
   - Cards reference recipe slugs by id; when isLinked: true the card is a live mirror of the source recipe's configuration.
   - KPI cards use the metric vizType applied to the source chart-recipe — Lovable renders the recipe's headline metric as a single number.
   ```
