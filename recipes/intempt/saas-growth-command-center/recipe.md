---
frontmatter_id: saas-growth-command-center
slash_command: /saas-growth-command-center
description: 'Shows whether you are growing and whether growth is healthy on one dashboard: weekly actives, MRR, trial conversion, activation, retention and feature adoption.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: 'Gives a SaaS founder one dashboard showing whether the business is growing and whether that growth is healthy:
    weekly actives, MRR, trial conversion, activation, retention and feature adoption.'
  parameters:
  - name: defaultDateRange
    type: duration
    label: Default date range
    default: 30 d
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
  requirements:
  - slot: weekly_active_users_trend
    kind: segment
    meaning: Insights recipe tracking weekly active users over time
  - slot: mrr_trend
    kind: segment
    meaning: Insights recipe tracking monthly recurring revenue over time
  - slot: trial_to_paid_conversion_rate
    kind: segment
    meaning: Insights recipe tracking the trial to paid conversion rate
  - slot: stickiness_ratios_dau_wau_mau
    kind: segment
    meaning: Insights recipe tracking DAU/WAU/MAU stickiness ratios
  - slot: signup_activation_funnel
    kind: segment
    meaning: Funnel recipe tracking signup to activation steps
  - slot: feature_adoption_by_plan
    kind: segment
    meaning: Insights recipe tracking feature adoption broken down by plan
  - slot: user_retention_weekly
    kind: segment
    meaning: Retention recipe showing weekly cohort retention
  - slot: first_session_paths_after_signup
    kind: segment
    meaning: Path recipe showing user paths in the first session after signup
  steps:
  - id: s1
    builds: dashboard
    uses:
    - weekly_active_users_trend
    - mrr_trend
    - trial_to_paid_conversion_rate
    - stickiness_ratios_dau_wau_mau
    - signup_activation_funnel
    - feature_adoption_by_plan
    - user_retention_weekly
    - first_session_paths_after_signup
    - defaultDateRange
    - exclusionPeriod
    - boardVisibility
    instruction: 'Create a dashboard titled "SaaS Growth Command Center" on a 12-column canvas. Set the default date range
      to {defaultDateRange} and the exclusion period to {exclusionPeriod}. Set visibility to {boardVisibility}. No board filters
      or breakdowns by default; users may add a plan_tier filter at runtime. Mark every card as linked so it live-mirrors
      its source recipe. Row 1 (height 200 px): four metric cards, each 3 units wide, displayed as charts with vizType metric:
      {weekly_active_users_trend} titled "Weekly Active Users"; {mrr_trend} titled "MRR"; {trial_to_paid_conversion_rate}
      titled "Trial to Paid"; {stickiness_ratios_dau_wau_mau} titled "Stickiness (DAU/MAU)". Row 2 (height 400 px): two cards,
      each 6 units wide: a stacked_area trend from {mrr_trend}; a funnel_steps funnel from {signup_activation_funnel}. Row
      3 (height 400 px): two cards, each 6 units wide: a bar chart from {feature_adoption_by_plan}; a full line trend from
      {stickiness_ratios_dau_wau_mau}. Row 4 (height 440 px): two cards, each 6 units wide: a cohort table from {user_retention_weekly};
      a sankey-style path chart from {first_session_paths_after_signup}. Annotation: review the Row 1 KPIs alongside the stickiness
      ratio; high weekly actives and MRR with falling stickiness is a leading indicator of churn. All cards follow the board
      date range, and users may override the range per card.'
---

# SaaS growth command center

Slash command: /saas-growth-command-center

## Step 1: Build the growth board

Create a Dash board (12-column composition canvas) titled "SaaS Growth Command Center".
Persona: SaaS founder or GM. Question answered: "Are we growing, and is the growth healthy?"
Board-level configuration:
- defaultDateRange: last_30_days
- exclusionPeriod: incomplete_periods
- visibility: project
- boardFilters: none by default (allow user to add plan_tier filter at runtime)
- boardBreakdowns: none
Layout: 4 rows × variable cards per row. All cards isLinked: true (live-mirror the source recipe). Widths sum to 12 per row.
Row 1: Headline KPIs (heightPx: 200, four metric cards at widthUnits: 3 each):
- Card 1: Insights metric card to source recipe: weekly-active-users-trend, displayMode: chart, vizType: metric, titleOverride: "Weekly Active Users"
- Card 2: Insights metric card to source recipe: mrr-trend, displayMode: chart, vizType: metric, titleOverride: "MRR"
- Card 3: Insights metric card to source recipe: trial-to-paid-conversion-rate, displayMode: chart, vizType: metric, titleOverride: "Trial to Paid"
- Card 4: Insights metric card to source recipe: stickiness-ratios-dau-wau-mau, displayMode: chart, vizType: metric, titleOverride: "Stickiness (DAU/MAU)"
Row 2: Growth trends (heightPx: 400, two cards at widthUnits: 6 each):
- Card 1: Insights trend to source recipe: mrr-trend, displayMode: chart, vizType: stacked_area
- Card 2: Funnel to source recipe: signup-activation-funnel, displayMode: chart, vizType: funnel_steps
Row 3: Activation depth (heightPx: 400, two cards at widthUnits: 6 each):
- Card 1: Insights to source recipe: feature-adoption-by-plan, displayMode: chart, vizType: bar
- Card 2: Insights to source recipe: stickiness-ratios-dau-wau-mau, displayMode: chart, vizType: line (full trend, not just metric)
Row 4: Retention and behavior (heightPx: 440, two cards at widthUnits: 6 each):
- Card 1: Retention to source recipe: user-retention-weekly, displayMode: table (cohort grid)
- Card 2: Path to source recipe: first-session-paths-after-signup, displayMode: chart, vizType: sankey-style path
Annotations:
- The four KPIs in Row 1 should be reviewed alongside the stickiness ratio (Row 1 Card 4): high WAU/MRR with falling stickiness is a leading indicator of churn.
- All cards respect the board-level date range; users can override per-card if needed.
Taxonomy notes:
- All 7 source recipes are taxonomy-grounded against Intempt V2.1.
- Cards reference recipe slugs by id; when isLinked: true the card is a live mirror of the source recipe's configuration.
- KPI cards use the metric vizType applied to the source chart-recipe: Lovable renders the recipe's headline metric as a single number.
