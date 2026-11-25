---
frontmatter_id: demo-request-fast-path
slash_command: /demo-request-fast-path
description: Emails a triage alert the moment a demo request lands, with the requester's account and fit score, and a weekly
  digest of response time against a one-hour target.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds the recent demo requesters segment, emails an instant triage alert for each high-fit demo request, and emails
    a weekly response-time digest.
  parameters:
  - name: window
    type: duration
    label: Lookback window for recent demo requests
    default: 7 d
    required: false
  - name: icp_threshold
    type: number
    label: Fit score for a high-priority alert (0-100)
    default: 70
    required: false
  - name: sla_target
    type: duration
    label: First-contact target
    default: 60 min
    required: false
  - name: stale_threshold
    type: duration
    label: Flag demo requests with no completed follow-up after
    default: 2 h
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses that get the demo-request alerts
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: demo_form_submitted
    kind: event
    meaning: A customer submitted a demo request form
    properties:
    - name: form_type
      type: string
      meaning: Type of form submitted, equal to demo_request for demo requests
      optional: false
  - slot: task_completed
    kind: event
    meaning: A follow-up task for a contact was marked completed
  - slot: meeting_scheduled
    kind: event
    meaning: A sales meeting was scheduled with a prospect
  - slot: icp_fit_score
    kind: attribute
    meaning: ICP fit score (0-100) stored on the user record
  - slot: ae_owner_routing
    kind: attribute
    meaning: Account executive who owns the user's account
  - slot: company_name
    kind: attribute
    meaning: The requester's company name
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - demo_form_submitted
    - window
    instruction: Build a new segment of users named "Recent demo requesters". A user is in it when they did {demo_form_submitted}
      with {demo_form_submitted.form_type} equal to demo_request in the last {window}.
  - id: s2
    builds: automation
    uses:
    - demo_form_submitted
    - icp_fit_score
    - icp_threshold
    - ae_owner_routing
    - company_name
    - sla_target
    - alert_recipients
    instruction: Build an automation triggered when a user does {demo_form_submitted} with {demo_form_submitted.form_type}
      equal to demo_request. It continues only when the user's {icp_fit_score} is {icp_threshold} or more. It writes the user's
      name and email, {company_name}, {icp_fit_score}, the owner in {ae_owner_routing}, and the time of the request, and emails
      these lines as an alert to {alert_recipients}, asking for first contact within {sla_target}. It never emails the requester.
  - id: s3
    builds: automation
    uses:
    - s1
    - demo_form_submitted
    - task_completed
    - meeting_scheduled
    - icp_fit_score
    - icp_threshold
    - ae_owner_routing
    - sla_target
    - stale_threshold
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users in the
      segment from "Find recent demo requests" and writes these figures for the last 7 days: the number of demo requests;
      the share that did {task_completed} and the share that did {meeting_scheduled} after the request; the median and 75th-percentile
      time from {demo_form_submitted} to the first {task_completed}, against the {sla_target} target; the requests with no
      {task_completed} within {stale_threshold}, each by user; these split by {icp_fit_score} at or above {icp_threshold}
      versus below, and by {ae_owner_routing}. Then it emails these figures as plain-text lines, each with its window, to
      {digest_recipients}. Nothing else is sent.'
---

# Demo request fast path

Slash command: /demo-request-fast-path

## Step 1: Find recent demo requests

Build a new segment of users named "Recent demo requesters". A user is in it when they did demo form submitted with form type equal to demo_request in the last 7 d.

## Step 2: Alert the team inside the hour

Build an automation triggered when a user does demo form submitted with form type equal to demo_request. It continues only when the user's icp fit score is 70 or more. It writes the user's name and email, company name, icp fit score, the owner in ae owner routing, and the time of the request, and emails these lines as an alert to the email addresses that get the demo-request alerts, asking for first contact within 60 min. It never emails the requester.

## Step 3: Email the weekly response-time digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users in the segment from "Find recent demo requests" and writes these figures for the last 7 days: the number of demo requests; the share that did task completed and the share that did meeting scheduled after the request; the median and 75th-percentile time from demo form submitted to the first task completed, against the 60 min target; the requests with no task completed within 2 h, each by user; these split by icp fit score at or above 70 versus below, and by ae owner routing. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
