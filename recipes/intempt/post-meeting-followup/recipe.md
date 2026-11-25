---
frontmatter_id: post-meeting-followup
slash_command: /post-meeting-followup
description: When a meeting ends, analyzes its transcript into decisions, action items with owners and due dates, and the
  next step, and emails that recap to the host to send on, plus a weekly follow-up digest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails the host a structured recap of every completed meeting, with decisions, action items, owners, due dates
    and next step, and a weekly follow-up digest.
  parameters:
  - name: follow_up_tone
    type: enum
    label: Tone of the recap
    default: professional_warm
    required: false
    options:
    - professional_warm
    - formal
    - casual
  - name: stale_threshold
    type: duration
    label: Flag meetings with no follow-up after
    default: 4 h
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: meeting_completed_event
    kind: event
    meaning: A meeting was completed, with its transcript available
    properties:
    - name: meeting_subject
      type: string
      meaning: Subject of the meeting
      optional: false
    - name: transcript
      type: string
      meaning: Transcript text of the meeting
      optional: false
    - name: host_email
      type: string
      meaning: Email address of the meeting host
      optional: false
    - name: meeting_type
      type: string
      meaning: Type of meeting, such as discovery or demo
      optional: true
    - name: recording_url
      type: string
      meaning: Link to the meeting recording
      optional: true
  - slot: follow_up_sent
    kind: event
    meaning: A follow-up email was sent to a meeting's attendees
    optional: true
  steps:
  - id: s1
    builds: automation
    uses:
    - meeting_completed_event
    - follow_up_tone
    instruction: 'Build an automation triggered by {meeting_completed_event}. It analyzes {meeting_completed_event.transcript}
      and writes: a one-paragraph summary; the decisions reached; each action item with its owner and due date; objections
      raised; the proposed next step; and a ready-to-send recap for the attendees in a {follow_up_tone} tone that thanks them
      for {meeting_completed_event.meeting_subject}, lists the decisions and action items and links {meeting_completed_event.recording_url}
      when set. When the transcript is missing or too short, it says so instead. Then it emails these lines to {meeting_completed_event.host_email}.
      It never emails the attendees.'
  - id: s2
    builds: automation
    uses:
    - meeting_completed_event
    - follow_up_sent
    - stale_threshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last 7 days
      and writes these figures: the number of {meeting_completed_event} events; the share followed by {follow_up_sent} for
      the same users; the median time from {meeting_completed_event} to {follow_up_sent}; the meetings with no {follow_up_sent}
      within {stale_threshold}, each by {meeting_completed_event.meeting_subject} and {meeting_completed_event.host_email};
      these split by {meeting_completed_event.meeting_type}. Then it emails these figures as plain-text lines, each with its
      window, to {digest_recipients}. Nothing else is sent.'
---

# Post meeting follow up

Slash command: /post-meeting-followup

## Step 1: Email the host the recap

Build an automation triggered by meeting completed event. It analyzes transcript and writes: a one-paragraph summary; the decisions reached; each action item with its owner and due date; objections raised; the proposed next step; and a ready-to-send recap for the attendees in a professional_warm tone that thanks them for meeting subject, lists the decisions and action items and links recording url when set. When the transcript is missing or too short, it says so instead. Then it emails these lines to host email. It never emails the attendees.

## Step 2: Email the weekly follow-up digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last 7 days and writes these figures: the number of meeting completed event events; the share followed by follow up sent for the same users; the median time from meeting completed event to follow up sent; the meetings with no follow up sent within 4 h, each by meeting subject and host email; these split by meeting type. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
