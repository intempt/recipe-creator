---
frontmatter_id: lead-customer-sales
slash_command: /lead-customer-sales
description: Emails a weekly digest of how many demo requests turn into booked meetings, completed demos, proposals and won
  deals, and which lead sources convert.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a weekly digest of demo requests moving to meetings, demos, proposals and won deals, by lead source, with
    stalled-stage flags.
  parameters:
  - name: demo_form_id
    type: string
    label: Form id of the demo-request form
    required: true
  - name: proposal_stage
    type: string
    label: Deal stage name that marks a proposal
    default: proposal
    required: false
  - name: conversionWindow
    type: duration
    label: Conversion window
    default: 60 d
    required: false
  - name: topSources
    type: number
    label: Number of lead sources to break down
    default: 8
    required: false
  - name: deadStageDays
    type: number
    label: Median stage velocity alert threshold (days)
    default: 14
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: demo_request_form_event
    kind: event
    meaning: A customer submitted a form, including demo-request forms (a form on the site, never a survey or NPS answer)
    properties:
    - name: form_id
      type: string
      meaning: Identifier of the submitted form, used to match the demo-request form
      optional: false
  - slot: meeting_scheduled_event
    kind: event
    meaning: A meeting was scheduled with a lead or customer user
    properties:
    - name: primary_user_id
      type: string
      meaning: User the meeting is linked to
      optional: true
    - name: user_ids
      type: array
      meaning: Users attached to the meeting
      optional: true
    - name: canceled_at
      type: date
      meaning: Time the meeting was canceled, empty if not canceled
      optional: true
    - name: start_time
      type: date
      meaning: Meeting start time
      optional: false
    - name: end_time
      type: date
      meaning: Meeting end time
      optional: false
  - slot: deal_stage_changed_event
    kind: event
    meaning: A deal moved to a different stage in the sales pipeline
    properties:
    - name: previous_stage
      type: string
      meaning: Stage the deal left
      optional: true
    - name: new_stage
      type: string
      meaning: Stage the deal entered, used to match the proposal stage
      optional: false
    - name: amount
      type: number
      meaning: Deal amount
      optional: true
  - slot: deal_won_event
    kind: event
    meaning: A deal was marked as won (closed customer deal)
    properties:
    - name: amount
      type: number
      meaning: Amount of the won deal
      optional: true
  - slot: user_utm_source_attribute
    kind: attribute
    meaning: The first-touch lead source (UTM source) recorded on the user record
  steps:
  - id: s1
    builds: automation
    uses:
    - demo_request_form_event
    - meeting_scheduled_event
    - deal_stage_changed_event
    - deal_won_event
    - user_utm_source_attribute
    - demo_form_id
    - proposal_stage
    - conversionWindow
    - topSources
    - deadStageDays
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {demo_request_form_event}
      with {demo_request_form_event.form_id} equal to {demo_form_id} in the last 60 days, against the 60 days before, through
      these steps within {conversionWindow}: demo requested; meeting booked ({meeting_scheduled_event}); demo held ({meeting_scheduled_event}
      with {meeting_scheduled_event.canceled_at} empty and {meeting_scheduled_event.end_time} in the past); proposal ({deal_stage_changed_event}
      with {deal_stage_changed_event.new_stage} equal to {proposal_stage}); won ({deal_won_event}). It writes: users at each
      step and the step-to-step conversion %, split by {user_utm_source_attribute} for the top {topSources} sources; median
      days between steps; won revenue (sum of {deal_won_event.amount}); the source with the best win rate at volume; sources
      with rising requests but falling win rate. Then it emails these figures as plain-text lines, each with its window, to
      {digest_recipients}. The email flags any step whose median takes more than {deadStageDays} days. Nothing else is sent.'
---

# Lead to customer

Slash command: /lead-customer-sales

## Step 1: Email the weekly lead to customer digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did demo request form event with form id equal to the form id of the demo-request form in the last 60 days, against the 60 days before, through these steps within 60 d: demo requested; meeting booked (meeting scheduled event); demo held (meeting scheduled event with canceled at empty and end time in the past); proposal (deal stage changed event with new stage equal to proposal); won (deal won event). It writes: users at each step and the step-to-step conversion %, split by user utm source attribute for the top 8 sources; median days between steps; won revenue (sum of amount); the source with the best win rate at volume; sources with rising requests but falling win rate. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email flags any step whose median takes more than 14 days. Nothing else is sent.
