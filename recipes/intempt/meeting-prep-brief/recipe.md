---
frontmatter_id: meeting-prep-brief
slash_command: /meeting-prep-brief
description: 'Emails the host a brief 24 hours before a meeting: who is coming, how the account is doing, the last few touches,
  and what to talk about.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails the meeting host a prep brief 24 hours before each meeting with attendees, account health, prior touches
    and talking points.
  parameters:
  - name: delivery_lead_time
    type: duration
    label: How long before the meeting the brief is sent
    default: 24 h
    required: false
  - name: recent_touch_count
    type: number
    label: Number of prior interactions included in the brief
    default: 5
    required: false
  requirements:
  - slot: meeting_scheduled
    kind: event
    meaning: A meeting was scheduled with a customer
    properties:
    - name: meeting_id
      type: string
      meaning: Id of the meeting
      optional: false
    - name: meeting_time
      type: date
      meaning: When the meeting starts
      optional: false
    - name: meeting_type
      type: string
      meaning: Type of meeting, such as demo, discovery, expansion or renewal
      optional: false
    - name: host_email
      type: string
      meaning: Email address of the meeting host
      optional: false
  - slot: meeting_rescheduled
    kind: event
    meaning: A scheduled meeting was moved to a different time
    properties:
    - name: meeting_id
      type: string
      meaning: Id of the meeting
      optional: false
  - slot: meeting_cancelled
    kind: event
    meaning: A scheduled meeting was cancelled
    properties:
    - name: meeting_id
      type: string
      meaning: Id of the meeting
      optional: false
  - slot: plan
    kind: attribute
    meaning: The customer's plan
  - slot: health_score
    kind: attribute
    meaning: The account's health score
    optional: true
  - slot: support_ticket
    kind: event
    meaning: The customer opened a support ticket
    optional: true
  steps:
  - id: s1
    builds: automation
    uses:
    - meeting_scheduled
    - meeting_rescheduled
    - meeting_cancelled
    - plan
    - health_score
    - support_ticket
    - delivery_lead_time
    - recent_touch_count
    instruction: 'Build an automation triggered by {meeting_scheduled}. It waits until {delivery_lead_time} before {meeting_scheduled.meeting_time},
      or goes on at once when the meeting is sooner, and stops when {meeting_cancelled} or {meeting_rescheduled} with the
      same meeting_id happened meanwhile. It analyzes the user and their account and writes a brief: the meeting time and
      {meeting_scheduled.meeting_type}; the attendees from the account with name, title and last activity; the account snapshot
      with {plan}, {health_score} and open {support_ticket} events from the last 30 days; the last {recent_touch_count} emails,
      meetings and tickets; three talking points from recent product use and open tickets. Then it emails the brief to {meeting_scheduled.host_email}.
      It never emails the attendees.'
---

# Meeting prep brief

Slash command: /meeting-prep-brief

## Step 1: Email the host the brief a day before

Build an automation triggered by meeting scheduled. It waits until 24 h before meeting time, or goes on at once when the meeting is sooner, and stops when meeting cancelled or meeting rescheduled with the same meeting_id happened meanwhile. It analyzes the user and their account and writes a brief: the meeting time and meeting type; the attendees from the account with name, title and last activity; the account snapshot with plan, health score and open support ticket events from the last 30 days; the last 5 emails, meetings and tickets; three talking points from recent product use and open tickets. Then it emails the brief to host email. It never emails the attendees.
