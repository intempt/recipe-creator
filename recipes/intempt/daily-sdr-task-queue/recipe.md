---
frontmatter_id: daily-sdr-task-queue
slash_command: /daily-sdr-task-queue
description: Build a prioritized report of each SDR's open tasks, ranked by signal strength and recency.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Gives each SDR a daily 8am Slack list of their top 25 open tasks, ranked by signal strength, recency and account
    fit, with suggested first-touch angles.
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
  requirements:
  - slot: sdr_open_task
    kind: event
    meaning: An SDR has an open task created from a buyer signal
    properties:
    - name: signal_source
      type: enum
      meaning: Signal source type (PQA, PQL, pricing-intent, named-account-touch, generic-inbound, cold-outbound-followup)
      optional: false
    - name: signal_at
      type: date
      meaning: When the signal fired
      optional: false
    - name: account_name
      type: string
      meaning: Name of the account the task concerns
      optional: false
    - name: icp_tier
      type: enum
      meaning: ICP fit tier of the account (ideal, viable, marginal)
      optional: false
    - name: account_size_tier
      type: enum
      meaning: Account size tier (enterprise or other)
      optional: true
  - slot: sdr_owner
    kind: attribute
    meaning: The SDR user who owns each task
  - slot: meeting_booked
    kind: event
    meaning: A meeting was booked from an SDR task
    properties:
    - name: task_id
      type: string
      meaning: Identifier of the task that converted
      optional: false
  - slot: sdr_slack
    kind: integration
    meaning: A connected Slack workspace for sending direct messages to SDRs and the SDR manager
    channel: slack
  - slot: sdr_manager
    kind: attribute
    meaning: The SDR manager user who receives the team summary
  - slot: business_calendar
    kind: knowledge
    meaning: Business day calendar with weekends, public holidays and each SDR's timezone
  steps:
  - id: s1
    builds: attribute
    uses:
    - sdr_open_task
    - fresh_window
    - enterprise_multiplier
    instruction: 'Create an AI-derived attribute ''task_priority_score'' on {sdr_open_task}. Composite score: (a) signal source
      weight: PQA 50, PQL 40, pricing-intent 35, named-account-touch 30, generic-inbound 20, cold-outbound-followup 10; (b)
      recency multiplier: fresh signal (under {fresh_window}) x1.5, day 2 x1.0, day 3-7 x0.7, day 8 or later x0.4; (c) ICP
      fit boost: ideal tier x1.3, viable x1.0, marginal x0.5; (d) account size weight: enterprise tier x{enterprise_multiplier}.
      Output a 0-150 score used for ranking.'
  - id: s2
    builds: report
    uses:
    - s1
    - sdr_owner
    - queue_size
    - sdr_open_task
    instruction: 'Build a report ''SDR daily queue snapshot'' that computes, per {sdr_owner}, the top {queue_size} open tasks
      ranked by ''task_priority_score'' from "Rank every task by signal". Each task shows: signal source (PQL, PQA or intent),
      account name, ICP tier, days since signal fired, and a suggested first-touch angle based on signal type and account
      context. The queue is capped at {queue_size} because SDR daily-touch capacity is realistically 20-25 outreaches.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - sdr_slack
    - sdr_manager
    - business_calendar
    - delivery_time
    - queue_size
    - underfed_threshold
    - backlog_threshold
    instruction: 'Create a scheduled workflow that fires every business day at {delivery_time} in each SDR''s local timezone,
      skipping weekends and holidays from {business_calendar}. Steps in order: (1) refresh ''task_priority_score'' across
      all open SDR tasks so overnight signals are included; (2) generate each SDR''s top {queue_size} queue from "Build a
      report" (''SDR daily queue snapshot''); (3) send each SDR a Slack DM with their prioritized list and a one-click link
      to each task; (4) post a team summary to {sdr_manager} covering queue-size distribution (any SDR under {underfed_threshold}
      tasks is underfed, over {backlog_threshold} is backlog), top signal sources today, and ICP-tier mix.'
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - meeting_booked
    instruction: 'Compose an SDR productivity dashboard with four panels: (a) daily queue delivery rate, the percentage of
      SDRs receiving their queue each day; (b) tasks worked per SDR per day compared with queue size delivered; (c) top-of-queue
      conversion, the percentage of the #1-#5 priority tasks that became a booked meeting compared with lower-ranked tasks,
      using {meeting_booked}; (d) a rep leaderboard on signal-to-meeting velocity. Together these show whether the prioritization
      in "Rank every task by signal" directs SDRs to the right targets. Use the queue from "Build a report" and the delivery
      from "Create a scheduled workflow".'
---

# Daily SDR task queue

Slash command: /daily-sdr-task-queue

## Step 1: Rank every task by signal

Create an AI-derived attribute 'task_priority_score' on the Task object. Composite: (a) signal source weight: PQA: 50, PQL: 40, pricing-intent: 35, named-account-touch: 30, generic-inbound: 20, cold-outbound-followup: 10; (b) recency multiplier (fresh signal (<24hr) × 1.5, day-2 × 1.0, day-3-7 × 0.7, day-8+ × 0.4; (c) ICP fit boost) ideal-tier accounts × 1.3, viable × 1.0, marginal × 0.5; (d) account size weight: enterprise tier × 1.5. Output: 0-150 score for ranking.

## Step 2: Cut it to 25 a day

Build a report 'SDR daily queue snapshot' computing, per SDR, their top 25 open tasks ranked by task_priority_score, with each task showing: signal source (PQL / PQA / intent), account name, ICP tier, days since signal fired, suggested first-touch angle (based on signal type and account context). Caps queue at 25 because SDR daily-touch capacity is realistically 20-25 outreaches. Use the result of "Rank every task by signal".

## Step 3: Deliver it at 8am

Create a scheduled workflow firing every business day at 8am local time per SDR (timezone-aware). Step sequence: (1) refresh task_priority_score across all open SDR tasks (catches new signals from overnight); (2) generate each SDR's top-25 queue; (3) deliver via Slack DM to the SDR with the prioritized list and one-click links to each task; (4) post a team-level summary to the SDR manager: queue-size distribution (any SDR with <10 tasks = underfed, >50 = backlog), top signal sources today, ICP-tier mix. Skip on weekends and holidays. Use the result of "Rank every task by signal", "Cut it to 25 a day".

## Step 4: Check the ranking is right

Compose an SDR productivity dashboard: daily-queue delivery rate (% of SDRs receiving their queue daily: operational health), tasks worked per SDR per day vs. queue-size delivered (working-rate), top-of-queue conversion (% of #1-#5 priority tasks that converted to meeting vs. lower-ranked), and rep-leaderboard on signal-to-meeting velocity. Surfaces whether the prioritization model is actually directing SDRs to the right targets. Use the result of "Rank every task by signal", "Cut it to 25 a day", "Deliver it at 8am".
