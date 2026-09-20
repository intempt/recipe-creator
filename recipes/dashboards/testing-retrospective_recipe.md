---
name: testing-retrospective
description: |
  Use when a user mentions "testing retrospective", or asks for related help. Quarterly experiment review and roadmap for next testing cycle.
arguments: []
intempt:
  id: testing-retrospective
  version: 1.0.1
  slashCommand: /testing-retrospective
  group: Dashboards
  title: "Quarterly experiment retrospective"
  shortDescription: "Pulls every experiment you ran last quarter into one review: what won, what lost, what the results have in common, and what to test next."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: experience-optimizer
    mode: [all]
    complexity: standard
    executionMode: live
    tags: [testing-retrospective]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_report
    - build_insights_report
    - create_dashboard
  procedure:
    - step: 1
      title: "Compile the quarter's results"
      command: create_report
      produces: report
      bindsAs: report
      description: "Every experiment run in the period sorted into winners, losers and inconclusive."
      prompt: "Compile results across all experiments run in the period: winners, losers, inconclusive."
    - step: 2
      title: "Find the patterns that repeat"
      command: build_insights_report
      produces: report
      bindsAs: report_2
      dependsOn: [report]
      description: "Which kinds of hypothesis won, which traffic sources behaved differently, and which surfaces performed best."
      prompt: "Generate insights report extracting patterns: which hypothesis families won, which traffic sources differed, best surfaces."
    - step: 3
      title: "Track cadence and impact"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [report, report_2]
      description: "How many tests you ran, what share of them won, and the revenue those wins produced."
      prompt: "Compose a dashboard summarizing testing cadence, win rate, and revenue impact."
  outputs:
    - { name: report, type: report, cardinality: multi, description: "Reports produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Quarterly experiment retrospective

Pulls every experiment you ran last quarter into one review: what won, what lost, what the results have in common, and what to test next.

## What it does

1. **Compile the quarter's results** (`create_report`)

   Every experiment run in the period sorted into winners, losers and inconclusive.

2. **Find the patterns that repeat** (`build_insights_report`)

   Which kinds of hypothesis won, which traffic sources behaved differently, and which surfaces performed best.

3. **Track cadence and impact** (`create_dashboard`)

   How many tests you ran, what share of them won, and the revenue those wins produced.

## What you end up with

- **report** (report): Reports produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
