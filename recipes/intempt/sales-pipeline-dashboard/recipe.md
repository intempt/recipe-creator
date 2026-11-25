---
frontmatter_id: sales-pipeline-dashboard
slash_command: /sales-pipeline-dashboard
description: 'Emails account executives a Monday digest of which open deals need attention now: open pipeline value by stage,
  stalled deals, time in stage and accounts whose engagement is rising or falling.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails account executives a Monday list of open pipeline by stage, stalled deals, deals with no recent meeting
    and accounts whose product engagement is rising or falling.
  parameters:
  - name: stalledWindow
    type: duration
    label: No stage change for this long marks a deal stalled
    default: 14 d
    required: false
  - name: meetingWindow
    type: duration
    label: No meeting for this long flags a deal
    default: 21 d
    required: false
  - name: tableTopN
    type: number
    label: Accounts listed as rising and falling
    default: 10
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: deal_created_event
    kind: event
    meaning: A new deal was created
    properties:
    - name: deal_id
      type: string
      meaning: Deal identifier
      optional: false
    - name: amount
      type: number
      meaning: Deal amount
      optional: false
    - name: owner_id
      type: string
      meaning: The rep who owns the deal
      optional: false
  - slot: deal_stage_changed_event
    kind: event
    meaning: A deal moved to a different pipeline stage
    properties:
    - name: deal_id
      type: string
      meaning: Deal identifier
      optional: false
    - name: stage
      type: string
      meaning: The new stage
      optional: false
  - slot: deal_won_event
    kind: event
    meaning: A deal was closed as won
    properties:
    - name: deal_id
      type: string
      meaning: Deal identifier
      optional: false
  - slot: deal_lost_event
    kind: event
    meaning: A deal was closed as lost
    properties:
    - name: deal_id
      type: string
      meaning: Deal identifier
      optional: false
  - slot: meeting_scheduled_event
    kind: event
    meaning: A meeting was scheduled with a deal contact
    properties:
    - name: deal_id
      type: string
      meaning: Deal the meeting is for
      optional: false
  - slot: session_start_event
    kind: event
    meaning: A user at a customer account started a product session
  steps:
  - id: s1
    builds: automation
    uses:
    - deal_created_event
    - deal_stage_changed_event
    - deal_won_event
    - deal_lost_event
    - meeting_scheduled_event
    - session_start_event
    - stalledWindow
    - meetingWindow
    - tableTopN
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 07:00 on a schedule. Each run it analyzes open deals, the
      deal_id values with a {deal_created_event} and no {deal_won_event} or {deal_lost_event}, and writes these figures: the
      count and sum of {deal_created_event.amount} of open deals, in total and per latest {deal_stage_changed_event.stage};
      the median days open deals have spent in their current stage, per stage; the 10 largest open deals with no {deal_stage_changed_event}
      in the last {stalledWindow}, each with its amount, stage and {deal_created_event.owner_id}; the open deals with no {meeting_scheduled_event}
      in the last {meetingWindow}; the {tableTopN} accounts with the largest rise and the {tableTopN} with the largest fall
      in {session_start_event} count this week against last week, each by name. Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Deals to work this week

Slash command: /sales-pipeline-dashboard

## Step 1: Email the Monday deals digest

Build an automation that runs every Monday at 07:00 on a schedule. Each run it analyzes open deals, the deal_id values with a deal created event and no deal won event or deal lost event, and writes these figures: the count and sum of amount of open deals, in total and per latest stage; the median days open deals have spent in their current stage, per stage; the 10 largest open deals with no deal stage changed event in the last 14 d, each with its amount, stage and owner id; the open deals with no meeting scheduled event in the last 21 d; the 10 accounts with the largest rise and the 10 with the largest fall in session start event count this week against last week, each by name. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
