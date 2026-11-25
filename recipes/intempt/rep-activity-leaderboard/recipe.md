---
frontmatter_id: rep-activity-leaderboard
slash_command: /rep-activity-leaderboard
description: Emails a sales manager a weekly per-rep leaderboard of calls, emails, meetings and tasks next to revenue closed,
  with revenue per 100 calls and flags for coaching and engagement drops.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a weekly per-rep leaderboard of calls, outbound emails, meetings and tasks next to revenue closed, with
    flags for engagement drops and coaching.
  parameters:
  - name: time_window
    type: duration
    label: Window analyzed
    default: 30 d
    required: false
  - name: comparison_window
    type: duration
    label: Earlier window it is compared with
    default: 30 d
    required: false
  - name: engagement_drop_threshold
    type: number
    label: Drop in a rep's activity that gets flagged (%)
    default: 30
    required: false
  - name: efficiency_benchmark_factor
    type: number
    label: Share of the team median revenue per 100 calls below which a rep is flagged for coaching
    default: 0.5
    required: false
  - name: default_sort
    type: enum
    label: Leaderboard sort
    default: revenue_closed
    required: false
    options:
    - revenue_closed
    - calls
    - revenue_per_100_calls
    - activity_velocity
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: call_completed_event
    kind: event
    meaning: A sales rep completed a call with a prospect or customer
    properties:
    - name: created_by
      type: string
      meaning: Rep who made the call
      optional: false
  - slot: outbound_email_event
    kind: event
    meaning: A sales rep sent an outbound email to a prospect or customer
    optional: true
    properties:
    - name: created_by
      type: string
      meaning: Rep who sent the email
      optional: false
  - slot: meeting_scheduled_event
    kind: event
    meaning: A sales rep booked a meeting with a prospect or customer
    optional: true
    properties:
    - name: created_by
      type: string
      meaning: Rep who booked the meeting
      optional: false
  - slot: task_completed_event
    kind: event
    meaning: A sales rep completed a sales task
    optional: true
    properties:
    - name: owner_id
      type: string
      meaning: Rep who owns the task
      optional: false
  - slot: deal_won_event
    kind: event
    meaning: A deal was won (closed won)
    properties:
    - name: owner_id
      type: string
      meaning: Rep who owns the deal
      optional: false
    - name: amount
      type: number
      meaning: Deal amount
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - call_completed_event
    - outbound_email_event
    - meeting_scheduled_event
    - task_completed_event
    - deal_won_event
    - time_window
    - comparison_window
    - engagement_drop_threshold
    - efficiency_benchmark_factor
    - default_sort
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last {time_window}
      and writes one line per rep, matching reps across events: calls ({call_completed_event} by {call_completed_event.created_by}),
      outbound emails ({outbound_email_event} by {outbound_email_event.created_by}), meetings booked ({meeting_scheduled_event}
      by {meeting_scheduled_event.created_by}), tasks completed ({task_completed_event} by {task_completed_event.owner_id}),
      revenue closed (sum of {deal_won_event.amount} by {deal_won_event.owner_id}) and revenue per 100 calls, each next to
      the {comparison_window} before, sorted by {default_sort}. When a rep''s total activity fell by more than {engagement_drop_threshold}%,
      or their revenue per 100 calls is below {efficiency_benchmark_factor} times the team median, the email''s first line
      names them. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing
      else is sent.'
---

# Rep activity leaderboard

Slash command: /rep-activity-leaderboard

## Step 1: Email the weekly rep leaderboard

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last 30 d and writes one line per rep, matching reps across events: calls (call completed event by created by), outbound emails (outbound email event by created by), meetings booked (meeting scheduled event by created by), tasks completed (task completed event by owner id), revenue closed (sum of amount by owner id) and revenue per 100 calls, each next to the 30 d before, sorted by revenue_closed. When a rep's total activity fell by more than 30%, or their revenue per 100 calls is below 0.5 times the team median, the email's first line names them. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
