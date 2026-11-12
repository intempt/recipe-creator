---
frontmatter_id: weekly-forecast-rollup
slash_command: /weekly-forecast-rollup
description: Freezes the pipeline every Monday, sends leadership the weighted forecast and what moved, and keeps the snapshot so last week can be checked.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Freezes the pipeline each Monday and emails leadership the weighted forecast and weekly pipeline movement, while
    keeping snapshots to check last week's forecast.
  parameters:
  - name: send_time
    type: string
    label: Weekly send time (local time)
    default: 07:00
    required: false
  - name: send_day
    type: enum
    label: Day of week to run
    default: monday
    required: false
    options:
    - monday
    - tuesday
    - wednesday
    - thursday
    - friday
  - name: forecast_window
    type: duration
    label: Forecast-vs-actual lookback window
    default: 4 w
    required: false
  - name: variance_excellent_pct
    type: number
    label: Forecast variance threshold for excellent (%)
    default: 10
    required: false
  - name: variance_solid_pct
    type: number
    label: Forecast variance threshold for solid (%)
    default: 20
    required: false
  requirements:
  - slot: pipeline_opportunity_event
    kind: event
    meaning: A deal in the sales pipeline was created, advanced, lost, or closed-won
    properties:
    - name: stage
      type: string
      meaning: Current pipeline stage of the deal
      optional: false
    - name: amount_arr
      type: number
      meaning: Annual recurring revenue value of the deal
      optional: false
    - name: forecast_category
      type: string
      meaning: Forecast category of the deal (Commit, Best Case, Pipeline, Omitted)
      optional: false
    - name: owner
      type: string
      meaning: Account executive who owns the deal
      optional: false
  - slot: sales_leadership_list
    kind: segment
    meaning: 'Sales leadership recipients: CRO, VP Sales, and AE managers'
  - slot: ae_list
    kind: segment
    meaning: Account executives who each receive a personal pipeline movement snippet
  - slot: quota_attribute
    kind: attribute
    meaning: Sales quota target for the team or period
  - slot: forecast_category_attribute
    kind: attribute
    meaning: Deal-level forecast category (Commit, Best Case, Pipeline, Omitted)
  - slot: revenue_slack_channel
    kind: integration
    meaning: 'Slack workspace connection with access to the #revenue channel'
    channel: slack
  - slot: leadership_email_sender
    kind: destination
    meaning: Email sending identity for the CRO or VP Sales address
    channel: email
  - slot: pipeline_snapshot_report
    kind: knowledge
    meaning: Historical store of weekly frozen pipeline forecast snapshots
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - pipeline_opportunity_event
    - forecast_category_attribute
    - quota_attribute
    instruction: 'Build an insights report named ''Weekly pipeline forecast snapshot'' that computes: (a) total open pipeline
      ARR by stage; (b) weighted forecast, where each stage''s ARR is multiplied by its historical win probability; (c) commit-category
      breakdown (Commit, Best Case, Pipeline, Omitted) using {forecast_category_attribute}; (d) week-over-week pipeline movement
      showing deals added, advanced, lost, and closed-won, based on {pipeline_opportunity_event}; (e) forecast-vs-actual for
      closed quarters, testing whether last week''s forecast was accurate. Set the report to be freezable so each Monday''s
      version is preserved for historical comparison. Compare weighted forecast against {quota_attribute}.'
  - id: s2
    builds: email
    uses:
    - s1
    - leadership_email_sender
    - quota_attribute
    instruction: 'Write a weekly forecast snapshot email for sales leadership. Open with an executive summary of three one-sentence
      items: weighted forecast versus {quota_attribute}, week-over-week pipeline change, and top deal moves this week. Follow
      with the full report from "Snapshot the pipeline" rendered as a scannable HTML table. Tone: concise and exec-ready.
      Send from the CRO or VP Sales address via {leadership_email_sender}, not a no-reply system. Use the result of "Snapshot
      the pipeline".'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - sales_leadership_list
    - revenue_slack_channel
    - ae_list
    - send_day
    - send_time
    instruction: 'Create a scheduled workflow that fires every {send_day} at {send_time} local time. Steps in order: (1) refresh
      the forecast snapshot report from "Snapshot the pipeline"; (2) freeze the snapshot to the historical store so last week''s
      forecast can be queried; (3) compose the weekly snapshot email from "Write the leadership email" with the latest data;
      (4) deliver that email to {sales_leadership_list}; (5) post a condensed Slack version to #revenue via {revenue_slack_channel}
      with the top-line numbers and a link to the full report; (6) send each member of {ae_list} a personalized snippet with
      their own pipeline movement, kept separate from the executive email. Use the results of "Snapshot the pipeline" and
      "Write the leadership email".'
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - forecast_category_attribute
    - forecast_window
    - variance_excellent_pct
    - variance_solid_pct
    instruction: 'Build a forecast accuracy dashboard reading from the historical snapshot series over {forecast_window}.
      Show: (a) forecast-vs-actual variance by week, rated excellent under {variance_excellent_pct}%, solid between {variance_excellent_pct}%
      and {variance_solid_pct}%, and needing process work at {variance_solid_pct}% or above; (b) variance by rep, identifying
      which AEs forecast accurately and which are optimistic or pessimistic; (c) forecast-category calibration, checking whether
      Commit-tier deals close at 90% or higher and Best Case deals close at about 50%, using {forecast_category_attribute}.
      Surface patterns leadership can coach on. Use the results of "Snapshot the pipeline", "Write the leadership email",
      and "Send it Monday at 7am".'
