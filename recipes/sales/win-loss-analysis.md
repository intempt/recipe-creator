---
name: Win Loss Analysis
description: Patterns across won vs lost deals — competitive intelligence, objection themes, battlecard.
intempt:
  id: win-loss-analysis
  version: 1.0.1
  slashCommand: /win-loss-analysis
  shortDescription: Patterns across won vs lost deals — competitive intelligence, objection themes, battlecard.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    - analytics
    agent: meeting-notetaker
    mode:
    - b2b
    complexity: standard
    executionMode: oneshot
    tags:
    - win-loss-analysis
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: analyze-deal-patterns
    describe: 'Analyze closed deals (won and lost) to extract patterns: competitive mentions, objection themes, decision criteria.'
    produces: report
  - id: generate-battlecard
    describe: Generate a battlecard content asset summarizing competitive positioning, common objections, and counter-messaging.
    produces: content
  - id: build-insights-dashboard
    describe: Compose a dashboard surfacing win/loss patterns by competitor, objection type, and deal size.
    produces: dashboard
---

# Win Loss Analysis

Patterns across won vs lost deals — competitive intelligence, objection themes, battlecard.

## Outputs

- **report** (report): Report produced by this recipe.
- **content** (content): Content produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Analyze closed deals (won and lost) to extract patterns: competitive mentions, objection themes, decision criteria.
2. Generate a battlecard content asset summarizing competitive positioning, common objections, and counter-messaging.
3. Compose a dashboard surfacing win/loss patterns by competitor, objection type, and deal size.
