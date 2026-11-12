---
frontmatter_id: business-review
slash_command: /business-review
description: Builds the weekly scorecard, writes the narrative on what moved and why, and posts both to Slack on the cadence you pick.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds a weekly business scorecard with headline KPIs, week-over-week changes, wins and concerns, writes a narrative
    on what moved and why, and posts both to Slack on a chosen cadence.
  parameters:
  - name: cadence
    type: enum
    label: Delivery cadence
    default: weekly
    required: false
    options:
    - daily
    - weekly
    - monthly
  - name: slack_channel
    type: string
    label: Slack channel to post the digest to
    required: true
  requirements:
  - slot: slack_workspace
    kind: integration
    meaning: A connected Slack workspace that can receive scheduled digest posts
    channel: slack
  - slot: business_kpis
    kind: event
    meaning: Business performance data (headline KPIs) tracked for the company
    properties:
    - name: metric_name
      type: string
      meaning: Name of the KPI being measured
      optional: false
    - name: metric_value
      type: number
      meaning: Value of the KPI for the period
      optional: false
    - name: period_date
      type: date
      meaning: Date the KPI value applies to
      optional: false
  steps:
  - id: s1
    builds: dashboard
    uses:
    - business_kpis
    instruction: Compose a business review dashboard showing headline KPIs from {business_kpis}, week-over-week deltas, top
      wins, and top concerns. Use {business_kpis.metric_name}, {business_kpis.metric_value}, and {business_kpis.period_date}
      as the data fields.
  - id: s2
    builds: report
    uses:
    - s1
    instruction: 'Generate a narrative report summarizing the period: what changed, why, and recommended actions. Base it
      on the dashboard from "Build the headline scorecard".'
  - id: s3
    builds: automation
    uses:
    - slack_workspace
    - s1
    - s2
    - cadence
    - slack_channel
    instruction: Create a workflow that delivers the dashboard from "Build the headline scorecard" and the narrative from
      "Write the period narrative" as a scheduled digest posted to {slack_channel} in {slack_workspace} at the {cadence} cadence.
---

# Weekly business review pack

Slash command: /business-review

## Step 1: Build the headline scorecard

Compose a business review dashboard with headline KPIs, WoW deltas, top wins, and top concerns.

## Step 2: Write the period narrative

Generate a narrative report summarizing the period: what changed, why, and recommended actions. Use the result of "Build the headline scorecard".

## Step 3: Send it to Slack on a cadence

Create a workflow that delivers the dashboard and narrative as a scheduled Slack digest at the chosen cadence. Use the result of "Build the headline scorecard", "Write the period narrative".
