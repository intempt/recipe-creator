---
frontmatter_id: lead-to-mql-to-sql-funnel
slash_command: /lead-to-mql-to-sql-funnel
description: Emails a weekly digest of how leads move through MQL, SQL, demo and closed won, where they stall, and how long
  the whole sales cycle takes.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of leads moving from creation through MQL, SQL, demo and closed won, by source, with drop-off
    flags and sales-cycle length.
  parameters:
  - name: mql_stage
    type: string
    label: Lead stage name that marks an MQL
    default: MQL
    required: false
  - name: conversion_window
    type: duration
    label: Conversion window
    default: 90 d
    required: false
  - name: breakdown_top_n
    type: number
    label: Number of top sources to break down by
    default: 6
    required: false
  - name: comparison_period
    type: duration
    label: Comparison period (prior period length)
    default: 90 d
    required: false
  - name: mql_to_sql_threshold
    type: number
    label: MQL-to-SQL conversion flag threshold (%)
    default: 20
    required: false
  - name: sql_to_won_threshold
    type: number
    label: SQL-to-Closed-Won conversion flag threshold (%)
    default: 15
    required: false
  - name: high_volume_end_to_end_threshold
    type: number
    label: High-volume end-to-end conversion threshold (%)
    default: 5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: lead_created_event
    kind: event
    meaning: A new user account was created with UTM source tracking
    properties:
    - name: utm_source
      type: string
      meaning: UTM source recorded on the user
      optional: false
  - slot: lead_stage_changed_event
    kind: event
    meaning: A lead's stage changed to a new lead stage
    properties:
    - name: new_stage
      type: string
      meaning: The lead stage the lead moved into
      optional: false
  - slot: deal_created_event
    kind: event
    meaning: A sales deal was created for a customer
  - slot: meeting_scheduled_event
    kind: event
    meaning: A customer meeting was scheduled
    properties:
    - name: canceled_at
      type: date
      meaning: When the meeting was canceled, empty if not canceled
      optional: true
    - name: end_time
      type: date
      meaning: When the meeting ends
      optional: false
  - slot: deal_won_event
    kind: event
    meaning: A sales deal was marked closed won
  - slot: utm_source_user_attribute
    kind: attribute
    meaning: The UTM source recorded on a user, used to break down the funnel by traffic source
  steps:
  - id: s1
    builds: automation
    uses:
    - lead_created_event
    - lead_stage_changed_event
    - deal_created_event
    - meeting_scheduled_event
    - deal_won_event
    - utm_source_user_attribute
    - mql_stage
    - conversion_window
    - breakdown_top_n
    - comparison_period
    - mql_to_sql_threshold
    - sql_to_won_threshold
    - high_volume_end_to_end_threshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {lead_created_event}
      with {lead_created_event.utm_source} not empty in the last {comparison_period}, against the {comparison_period} before,
      through five steps within {conversion_window}: lead created; MQL ({lead_stage_changed_event} with {lead_stage_changed_event.new_stage}
      equal to {mql_stage}); SQL ({deal_created_event} for that user); demo held ({meeting_scheduled_event} with {meeting_scheduled_event.canceled_at}
      empty and {meeting_scheduled_event.end_time} in the past); closed won ({deal_won_event}). It writes: users at each step
      and step-to-step conversion %, split by {utm_source_user_attribute} for the top {breakdown_top_n} sources; the largest
      drop-off; median days between steps and median lead-to-won days, against the period before. Then it emails these figures
      as plain-text lines, each with its window, to {digest_recipients}. The email flags sources with MQL-to-SQL under {mql_to_sql_threshold}%
      or SQL-to-won under {sql_to_won_threshold}%, and names high-volume sources with end-to-end conversion above {high_volume_end_to_end_threshold}%.
      Nothing else is sent.'
---

# Lead qualification funnel

Slash command: /lead-to-mql-to-sql-funnel

## Step 1: Email the weekly lead qualification digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did lead created event with utm source not empty in the last 90 d, against the 90 d before, through five steps within 90 d: lead created; MQL (lead stage changed event with new stage equal to MQL); SQL (deal created event for that user); demo held (meeting scheduled event with canceled at empty and end time in the past); closed won (deal won event). It writes: users at each step and step-to-step conversion %, split by utm source user attribute for the top 6 sources; the largest drop-off; median days between steps and median lead-to-won days, against the period before. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email flags sources with MQL-to-SQL under 20% or SQL-to-won under 15%, and names high-volume sources with end-to-end conversion above 5%. Nothing else is sent.