---

# Weekly forecast rollup

Slash command: /weekly-forecast-rollup

## Step 1: Snapshot the pipeline

Build an insights report 'Weekly pipeline forecast snapshot' computing: (a) total open pipeline ARR by stage; (b) weighted forecast (each stage × its historical win-probability); (c) commit-category breakdown (Commit / Best Case / Pipeline / Omitted: sourced from deal-level forecast_category attribute); (d) week-over-week pipeline movement (deals added / advanced / lost / closed-won); (e) forecast-vs-actual for closed quarters (was last week's forecast accurate?). Freezable: each Monday's report is preserved for historical comparison.

## Step 2: Write the leadership email

Generate a weekly forecast snapshot email for sales leadership. Structure: executive summary at top (one sentence per: weighted forecast vs. quota, week-over-week pipeline change, top deal moves this week), then the full report rendered as a scannable HTML table. Tone: concise, exec-ready. Send-from: the CRO or VP Sales address (not from a no-reply system). Use the result of "Snapshot the pipeline".

## Step 3: Send it Monday at 7am

Create a scheduled workflow firing every Monday at 7am local time. Step sequence: (1) refresh the forecast snapshot report; (2) freeze the snapshot to historical store (so 'last week's forecast' is queryable); (3) compose the weekly snapshot email with the latest data; (4) deliver to sales leadership list (CRO, VP Sales, AE managers); (5) post a condensed Slack version to #revenue with the top-line numbers + link to the full report; (6) for AEs specifically, send each AE a personalized snippet with their own pipeline movement (separate channel: don't make exec emails AE-personal). Use the result of "Snapshot the pipeline", "Write the leadership email".

## Step 4: Check who forecasts honestly

Compose a forecast accuracy dashboard reading from the historical snapshot series: forecast-vs-actual variance by week (sub-10% = excellent, 10-20% = solid, 20%+ = forecast process needs work), variance by rep (which AEs forecast accurately vs. who's optimistic / pessimistic), and forecast-category accuracy (do Commit-tier deals actually close at 90%+? Best-Case at 50%?: calibration health). Surfaces patterns leadership can coach on. Use the result of "Snapshot the pipeline", "Write the leadership email", "Send it Monday at 7am".
