---
frontmatter_id: meeting-prep-brief
slash_command: /meeting-prep-brief
description: 'Sends the host a brief 24 hours before a meeting: who is coming, how the account is doing, every prior touch, and what to talk about.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sends the meeting host a prep brief 24 hours before each meeting covering attendees, account health, prior touches,
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
  - name: reschedule_refresh_window
    type: duration
    label: Window before meeting time in which a newly added attendee refreshes the brief
    default: 1 h
    required: false
  - name: prefer_slack
    type: boolean
    label: Prefer Slack DM over email when the host has a Slack ID
    default: true
    required: false
  - name: dashboard_meeting_types
    type: enum
    label: Meeting types shown in the coverage dashboard
    default: demo
    required: false
    options:
    - demo
    - discovery
    - expansion
    - renewal
  requirements:
  - slot: meeting_scheduled
    kind: event
    meaning: A meeting was scheduled with a customer
    properties:
    - name: meeting_id
      type: string
      meaning: Unique identifier of the meeting
      optional: false
    - name: meeting_time
      type: date
      meaning: Start time of the meeting
      optional: false
    - name: duration
      type: number
      meaning: Length of the meeting in minutes
      optional: true
    - name: meeting_type
      type: string
      meaning: Type of meeting such as demo, discovery, expansion, or renewal
      optional: true
    - name: host_id
      type: string
      meaning: Identifier of the employee hosting the meeting
      optional: false
  - slot: meeting_rescheduled
    kind: event
    meaning: A scheduled meeting was moved to a different time
    properties:
    - name: meeting_id
      type: string
      meaning: Unique identifier of the meeting
      optional: false
    - name: new_meeting_time
      type: date
      meaning: New start time of the meeting
      optional: false
  - slot: meeting_cancelled
    kind: event
    meaning: A scheduled meeting was cancelled
    properties:
    - name: meeting_id
      type: string
      meaning: Unique identifier of the meeting
      optional: false
  - slot: attendee_added
    kind: event
    meaning: A new attendee was added to a scheduled meeting
    properties:
    - name: meeting_id
      type: string
      meaning: Unique identifier of the meeting
      optional: false
    - name: attendee_id
      type: string
      meaning: Identifier of the added attendee
      optional: false
  - slot: meeting_object
    kind: attribute
    meaning: Meeting records with host, attendees, scheduled time, and deal link
  - slot: prep_brief
    kind: attribute
    meaning: AI-generated pre-meeting brief attribute on the meeting record
  - slot: host_slack_id
    kind: attribute
    meaning: Slack user ID of the meeting host
    optional: true
  - slot: slack_integration
    kind: integration
    meaning: A connected Slack workspace used to send direct messages
    optional: true
    channel: slack
  - slot: email_destination
    kind: destination
    meaning: An outbound email sending channel for transactional messages
    channel: email
  - slot: brief_email_template
    kind: knowledge
    meaning: Email layout used to render the prep brief for the host
  steps:
  - id: s1
    builds: attribute
    uses:
    - meeting_scheduled
    - attendee_added
    - meeting_object
    - prep_brief
    - recent_touch_count
    - reschedule_refresh_window
    instruction: 'Create an AI-derived attribute on the Meeting object called ''prep_brief'', computed at {meeting_scheduled.meeting_time}.
      Output a structured brief with sections: (a) attendees: name, title, role on deal, recent activity; (b) account snapshot:
      ARR, plan, health score, open opportunities; (c) prior touch history: last {recent_touch_count} interactions across
      email, meetings, and support; (d) suggested talking points derived from deal stage, recent product usage, and any open
      support tickets; (e) competitive intel, if any flag exists. Refresh the attribute if an attendee is added within {reschedule_refresh_window}
      of meeting time, using {attendee_added.attendee_id}.'
  - id: s2
    builds: email
    uses:
    - s1
    - prep_brief
    - brief_email_template
    instruction: Generate an HTML email template that renders the {prep_brief} attribute in a clean, scannable, utilitarian
      layout (not marketing). Place a meeting summary at top showing date, time, duration, and attendees. Below, include collapsible
      sections for account, prior touches, talking points, and competitive intel. Include a call-to-action button to view
      the brief in the app. Use the result of "Assemble the brief".
  - id: s3
    builds: automation
    uses:
    - meeting_scheduled
    - meeting_rescheduled
    - meeting_cancelled
    - delivery_lead_time
    - prep_brief
    - s1
    - s2
    instruction: Create a workflow that fires on {meeting_scheduled}. Schedule a delayed step to fire {delivery_lead_time}
      before the meeting, or immediately if the meeting is within {delivery_lead_time} of now. On firing, recompute the {prep_brief}
      attribute so last-minute updates are captured, then trigger the brief delivery journey for the host. If {meeting_rescheduled}
      occurs, cancel the pending delivery and reschedule it for the new time. If {meeting_cancelled} occurs, suppress delivery.
      Use the results of "Assemble the brief" and "Lay it out to be skimmed".
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - email_destination
    - slack_integration
    - host_slack_id
    - prefer_slack
    - prep_brief
    instruction: Build a single-touch journey that sends the prep-brief email to the meeting host when triggered by the prep
      delivery workflow in "Send it a day before". Audience is the meeting host only, not the attendees. Default channel is
      email using {email_destination} and the template from "Lay it out to be skimmed". If {slack_integration} is connected
      and the host has a {host_slack_id}, and {prefer_slack} is true, send a Slack direct message with a link to the brief
      instead. Render the content from {prep_brief}.
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - prep_brief
    - meeting_scheduled
    - dashboard_meeting_types
    instruction: Build a dashboard tracking prep-brief coverage. Show the percentage of meetings where a brief was delivered,
      the median time between brief send and meeting start, and the host open rate on brief emails. Break results down by
      meeting type (demo, discovery, expansion, renewal), with {dashboard_meeting_types} as the default filter. Flag any meeting
      where {prep_brief} computation failed due to missing data or an attribute compute error. Use the results of "Assemble
      the brief", "Lay it out to be skimmed", "Send it a day before", and "Deliver it to the host".
