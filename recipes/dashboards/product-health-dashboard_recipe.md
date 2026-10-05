---
name: product-health-dashboard
description: |
  Use when a user mentions "product health dashboard", asks for a product manager dashboard, or asks for related help. PM view: stickiness, feature adoption depth, retention by feature, NPS, and the active vs. passive user split.
arguments: []
intempt:
  id: product-health-dashboard
  version: 1.0.0
  slashCommand: /product-health-dashboard
  group: Dashboards
  shortDescription: "Produce a Product Health dashboard with stickiness, feature adoption depth, retention by feature, NPS, and active vs passive user split."
  availability: coming-soon
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
        Create a Dash board (12-column composition canvas) titled "Product Health".

        Persona: Product Manager / Product Lead. Question answered: "Is the product getting more or less engaging? Which features matter? How do users feel about it?"

        Board-level configuration:
        - defaultDateRange: last_30_days
        - exclusionPeriod: incomplete_periods
        - visibility: project
        - boardFilters: none by default
        - boardBreakdowns: plan_name (resolved from each user's most-recent active subscription) — pushed down to all cards as a secondary breakdown

        Layout: 4 rows.

        Row 1 — Engagement headline (heightPx: 200, four metric cards at widthUnits: 3):
        - Card 1: Insights metric → source recipe: stickiness-ratios-dau-wau-mau, vizType: metric, titleOverride: "DAU/MAU Stickiness"
        - Card 2: Insights metric → source recipe: weekly-active-users-trend, vizType: metric, titleOverride: "WAU"
        - Card 3: Insights metric → source recipe: active-vs-passive-users, vizType: metric, titleOverride: "Producer Share %"
        - Card 4: Insights metric → source recipe: nps-tracking, vizType: metric, titleOverride: "NPS Score"

        Row 2 — Feature engagement depth (heightPx: 440, two cards at widthUnits: 6):
        - Card 1: Insights → source recipe: feature-adoption-by-plan, displayMode: chart, vizType: bar
        - Card 2: Funnel → source recipe: feature-discovery-adoption, displayMode: chart, vizType: funnel_steps

        Row 3 — Retention drivers (heightPx: 400, two cards at widthUnits: 6):
        - Card 1: Retention → source recipe: retention-lifted-by-feature-adoption, displayMode: chart (the side-by-side curve comparison)
        - Card 2: Insights → source recipe: feature-usage-heatmap-by-cohort, displayMode: chart, vizType: heatmap

        Row 4 — Engagement segmentation and support pulse (heightPx: 400, two cards at widthUnits: 6):
        - Card 1: Insights → source recipe: active-vs-passive-users, displayMode: chart, vizType: stacked_area
        - Card 2: Insights → source recipe: support-tickets-vs-churn-correlation, displayMode: chart, vizType: line (dual-axis)

        Annotations:
        - Row 1's four KPIs together answer: are users active (WAU), are they sticky (DAU/MAU), are they actively producing (Producer Share %), and how do they feel (NPS). Each is a different lens; reading them together is the key.
        - The board's value comes from reading the four rows together: Row 1 reports headline state, Row 2 reports feature engagement depth, Row 3 reports retention drivers, Row 4 reports segmentation and support pulse.

        Taxonomy notes:
        - All 8 source recipes are taxonomy-grounded.
        - nps-tracking depends on feedback_submitted events with survey_type = "nps" — see that recipe's notes.
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---

# Product Health Dashboard

## Procedure

1. **Build Dashboard** [`create_dashboard`] — Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below. → produces: dashboard

   ```text
   Create a Dash board (12-column composition canvas) titled "Product Health".

   Persona: Product Manager / Product Lead. Question answered: "Is the product getting more or less engaging? Which features matter? How do users feel about it?"

   Board-level configuration:
   - defaultDateRange: last_30_days
   - exclusionPeriod: incomplete_periods
   - visibility: project
   - boardFilters: none by default
   - boardBreakdowns: plan_name (resolved from each user's most-recent active subscription) — pushed down to all cards as a secondary breakdown

   Layout: 4 rows.

   Row 1 — Engagement headline (heightPx: 200, four metric cards at widthUnits: 3):
   - Card 1: Insights metric → source recipe: stickiness-ratios-dau-wau-mau, vizType: metric, titleOverride: "DAU/MAU Stickiness"
   - Card 2: Insights metric → source recipe: weekly-active-users-trend, vizType: metric, titleOverride: "WAU"
   - Card 3: Insights metric → source recipe: active-vs-passive-users, vizType: metric, titleOverride: "Producer Share %"
   - Card 4: Insights metric → source recipe: nps-tracking, vizType: metric, titleOverride: "NPS Score"

   Row 2 — Feature engagement depth (heightPx: 440, two cards at widthUnits: 6):
   - Card 1: Insights → source recipe: feature-adoption-by-plan, displayMode: chart, vizType: bar
   - Card 2: Funnel → source recipe: feature-discovery-adoption, displayMode: chart, vizType: funnel_steps

   Row 3 — Retention drivers (heightPx: 400, two cards at widthUnits: 6):
   - Card 1: Retention → source recipe: retention-lifted-by-feature-adoption, displayMode: chart (the side-by-side curve comparison)
   - Card 2: Insights → source recipe: feature-usage-heatmap-by-cohort, displayMode: chart, vizType: heatmap

   Row 4 — Engagement segmentation and support pulse (heightPx: 400, two cards at widthUnits: 6):
   - Card 1: Insights → source recipe: active-vs-passive-users, displayMode: chart, vizType: stacked_area
   - Card 2: Insights → source recipe: support-tickets-vs-churn-correlation, displayMode: chart, vizType: line (dual-axis)

   Annotations:
   - Row 1's four KPIs together answer: are users active (WAU), are they sticky (DAU/MAU), are they actively producing (Producer Share %), and how do they feel (NPS). Each is a different lens; reading them together is the key.
   - The board's value comes from reading the four rows together: Row 1 reports headline state, Row 2 reports feature engagement depth, Row 3 reports retention drivers, Row 4 reports segmentation and support pulse.

   Taxonomy notes:
   - All 8 source recipes are taxonomy-grounded.
   - nps-tracking depends on feedback_submitted events with survey_type = "nps" — see that recipe's notes.
   ```
