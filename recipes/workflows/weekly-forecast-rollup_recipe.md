---
name: weekly-forecast-rollup
description: Use when a user mentions "weekly forecast rollup", "pipeline snapshot weekly", "forecast vs actual report", or asks for related help. Every Monday morning, snapshot the pipeline (deals by stage, weighted forecast, committed pipeline, forecast-vs-actual variance for trailing periods), deliver to sales leadership via email + Slack, and freeze the snapshot for historical comparison.
arguments: []
intempt:
  id: weekly-forecast-rollup
  title: "Weekly forecast rollup"
  version: 1.0.0
  slashCommand: /weekly-forecast-rollup
  group: Workflows
  shortDescription: "Freezes the pipeline every Monday, sends leadership the weighted forecast and what moved, and keeps the snapshot so last week can be checked."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [forecast, pipeline-snapshot, scheduled-rollup]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
  invokesCommands:
    - build_insights_report
    - create_email_content
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Snapshot the pipeline"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Open pipeline by stage, the weighted forecast using each stage's historical win rate, the split across commit, best case, pipeline and omitted, what moved week over week in deals added, advanced, lost and won, and how last week's forecast compared with what actually closed. Each Monday's version is kept."
      prompt: 'Build an insights report ''Weekly pipeline forecast snapshot'' computing: (a) total open pipeline ARR by stage; (b) weighted forecast (each stage × its historical win-probability); (c) commit-category breakdown (Commit / Best Case / Pipeline / Omitted: sourced from the deal-level forecast category attribute); (d) week-over-week pipeline movement (deals added / advanced / lost / closed-won); (e) forecast-vs-actual for closed quarters (was last week''s forecast accurate?). Freezable: each Monday''s report is preserved for historical comparison.'
    - step: 2
      title: "Write the leadership email"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - report
      description: "A line each on the weighted forecast against quota, the week over week change and the biggest deal moves, then the full report as a scannable table. Concise, and from the CRO or VP Sales rather than a no reply address."
      prompt: 'Generate a weekly forecast snapshot email for sales leadership. Structure: executive summary at top (one sentence per: weighted forecast vs. quota, week-over-week pipeline change, top deal moves this week), then the full report rendered as a scannable HTML table. Tone: concise, exec-ready. Send-from: the CRO or VP Sales address (not from a no-reply system).'
    - step: 3
      title: "Send it Monday at 7am"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - report
      - asset
      description: "Weekly: it refreshes the snapshot, freezes it so last week's forecast stays queryable, writes the email with the current numbers, sends it to the leadership list, posts a condensed version with the headline numbers and a link to the revenue channel, and sends each AE their own pipeline movement separately, so the leadership email stays about the whole picture."
      prompt: 'Create a scheduled workflow firing every Monday at 7am local time. Step sequence: (1) refresh the forecast snapshot report; (2) freeze the snapshot to historical store (so ''last week''s forecast'' is queryable); (3) compose the weekly snapshot email with the latest data; (4) deliver to sales leadership list (CRO, VP Sales, AE managers); (5) post a condensed Slack version to #revenue with the top-line numbers + link to the full report; (6) for AEs specifically, send each AE a personalized snippet with their own pipeline movement (separate channel: don''t make exec emails AE-personal).'
    - step: 4
      title: "Check who forecasts honestly"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - report
      - asset
      - workflow
      description: "Reading the frozen snapshots: how far each week's forecast landed from what happened, where under 10% is excellent and over 20% means the process needs work, the variance per rep, and whether commit deals really close around 90% of the time and best case around half."
      prompt: 'Compose a forecast accuracy dashboard reading from the historical snapshot series: forecast-vs-actual variance by week (sub-10% = excellent, 10-20% = solid, 20%+ = forecast process needs work), variance by rep (which AEs forecast accurately vs. who''s optimistic / pessimistic), and forecast-category accuracy (do Commit-tier deals actually close at 90%+? Best-Case at 50%?: calibration health). Surfaces patterns leadership can coach on.'
  outputs:
    - { name: report, type: report, cardinality: single, description: "Insights Report produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Weekly forecast rollup

Freezes the pipeline every Monday, sends leadership the weighted forecast and what moved, and keeps the snapshot so last week can be checked.

## Before you run it

- Connect slack

## What it does

1. **Snapshot the pipeline** (`build_insights_report`)

   Open pipeline by stage, the weighted forecast using each stage's historical win rate, the split across commit, best case, pipeline and omitted, what moved week over week in deals added, advanced, lost and won, and how last week's forecast compared with what actually closed. Each Monday's version is kept.

2. **Write the leadership email** (`create_email_content`)

   A line each on the weighted forecast against quota, the week over week change and the biggest deal moves, then the full report as a scannable table. Concise, and from the CRO or VP Sales rather than a no reply address.

3. **Send it Monday at 7am** (`create_workflow`)

   Weekly: it refreshes the snapshot, freezes it so last week's forecast stays queryable, writes the email with the current numbers, sends it to the leadership list, posts a condensed version with the headline numbers and a link to the revenue channel, and sends each AE their own pipeline movement separately, so the leadership email stays about the whole picture.

4. **Check who forecasts honestly** (`create_dashboard`)

   Reading the frozen snapshots: how far each week's forecast landed from what happened, where under 10% is excellent and over 20% means the process needs work, the variance per rep, and whether commit deals really close around 90% of the time and best case around half.

## What you end up with

- **report** (report): Insights Report produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