---

# Meeting prep brief

Slash command: /meeting-prep-brief

## Step 1: Assemble the brief

Create an AI-derived attribute on the Meeting object called 'prep_brief'. Computed at Meeting scheduled time. Output: a structured brief with sections: (a) attendees: name, title, role on deal, recent activity; (b) account snapshot: ARR, plan, health score, open opportunities; (c) prior touch history: last 5 interactions across email/meetings/support; (d) suggested talking points: AI-derived from deal stage, recent product usage, and any open support tickets; (e) competitive intel: if any flag exists. Refreshes if a new attendee is added within 1 hour of meeting time.

## Step 2: Lay it out to be skimmed

Generate an HTML email template that renders the prep_brief attribute in a clean, scannable layout. Sections: meeting summary at top (date, time, duration, attendees), then collapsible sections for account, prior touches, talking points, competitive intel. Include a CTA button to view the brief in the app. Tone: utilitarian, not marketing. Use the result of "Assemble the brief".

## Step 3: Send it a day before

Create a workflow firing on Meeting scheduled. Schedule a delayed step to fire 24 hours before the meeting (or immediately if the meeting is within 24 hours). On firing: re-compute the prep_brief attribute (catches any last-minute updates), then trigger the brief journey to deliver to the host. If the meeting is rescheduled, cancel the pending delivery and re-schedule. If cancelled, suppress delivery. Use the result of "Assemble the brief", "Lay it out to be skimmed".

## Step 4: Deliver it to the host

Build a 1-touch journey that sends the prep-brief email to the meeting host when triggered by the prep delivery workflow. Audience: the meeting host (not the attendees). Channel: email by default; if a Slack integration is connected and the host has a Slack ID, prefer Slack DM with a link to the brief. Use the result of "Assemble the brief", "Lay it out to be skimmed", "Send it a day before".

## Step 5: Check every meeting got one

Compose a dashboard tracking prep-brief coverage: % of meetings where a brief was delivered, median time before meeting the brief was sent, and host open rate on brief emails. Break down by meeting type (demo, discovery, expansion, renewal). Flag any meetings where prep_brief computation failed (missing data, attribute compute error). Use the result of "Assemble the brief", "Lay it out to be skimmed", "Send it a day before", "Deliver it to the host".
