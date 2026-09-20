---
name: path-explorer-dashboard
description: |
  Use when a user mentions "path explorer dashboard", asks for a ux researcher / pm dashboard, or asks for related help. UX / PM research view: the full set of behavioral path analyses on one canvas: first-session, feature paths, support deflection, pre-churn.
arguments: []
intempt:
  id: path-explorer-dashboard
  version: 1.0.0
  slashCommand: /path-explorer-dashboard
  group: Dashboards
  title: "What users actually do"
  shortDescription: "Answers where real user journeys diverge from the one you designed, across the first session, feature use, support and the weeks before churn."
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
      title: "Build the path explorer board"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      description: "Four path analyses on one canvas: first-session onboarding, feature interaction, support and friction, and the paths that precede churn."
      prompt: |
        Create a Dash board (12-column composition canvas) titled "Path Explorer".

        Persona: UX Researcher, PM Researcher, or PMM. Question answered: "What do users actually do? Where do their journeys diverge from what we designed?"

        This dashboard composes the path-engine recipes into one canvas: the dedicated artifact for behavioral exploration.

        Board-level configuration:
        - defaultDateRange: last_30_days
        - exclusionPeriod: incomplete_periods
        - visibility: project
        - boardFilters: none by default
        - boardBreakdowns: utm_source (pushed down where applicable)

        Layout: 4 rows. Each row pairs path views appropriately. Path visualizations need width: most cards are widthUnits: 12 (full-width).

        Row 1: Onboarding paths (heightPx: 480, full-width single card at widthUnits: 12):
        - Card 1: Path to source recipe: first-session-paths-after-signup, displayMode: chart (forward path from user_created)

        Row 2: Feature interaction (heightPx: 480, full-width single card at widthUnits: 12):
        - Card 1: Path to source recipe: paths-around-power-feature, displayMode: chart (bidirectional)

        Row 3: Support and friction (heightPx: 480, full-width single card at widthUnits: 12):
        - Card 1: Path to source recipe: support-deflection-paths, displayMode: chart (backward path from ticket_created)

        Row 4: Churn and retention paths (heightPx: 480, two cards at widthUnits: 6):
        - Card 1: Path to source recipe: pre-churn-behavioral-signals, displayMode: chart
        - Card 2: Path to source recipe: exit-paths-pre-cancellation, displayMode: chart

        Annotations:
        - Path analysis is the technique most product teams underuse. This dashboard surfaces 5 high-value path analyses on one canvas: read top to bottom, it tracks the user journey from acquisition through engagement, friction, and attrition.
        - Row 4 pairs the 30-day "what predicts churn" view with the in-session "what saves vs. kills retention" view.
        - Path reports are computationally heavier than other reports: be mindful of date ranges.

        Taxonomy notes:
        - All 5 source path recipes use canonical events: user_created, click_on, page_viewed, session_start, ticket_created, subscription_cancelled.
  outputs:
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dash board (composition canvas) produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# What users actually do

Answers where real user journeys diverge from the one you designed, across the first session, feature use, support and the weeks before churn.

## What it does

1. **Build the path explorer board** (`create_dashboard`)

   Four path analyses on one canvas: first-session onboarding, feature interaction, support and friction, and the paths that precede churn.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.
