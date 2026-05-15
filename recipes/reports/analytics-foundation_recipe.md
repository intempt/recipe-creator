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
  shortDescription: "Map events, build core reports (Insights, Funnels, Retention, Paths), compose executive dashboard."
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
      title: "Build Core Reports"
      command: create_report
      produces: report
      bindsAs: report
      description: "Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis), Paths (user flows)."
      prompt: "Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis), Paths (user flows)."
    - step: 2
      title: "Compose Exec Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [report]
      description: "Compose an executive dashboard surfacing headline metrics with comparisons and trends."
      prompt: "Compose an executive dashboard surfacing headline metrics with comparisons and trends."
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Analytics Foundation

## Procedure

1. **Build Core Reports** [`create_report`] — Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort analysis), Paths (user flows). → produces: report
2. **Compose Exec Dashboard** [`create_dashboard`] — Compose an executive dashboard surfacing headline metrics with comparisons and trends. → produces: dashboard
