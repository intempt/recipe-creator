---
frontmatter_id: demo-request-fast-path
slash_command: /demo-request-fast-path
description: Enriches a demo request the moment it lands, puts a same day task on the right AE, and posts it to Slack, aiming for first contact inside an hour.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Enriches each demo request as it arrives, creates a same-day task for the right AE, posts a triage card to Slack,
    and tracks response time against a one-hour target.
  parameters:
  - name: window
    type: duration
    label: Lookback window for recent demo requests
    default: 7 d
    required: false
  - name: icp_threshold
    type: number
    label: ICP fit score for high-priority routing (0-100)
    default: 70
    required: false
  - name: sla_target
    type: duration
    label: First-contact SLA target
    default: 60 min
    required: false
  - name: stale_threshold
    type: duration
    label: Flag demo requests open without task completion after
    default: 2 h
    required: false
  requirements:
  - slot: demo_form_submitted
    kind: event
    meaning: A customer submitted a demo request form
    properties:
    - name: form_type
      type: string
      meaning: Type of form submitted, equal to demo_request for demo requests
      optional: false
  - slot: task_created
    kind: event
    meaning: A follow-up task was created for a contact
  - slot: task_completed
    kind: event
    meaning: A follow-up task was marked completed
  - slot: meeting_scheduled
    kind: event
    meaning: A sales meeting was scheduled with a prospect
  - slot: requester_profile
    kind: attribute
    meaning: Requester name, account name, employee count, industry, and deal-size estimate
  - slot: icp_fit_score
    kind: attribute
    meaning: ICP fit score (0-100) stored on the user record
  - slot: demo_requesters
    kind: segment
    meaning: Users who submitted a demo request in the last several days
    creatable: true
    definition: users who did {demo_form_submitted} with form_type = demo_request in the last {window}
  - slot: firmographic_enrichment
    kind: integration
    meaning: Firmographic lookup service that enriches account data
    channel: email
  - slot: ae_owner_routing
    kind: attribute
    meaning: Account executive owner assigned to each account
  - slot: sales_slack_channel
    kind: destination
    meaning: Slack channel where demo-request alerts are posted
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - demo_form_submitted
    - window
    - demo_requesters
    instruction: Build the segment {demo_requesters} of users who did {demo_form_submitted} where {demo_form_submitted.form_type}
      = demo_request in the last {window}. Use it to identify requesters for the fast-path and exclude them from standard
      nurture journeys while the fast-path window is open.
  - id: s2
    builds: slack
    uses:
    - s1
    - requester_profile
    - icp_fit_score
    - sales_slack_channel
    instruction: Write a terse, scannable Slack triage card for {sales_slack_channel} using the result of "Find recent demo
      requests". Include requester name, account name, employee count, industry, deal-size estimate if available, last engagement,
      {icp_fit_score}, and a direct link to the user record. No marketing language.
  - id: s3
    builds: automation
    uses:
    - demo_form_submitted
    - firmographic_enrichment
    - icp_fit_score
    - icp_threshold
    - ae_owner_routing
    - sales_slack_channel
    - s1
    - s2
    instruction: 'Create a workflow triggered by {demo_form_submitted} where {demo_form_submitted.form_type} = demo_request.
      Steps: (1) enrich the account via {firmographic_enrichment} if not already enriched; (2) compute the ICP fit score and
      store it in {icp_fit_score}; (3) if {icp_fit_score} is at least {icp_threshold}, create a high-priority task for the
      owner in {ae_owner_routing} due the same day, with the contact details, account context and form responses attached;
      otherwise enroll the user in self serve nurture; (4) post the alert from "Write the triage card" to {sales_slack_channel}.
      Use the result of "Find recent demo requests" for the requester list.'
  - id: s4
    builds: dashboard
    uses:
    - demo_form_submitted
    - task_created
    - task_completed
    - meeting_scheduled
    - icp_fit_score
    - ae_owner_routing
    - sla_target
    - stale_threshold
    - s1
    - s2
    - s3
    instruction: 'Build a dashboard tracking the demo-request response funnel: {demo_form_submitted} to {task_created} to
      {task_completed} to {meeting_scheduled}. Show median and p75 time from {demo_form_submitted} to AE first touch, measured
      against {sla_target} during business hours. Break down by {icp_fit_score} tier (high, medium, low) and by {ae_owner_routing}.
      Add a card flagging any demo request open longer than {stale_threshold} without a {task_completed}. Use the results
      of "Find recent demo requests", "Write the triage card" and "Route it inside the hour".'
---

# Demo request fast path

Slash command: /demo-request-fast-path

## Step 1: Find recent demo requests

Build a segment 'Demo Requesters - last 7 days' capturing users with Form submitted event where form_type = demo_request in the last 7 days. Used by the routing workflow to identify which users should hit the fast-path and excluded from standard nurture journeys for the duration of the fast-path window.

## Step 2: Write the triage card

Generate Slack alert content for the #demo-requests channel. Include: requester name, account name, employee count, industry, deal-size estimate (if available), prior touch history (last engagement, ICP fit score), and a direct link to the user record. Tone: terse, scannable: this is a triage card, not a marketing message. Use the result of "Find recent demo requests".

## Step 3: Route it inside the hour

Create a workflow firing on Form submitted where form_type = demo_request. Step sequence: (1) enrich account via firmographic lookup if not already enriched; (2) compute ICP fit score and store as user attribute; (3) for high-fit ICPs (score >= 70), create a high-priority AE task due same-day with the prospect's contact info, account context, and form responses pre-attached; (4) post the alert content to Slack #demo-requests. For low-fit ICPs, drop into self-serve nurture journey instead. Use the result of "Find recent demo requests", "Write the triage card".

## Step 4: Hold the response time

Compose a dashboard tracking the demo-request response funnel: Form submitted to task_created to Task completed to Meeting scheduled. Surface median + p75 time from Form submitted to AE first-touch (SLA metric: target: under 60 minutes during business hours). Break down by ICP fit tier (high/med/low) and by AE owner. Add a card flagging any demo request open >2 hours without a task completion. Use the result of "Find recent demo requests", "Write the triage card", "Route it inside the hour".
