---
name: weekly-forecast-rollup
description: Use when a user mentions "weekly forecast rollup", "pipeline snapshot weekly", "forecast vs actual report", or asks for related help. Every Monday morning, snapshot the pipeline (deals by stage, weighted forecast, committed pipeline, forecast-vs-actual variance for trailing periods), deliver to sales leadership via email + Slack, and freeze the snapshot for historical comparison.
arguments: []
intempt:
  id: weekly-forecast-rollup
  version: 1.0.0
  slashCommand: /weekly-forecast-rollup
  group: Workflows
  shortDescription: "Every Monday morning, snapshot the pipeline (deals by stage, weighted forecast, committed pipeline, forecast-vs-actual variance for trailing periods), deliver to sales leadership via email + Slack, and freeze the snapshot for historical comparison."
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
  invokesCommands:
    - build_insights_report
    - create_email_content
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Build Forecast Snapshot Report
      command: build_insights_report
      produces: report
      bindsAs: report
      description: 'Build an insights report ''Weekly pipeline forecast snapshot'' computing: (a) total open pipeline ARR by stage; (b) weighted forecast (each stage × its historical win-probability); (c) commit-category breakdown (Commit / Best Case / Pipeline / Omitted — sourced from deal-level forecast_category attribute); (d) week-over-week pipeline movement (deals added / advanced / lost / closed-won); (e) forecast-vs-actual for closed quarters (was last week''s forecast accurate?). Freezable: each Monday''s report is preserved for historical comparison.'
      prompt: 'Build an insights report ''Weekly pipeline forecast snapshot'' computing: (a) total open pipeline ARR by stage; (b) weighted forecast (each stage × its historical win-probability); (c) commit-category breakdown (Commit / Best Case / Pipeline / Omitted — sourced from deal-level forecast_category attribute); (d) week-over-week pipeline movement (deals added / advanced / lost / closed-won); (e) forecast-vs-actual for closed quarters (was last week''s forecast accurate?). Freezable: each Monday''s report is preserved for historical comparison.'
    - step: 2
      title: Build Weekly Snapshot Email Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - report
      description: 'Generate a weekly forecast snapshot email for sales leadership. Structure: executive summary at top (one sentence per: weighted forecast vs. quota, week-over-week pipeline change, top deal moves this week), then the full report rendered as a scannable HTML table. Tone: concise, exec-ready. Send-from: the CRO or VP Sales address (not from a no-reply system).'
      prompt: 'Generate a weekly forecast snapshot email for sales leadership. Structure: executive summary at top (one sentence per: weighted forecast vs. quota, week-over-week pipeline change, top deal moves this week), then the full report rendered as a scannable HTML table. Tone: concise, exec-ready. Send-from: the CRO or VP Sales address (not from a no-reply system).'
    - step: 3
      title: Build Weekly Rollup Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - report
      - asset
      description: 'Create a scheduled workflow firing every Monday at 7am local time. Step sequence: (1) refresh the forecast snapshot report; (2) freeze the snapshot to historical store (so ''last week''s forecast'' is queryable); (3) compose the weekly snapshot email with the latest data; (4) deliver to sales leadership list (CRO, VP Sales, AE managers); (5) post a condensed Slack version to #revenue with the top-line numbers + link to the full report; (6) for AEs specifically, send each AE a personalized snippet with their own pipeline movement (separate channel — don''t make exec emails AE-personal).'
      prompt: 'Create a scheduled workflow firing every Monday at 7am local time. Step sequence: (1) refresh the forecast snapshot report; (2) freeze the snapshot to historical store (so ''last week''s forecast'' is queryable); (3) compose the weekly snapshot email with the latest data; (4) deliver to sales leadership list (CRO, VP Sales, AE managers); (5) post a condensed Slack version to #revenue with the top-line numbers + link to the full report; (6) for AEs specifically, send each AE a personalized snippet with their own pipeline movement (separate channel — don''t make exec emails AE-personal).'
    - step: 4
      title: Build Forecast Accuracy Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - report
      - asset
      - workflow
      description: 'Compose a forecast accuracy dashboard reading from the historical snapshot series: forecast-vs-actual variance by week (sub-10% = excellent, 10-20% = solid, 20%+ = forecast process needs work), variance by rep (which AEs forecast accurately vs. who''s optimistic / pessimistic), and forecast-category accuracy (do Commit-tier deals actually close at 90%+? Best-Case at 50%? — calibration health). Surfaces patterns leadership can coach on.'
      prompt: 'Compose a forecast accuracy dashboard reading from the historical snapshot series: forecast-vs-actual variance by week (sub-10% = excellent, 10-20% = solid, 20%+ = forecast process needs work), variance by rep (which AEs forecast accurately vs. who''s optimistic / pessimistic), and forecast-category accuracy (do Commit-tier deals actually close at 90%+? Best-Case at 50%? — calibration health). Surfaces patterns leadership can coach on.'
  outputs:
    - { name: report, type: report, cardinality: single, description: "Insights Report produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Weekly Forecast Rollup

## Procedure

1. **Build Forecast Snapshot Report** [`build_insights_report`] — Build an insights report 'Weekly pipeline forecast snapshot' computing: (a) total open pipeline ARR by stage; (b) weighted forecast (each stage × its historical win-probability); (c) commit-category breakdown (Commit / Best Case / Pipeline / Omitted — sourced from deal-level forecast_category attribute); (d) week-over-week pipeline movement (deals added / advanced / lost / closed-won); (e) forecast-vs-actual for closed quarters (was last week's forecast accurate?). Freezable: each Monday's report is preserved for historical comparison. → produces: report
2. **Build Weekly Snapshot Email Content** [`create_email_content`] — Generate a weekly forecast snapshot email for sales leadership. Structure: executive summary at top (one sentence per: weighted forecast vs. quota, week-over-week pipeline change, top deal moves this week), then the full report rendered as a scannable HTML table. Tone: concise, exec-ready. Send-from: the CRO or VP Sales address (not from a no-reply system). → produces: asset
3. **Build Weekly Rollup Workflow** [`create_workflow`] — Create a scheduled workflow firing every Monday at 7am local time. Step sequence: (1) refresh the forecast snapshot report; (2) freeze the snapshot to historical store (so 'last week's forecast' is queryable); (3) compose the weekly snapshot email with the latest data; (4) deliver to sales leadership list (CRO, VP Sales, AE managers); (5) post a condensed Slack version to #revenue with the top-line numbers + link to the full report; (6) for AEs specifically, send each AE a personalized snippet with their own pipeline movement (separate channel — don't make exec emails AE-personal). → produces: workflow
4. **Build Forecast Accuracy Dashboard** [`create_dashboard`] — Compose a forecast accuracy dashboard reading from the historical snapshot series: forecast-vs-actual variance by week (sub-10% = excellent, 10-20% = solid, 20%+ = forecast process needs work), variance by rep (which AEs forecast accurately vs. who's optimistic / pessimistic), and forecast-category accuracy (do Commit-tier deals actually close at 90%+? Best-Case at 50%? — calibration health). Surfaces patterns leadership can coach on. → produces: dashboard
