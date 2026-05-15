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
  shortDescription: "Quarterly experiment review and roadmap for next testing cycle."
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
      title: "Compile Experiment Results"
      command: create_report
      produces: report
      bindsAs: report
      description: "Compile results across all experiments run in the period — winners, losers, inconclusive."
      prompt: "Compile results across all experiments run in the period — winners, losers, inconclusive."
    - step: 2
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report_2
      dependsOn: [report]
      description: "Generate insights report extracting patterns: which hypothesis families won, which traffic sources differed, best surfaces."
      prompt: "Generate insights report extracting patterns: which hypothesis families won, which traffic sources differed, best surfaces."
    - step: 3
      title: "Build Retrospective Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [report, report_2]
      description: "Compose a dashboard summarizing testing cadence, win rate, and revenue impact."
      prompt: "Compose a dashboard summarizing testing cadence, win rate, and revenue impact."
  outputs:
    - { name: report, type: report, cardinality: multi, description: "Reports produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Testing Retrospective

## Procedure

1. **Compile Experiment Results** [`create_report`] — Compile results across all experiments run in the period — winners, losers, inconclusive. → produces: report
2. **Build Insights Report** [`build_insights_report`] — Generate insights report extracting patterns: which hypothesis families won, which traffic sources differed, best surfaces. → produces: report
3. **Build Retrospective Dashboard** [`create_dashboard`] — Compose a dashboard summarizing testing cadence, win rate, and revenue impact. → produces: dashboard
