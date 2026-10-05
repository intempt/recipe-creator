---
name: win-loss-analysis
description: |
  Use when a user mentions "win/loss analysis", or asks for related help. Patterns across won vs lost deals — competitive intelligence, objection themes, battlecard.
arguments: []
intempt:
  id: win-loss-analysis
  version: 1.0.1
  slashCommand: /win-loss-analysis
  group: Dashboards
  shortDescription: "Generate a win/loss report, battlecard content asset, and dashboard analyzing won vs lost deals by competitor, objection theme, and deal size."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, analytics]
    agent: meeting-notetaker
    mode: [b2b]
    complexity: standard
    executionMode: oneshot
    tags: [win-loss-analysis]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_report
    - create_page_content
    - create_dashboard
  procedure:
    - step: 1
      title: "Analyze Deal Patterns"
      command: create_report
      produces: report
      bindsAs: report
      description: "Analyze closed deals (won and lost) to extract patterns: competitive mentions, objection themes, decision criteria."
      prompt: "Analyze closed deals (won and lost) to extract patterns: competitive mentions, objection themes, decision criteria."
    - step: 2
      title: "Generate Battlecard"
      command: create_page_content
      produces: asset
      bindsAs: asset
      dependsOn: [report]
      description: "Generate a battlecard content asset summarizing competitive positioning, common objections, and counter-messaging."
      prompt: "Generate a battlecard content asset summarizing competitive positioning, common objections, and counter-messaging."
    - step: 3
      title: "Build Insights Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [report, asset]
      description: "Compose a dashboard surfacing win/loss patterns by competitor, objection type, and deal size."
      prompt: "Compose a dashboard surfacing win/loss patterns by competitor, objection type, and deal size."
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Win/Loss Analysis

## Procedure

1. **Analyze Deal Patterns** [`create_report`] — Analyze closed deals (won and lost) to extract patterns: competitive mentions, objection themes, decision criteria. → produces: report
2. **Generate Battlecard** [`create_page_content`] — Generate a battlecard content asset summarizing competitive positioning, common objections, and counter-messaging. → produces: asset
3. **Build Insights Dashboard** [`create_dashboard`] — Compose a dashboard surfacing win/loss patterns by competitor, objection type, and deal size. → produces: dashboard
