---
frontmatter_id: weekly-forecast-rollup
slash_command: /weekly-forecast-rollup
description: Every week analyzes the pipeline and emails leadership the weighted forecast against quota and what moved, plus
  a monthly check of forecast against actual by rep.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails leadership a weekly weighted pipeline forecast against quota with deal movement, and a monthly forecast-accuracy
    check by rep and forecast category.
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
  - name: quota_target
    type: number
    label: Team quota for the quarter
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses of sales leadership that get the digest
    required: true
  requirements:
  - slot: pipeline_opportunity_event
    kind: event
    meaning: A deal in the sales pipeline was created, advanced, lost, or closed-won
    properties:
    - name: stage
      type: string
      meaning: Deal stage after the change, including Closed Won and Closed Lost
      optional: false
    - name: amount_arr
      type: number
      meaning: Annual value of the deal
      optional: false
    - name: forecast_category
      type: string
      meaning: Commit, Best Case, Pipeline or Omitted
      optional: false
    - name: owner
      type: string
      meaning: Account executive who owns the deal
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - pipeline_opportunity_event
    - send_day
    - send_time
    - quota_target
    - digest_recipients
    instruction: 'Build an automation that runs every {send_day} at {send_time} on a schedule. Each run it analyzes the latest
      {pipeline_opportunity_event} per deal and writes these figures: open pipeline {pipeline_opportunity_event.amount_arr}
      by {pipeline_opportunity_event.stage}; the weighted forecast, each stage''s value times its win rate over the last 12
      months; that forecast against {quota_target}; value by {pipeline_opportunity_event.forecast_category}; deals added,
      advanced, lost and closed-won in the last 7 days with their value; the five largest moves by deal and {pipeline_opportunity_event.owner};
      last week''s weighted forecast for comparison. Then it emails these figures as plain-text lines, each with its window,
      to {digest_recipients}. Nothing else is sent.'
  - id: s2
    builds: automation
    uses:
    - pipeline_opportunity_event
    - forecast_window
    - variance_excellent_pct
    - variance_solid_pct
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes {pipeline_opportunity_event}
      over the last {forecast_window} and writes these figures: the value forecast as Commit and Best Case by {pipeline_opportunity_event.forecast_category}
      at the start of the window against the value that reached Closed Won, as a variance in percent, rated excellent below
      {variance_excellent_pct}%, solid below {variance_solid_pct}%, else needs work; the same variance by {pipeline_opportunity_event.owner},
      marking each as optimistic or pessimistic; the close rate of Commit deals against 90% and of Best Case deals against
      50%. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is
      sent.'
---

# Weekly forecast rollup

Slash command: /weekly-forecast-rollup

## Step 1: Email the weekly forecast

Build an automation that runs every monday at 07:00 on a schedule. Each run it analyzes the latest pipeline opportunity event per deal and writes these figures: open pipeline amount arr by stage; the weighted forecast, each stage's value times its win rate over the last 12 months; that forecast against the team quota for the quarter; value by forecast category; deals added, advanced, lost and closed-won in the last 7 days with their value; the five largest moves by deal and owner; last week's weighted forecast for comparison. Then it emails these figures as plain-text lines, each with its window, to the email addresses of sales leadership that get the digest. Nothing else is sent.

## Step 2: Email the monthly forecast accuracy check

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes pipeline opportunity event over the last 4 w and writes these figures: the value forecast as Commit and Best Case by forecast category at the start of the window against the value that reached Closed Won, as a variance in percent, rated excellent below 10%, solid below 20%, else needs work; the same variance by owner, marking each as optimistic or pessimistic; the close rate of Commit deals against 90% and of Best Case deals against 50%. Then it emails these figures as plain-text lines, each with its window, to the email addresses of sales leadership that get the digest. Nothing else is sent.
