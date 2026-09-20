---
name: analytics-foundation
description: |
  Use when a user mentions "analytics foundation", or asks for related help. Map events, build core reports (Insights, Funnels, Retention, Paths), compose executive dashboard.
arguments: []
intempt:
  id: analytics-foundation
  version: 1.0.1
  slashCommand: /analytics-foundation
  group: Reports
  title: "Analytics foundation"
  shortDescription: "Sets up your core analytics in one pass: the key metric, conversion, cohort and user flow reports, then an executive dashboard that pulls the headline numbers together."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [all]
    complexity: standard
    executionMode: scheduled
    tags: [analytics-foundation]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: session_start, severity: blocking }  # Baseline engagement event
      - { value: page_viewed, severity: blocking }  # Funnel-step source event
      - { value: click_on, severity: recommended }  # Activity-volume baseline
  invokesCommands:
    - create_report
    - create_dashboard
  procedure:
    - step: 1
      title: "Build the core report set"
      command: create_report
      produces: report
      bindsAs: report
      description: "Creates the four reports every team starts with: key metrics, conversion funnels, cohort retention and user flows."
      prompt: "Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis), Paths (user flows)."
    - step: 2
      title: "Compose the exec dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [report]
      description: "Pulls the headline numbers onto one dashboard, each with a period comparison and a trend."
      prompt: "Compose an executive dashboard surfacing headline metrics with comparisons and trends."
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Analytics foundation

Sets up your core analytics in one pass: the key metric, conversion, cohort and user flow reports, then an executive dashboard that pulls the headline numbers together.

## Before you run it

- Send the `session_start` event
- Send the `page_viewed` event
- Send the `click_on` event

## What it does

1. **Build the core report set** (`create_report`)

   Creates the four reports every team starts with: key metrics, conversion funnels, cohort retention and user flows.

2. **Compose the exec dashboard** (`create_dashboard`)

   Pulls the headline numbers onto one dashboard, each with a period comparison and a trend.

## What you end up with

- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
