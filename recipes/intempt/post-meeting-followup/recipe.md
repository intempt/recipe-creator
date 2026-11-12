---
frontmatter_id: post-meeting-followup
slash_command: /post-meeting-followup
description: Builds a post-meeting follow-up journey that creates tasks with owners and due dates from action items you provide, and can send a structured follow-up email to attendees.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: After a meeting ends, the customer gets a structured recap email to attendees, CRM tasks for each action item with
    owner and due date, and a dashboard tracking follow-up health.
  parameters:
  - name: summary_window
    type: duration
    label: Time limit to send follow-up after meeting
    default: 30 m
    required: false
  - name: stale_threshold
    type: duration
    label: Flag meetings without follow-up after
    default: 4 h
    required: false
  - name: follow_up_tone
    type: enum
    label: Email tone
    default: professional_warm
    required: false
    options:
    - professional_warm
    - formal
    - casual
  - name: sales_target_minutes
    type: number
    label: Target median minutes from meeting end to follow-up sent
    default: 30
    required: false
  requirements:
  - slot: meeting_completed_event
    kind: event
    meaning: A meeting was completed, with its transcript available
    properties:
    - name: meeting_id
      type: string
      meaning: Identifier of the meeting
      optional: false
    - name: meeting_subject
      type: string
      meaning: Subject of the meeting
      optional: false
    - name: transcript
      type: text
      meaning: Meeting transcript text
      optional: true
    - name: host_email
      type: string
      meaning: Email of the meeting host
      optional: false
    - name: meeting_type
      type: string
      meaning: Type of meeting
      optional: true
    - name: recording_url
      type: string
      meaning: Link to the meeting recording
      optional: true
  - slot: meeting_attendees
    kind: segment
    meaning: Attendees of a completed meeting who are external to the company
  - slot: meeting_summary_attribute
    kind: attribute
    meaning: An AI-generated summary attribute on the Meeting object holding decisions, action items, objections, sentiment
      and next step
  - slot: linked_deal
    kind: attribute
    meaning: The deal record linked to a meeting, which can receive next step, objections, sentiment and notes
  - slot: crm_task
    kind: attribute
    meaning: A CRM task object that can be assigned to an owner with a due date
  - slot: slack_workspace
    kind: integration
    meaning: A Slack connection to notify the meeting host of a failed summary
    channel: slack
  - slot: follow_up_email_journey
    kind: destination
    meaning: A journey or email channel that sends the follow-up recap email to attendees
    channel: email
  steps:
  - id: s1
    builds: attribute
    uses:
    - meeting_completed_event
    - meeting_summary_attribute
    instruction: 'Create an AI-derived attribute on the Meeting object named ''meeting_summary'', computed when {meeting_completed_event}
      fires, from the {meeting_completed_event.transcript}. Output a structured object with: (a) a one-paragraph executive
      summary; (b) decisions reached as a list; (c) action items as a list of {assignee, due, description}; (d) objections
      raised as a list; (e) a sentiment score; (f) the next step proposed as free text. If the transcript is incomplete or
      short, return a gracefully partial output.'
  - id: s2
    builds: email
    uses:
    - s1
    - meeting_summary_attribute
    - meeting_completed_event
    - follow_up_tone
    instruction: 'Create a follow-up email template that renders the meeting_summary from "Pull the meeting apart". Structure:
      a thank-you opening that references {meeting_completed_event.meeting_subject} and the attendees; a recap of decisions;
      bulleted action items with owners and due dates; a link to {meeting_completed_event.recording_url} if available; a signature
      with the proposed next step and a scheduling link. Tone: {follow_up_tone}, reflecting the rep''s voice from prior outbound
      style if available. Send from {meeting_completed_event.host_email}.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - linked_deal
    - crm_task
    - slack_workspace
    - follow_up_email_journey
    - meeting_completed_event
    instruction: 'Create a workflow triggered by {meeting_completed_event}. Steps in order: (1) compute {meeting_summary_attribute}
      from "Pull the meeting apart"; (2) update {linked_deal} with the AI-extracted next step, objections, sentiment and the
      meeting note; (3) for each action item in the summary, create a {crm_task} assigned to the named owner with the due
      date; (4) trigger {follow_up_email_journey} to send the email from "Write the recap email". If the summary computation
      fails (no transcript or processing error), create a {crm_task} for the host {meeting_completed_event.host_email} to
      follow up manually and notify the host in {slack_workspace}.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - meeting_attendees
    - follow_up_email_journey
    - summary_window
    instruction: 'Build a single-touch journey that sends the email from "Write the recap email" to all {meeting_attendees}
      within {summary_window} of {meeting_completed_event}, only when triggered by the workflow "File it and raise the tasks".
      Personalize per attendee: the body stays the same but the salutation and signature adapt to each attendee. Use {follow_up_email_journey}
      as the sending channel.'
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - crm_task
    - meeting_completed_event
    - stale_threshold
    - sales_target_minutes
    instruction: 'Compose a dashboard tracking post-meeting follow-up health: median time from {meeting_completed_event} to
      follow-up email sent (target under {sales_target_minutes} minutes); percent of meetings with completed follow-ups versus
      missed; action-item completion rate (tasks created versus {crm_task} completed); and reply rate to follow-up emails.
      Break down by {meeting_completed_event.meeting_type} and by rep. Flag any meeting older than {stale_threshold} without
      a follow-up sent.'
---

# Post meeting follow up

Slash command: /post-meeting-followup

## Step 1: Pull the meeting apart

Create an AI-derived attribute on the Meeting object called 'meeting_summary'. Computed at meeting_completed from the transcript. Output: structured object with (a) one-paragraph executive summary; (b) decisions reached (list); (c) action items (list of {assignee, due, description}); (d) objections raised (list); (e) sentiment score; (f) next step proposed (free-text). Falls back to gracefully partial output if transcript is incomplete or short.

## Step 2: Write the recap email

Generate a follow-up email template that renders the meeting_summary attribute. Structure: thank-you opening referencing meeting subject and attendees, recap of decisions, bulleted action items with owners and due dates, link to recording if available, signature with proposed next step and a scheduling link. Tone: professional but warm; reflects the rep's voice based on prior outbound style if available. Send-from address: the meeting host's email. Use the result of "Pull the meeting apart".

## Step 3: File it and raise the tasks

Create a workflow firing on meeting_completed. Step sequence: (1) compute meeting_summary attribute; (2) update the linked deal record with the AI-extracted next step, objections, sentiment, and the meeting note; (3) for each action item in the summary, create a CRM task assigned to the named owner with the due date; (4) trigger the follow-up journey to send the recap email. If meeting_summary computation fails (no transcript, processing error), still create a task for the host to manually follow up and notify them via Slack. Use the result of "Pull the meeting apart", "Write the recap email".

## Step 4: Send it within 30 minutes

Build a 1-touch journey that sends the follow-up email to all meeting attendees (excluding internal users) within 30 minutes of meeting_completed, when triggered by the post-meeting workflow. Personalize per attendee: the body stays the same but the salutation and signature adapt. Use the result of "Pull the meeting apart", "Write the recap email", "File it and raise the tasks".

## Step 5: Check nothing goes unanswered

Compose a dashboard tracking post-meeting follow-up health: median time from meeting_completed to follow-up email sent (target: under 30 min), % of meetings with completed follow-ups vs missed, action-item completion rate (tasks created vs tasks completed), and reply rate to follow-up emails. Break down by meeting type and rep. Flag any meeting older than 4 hours without a follow-up sent. Use the result of "Pull the meeting apart", "Write the recap email", "File it and raise the tasks", "Send it within 30 minutes".
