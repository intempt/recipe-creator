---
frontmatter_id: daily-sdr-task-queue
slash_command: /daily-sdr-task-queue
description: Ranks each SDR's open tasks by signal strength, recency and account fit every business day, and emails the team
  each SDR's top tasks with a suggested first-touch angle.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails the SDR team every business morning each SDR's top open tasks ranked by signal, recency and fit, with first-touch
    angles, plus a weekly ranking check.
  parameters:
  - name: queue_size
    type: number
    label: Tasks per SDR queue
    default: 25
    required: false
  - name: delivery_time
    type: string
    label: Delivery time (local)
    default: 08:00
    required: false
  - name: underfed_threshold
    type: number
    label: Underfed queue threshold (tasks)
    default: 10
    required: false
  - name: backlog_threshold
    type: number
    label: Backlog queue threshold (tasks)
    default: 50
    required: false
  - name: fresh_window
    type: duration
    label: Fresh signal window
    default: 24 h
    required: false
  - name: enterprise_multiplier
    type: number
    label: Enterprise account size multiplier
    default: 1.5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses of the SDRs and their manager
    required: true
  requirements:
  - slot: sdr_open_task
    kind: event
    meaning: An open SDR task was created from a buyer signal
    properties:
    - name: signal_source
      type: string
      meaning: 'Signal type: PQA, PQL, pricing-intent, named-account-touch, generic-inbound or cold-outbound-followup'
      optional: false
    - name: signal_at
      type: date
      meaning: When the signal fired
      optional: false
    - name: account_name
      type: string
      meaning: Account the task is about
      optional: false
    - name: icp_tier
      type: string
      meaning: 'ICP fit tier: ideal, viable or marginal'
      optional: false
    - name: account_size_tier
      type: string
      meaning: Account size tier, such as enterprise
      optional: false
  - slot: sdr_owner
    kind: attribute
    meaning: The SDR who owns the prospect's tasks
  - slot: task_completed
    kind: event
    meaning: An SDR task was completed
  - slot: meeting_booked
    kind: event
    meaning: A meeting was booked with the prospect
  steps:
  - id: s1
    builds: automation
    uses:
    - sdr_open_task
    - sdr_owner
    - task_completed
    - queue_size
    - delivery_time
    - fresh_window
    - enterprise_multiplier
    - underfed_threshold
    - backlog_threshold
    - digest_recipients
    instruction: 'Build an automation that runs Monday to Friday at {delivery_time} on a schedule. Each run it analyzes {sdr_open_task}
      events with no later {task_completed} for the same user and scores each: source weight PQA 50, PQL 40, pricing-intent
      35, named-account-touch 30, generic-inbound 20, cold-outbound-followup 10; times 1.5 when {sdr_open_task.signal_at}
      is within {fresh_window}, 1.0 on day 2, 0.7 on days 3-7, 0.4 after; times 1.3 for {sdr_open_task.icp_tier} ideal, 1.0
      viable, 0.5 marginal; times {enterprise_multiplier} when {sdr_open_task.account_size_tier} is enterprise. It writes,
      per {sdr_owner}, the top {queue_size} tasks with account, source, days since signal and a one-line first-touch angle,
      and flags SDRs with fewer than {underfed_threshold} or more than {backlog_threshold} open tasks. Then it emails these
      lines to {digest_recipients}. Nothing else is sent.'
  - id: s2
    builds: automation
    uses:
    - sdr_open_task
    - sdr_owner
    - task_completed
    - meeting_booked
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 09:00 on a schedule. Each run it analyzes the last 7 days
      and writes these figures: {task_completed} per {sdr_owner} per day; the share of users with {sdr_open_task} by {sdr_open_task.signal_source}
      who did {meeting_booked} after it; the share of PQA and PQL tasks against the others that led to {meeting_booked}; the
      SDRs ranked by median days from {sdr_open_task} to {meeting_booked}. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Daily SDR task queue

Slash command: /daily-sdr-task-queue

## Step 1: Email each SDR's queue at 8am

Build an automation that runs Monday to Friday at 08:00 on a schedule. Each run it analyzes sdr open task events with no later task completed for the same user and scores each: source weight PQA 50, PQL 40, pricing-intent 35, named-account-touch 30, generic-inbound 20, cold-outbound-followup 10; times 1.5 when signal at is within 24 h, 1.0 on day 2, 0.7 on days 3-7, 0.4 after; times 1.3 for icp tier ideal, 1.0 viable, 0.5 marginal; times 1.5 when account size tier is enterprise. It writes, per sdr owner, the top 25 tasks with account, source, days since signal and a one-line first-touch angle, and flags SDRs with fewer than 10 or more than 50 open tasks. Then it emails these lines to the email addresses of the SDRs and their manager. Nothing else is sent.

## Step 2: Email the weekly ranking check

Build an automation that runs every Monday at 09:00 on a schedule. Each run it analyzes the last 7 days and writes these figures: task completed per sdr owner per day; the share of users with sdr open task by signal source who did meeting booked after it; the share of PQA and PQL tasks against the others that led to meeting booked; the SDRs ranked by median days from sdr open task to meeting booked. Then it emails these figures as plain-text lines, each with its window, to the email addresses of the SDRs and their manager. Nothing else is sent.
