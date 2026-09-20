---
name: win-loss-analysis
description: |
  Use when a user mentions "win/loss analysis", or asks for related help. Patterns across won vs lost deals: competitive intelligence, objection themes, battlecard.
arguments: []
intempt:
  id: win-loss-analysis
  version: 1.0.1
  slashCommand: /win-loss-analysis
  group: Dashboards
  title: "Win/loss patterns from closed deals"
  shortDescription: "Reads your closed deals to show which competitors, objections and decision criteria separate the ones you win from the ones you lose."
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
      title: "Compare won and lost deals"
      command: create_report
      produces: report
      bindsAs: report
      description: "Closed-won and closed-lost deals read side by side for competitor mentions, objection themes and the decision criteria buyers stated."
      prompt: "Analyze closed deals (won and lost) to extract patterns: competitive mentions, objection themes, decision criteria."
    - step: 2
      title: "Write the battlecard"
      command: create_page_content
      produces: asset
      bindsAs: asset
      dependsOn: [report]
      description: "A one-page battlecard with competitive positioning, the objections that come up most, and the responses that work."
      prompt: "Generate a battlecard content asset summarizing competitive positioning, common objections, and counter-messaging."
    - step: 3
      title: "Track the patterns over time"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [report, asset]
      description: "Win and loss rates split by competitor, objection type and deal size."
      prompt: "Compose a dashboard surfacing win/loss patterns by competitor, objection type, and deal size."
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Win/loss patterns from closed deals

Reads your closed deals to show which competitors, objections and decision criteria separate the ones you win from the ones you lose.

## What it does

1. **Compare won and lost deals** (`create_report`)

   Closed-won and closed-lost deals read side by side for competitor mentions, objection themes and the decision criteria buyers stated.

2. **Write the battlecard** (`create_page_content`)

   A one-page battlecard with competitive positioning, the objections that come up most, and the responses that work.

3. **Track the patterns over time** (`create_dashboard`)

   Win and loss rates split by competitor, objection type and deal size.

## What you end up with

- **report** (report): Report produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
