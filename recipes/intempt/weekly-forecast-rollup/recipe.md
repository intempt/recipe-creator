---
id: weekly-forecast-rollup
title: Weekly forecast rollup
slash_command: /weekly-forecast-rollup
group: Workflows
owner: intempt
summary: Freezes the pipeline every Monday, sends leadership the weighted forecast and what moved, and
  keeps the snapshot so last week can be checked.
description: >-
  Every Monday morning, snapshot the pipeline (deals by stage, weighted forecast, committed pipeline,
  forecast-vs-actual variance for trailing periods), deliver to sales leadership via email + Slack, and
  freeze the snapshot for historical comparison.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - forecast
    - pipeline-snapshot
    - scheduled-rollup
prerequisites:
  integrations:
    - value: slack
      severity: recommended
touches:
  reads:
    - Your Slack connection
  writes:
    - A new report, from step 1 "Snapshot the pipeline"
    - A new designed email, from step 2 "Write the leadership email"
    - A new workflow, from step 3 "Send it Monday at 7am"
    - A new dashboard, from step 4 "Check who forecasts honestly"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Snapshot the pipeline
    summary: >-
      Open pipeline by stage, the weighted forecast using each stage's historical win rate, the split
      across commit, best case, pipeline and omitted, what moved week over week in deals added, advanced,
      lost and won, and how last week's forecast compared with what actually closed. Each Monday's version
      is kept.
    builds: report
    description: >-
      Build an insights report 'Weekly pipeline forecast snapshot' computing: (a) total open pipeline
      ARR by stage; (b) weighted forecast (each stage × its historical win-probability); (c) commit-category
      breakdown (Commit / Best Case / Pipeline / Omitted: sourced from deal-level forecast_category attribute);
      (d) week-over-week pipeline movement (deals added / advanced / lost / closed-won); (e) forecast-vs-actual
      for closed quarters (was last week's forecast accurate?). Freezable: each Monday's report is preserved
      for historical comparison.
  - id: s2
    title: Write the leadership email
    summary: >-
      A line each on the weighted forecast against quota, the week over week change and the biggest deal
      moves, then the full report as a scannable table. Concise, and from the CRO or VP Sales rather than
      a no reply address.
    builds: email_html
    description: >-
      Generate a weekly forecast snapshot email for sales leadership. Structure: executive summary at
      top (one sentence per: weighted forecast vs. quota, week-over-week pipeline change, top deal moves
      this week), then the full report rendered as a scannable HTML table. Tone: concise, exec-ready.
      Send-from: the CRO or VP Sales address (not from a no-reply system). Use the result of "Snapshot
      the pipeline".
    dependsOn:
      - s1
  - id: s3
    title: Send it Monday at 7am
    summary: >-
      Weekly: it refreshes the snapshot, freezes it so last week's forecast stays queryable, writes the
      email with the current numbers, sends it to the leadership list, posts a condensed version with
      the headline numbers and a link to the revenue channel, and sends each AE their own pipeline movement
      separately, so the leadership email stays about the whole picture.
    builds: workflow
    description: >-
      Create a scheduled workflow firing every Monday at 7am local time. Step sequence: (1) refresh the
      forecast snapshot report; (2) freeze the snapshot to historical store (so 'last week's forecast'
      is queryable); (3) compose the weekly snapshot email with the latest data; (4) deliver to sales
      leadership list (CRO, VP Sales, AE managers); (5) post a condensed Slack version to #revenue with
      the top-line numbers + link to the full report; (6) for AEs specifically, send each AE a personalized
      snippet with their own pipeline movement (separate channel: don't make exec emails AE-personal).
      Use the result of "Snapshot the pipeline", "Write the leadership email".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Check who forecasts honestly
    summary: >-
      Reading the frozen snapshots: how far each week's forecast landed from what happened, where under
      10% is excellent and over 20% means the process needs work, the variance per rep, and whether commit
      deals really close around 90% of the time and best case around half.
    builds: dashboard
    description: >-
      Compose a forecast accuracy dashboard reading from the historical snapshot series: forecast-vs-actual
      variance by week (sub-10% = excellent, 10-20% = solid, 20%+ = forecast process needs work), variance
      by rep (which AEs forecast accurately vs. who's optimistic / pessimistic), and forecast-category
      accuracy (do Commit-tier deals actually close at 90%+? Best-Case at 50%?: calibration health). Surfaces
      patterns leadership can coach on. Use the result of "Snapshot the pipeline", "Write the leadership
      email", "Send it Monday at 7am".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Insights Report produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Weekly forecast rollup

Freezes the pipeline every Monday, sends leadership the weighted forecast and what moved, and keeps the snapshot so last week can be checked.

## Steps

1. **Snapshot the pipeline** (builds report)

   Open pipeline by stage, the weighted forecast using each stage's historical win rate, the split across commit, best case, pipeline and omitted, what moved week over week in deals added, advanced, lost and won, and how last week's forecast compared with what actually closed. Each Monday's version is kept.

2. **Write the leadership email** (builds email_html)

   A line each on the weighted forecast against quota, the week over week change and the biggest deal moves, then the full report as a scannable table. Concise, and from the CRO or VP Sales rather than a no reply address.

3. **Send it Monday at 7am** (builds workflow)

   Weekly: it refreshes the snapshot, freezes it so last week's forecast stays queryable, writes the email with the current numbers, sends it to the leadership list, posts a condensed version with the headline numbers and a link to the revenue channel, and sends each AE their own pipeline movement separately, so the leadership email stays about the whole picture.

4. **Check who forecasts honestly** (builds dashboard)

   Reading the frozen snapshots: how far each week's forecast landed from what happened, where under 10% is excellent and over 20% means the process needs work, the variance per rep, and whether commit deals really close around 90% of the time and best case around half.

## What you end up with

- **report** (report): Insights Report produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Your Slack connection

Writes:

- A new report, from step 1 "Snapshot the pipeline"
- A new designed email, from step 2 "Write the leadership email"
- A new workflow, from step 3 "Send it Monday at 7am"
- A new dashboard, from step 4 "Check who forecasts honestly"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, report, workflow.
